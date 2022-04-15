#!/usr/bin/python3
import argparse
import re
import pymysql
import json
import os
import subprocess
import traceback
import tempfile
from typing import Callable, List, Tuple

pas: str = "../tests/"


def check_exist(ref_json: json, error_json: json, col: str) -> bool:
    try:
        for item in ref_json["errors"]["errors"]:
            for chk in error_json["errors"]:
                if item["kind"] == chk["kind"]:
                    return True
        return False
    except:
        return False


def hash_list_to_string(hash_list) -> str:
    return str(hash_list["location"])+str(hash_list["kind"])


def check_location(ref_loc: List[int], out_loc: List[int]):
    # if abs(ref_loc[0] - out_loc[0]) < 10 and abs(ref_loc[1] - out_loc[1]) < 10 and abs(ref_loc[2] - out_loc[2]) < 10 and abs(ref_loc[3] - out_loc[3]) < 10:
    #     return True
    return True


def check_good(ref, out_json):
    cur_item = out_json
    for i in cur_depth:
        cur_item = cur_item[i]
    for item in ref:
        if isinstance(ref[item], list):
            if any(isinstance(j, int) for j in ref[item]) and check_location(ref[item], cur_item[item]) or len(ref[item]) == 0:
                pass
            else:
                cur_depth.append(item)
                for i1, j1 in enumerate(ref[item]):
                    cur_depth.append(i1)
                    if not dfs(visited, j1, out_json,
                               j1):
                        return False
                    cur_depth.pop()
                cur_depth.pop()
        elif isinstance(ref[item], dict):
            cur_depth.append(item)
            if check_good(ref[item], out_json):
                return False
            cur_depth.pop()
        elif ref[item] != cur_item[item]:
            return False


visited = set()

# dfs check ref_json that out has.


cur_depth = []


def dfs(visited, ref_json, out_json, node):
    hashed_node = hash_list_to_string(node)
    if hashed_node not in visited:
        visited.add(hashed_node)
        try:
            cur_depth.append("statements")
            for i, neighbor in enumerate(ref_json["statements"]):
                cur_depth.append(i)
                cur_item = out_json
                for item in cur_depth:
                    cur_item = cur_item[item]

                # check everything except location
                for item in neighbor:
                    if isinstance(neighbor[item], list):
                        if any(isinstance(j, int) for j in neighbor[item]) and check_location(neighbor[item], cur_item[item]) or len(neighbor[item]) == 0:
                            pass
                        else:
                            cur_depth.append(item)
                            for i1, j1 in enumerate(neighbor[item]):
                                if isinstance(neighbor[item], list):
                                    cur_depth.append(i1)
                                else:
                                    cur_depth.append(j1)
                                if not dfs(visited, j1, out_json,
                                           j1):
                                    return False
                                cur_depth.pop()
                            cur_depth.pop()
                    elif isinstance(neighbor[item], dict):
                        cur_depth.append(item)
                        if check_good(neighbor[item], out_json):
                            return False
                        cur_depth.pop()
                    elif neighbor[item] != cur_item[item]:
                        return False
                cur_depth.pop()
            cur_depth.clear()
        except:
            cur_depth.pop()
            cur_depth.append("declarations")
            try:
                for i, neighbor in enumerate(ref_json["declarations"]):
                    cur_depth.append(i)
                    cur_item = out_json
                    for item in cur_depth:
                        cur_item = cur_item[item]

                    # check everything except location
                    for item in neighbor:
                        if isinstance(neighbor[item], list):
                            if any(isinstance(j, int) for j in neighbor[item]) and check_location(neighbor[item], cur_item[item]) or len(neighbor[item]) == 0:
                                pass
                            else:
                                for i1, j1 in enumerate(neighbor[item]):
                                    cur_depth.append(item)
                                    cur_depth.append(i1)
                                    if dfs(visited, j1, out_json,
                                           j1):
                                        return False
                                    cur_depth.pop()
                        elif isinstance(neighbor[item], dict):
                            cur_depth.append(item)
                            if check_good(neighbor[item], out_json):
                                return False
                            cur_depth.pop()
                        elif neighbor[item] != cur_item[item]:
                            return False
                    cur_depth.pop()
                cur_depth.clear()
            except:
                try:
                    cur_depth.pop()
                    cur_item = out_json
                    for item in cur_depth:
                        cur_item = cur_item[item]
                    neighbor = ref_json
                    # check everything except location
                    for item in neighbor:
                        if isinstance(neighbor[item], list):
                            if any(isinstance(j, int) for j in neighbor[item]) and check_location(neighbor[item], cur_item[item]) or len(neighbor[item]) == 0:
                                pass
                            else:
                                cur_depth.append(item)
                                for i2, j2 in enumerate(neighbor[item]):
                                    cur_depth.append(i2)
                                    if not dfs(visited, j2, out_json,
                                               j2):
                                        return False
                                    cur_depth.pop()
                                cur_depth.pop()
                        elif isinstance(neighbor[item], dict):
                            cur_depth.append(item)
                            if check_good(neighbor[item], out_json):
                                return False
                            cur_depth.pop()
                        elif neighbor[item] != cur_item[item]:
                            return False
                except:
                    cur_item = out_json
                    for item in cur_depth:
                        cur_item = cur_item[item]
                    neighbor = ref_json
                    # check everything except location
                    for item in neighbor:
                        if isinstance(neighbor[item], list):
                            if any(isinstance(j, int) for j in neighbor[item]) and check_location(neighbor[item], cur_item[item]) or len(neighbor[item]) == 0:
                                pass
                            else:
                                cur_depth.append(item)
                                for i2, j2 in enumerate(neighbor[item]):
                                    cur_depth.append(i2)
                                    if not dfs(visited, j2, out_json,
                                               j2):
                                        return False
                                    cur_depth.pop()
                                cur_depth.pop()
                        elif isinstance(neighbor[item], dict):
                            cur_depth.append(item)
                            if check_good(neighbor[item], out_json):
                                return False
                            cur_depth.pop()
                        elif neighbor[item] != cur_item[item]:
                            return False
        return True


def check_stage(ref: str, out: str) -> bool:
    ref_json = json.loads(ref)
    out_json = json.loads(out)
    if check_exist(ref_json, out_json,
                   "errors"):
        return True
    try:
        if dfs(visited, ref_json, out_json, ref_json["statements"][0]):
            return True
    except:
     try:
        if dfs(visited, ref_json, out_json, ref_json["declarations"][0]):
            return True
     except:
        print("fall back to naive check")
        return check_stage_naive(ref,out)
    return False


def check_stage_naive(ref: str, out: str) -> bool:
    pattern = r'"location"\s*:\s*\[.+?\],'
    mod_ref = re.sub(pattern, '', ref)
    mod_out = re.sub(pattern, '', out)
    ref_json = json.loads(mod_ref)
    out_json = json.loads(mod_out)
    if check_exist(ref_json, out_json,
                   "errors"):
        return True
    if ref_json == out_json:
        return True
    return False


def check_once(pa_index: int):
    """
    parameter:
      pa_index(int): one of 1,2,3,4
    return:
      whether the solution has passed
    """

    count: list = [0, 0, 0]
    success_count: list = [0, 0, 0]
    test_results: list = []

    pa_roots: List[str] = ['/sample', '/student', '/fuzz']
    for i, pa_root in enumerate(pa_roots):
        try:
            pa_root = os.path.join(pas + f'pa{pa_index}' + pa_root)
        except:
            break
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

        for case in test_cases:
            reference_output_path: str = {
                1: os.path.join(pa_root, f'{case}.ast'),
                2: os.path.join(pa_root, f'{case}.out.typed'),
                3: os.path.join(pa_root, f'{case}.typed.ll.result'),
                4: os.path.join(pa_root, f'{case}.ast.typed.s.result'),
            }[pa_index]
            reference_output: str
            if pa_index == 1 or pa_index == 2:
                reference_output_path_out: str = reference_output_path+".bak"
                print(" ".join(["../build/cjson_formatter",
                      reference_output_path, ">", reference_output_path_out]))
                os.system(
                    " ".join(["../build/cjson_formatter", reference_output_path, ">", reference_output_path_out]))
                reference_output = readfile(reference_output_path_out).strip()
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
                # print(" ".join(program_path.split(" ") +
                #       [os.path.join(pa_root, case)]))
                program_output = subprocess.run(
                    program_path.split(" ") + [os.path.join(pa_root, case)],
                    capture_output=True).stdout.decode('utf-8').replace(" ", "").replace("bblloader", "").strip()

            checker: Callable[[str, str], bool] = {
                1: lambda std, out: check_stage(std, out),
                2: lambda std, out: check_stage(std, out),
                3: lambda std, out: std == out,
                4: lambda std, out: std == out,
            }[pa_index]

            test_results.append(f'begin({case})')
            count[i] += 1
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
                    success_count[i] += 1
                    test_results.append('*Success!*')

            except BaseException as e:
                test_results.append(f'*FAILED* with exception')
                with tempfile.TemporaryFile('w+') as f:
                    traceback.print_exception(
                        type(e), e, e.__traceback__, file=f)
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
        print(
            f'{count[i]} tests, {success_count[i]} success, {count[i] - success_count[i]} failed in '+pa_root)
    for i in test_results:
        print(i)
    return sum(success_count)


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

    pa = args.pa[0]
    print(f'[pa{pa} test begin]')
    score = check_once(pa)
    # print(res)
    print(f'The final score is {score}')