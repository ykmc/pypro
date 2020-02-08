import click
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@click.group()
def atcoder():
    pass

@atcoder.command()
@click.argument("url")
@click.option("--problem", "-p", default="all")
def get(url, problem):
    atcoder = AtCoder()
    # contest が URLでない場合, URLに整形する
    if not atcoder.is_url(url):
        url = "https://atcoder.jp/contests/" + url
    # テストケースを取得
    data = atcoder.get(Path(url), problem)
    # テストケースを格納
    atcoder.save(data)

@atcoder.command()
def init():
    print("init")
    # ファイルが既にあるならエラー
    # ない場合、作成する

@atcoder.command()
@click.pass_context
def test(ctx):
    print("test")
    # ケースがローカルにない場合、getする
    #ctx.forward(get, problem="a")
    # テスト実行

@atcoder.command()
def git():
    print("git")
    # コンテスト日付を取得する
    # 格納先ディレクトリがなければ作る
    # mv
    # git add filepath
    # git commit -m "xxx"
    # git push origin master

class AtCoder:

    def __init__(self):
        self.data_dir_path = Path(__file__).parent / "data"
        self.options = Options()
        self.options.set_headless(True)
        self.driver = webdriver.Chrome(chrome_options=self.options)
    
    def is_url(self, string):
        if string[0:19] == "https://atcoder.jp/":
            return True
        else:
            return False
    
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
        for problem in target_problem_list:
            problem_url = url / (contest + "_" + problem)
            self.driver.get(str(problem_url))
            soup = BeautifulSoup(self.driver.page_source.encode('utf-8'), "html.parser")
            div = soup.find_all("div", class_="part")

            i_in, i_out = 0,0
            for d in div:
                if (d.find("h3").text)[:3] == "入力例":
                    i_in += 1
                    file_name = "in_" + str(i_in) + ".txt"
                    file_path = contest_dir_path / problem / file_name
                    res.append({"path":file_path, "data":d.find("pre").string})
                if (d.find("h3").text)[:3] == "出力例":
                    i_out += 1
                    file_name = "out_" + str(i_out) + ".txt"
                    file_path = contest_dir_path / problem / file_name
                    res.append({"path":file_path, "data":d.find("pre").string})            
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
    
    def mkdir(self, path, problems):
        # コンテストディレクトリがなければ作成
        if not path.exists():
            path.mkdir()
        # 問題ディレクトリがなければ作成
        for p in problems:
            if not (path / p).exists():
                (path / p).mkdir()

    def save(self, data):
        for d in data:
            path,data = d["path"],d["data"]
            # 既に存在したらスキップ
            if path.exists():
                print("exists : " + str(path))
            else:
                with path.open(mode='w') as f:
                    f.write(data.string)

if __name__ == "__main__":
    atcoder()