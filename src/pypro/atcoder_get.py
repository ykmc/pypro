import click
from pypro.chrome import Chrome

@click.group()
def get():
    pass

# test用
@get.command()
def list():
    click.echo('show list!!')

@get.command()
@click.argument("contest")
def case(contest):
    # abcのみ対応
    if contest[0:3] not in ["abc"]:
        raise Exception
    # case取得
    chrome = Chrome()
    chrome.get_case(contest)

if __name__ == '__main__':
    get()