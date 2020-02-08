import click
from pypro.atcoder import atcoder

@click.group()
def main():
    pass

# --------------------------------
# pp atcoder xxx
# --------------------------------
main.add_command(atcoder)

if __name__ == "__main__":
    main()