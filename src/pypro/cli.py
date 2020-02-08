import click
from pypro.atcoder import atcoder


@click.group()
def main():
    pass

main.add_command(atcoder)


if __name__ == "__main__":
    main()