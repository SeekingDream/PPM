dataset1 = [
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def int2float(numbers: List[int]) -> List[float]:\n"
            "    \"\"\" Change all int type values of input list to float type, and add by 0.1.\n"
            "    >>> int2float([1, 2, 3])\n    [1.1, 2.1, 3.1]\n"
            "    >>> int2float([1, 2, 3, 4, 5, 2])\n    [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test":
            "def check(candidate):\n"
            "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
            "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
            "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
            "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
            "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
            "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
            "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 1,
        "prompt":
            "from typing import List\n\n\n"
            "def int2string(numbers: List[int]) -> List[string]:\n"
            "    \"\"\" Change all int type values of input list to string type, each string would be the int value add one.\n"
            "    >>> int2string([1, 2, 3])\n    ['2', '3', '4']\n"
            "    >>> int2string([1, 2, 3, 4, 5, 2])\n    ['2', '3', '4', '5', '6', '3']\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test":
            "def check(candidate):\n"
            "    assert candidate([1, 2, 4, 4, 5, 2]) == ['2', '3', '5', '5', '6', '3']\n"
            "    assert candidate([1, 2, 3, 4, 5, 2]) == ['2', '3', '4', '5', '6', '3']\n"
            "    assert candidate([1, 2, 5, 4, 5]) == ['2', '3', '6', '5', '6']\n"
            "    assert candidate([1, 2, 5, 3, 5]) == ['2', '3', '6', '4', '6']\n"
            "    assert candidate([1, 2, 3, 4, 6, 2]) == ['2', '3', '4', '5', '7', '3']\n"
            "    assert candidate([1, 2, 3, 4, 9]) == ['2', '3', '4', '5', '10']\n"
            "    assert candidate([1, 2, 3, 2, 5]) == ['2', '3', '4', '3', '6']\n\n"

    },
    {
        "id": 2,
        "prompt":
            "from typing import List\n\n\n"
            "def int2bool(numbers: List[int]) -> List[float]:\n"
            "    \"\"\" Change all int type values of the input list to bool type, change all odd values to True, and all even values to False.\n"
            "    >>> int2bool([1, 2, 3])\n    [True, False, True]\n"
            "    >>> int2bool([1, 2, 3, 4, 5, 2])\n    [True, False, True, False, True, False]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test":
            "def check(candidate):\n"
            "    assert candidate([1, 2, 4, 4, 5, 2]) == [True, False, False, False, True, False]\n"
            "    assert candidate([1, 2, 3, 4, 5, 2]) == [True, False, True, False, True, False]\n"
            "    assert candidate([1, 2, 5, 4, 5]) == [True, False, True, False, True]\n"
            "    assert candidate([1, 2, 5, 3, 5]) == [True, False, True, True, True]\n"
            "    assert candidate([1, 2, 3, 4, 6, 2]) == [True, False, True, False, False, False]\n"
            "    assert candidate([1, 2, 3, 4, 9]) == [True, False, True, False, True]\n"
            "    assert candidate([1, 2, 3, 2, 5]) == [True, False, True, False, True]\n\n"

    },

    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def float2int(numbers: List[float]) -> List[int]:\n"
            "    \"\"\" Change all float type values of the input list to int type, keep the integer part of the float plus 1.\n"
            "    >>> float2int([1.1, 2.1, 3.1])\n"
            "    [2, 3, 4]\n"
            "    >>> int2float([1.1, 2.1, 3.1, 4.1, 5.1, 2.1])\n"
            "    [2, 3, 4, 5, 6, 3]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
            # "def check(candidate):\n"
            # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
            # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
            # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
            # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
            # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
            # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
            # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def float2string(numbers: List[float]) -> List[string]:\n"
            "    \"\"\" Change all float type values of the input list to string type, return the string value of integer part plus 1.\n"
            "    >>> float2string([1.1, 2.1, 3.1])\n"
            "    ['2', '3', '4']\n"
            "    >>> float2string([1.1, 2.1, 3.1, 4.1, 5.1, 2.1])\n"
            "    ['2', '3', '4', '5', '6', '3']\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
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
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },

    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def string2int(numbers: List[string]) -> List[int]:\n"
            "    \"\"\" Change all string type values of the input list to int type, each int value would be the length of the string plus 1.\n"
            "    >>> string2int(['hello', 'my', 'name'])\n"
            "    [6, 3, 5]\n"
            "    >>> string2int(['hello', 'my', 'name', 'machine', 'learning])\n"
            "    [6, 3, 5, 8, 9]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def string2float(numbers: List[string]) -> List[float]:\n"
            "    \"\"\" Change all string type values of the input list to int type, each int value would be the length of the string plus 1.1.\n"
            "    >>> string2float(['hello', 'my', 'name'])\n"
            "    [6.1, 3.1, 5.1]\n"
            "    >>> string2float(['hello', 'my', 'name', 'machine', 'learning])\n"
            "    [6.1, 3.1, 5.1, 8.1, 9.1]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def string2bool(numbers: List[string]) -> List[bool]:\n"
            "    \"\"\" Change all string type values of the input list to bool type, change all odd-length strings to True, and all even-length strings to False.\n"
            "    >>> string2bool(['hello', 'my', 'name'])\n"
            "    [True, False, False]\n"
            "    >>> string2bool(['hello', 'my', 'name', 'machine', 'learning])\n"
            "    [True, False, False, True, False]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },

    {
        "id": 0,
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
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
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
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def bool2string(numbers: List[bool]) -> List[string]:\n"
            "    \"\"\" Change all bool type values of input list to string type, and change True to 'A', and False to 'B'.\n"
            "    >>> bool2string([True, False, True])\n"
            "    ['A', 'B', 'A']\n"
            "    >>> bool2string([True, False, True, False, False])\n"
            "    ['A', 'B', 'A', 'B', 'B']\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
]



dataset2 = [
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def add_int(numbers: List[int]) -> List[int]:\n"
            "    \"\"\" For all int type values in the input list, increase each value by 1.\n"
            "    >>> add_int([1, 2, 3])\n    [2, 3, 4]\n"
            "    >>> add_int([1, 2, 3, 4, 5, 2])\n    [2, 3, 4, 5, 6, 3]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
            # "def check(candidate):\n"
            # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
            # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
            # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
            # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
            # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
            # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
            # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def add_float(numbers: List[float]) -> List[float]:\n"
            "    \"\"\" For all float type values in the input list, increase each value by 0.1.\n"
            "    >>> add_float([1.1, 2.21, 3.5])\n    [1.2, 2.31, 3.6]\n"
            "    >>> add_int([1.1, 2.4, 3.25, 4.43, 5.1, 2.0])\n    [1.2, 2.5, 3.35, 4.53, 5.2, 2.1]\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
            # "def check(candidate):\n"
            # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
            # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
            # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
            # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
            # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
            # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
            # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def map_string(numbers: str) -> str:\n"
            "    \"\"\" Map each character in the input string to the character whose ASCII number is the current ASCII value plus 1.\n"
            "    >>> map_string('hello')\n"
            "    'ifmmp'\n"
            "    >>> map_string('machine learning')\n"
            "    nbdijof!mfbsojoh\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
            # "def check(candidate):\n"
            # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
            # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
            # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
            # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
            # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
            # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
            # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
    {
        "id": 0,
        "prompt":
            "from typing import List\n\n\n"
            "def map_bool(numbers: bool) -> bool:\n"
            "    \"\"\" Invert True to False and False to True.\n"
            "    >>> map_bool(True)\n"
            "    False\n"
            "    \"\"\"\n",
        "canonical_solution": "pass",
        "test": ""
        # "def check(candidate):\n"
        # "    assert candidate([1, 2, 4, 4, 5, 2]) == [1.1, 2.1, 4.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 5, 2]) == [1.1, 2.1, 3.1, 4.1, 5.1, 2.1]\n"
        # "    assert candidate([1, 2, 5, 4, 5]) == [1.1, 2.1, 5.1, 4.1, 5.1]\n"
        # "    assert candidate([1, 2, 5, 3, 5]) == [1.1, 2.1, 5.1, 3.1, 5.1]\n"
        # "    assert candidate([1, 2, 3, 4, 6, 2]) == [1.1, 2.1, 3.1, 4.1, 6.1, 2.1]\n"
        # "    assert candidate([1, 2, 3, 4, 9]) == [1.1, 2.1, 3.1, 4.1, 9.1]\n"
        # "    assert candidate([1, 2, 3, 2, 5]) == [1.1, 2.1, 3.1, 2.1, 5.1]\n\n"

    },
]
