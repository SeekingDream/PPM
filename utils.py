
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


dataset1 = [
    {
        "id": '0',
        "prompt":
            "from typing import List\n\n\n"
            "def int2float(numbers: List[int]) -> List[float]:\n"
            "    \"\"\" Change all int type values of input list to float type, and add by 0.1.\n"
            "    >>> int2float([1, 2, 3])\n    [1.1, 2.1, 3.1]\n"
            "    >>> int2float([1, 2, 3, 4, 5, 2])\n    [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
            "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
            "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
            "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
            "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
            "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
            "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n"
            "def test_check():\n"
            "    check(int2float)\n\n"
            "test_check()\n"

    },
    {
        "id": '1',
        "prompt":
            "from typing import List\n\n\n"
            "def int2string(numbers: List[int]) -> List[str]:\n"
            "    \"\"\" Change all int type values of input list to string type, each string would be the int value add one.\n"
            "    >>> int2string([1, 2, 3])\n    ['2', '3', '4']\n"
            "    >>> int2string([1, 2, 3, 4, 5, 2])\n    ['2', '3', '4', '5', '6', '3']\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([1, 2, 4, 4, 5, 2]) == ['2', '3', '5', '5', '6', '3']\n"
            "    assert candidate([1, 2, 3, 4, 5, 2]) == ['2', '3', '4', '5', '6', '3']\n"
            "    assert candidate([1, 2, 5, 4, 5]) == ['2', '3', '6', '5', '6']\n"
            "    assert candidate([1, 2, 5, 3, 5]) == ['2', '3', '6', '4', '6']\n"
            "    assert candidate([1, 2, 3, 4, 6, 2]) == ['2', '3', '4', '5', '7', '3']\n"
            "    assert candidate([1, 2, 3, 4, 9]) == ['2', '3', '4', '5', '10']\n"
            "    assert candidate([1, 2, 3, 2, 5]) == ['2', '3', '4', '3', '6']\n\n"
            "def test_check():\n"
            "    check(int2string)\n\n"
            "test_check()\n"

    },
    {
        "id": '2',
        "prompt":
            "from typing import List\n\n\n"
            "def int2bool(numbers: List[int]) -> List[bool]:\n"
            "    \"\"\" Change all int type values of the input list to bool type, change all odd values to True, and all even values to False.\n"
            "    >>> int2bool([1, 2, 3])\n    [True, False, True]\n"
            "    >>> int2bool([1, 2, 3, 4, 5, 2])\n    [True, False, True, False, True, False]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([1, 2, 4, 4, 5, 2]) == [True, False, False, False, True, False]\n"
            "    assert candidate([1, 2, 3, 4, 5, 2]) == [True, False, True, False, True, False]\n"
            "    assert candidate([1, 2, 5, 4, 5]) == [True, False, True, False, True]\n"
            "    assert candidate([1, 2, 5, 3, 5]) == [True, False, True, True, True]\n"
            "    assert candidate([1, 2, 3, 4, 6, 2]) == [True, False, True, False, False, False]\n"
            "    assert candidate([1, 2, 3, 4, 9]) == [True, False, True, False, True]\n"
            "    assert candidate([1, 2, 3, 2, 5]) == [True, False, True, False, True]\n\n"
            "def test_check():\n"
            "    check(int2bool)\n\n"            
            "test_check()\n"
    },

    {
        "id": '3',
        "prompt":
            "from typing import List\n\n\n"
            "def float2int(numbers: List[float]) -> List[int]:\n"
            "    \"\"\" Change all float type values of the input list to int type, keep the integer part of the float plus 1.\n"
            "    >>> float2int([1.1, 2.1, 3.1])\n"
            "    [2, 3, 4]\n"
            "    >>> float2int([1.1, 2.1, 3.1, 4.1, 5.1, 2.1])\n"
            "    [2, 3, 4, 5, 6, 3]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([1.1, 2.1, 4.1, 4.1, 5.1, 2.1]) == [2, 3, 5, 5, 6, 3]\n"
            "    assert candidate([1.1, 2.1, 3.1, 4.1, 5.1, 2.1]) == [2, 3, 4, 5, 6, 3]\n"
            "    assert candidate([1.1, 2.1, 5.1, 4.1, 5.1]) == [2, 3, 6, 5, 6]\n"
            "    assert candidate([1.1, 2.1, 5.1, 3.1, 5.1]) == [2, 3, 6, 4, 6]\n"
            "    assert candidate([1.1, 2.1, 3.1, 4.1, 6.1, 2.1]) == [2, 3, 4, 5, 7, 3]\n"
            "    assert candidate([1.1, 2.1, 3.1, 4.1, 9.1]) == [2, 3, 4, 5, 10]\n"
            "    assert candidate([1.1, 2.1, 3.1, 2.1, 5.1]) == [2, 3, 4, 3, 6]\n\n"
            "def test_check():\n"
            "    check(float2int)\n\n"      
            "test_check()\n"          

    },
    {
        "id": '4',
        "prompt":
            "from typing import List\n\n\n"
            "def float2string(numbers: List[float]) -> List[str]:\n"
            "    \"\"\" Change all float type values of the input list to string type, return the string value of integer part plus 1.\n"
            "    >>> float2string([1.1, 2.1, 3.1])\n"
            "    ['2', '3', '4']\n"
            "    >>> float2string([1.1, 2.1, 3.1, 4.1, 5.1, 2.1])\n"
            "    ['2', '3', '4', '5', '6', '3']\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([1.1, 2.1, 4.1, 4.1, 5.1, 2.1]) == ['2', '3', '5', '5', '6', '3']\n"
            "    assert candidate([1.1, 2.1, 3.1, 4.1, 5.1, 2.1]) == ['2', '3', '4', '5', '6', '3']\n"
            "    assert candidate([1.1, 2.1, 5.1, 4.1, 5.1]) == ['2', '3', '6', '5', '6']\n"
            "    assert candidate([1.1, 2.1, 5.1, 3.1, 5.1]) == ['2', '3', '6', '4', '6']\n"
            "    assert candidate([1.1, 2.1, 3.1, 4.1, 6.1, 2.1]) == ['2', '3', '4', '5', '7', '3']\n"
            "    assert candidate([1.1, 2.1, 3.1, 4.1, 9.1]) == ['2', '3', '4', '5', '10']\n"
            "    assert candidate([1.1, 2.1, 3.1, 2.1, 5.1]) == ['2', '3', '4', '3', '6']\n\n"
            "def test_check():\n"
            "    check(float2string)\n\n" 
            "test_check()\n"   
    },
    {
        "id": '5',
        "prompt":
            "from typing import List\n\n\n"
            "def float2bool(numbers: List[float]) -> List[bool]:\n"
            "    \"\"\" Change all float type values of the input list to bool type, if the float value is larger than 0.0, return True, else return False.\n"
            "    >>> float2bool([1.1, -2.1, 3.1])\n"
            "    [True, False, True]\n"
            "    >>> float2bool([-1.1, 2.1, -3.1, -4.1, 5.1, 2.1])\n"
            "    [False, True, False, False, True, True]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([-1.1, 2.1, -4.1, -4.1, 5.1, 2.1]) == [False, True, False, False, True, True]\n"
            "    assert candidate([1.1, 2.1, -3.1, -4.1, 5.1, 2.1]) == [True, True, False, False, True, True]\n"
            "    assert candidate([-1.1, 2.1, -5.1, 4.1, -5.1]) == [False, True, False, True, False]\n"
            "    assert candidate([1.1, 2.1, 5.1, 3.1, 5.1]) == [True, True, True, True, True]\n"
            "    assert candidate([-1.1, 2.1, 3.1, -4.1, 6.1, 2.1]) == [False, True, True, False, True, True]\n"
            "    assert candidate([-1.1, -2.1, -3.1, -4.1, -9.1]) == [False, False, False, False, False]\n"
            "    assert candidate([-1.1, 2.1, 3.1, 2.1, -5.1]) == [False, True, True, True, False]\n\n"
            "def test_check():\n"
            "    check(float2bool)\n\n" 
            "test_check()\n"             

    },

    {
        "id": '6',
        "prompt":
            "from typing import List\n\n\n"
            "def string2int(numbers: List[str]) -> List[int]:\n"
            "    \"\"\" Change all string type values of the input list to int type, each int value would be the length of the string plus 1.\n"
            "    >>> string2int(['hello', 'my', 'name'])\n"
            "    [6, 3, 5]\n"
            "    >>> string2int(['hello', 'my', 'name', 'machine', 'learning'])\n"
            "    [6, 3, 5, 8, 9]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate(['play', 'this', 'game', 'apple']) == [5, 5, 5, 6]\n"
            "    assert candidate(['school', 'AI', 'Yes', 'admin', 'hi']) == [7, 3, 4, 6, 3]\n"
            "    assert candidate(['Is', 'the', 'sky', 'blue', 'love', 'It']) == [3, 4, 4, 5, 5, 3]\n"
            "    assert candidate(['there', 'is', 'no', 'place', 'available', 'here']) == [6, 3, 3, 6, 10, 5]\n"
            "    assert candidate(['Hi', 'I', 'am', 'Hussein']) == [3, 2, 3, 8]\n"
            "    assert candidate(['Mary', 'had', 'a', 'little', 'lamb']) == [5, 4, 2, 7, 5]\n"
            "    assert candidate(['One', 'two', 'three', 'four', 'five', 'six']) == [4, 4, 6, 5, 5, 4]\n\n"
            "def test_check():\n"
            "    check(string2int)\n\n"
            "test_check()\n"  

    },
    {
        "id": '7',
        "prompt":
            "from typing import List\n\n\n"
            "def string2float(numbers: List[str]) -> List[float]:\n"
            "    \"\"\" Change all string type values of the input list to int type, each int value would be the length of the string plus 1.1.\n"
            "    >>> string2float(['hello', 'my', 'name'])\n"
            "    [6.1, 3.1, 5.1]\n"
            "    >>> string2float(['hello', 'my', 'name', 'machine', 'learning'])\n"
            "    [6.1, 3.1, 5.1, 8.1, 9.1]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate(['play', 'this', 'game', 'apple']) == [5.1, 5.1, 5.1, 6.1]\n"
            "    assert candidate(['school', 'AI', 'Yes', 'admin', 'hi']) == [7.1, 3.1, 4.1, 6.1, 3.1]\n"
            "    assert candidate(['Is', 'the', 'sky', 'blue', 'love', 'It']) == [3.1, 4.1, 4.1, 5.1, 5.1, 3.1]\n"
            "    assert candidate(['there', 'is', 'no', 'place', 'available', 'here']) == [6.1, 3.1, 3.1, 6.1, 10.1, 5.1]\n"
            "    assert candidate(['Hi', 'I', 'am', 'Hussein']) == [3.1, 2.1, 3.1, 8.1]\n"
            "    assert candidate(['Mary', 'had', 'a', 'little', 'lamb']) == [5.1, 4.1, 2.1, 7.1, 5.1]\n"
            "    assert candidate(['One', 'two', 'three', 'four', 'five', 'six']) == [4.1, 4.1, 6.1, 5.1, 5.1, 4.1]\n\n"
            "def test_check():\n"
            "    check(string2float)\n\n" 
            "test_check()\n" 
    },
    {
        "id": '8',
        "prompt":
            "from typing import List\n\n\n"
            "def string2bool(numbers: List[str]) -> List[bool]:\n"
            "    \"\"\" Change all string type values of the input list to bool type, change all odd-length strings to True, and all even-length strings to False.\n"
            "    >>> string2bool(['hello', 'my', 'name'])\n"
            "    [True, False, False]\n"
            "    >>> string2bool(['hello', 'my', 'name', 'machine', 'learning'])\n"
            "    [True, False, False, True, False]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate(['play', 'this', 'game', 'apple']) == [False, False, False, True]\n"
            "    assert candidate(['school', 'AI', 'Yes', 'admin', 'hi']) == [False, False, True, True, False]\n"
            "    assert candidate(['Is', 'the', 'sky', 'blue', 'love', 'It']) == [False, True, True, False, False, False]\n"
            "    assert candidate(['there', 'is', 'no', 'place', 'available', 'here']) == [True, False, False, True, True, False]\n"
            "    assert candidate(['Hi', 'I', 'am', 'Hussein']) == [False, True, False, True]\n"
            "    assert candidate(['Mary', 'had', 'a', 'little', 'lamb']) == [False, False, False, True, True]\n"
            "    assert candidate(['One', 'two', 'three', 'four', 'five', 'six']) == [True, True, True, False, False, True]\n\n"
            "def test_check():\n"
            "    check(string2bool)\n\n"
            "test_check()\n" 

    },

    {
        "id": '9',
        "prompt":
            "from typing import List\n\n\n"
            "def bool2int(numbers: List[bool]) -> List[int]:\n"
            "    \"\"\" Change all bool type values of the input list to int type,  and add 1.\n"
            "    >>> bool2int([True, False, True])\n"
            "    [2, 1, 2]\n"
            "    >>> bool2int([True, False, True, False, False])\n"
            "    [2, 1, 2, 1, 1]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([True, False, True, False, False]) == [2, 1, 2, 1, 1]\n"
            "    assert candidate([False, False, True, False, True, True]) == [1, 1, 2, 1, 2, 2]\n"
            "    assert candidate([False, False, True, False, True]) == [1, 1, 2, 1, 2]\n"
            "    assert candidate([True, True, False, True, True]) == [2, 2, 1, 2, 2]\n"
            "    assert candidate([True, True, False, False, False, True]) == [2, 2, 1, 1, 1, 2]\n"
            "    assert candidate([True, False, True, False, False]) == [2, 1, 2, 1, 1]\n"
            "    assert candidate([False, False, True, False, True]) == [1, 1, 2, 1, 2]\n\n"
            "def test_check():\n"
            "    check(bool2int)\n\n" 
            "test_check()\n"
    },
    {
        "id": '10',
        "prompt":
            "from typing import List\n\n\n"
            "def bool2float(numbers: List[bool]) -> List[float]:\n"
            "    \"\"\" Change all bool type values of the input list to int type,  and add 1.1.\n"
            "    >>> bool2float([True, False, True])\n"
            "    [2.1, 1.1, 2.1]\n"
            "    >>> bool2float([True, False, True, False, False])\n"
            "    [2.1, 1.1, 2.1, 1.1, 1.1]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([True, False, True, False, False]) == [2.1, 1.1, 2.1, 1.1, 1.1]\n"
            "    assert candidate([False, False, True, False, True, True]) == [1.1, 1.1, 2.1, 1.1, 2.1, 2.1]\n"
            "    assert candidate([False, False, True, False, True]) == [1.1, 1.1, 2.1, 1.1, 2.1]\n"
            "    assert candidate([True, True, False, True, True]) == [2.1, 2.1, 1.1, 2.1, 2.1]\n"
            "    assert candidate([True, True, False, False, False, True]) == [2.1, 2.1, 1.1, 1.1, 1.1, 2.1]\n"
            "    assert candidate([True, False, True, False, False]) == [2.1, 1.1, 2.1, 1.1, 1.1]\n"
            "    assert candidate([False, False, True, False, True]) == [1.1, 1.1, 2.1, 1.1, 2.1]\n\n"
            "def test_check():\n"
            "    check(bool2float)\n\n"
            "test_check()\n" 
    },
    {
        "id": '11',
        "prompt":
            "from typing import List\n\n\n"
            "def bool2string(numbers: List[bool]) -> List[str]:\n"
            "    \"\"\" Change all bool type values of input list to string type, and change True to 'A', and False to 'B'.\n"
            "    >>> bool2string([True, False, True])\n"
            "    ['A', 'B', 'A']\n"
            "    >>> bool2string([True, False, True, False, False])\n"
            "    ['A', 'B', 'A', 'B', 'B']\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([True, False, True, False, False]) == ['A', 'B', 'A', 'B', 'B']\n"
            "    assert candidate([False, False, True, False, True, True]) == ['B', 'B', 'A', 'B', 'A', 'A']\n"
            "    assert candidate([False, False, True, False, True]) == ['B', 'B', 'A', 'B', 'A']\n"
            "    assert candidate([True, True, False, True, True]) == ['A', 'A', 'B', 'A', 'A']\n"
            "    assert candidate([True, True, False, False, False, True]) == ['A', 'A', 'B', 'B', 'B', 'A']\n"
            "    assert candidate([True, False, True, False, False]) == ['A', 'B', 'A', 'B', 'B']\n"
            "    assert candidate([False, False, True, False, True]) == ['B', 'B', 'A', 'B', 'A']\n\n"
            "def test_check():\n"
            "    check(bool2string)\n\n" 
            "test_check()\n"
    },
]



dataset2 = [
    {
        "id": '0',
        "prompt":
            "from typing import List\n\n\n"
            "def add_int(numbers: List[int]) -> List[int]:\n"
            "    \"\"\" For all int type values in the input list, increase each value by 1.\n"
            "    >>> add_int([1, 2, 3])\n    [2, 3, 4]\n"
            "    >>> add_int([1, 2, 3, 4, 5, 2])\n    [2, 3, 4, 5, 6, 3]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate([1, 2, 4, 4, 5, 2]) == [2, 3, 5, 5, 6, 3]\n"
            "    assert candidate([1, 2, 3, 4, 5, 2]) == [2, 3, 4, 5, 6, 3]\n"
            "    assert candidate([1, 2, 5, 4, 5]) == [2, 3, 6, 5, 6]\n"
            "    assert candidate([1, 2, 5, 3, 5]) == [2, 3, 6, 4, 6]\n"
            "    assert candidate([1, 2, 3, 4, 6, 2]) == [2, 3, 4, 5, 7, 3]\n"
            "    assert candidate([1, 2, 3, 4, 9]) == [2, 3, 4, 5, 10]\n"
            "    assert candidate([1, 2, 3, 2, 5]) == [2, 3, 4, 3, 6]\n\n"
            "def test_check():\n"
            "    check(add_int)\n\n" 
            "test_check()\n"

    },
    {
        "id": '1',
        "prompt":
            "from typing import List\n"
            "import math\n\n\n"
            "def add_float(numbers: List[float]) -> List[float]:\n"
            "    \"\"\" For all float type values in the input list, increase each value by 0.1.\n"
            "    >>> add_float([1.1, 2.21, 3.5])\n    [1.2, 2.31, 3.6]\n"
            "    >>> add_float([1.1, 2.4, 3.25, 4.43, 5.1, 2.0])\n    [1.2, 2.5, 3.35, 4.53, 5.2, 2.1]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    tolerance = 1e-6\n"
            "    assert all(math.isclose(result, expected, rel_tol=tolerance) for result, expected in zip(candidate([1.1, 2.1, 4.1, 4.1, 5.1, 2.1]), [1.2, 2.2, 4.2, 4.2, 5.2, 2.2]))\n"
            "    assert all(math.isclose(result, expected, rel_tol=tolerance) for result, expected in zip(candidate([1.1, 2.1, 3.1, 4.1, 5.1, 2.1]), [1.2, 2.2, 3.2, 4.2, 5.2, 2.2]))\n"
            "    assert all(math.isclose(result, expected, rel_tol=tolerance) for result, expected in zip(candidate([1.1, 2.1, 5.1, 4.1, 5.1]), [1.2, 2.2, 5.2, 4.2, 5.2]))\n"
            "    assert all(math.isclose(result, expected, rel_tol=tolerance) for result, expected in zip(candidate([1.1, 2.1, 5.1, 3.1, 5.1]), [1.2, 2.2, 5.2, 3.2, 5.2]))\n"
            "    assert all(math.isclose(result, expected, rel_tol=tolerance) for result, expected in zip(candidate([1.1, 2.1, 3.1, 4.1, 6.1, 2.1]), [1.2, 2.2, 3.2, 4.2, 6.2, 2.2]))\n"
            "    assert all(math.isclose(result, expected, rel_tol=tolerance) for result, expected in zip(candidate([1.1, 2.1, 3.1, 4.1, 9.1]), [1.2, 2.2, 3.2, 4.2, 9.2]))\n"
            "    assert all(math.isclose(result, expected, rel_tol=tolerance) for result, expected in zip(candidate([1.1, 2.1, 3.1, 2.1, 5.1]), [1.2, 2.2, 3.2, 2.2, 5.2]))\n\n"
            "def test_check():\n"
            "    check(add_float)\n\n"  
            "test_check()\n"    

    },
    {
        "id": '2',
        "prompt":
            "from typing import List\n\n\n"
            "def map_string(numbers: str) -> str:\n"
            "    \"\"\" Map each character in the input string to the character whose ASCII number is the current ASCII value plus 1.\n"
            "    >>> map_string('hello')\n"
            "    'ifmmp'\n"
            "    >>> map_string('machine learning')\n"
            "    'nbdijof!mfbsojoh'\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate('play') == 'qmbz'\n"
            "    assert candidate('school') == 'tdippm'\n"
            "    assert candidate('the sky blue') == 'uif!tlz!cmvf'\n"
            "    assert candidate('there') == 'uifsf'\n"
            "    assert candidate('Hi') == 'Ij'\n"
            "    assert candidate('Mary') == 'Nbsz'\n"
            "    assert candidate('One') == 'Pof'\n\n"
            "def test_check():\n"
            "    check(map_string)\n\n" 
            "test_check()\n"             

    },
    {
        "id": '3',
        "prompt":
            "from typing import List\n\n\n"
            "def map_bool(numbers: bool) -> bool:\n"
            "    \"\"\" Invert True to False and False to True.\n"
            "    >>> map_bool(True)\n"
            "    False\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "tests":
            "def check(candidate):\n"
            "    assert candidate(True) == False\n"
            "    assert candidate(False) == True\n\n"
            "def test_check():\n"
            "    check(map_bool)\n\n" 
            "test_check()\n" 

    },
]


def get_lambda1() -> Dict[str, Dict]:

    for task in dataset1:
        task['task_id'] = task['id']

    return {task["task_id"]: task for task in dataset1}


def get_lambda2() -> Dict[str, Dict]:

    for task in dataset2:
        task['task_id'] = task['id']

    return {task["task_id"]: task for task in dataset2}
