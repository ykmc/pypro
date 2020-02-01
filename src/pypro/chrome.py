from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Chrome:
    
    def __init__(self):
        # データディレクトリへのパス (私のPCでしか動かないけどね)
        self.data_dir_path = Path("/Users/ykmc/src/github.com/ykmc/pypro/src/pypro/data")
        # browser options
        self.options = Options()
        # headless mode
        self.options.set_headless(True)
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def get_case(self, contest):
        # URLの組み立て
        base_url = "https://atcoder.jp/contests/" + contest + "/tasks/" + contest
        # ページを取得
        for problem in "a": # "abcdef" になおす、あとでやる
            url = base_url + "_" + problem
            self.driver.get(url)
            html = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "html.parser")

            # テストケースの取得
            div = soup.find_all("div", class_="part")
            i_in, i_out = 0,0
            for d in div:
                if (d.find("h3").text)[:3] == "入力例":
                    # サンプルケースを格納するコンテストディレクトリがなければ作成する
                    contest_dir_path = self.data_dir_path / contest
                    if not contest_dir_path.exists():
                        contest_dir_path.mkdir()
                    
                    # サンプルケースのナンバリング
                    i_in += 1
                    filename = "in_" + str(i_in) + ".txt"
                    file_path = contest_dir_path / filename
                    
                    # サンプルケースの存在確認
                    if file_path.exists():
                        print("exists : " + str(file_path))
                    else:
                        with file_path.open(mode='w') as f:
                            f.write(d.find("pre").string)
                
                if (d.find("h3").text)[:3] == "出力例":
                    # サンプルケースのナンバリング
                    i_out += 1
                    filename = "out_" + str(i_out) + ".txt"
                    file_path = contest_dir_path / filename

                    # サンプルケースの存在確認
                    if file_path.exists():
                        print("exists : " + str(file_path))
                    else:
                        with file_path.open(mode='w') as f:
                            f.write(d.find("pre").string)
