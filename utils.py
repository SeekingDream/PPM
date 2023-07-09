
import gzip
import json
import os
from typing import Dict
import tempdir
import wget
from appdirs import user_cache_dir

# CACHE_DIR = user_cache_dir("CodeModel")

CACHE_DIR = "./workdir/Dataset"
HUMANEVAL_URL = (
    "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz"
)
human_eval_cleaned_doc = './workdir/Dataset/humaneval-py-transform.json'
human_eval_cs = './workdir/Dataset/humaneval-cs-transform.json'
human_eval_cpp = './workdir/Dataset/humaneval-cpp-transform.json'
human_eval_java = './workdir/Dataset/humaneval-java-transform.json'
mbpp_dir = './workdir/Dataset/mbpp-py-reworded.json'


def get_human_eval() -> Dict[str, Dict]:
    """Get HumanEval from OpenAI's github repo and return as a list of parsed dicts.

    Returns:
        List[Dict[str, str]]: List of dicts with keys "prompt", "test", "entry_point"

    Notes:
        "task_id" is the identifier string for the task.
        "prompt" is the prompt to be used for the task (function signature with docstrings).
        "test" is test-cases wrapped in a `check` function.
        "entry_point" is the name of the function.
    """
    # Check if human eval file exists in CACHE_DIR
    human_eval_path = os.path.join(CACHE_DIR, "HumanEval.jsonl")
    human_eval = None
    if not os.path.exists(human_eval_path):
        # Install HumanEval dataset and parse as jsonl
        # https://github.com/openai/human-eval/blob/master/data/HumanEval.jsonl.gz
        print("Downloading HumanEval dataset...")
        with tempdir.TempDir() as tmpdir:
            human_eval_gz_path = os.path.join(tmpdir, "HumanEval.jsonl.gz")
            wget.download(HUMANEVAL_URL, human_eval_gz_path)

            with gzip.open(human_eval_gz_path, "rb") as f:
                human_eval = f.read().decode("utf-8")

        # create CACHE_DIR if not exists
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

        # Write the original human eval file to CACHE_DIR
        with open(human_eval_path, "w") as f:
            f.write(human_eval)

    human_eval = open(human_eval_path, "r").read() if not human_eval else human_eval
    human_eval = human_eval.split("\n")
    human_eval = [json.loads(line) for line in human_eval if line]


    # Handle 115_max_fill.py to make its docstring well-formed
    human_eval[114]["prompt"] = "import math\n" + human_eval[114]["prompt"].replace(
        "import math\n", ""
    )

    return {task["task_id"]: task for task in human_eval}


def get_human_eval_cleaned_doc() -> Dict[str, Dict]:
    with open(human_eval_cleaned_doc, 'r') as f:
        data = json.load(f)

    for task in data:
        name = task['name']
        pos = name.find("_", name.find("_") + 1)
        task['task_id'] = name[:pos]
        task['entry_point'] = name[pos + 1:]

    return {task["task_id"]: task for task in data}


def get_mbpp() -> Dict[str, Dict]:
    with open(mbpp_dir, 'r') as f:
        data = json.load(f)

    for task in data:
        name = task['name']
        pos = name.find("_", name.find("_") + 1)
        task['task_id'] = name[:pos]
        task['entry_point'] = name[pos + 1:]

    return {task["task_id"]: task for task in data}


def get_humaneval_cs() -> Dict[str, Dict]:
    with open(human_eval_cs, 'r') as f:
        data = json.load(f)

    for task in data:
        name = task['name']
        pos = name.find("_", name.find("_") + 1)
        task['task_id'] = name[:pos]
        task['entry_point'] = name[pos + 1:]

    return {task["task_id"]: task for task in data}

def get_humaneval_cpp() -> Dict[str, Dict]:
    with open(human_eval_cpp, 'r') as f:
        data = json.load(f)

    for task in data:
        name = task['name']
        pos = name.find("_", name.find("_") + 1)
        task['task_id'] = name[:pos]
        task['entry_point'] = name[pos + 1:]

    return {task["task_id"]: task for task in data}

def get_humaneval_java() -> Dict[str, Dict]:
    with open(human_eval_java, 'r') as f:
        data = json.load(f)

    for task in data:
        name = task['name']
        pos = name.find("_", name.find("_") + 1)
        task['task_id'] = name[:pos]
        task['entry_point'] = name[pos + 1:]

    return {task["task_id"]: task for task in data}


def get_dataset(dataset):
    if dataset == 'humaneval':
        return get_human_eval_cleaned_doc()  # 传递相应的参数
    elif dataset == 'mbpp':
        return get_mbpp()  # 传递相应的参数
    elif dataset == 'humaneval_cs':
        return get_humaneval_cs()  # 传递相应的参数
    elif dataset == 'humaneval_cpp':
        return get_humaneval_cpp()  # 传递相应的参数
    elif dataset == 'humaneval_java':
        return get_humaneval_java()  # 传递相应的参数
    else:
        raise ValueError('Invalid param')
