import click
import sys
import os
import subprocess
import pkgutil
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ----------------------------------------------------------------

@click.group()
def atcoder():
    pass

# --------------------------------
# pp atcoder get ...
# --------------------------------
@atcoder.command()
@click.argument("url_or_contest")
@click.option("--problem", "-p", default="all")
def get(url_or_contest, problem):
    atcoder = AtCoder()
    # contest が URLでない場合, URLに整形する
    url = atcoder.get_atcoder_url(url_or_contest)
    # テストケースを取得
    data = atcoder.get(Path(url), problem)
    # テストケースを格納
    atcoder.save(data)

# --------------------------------
# pp atcoder init ...
# --------------------------------
@atcoder.command()
def init():
    print("init")
    # ファイルが既にあるならエラー, 上書きオプション指定されていれば無視する
    # ファイルを作成する

# --------------------------------
# pp atcoder test ...
# --------------------------------
@atcoder.command()
@click.argument("python_file")
def test(python_file):
    atcoder = AtCoder()
    # テストの準備
    contest,problem,commands = atcoder.prepare_test(python_file)
    # テストケースを取得
    testcase_list = atcoder.get_testcase_files(contest, problem)
    # テスト実行
    atcoder.exec_test(testcase_list, contest, problem, commands)

# --------------------------------
# pp atcoder git ...
# --------------------------------
@atcoder.command()
@click.argument("python_file")
def git(python_file):
    atcoder = AtCoder()
    # ファイルの存在確認
    dir_path, file_name = atcoder.get_work_dir_path(python_file)
    # コンテスト, 問題を取得する
    contest, problem = file_name.split("_")[0],file_name.split("_")[1]
    # ここでabcとarcの同時開催を処理し、contest = abcxxx_arcxxx のようにする

    # コンテスト日付を取得する
    year,month,day = atcoder.get_contest_date(file_name)
    # 格納先ディレクトリがなければ作る
    contest_dir = month + day + "_" + contest
    atcoder.mkdir(atcoder.PYPRO_ATCODER_GIT_PATH / year, atcoder.PYPRO_ATCODER_GIT_PATH / year / contest_dir)
    # mv
    print("mv", atcoder.PYPRO_ATCODER_WORK_PATH, atcoder.PYPRO_ATCODER_GIT_PATH)
    # git add filepath
    # git commit -m "xxx"
    # git push origin master

# ----------------------------------------------------------------

CONTEST_FIND_BY_SECTION = ["abc034","abc036","abc041"]
CONTEST_ABC_TO_ARC = {
    "abc042":"arc058", 
    "abc043":"arc059", 
    "abc044":"arc060", 
    "abc045":"arc061", 
    "abc046":"arc062", 
    "abc047":"arc063", 
    "abc048":"arc064", 
    "abc049":"arc065", 
    "abc050":"arc066"
}
PROBLEM_ABC_TO_ABC = {"c":"a", "d":"b"}

# ----------------------------------------------------------------

class AtCoder:

    def __init__(self):
        self.data_dir_path = Path(__file__).parent / "data"
        self.options = Options()
        self.options.set_headless(True)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.PYPRO_HOME = os.environ["PYPRO_HOME"]
        self.PYPRO_ATCODER_WORK_DIR = os.environ["PYPRO_ATCODER_WORK_DIR"]
        self.PYPRO_ATCODER_GIT_DIR = os.environ["PYPRO_ATCODER_GIT_DIR"]
        self.PYPRO_ATCODER_WORK_PATH = Path(self.PYPRO_HOME) / self.PYPRO_ATCODER_WORK_DIR / "atcoder"
        self.PYPRO_ATCODER_GIT_PATH = Path(self.PYPRO_HOME) / self.PYPRO_ATCODER_GIT_DIR

    def __del__(self):
        self.driver.quit()
    
    def is_url(self, string):
        if string[0:19] == "https://atcoder.jp/":
            return True
        else:
            return False

    def get_atcoder_url(self, string):
        if string[0:19] == "https://atcoder.jp/":
            return string
        else:
            return "https://atcoder.jp/contests/" + string

    def get(self, url, problems):
        contest = str(url).split("/")[-1]
        contest_dir_path = self.data_dir_path / contest
        url = url / "tasks"

        # 指定コンテストの問題一覧を取得
        contest_problem_list = self.get_problem_list(str(url))

        # 処理対象の問題のリストを作成
        target_problem_list = self.get_target_problem_list(contest_problem_list, problems)

        # サンプルケースを格納するディレクトリがなければ作成する
        self.mkdir(contest_dir_path, target_problem_list)
        
        # 問題のテストケースを取得
        res = []
        case_count = []
        for problem in target_problem_list:
            problem_url = ""
            if problem in ["c","d"] and contest in CONTEST_ABC_TO_ARC.keys():
                problem_url = url / (CONTEST_ABC_TO_ARC[contest] + "_" + PROBLEM_ABC_TO_ABC[problem])
            else:
                problem_url = url / (contest + "_" + problem)

            self.driver.get(str(problem_url))
            if self.driver.title[0:3] == "404":
                num = ord(problem)-ord("a")+1
                problem_url = url / (contest + "_" + str(num))
                self.driver.get(str(problem_url))
            
            soup = BeautifulSoup(self.driver.page_source.encode('utf-8'), "html.parser")

            div = ""
            if contest in CONTEST_FIND_BY_SECTION:
                div = soup.find_all("section")
            else:
                div = soup.find_all("div", class_="part")

            i_in, i_out = 0,0
            for d in div:
                if d.find("h3") is not None and (d.find("h3").text)[:3] == "入力例":
                    i_in += 1
                    file_name = "in_" + str(i_in) + ".txt"
                    file_path = contest_dir_path / problem / file_name
                    res.append({"path":file_path, "data":d.find("pre").string})
                if d.find("h3") is not None and (d.find("h3").text)[:3] == "出力例":
                    i_out += 1
                    file_name = "out_" + str(i_out) + ".txt"
                    file_path = contest_dir_path / problem / file_name
                    res.append({"path":file_path, "data":d.find("pre").string})
            case_count.append(i_in+i_out)
        print(case_count)
        return res

    def get_problem_list(self, url):
        self.driver.get(str(url))
        soup = BeautifulSoup(self.driver.page_source.encode('utf-8'), "html.parser")
        htmls = soup.find_all("td", class_="text-center no-break")
        res = []
        for html in htmls:
            res.append(html.text.lower())
        return res
    
    def get_target_problem_list(self, contest_problem_list, problems):
        if problems == "all":
            return contest_problem_list
        else:
            user_problem_list = []
            for p in problems:
                user_problem_list.append(p)
            return sorted(list(set(user_problem_list) & set(contest_problem_list)))
    
    def mkdir(self, parent, children):
        # 親ディレクトリがなければ作成
        if not parent.exists():
            parent.mkdir()
        # 子ディレクトリがなければ作成
        if type(children) is not list:
            children = [children]
        for child in children:
            if not (parent / child).exists():
                (parent / child).mkdir()

    def save(self, data):
        for d in data:
            path,data = d["path"],d["data"]
            # 既に存在したらスキップ
            if path.exists():
                print("exists : " + str(path))
            # 存在しなければ保存する
            else:
                # データがない場合は空ファイルを作成する
                if data is None:
                    with path.open(mode='w') as f:
                        f.write("")
                else:
                    with path.open(mode='w') as f:
                        f.write(data.string)
    
    def prepare_test(self, python_file):
        name = python_file.replace(".py","")
        contest = name.split("_")[0]
        problem = name.split("_")[1]
        commands = ["python"]
        commands.append(self.PYPRO_ATCODER_WORK_PATH / (name + ".py"))
        return (contest,problem,commands)
    
    def get_testcase_files(self, contest, problem):
        test_case_dir_path = self.data_dir_path / contest / problem
        return sorted(test_case_dir_path.glob("in_*.txt"))
    
    def exec_test(self, testcase_list, contest, problem, commands):
        # ケースがローカルにない場合
        if len(testcase_list) == 0:
            print("テストケースを事前にダウンロードしてください")
            sys.exit()
        # テスト実行
        test_case_dir = "data/" + contest + "/" + problem
        for testcase in testcase_list:
            input_data  = pkgutil.get_data("pypro", test_case_dir + "/" + testcase.name)
            output_data = pkgutil.get_data("pypro", test_case_dir + "/" + (testcase.name).replace("in", "out")) # あとでリファクタする
            res = subprocess.run(commands, input=input_data, check=True, stdout=subprocess.PIPE)
            
            status = "AC" if output_data==res.stdout else "WA"
            print(testcase.name + " : " + status)
            print("[input]")
            print(input_data.decode().rstrip('\n'))
            print("[expected]")
            print(output_data.decode().rstrip('\n'))
            print("[your answer]")
            print(res.stdout.decode().rstrip('\n'))
            print("")
    
    def get_work_dir_path(self, python_file):
        path = self.PYPRO_ATCODER_WORK_PATH / python_file
        if path.exists():
            return (path.parent, path.name)
        else:
            raise Exception
    
    def get_contest_date(self, file_name):
        # url
        name = file_name.replace(".py","")
        contest = name.split("_")[0]
        problem = name.split("_")[1]
        url = self.get_atcoder_url(contest)
        # 開催日時を取得
        self.driver.get(str(url))
        soup = BeautifulSoup(self.driver.page_source.encode('utf-8'), "html.parser")
        html = soup.find("time").text
        year  = html[0:4] 
        month = html[5:7]
        day   = html[8:10]
        return (year,month,day)
        
    def exec_git(self):
        print("git xxx をやっていく")


if __name__ == "__main__":
    atcoder()