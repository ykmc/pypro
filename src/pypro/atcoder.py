import click
import subprocess
import pkgutil

from pathlib import Path
import glob

from pypro.atcoder_get import get
from pypro.chrome import Chrome

@click.group()
def main():
    pass

# サンプルケースをチェックする（現在はローカルケースのみ対応）
@main.command()
@click.argument("filename")
def test(filename):
    args = ["python"]
    args.append(filename)

    contest, problem = filename.split("-")
    test_case_dir = "data/" + contest
    test_case_dir_path = Path("/Users/ykmc/src/github.com/ykmc/pypro/src/pypro/data/" + contest)

    testcase_list = sorted(test_case_dir_path.glob("in_*.txt"))
    for testcase in testcase_list:
        input_data  = pkgutil.get_data("pypro", test_case_dir + "/" + testcase.name)
        output_data = pkgutil.get_data("pypro", test_case_dir + "/" + (testcase.name).replace("in", "out")) # あとでリファクタする
        res = subprocess.run(args, input=input_data, check=True, stdout=subprocess.PIPE)
        
        status = "AC" if output_data==res.stdout else "WA"
        print(testcase.name + " : " + status)
        print("[input]")
        print(input_data.decode().rstrip('\n'))
        print("[expected]")
        print(output_data.decode().rstrip('\n'))
        print("[your answer]")
        print(res.stdout.decode().rstrip('\n'))
        print("")

# pypa get xxx
main.add_command(get)



if __name__ == "__main__":
    main()