# atcoder-client-tools
何番煎じだよというツッコミ > /dev/null

# requirements

```
# python 3.8.0
pyenv install 3.8.0
pyenv local 3.8.0

# pipenv
pip install pipenv

# chromedriver
brew cask install chromedriver
```

# how to use

```sh
pipenv install git+https://github.com/ykmc/pypro.git@<release>#egg=pypro
```
release は v0.0.0的なやつ

環境変数の設定
```sh
# init時にファイルを出力するディレクトリ
export PPYPRO_WORK_DIR_PATH=/Users/ykmc/src/github.com/ykmc/contest/pypro/work
# init時に利用するテンプレートがあるディレクトリ
export PYPRO_ATCODER_TEMPLATE_DIR_PATH=/Users/ykmc/src/github.com/ykmc/contest/pypro/template-atcoder
```

