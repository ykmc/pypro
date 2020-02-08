import click
import os
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
    # ファイル名に拡張子がついている場合、落とす
    filename = filename.replace(".py","")

    # 実行コマンドを作成
    args = ["python"]
    args.append(filename + ".py")

    contest, problem = filename.split("-")

    test_case_dir_path = Path(__file__).parent / "data" / contest / problem
    test_case_dir = "data/" + contest + "/" + problem

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

# pypa init abc153 -p all -t default
@main.command()
@click.argument("contest")
@click.option("-p", "--problem", "problem", type=str, help="initialization target", default="all")
@click.option("-t", "--template", "template", type=str, help="template file name", default="default.py")
def init(contest, problem, template):
    # 初期処理
    problem_list = []

    # バリデーション (コンテスト、環境変数、problems、templateなど)
    # 未実装
    
    # コンテストの問題記号を取得
    contest_dir_path = Path(__file__).parent / "data" / contest
    contest_problem_dir_path_list = sorted(contest_dir_path.glob("*"))
    for contest_problem_dir_path in contest_problem_dir_path_list:
        problem_list.append(contest_problem_dir_path.name)

    # 作成するファイル
    if problem == "all":
        target_file_list = problem_list
    # そのほかの指定
        # 例えば a, b, abc, ad, a:d 等
    # それ以外はエラー
    else:
        raise Exception

    cmd = ["cp", str(Path(os.getenv("PYPRO_ATCODER_TEMPLATE_DIR_PATH")) / template)]
    for target in target_file_list:
        cmd.append(os.getenv("PYPRO_WORK_DIR_PATH") + "/" + contest + "-" + target + ".py")
        res = subprocess.call(cmd)
        cmd.pop(-1)

    # 正常終了のメッセージ、気の利いた文言にしたい
    print("copy " + str(len(target_file_list)) + " files.")

# pypa get xxx
main.add_command(get)



if __name__ == "__main__":
    main()