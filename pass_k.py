import json

import numpy as np
from pathlib import Path
import itertools
import argparse
import os


def estimator(n: int, c: int, k: int) -> float:
    """
    Calculates 1 - comb(n - c, k) / comb(n, k).
    """
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def for_file(path):
    with open(path, 'r') as f:
        # 读取 JSON 数据
        data = json.load(f)
    if data is None:
        return None
    n = len(data["results"])
    c = len([True for r in data["results"] if r["status"] == "OK" and r["exit_code"] == 0])
    return {
        "pass@1": estimator(n, c, 1),
        "pass@10": estimator(n, c, 10),
        "pass@100": estimator(n, c, 100),
        "n": n,
        "temperature": data["temperature"] if "temperature" in data else 0.2
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, help="The directory of the eval_results file ")
    args = parser.parse_args()

    results = []
    file_extension = '.results.json'  # 文件扩展名
    # 遍历指定目录下所有以 .results.json 结尾的文件
    for dirpath, dirnames, filenames in os.walk(args.dir):
        for filename in filenames:
            if filename.endswith(file_extension):
                file_path = os.path.join(dirpath, filename)
                results.append(for_file(file_path))

    # 去除空值
    results = [r for r in results if r is not None]
    pass_1 = np.mean([r["pass@1"] for r in results])
    pass_10 = np.mean([r["pass@10"] for r in results])
    pass_100 = np.mean([r["pass@100"] for r in results])
    num_problems = len(results)
    min_completions = np.min([r["n"] for r in results])
    max_completions = np.max([r["n"] for r in results])

    if (min_completions < 10):
        print(f"pass@1 : {pass_1}")
    elif (min_completions < 100):
        print(f"pass@1 : {pass_1}")
        print(f"pass@10 : {pass_10}")
    else:
        print(f"pass@100 : {pass_100}")


if __name__ == "__main__":
    main()
