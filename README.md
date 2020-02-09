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
# 絶対パスを設定する
export PYPRO_HOME=/Users/ykmc/src/github.com/ykmc/contest

# 以下、PYPRO_HOMEからの相対パスを設定する

# commit前のソースコードファイルをおく場所
export PYPRO_ATCODER_WORK_DIR=work
# atcoderの提出コードを保管するディレクトリ
export PYPRO_ATCODER_GIT_DIR=atcoder
# atcoderのpythonテンプレート
export PYPRO_ATCODER_TEMPLATE_DIR=template/atcoder
```