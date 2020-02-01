import click

@click.group()
def main():
    pass

@main.command()
def test():
    print("test")

if __name__ == "__main__":
    main()