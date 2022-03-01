#!/usr/bin/python3
import argparse
import json
import os
import subprocess
import traceback
import tempfile
from typing import Callable


def check_exist(ref_json: json, error_json: json, col: str) -> bool:
    try:
        for item in error_json[col]:
            for chk in ref_json[col]:
                if item == chk:
                    return True
        return False
    except:
        return False


def check_once(pa_index: int) -> list:
    """
    parameter:
      pa_index(int): one of 1,2,3,4
    return:
      whether the solution has passed
    """

    count: int = 0
    success_count: int = 0

    pa_root: str = os.path.join(f'../tests/pa{pa_index}', 'sample')
    files: list = [
        f
        for f in os.listdir(pa_root)
        if os.path.isfile(os.path.join(pa_root, f))
    ]
    is_testcase: Callable[[str], bool] = {
        1: lambda file_name: '.ast' not in file_name,
        2: lambda file_name: '.out' not in file_name,
        3: lambda
            file_name: '.typed' not in file_name and '.in' not in file_name and '.s' not in file_name and '.ll' not in file_name and '.py' in file_name,
        4: lambda file_name: '.typed' not in file_name and '.in' not in file_name and '.s' not in file_name,
    }[pa_index]
    test_cases: list = [
        file
        for file in files
        if is_testcase(file)
    ]

    test_results: list = []
    for case in test_cases:
        reference_output_path: str = {
            1: os.path.join(pa_root, f'{case}.ast'),
            2: os.path.join(pa_root, f'{case}.out.typed'),
            3: os.path.join(pa_root, f'{case}.typed.ll.result'),
            4: os.path.join(pa_root, f'{case}.ast.typed.s.result'),
        }[pa_index]
        reference_output: str
        if pa_index == 1 or pa_index == 2:
            reference_output = subprocess.run(
                ["../build/cjson_formatter", reference_output_path],
                capture_output=True, shell=True).stdout.decode('utf-8').replace(" ", "").strip()
        else:
            reference_output = readfile(reference_output_path).strip()

        program_path: str = {
            1: '../build/parser',
            2: '../build/semantic',
            3: './ir-optimizer -run',
            4: './cgen -run',
        }[pa_index]
        if pa == 3 or pa == 4:
            os.chdir('../build')
        program_output: str
        if case == "input.py":
            cmd = program_path.split(" ") + [os.path.join(pa_root, case)]
            text_file = open("../tests/pa3/sample/input.py.in", "r")
            data = text_file.read()
            text_file.close()
            ip = data.encode('utf-8')
            result = subprocess.run(cmd, stdout=subprocess.PIPE, input=ip)
            program_output = result.stdout.decode('utf-8')
        else:
            print(" ".join(program_path.split(" ") + [os.path.join(pa_root, case)]))
            program_output = subprocess.run(
                program_path.split(" ") + [os.path.join(pa_root, case)],
                capture_output=True).stdout.decode('utf-8').replace(" ", "").replace("bblloader", "").strip()

        checker: Callable[[str, str], bool] = {
            1: lambda std, out: json.loads(std) == json.loads(out) or check_exist(json.loads(std), json.loads(out),
                                                                                  "errors"),
            2: lambda std, out: json.loads(std) == json.loads(out) or check_exist(json.loads(std), json.loads(out),
                                                                                  "errors"),
            3: lambda std, out: std == out,
            4: lambda std, out: std == out,
        }[pa_index]

        test_results.append(f'begin({case})')
        count += 1
        try:
            if not checker(reference_output, program_output):
                test_results.append('*FAILED* incorrect output')
                test_results.append(f'begin expected')
                test_results.append(reference_output)
                test_results.append(f'end expected')
                test_results.append(f'begin output')
                test_results.append(program_output)
                test_results.append(f'end output')
            else:
                success_count += 1
                test_results.append('*Success!*')

        except BaseException as e:
            test_results.append(f'*FAILED* with exception')
            with tempfile.TemporaryFile('w+') as f:
                traceback.print_exception(type(e), e, e.__traceback__, file=f)
                f.flush()
                f.seek(0)
                test_results.append(f.read())
            test_results.append(f'begin expected')
            test_results.append(reference_output)
            test_results.append(f'end expected')
            test_results.append(f'begin output')
            test_results.append(program_output)
            test_results.append(f'end output')
            break
        finally:
            test_results.append(f'end({case})\n')
    print(f'{count} tests, {success_count} success, {count - success_count} failed')
    return test_results


def readfile(path: str) -> str:
    contents = ''
    with open(path, 'r') as f:
        contents = f.read()
    return contents


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="duipai for ChocoPy")
    parser.add_argument("--pa", metavar="N", type=int, nargs="+")

    args = parser.parse_args()
    if args.pa is None:
        parser.print_help()
        os.sys.exit(1)

    for pa in args.pa:
        print(f'[pa{pa} test begin]')
        res: list = check_once(pa)
        for i in res:
            print(i)
