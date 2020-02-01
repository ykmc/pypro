import click
import subprocess
import pkgutil
from pypro.atcoder_get import get
from pypro.chrome import Chrome

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

    input_str = pkgutil.get_data("pypro", "data/abc153_a_in1.txt")
    cp = subprocess.run(args, input=input_str)

# pypa get xxx
main.add_command(get)



if __name__ == "__main__":
    main()