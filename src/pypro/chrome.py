from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Chrome:
    
    def __init__(self):
        # データディレクトリへのパス (私のPCでしか動かないけどね)
        self.path_data_dir = Path("/Users/ykmc/src/github.com/ykmc/pypro/src/pypro/data")
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
            for d in div:
                if (d.find("h3").text)[:3] == "入力例":
                    # テストケースを保存
                    contest_dir = self.path_data_dir / contest
                    print(contest_dir)
                    if contest_dir.exists:
                        print("e")
                    else:
                        print("not e")

                    #print(d.find("pre").string)
                    #with p_new.open(mode='w') as f:
                    #    f.write('line 1\nline 2\nline 3')
