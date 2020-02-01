from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Chrome:
    
    def get(self):
        # ブラウザのオプションを格納する変数をもらってきます。
        options = Options()
        # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
        options.set_headless(True)

        # ブラウザアクセス
        driver = webdriver.Chrome(chrome_options=options)
        driver.get("https://atcoder.jp/contests/abc153/tasks/abc153_a")

        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        # サンプルの取得
        div = soup.find_all("div", class_="part")
        for d in div:
            if (d.find("h3").text)[:3] == "入力例":
                print("input")
                print(d.find("pre").string)