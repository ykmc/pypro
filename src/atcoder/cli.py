import click
import subprocess
import pkgutil
from atcoder.chrome import Chrome

@click.group()
def main():
    pass

@main.command()
@click.argument("name")
def test(name):
    #chrome = Chrome()
    #chrome.get()

    args = ["python"]
    args.append(name)
    #with open('x.txt', encoding='UTF-8') as fp:
    #    cp = subprocess.run(args, stdin=fp)

    input_str = pkgutil.get_data("atcoder", "data/abc153_a_in1.txt")
    cp = subprocess.run(args, input=input_str)


if __name__ == "__main__":
    main()