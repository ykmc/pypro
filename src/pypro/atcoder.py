import click

@click.group()
def atcoder():
    pass

@atcoder.command()
def get():
    print("get")

@atcoder.command()
def init():
    print("init")

@atcoder.command()
def test():
    print("test")

@atcoder.command()
def git():
    print("git")

if __name__ == "__main__":
    atcoder()