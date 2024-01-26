<p align="center">
 <a href="https://github.com/anonymousGithub2022/main/LICENSE"><img src="https://img.shields.io/github/license/anonymousGithub2022/DyCL"></a>
 <a href="https://github.com/anonymousGithub2022/main/LICENSE"><img src="https://img.shields.io/pypi/pyversions/tvm"></a>
 <a href="https://github.com/anonymousGithub2022/main/LICENSE"><img src="https://img.shields.io/github/languages/code-size/anonymousGithub2022/DyCL"></a>
</p>


# PPM
This code repository includes the main implementation of Programming Problem Merging, which can generate new programming problems to benchmark the programming capability of code generation models.


# Design Overview
<div  align="center">    
 <img src="https://github.com/Cap-Ning/PPM/blob/master/fig/PPM-overview.jpg" width="680" height="230" alt="Design Overview"/><br/>
</div>   

The figure above illustrates the design overview of PPM, encompassing three primary steps for generating a new programming problem. PPM's input is an existing programming problem, consisting of a natural language prompt, a corresponding implementation, and some test inputs. During the initial step, PPM analyzes the return value types of the given problem by executing the implementation on the provided test inputs. Subsequently, PPM selects a lambda programming task based on these return value types. Finally, PPM concatenates the existing problem with the lambda programming task to craft a new problem.

During the benchmarking stage, PPM feeds the newly created prompt to the code model and retrieves the generated program code. The generated code is then executed on the test inputs, and the resulting outputs are compared against the outputs from the new implementation.


# File Structure
+ src/methods               This directory includes the implementation of different methods to generate programming problems.
     + utils.py             This file implemenents some basic common functions.
     + abstract_methods.py  Implements the abstract class for each method, and the abstract class includes some common functions.
     + demo_mutate.py       This file implements the demo related mutation methods (Add Demo, Delete Demo, and Replace Demo)
     + description_mute.py  This file implements the natual language related mutation methods (Token Mutation and Character Mutation)
     + func_name.py         This file implements the function name mutation.
     + sytanx_mute.py       This file includes some sytanx level mutation (Insert Empty Line)
+ codeGen/model.py
     + semantic_mute.py     This file includes the implementation of our proposed programming problem merging methods.
+ ML/model.py               This file implements the infrastructure of loading large code model for inference.
+ evaluation                This directory inmplements the  infrastructure of executing the generated code and collect the execution outputs.
+ final_res                 This directory stores the results of our experiments.
+ generate.py               This file is used to generate program code from a code model.
+ generate_prompt.py        This file is used to generate prompt for each methods.
+ lambda_problem.py         This file is used to test the accuracy of oiur propsoed lambda problems.
+ pass_k.py                 This file is used to compute the pass@k metrics.
+ utils.py                  This file implements some basic functions.
+ diversity.py              This file is used to evaluate the diversity of the programming problems from each methods.
    
 
# How to Run
 ``python generate.py --model incoder-1b --construct_prompt token_mutation --dataset humaneval --n_samples 100``

+ `model`: the large code model for inference.
+ `construct_prompt`: the method to construct prompt. 
+ `dataset`: the seed dataset.
+ `n_samples`: the number of generated candidate programs.
 
## Supported Large Code Models
    {"gpt-4","chatgpt","codegen-2b","codegen-6b","codegen-6b-hf","codegen-16b","codegen2-16b","polycoder","vicuna-7b","vicuna-13b","santacoder","incoder-1b","incoder-6b","stablelm-7b","gptneo-2b","gpt-j","starcoder"}

## Supported Methods.
 {"base", "add_demo", "del_demo", "rep_demo", "char_mutation", "token_mutation", "func_name", "insert_line", "comment", "output_v_mutation", "output_mutation"}


 # PPM Problem Examples

## The Seed Problem and Generated Code of CodeGen

```
def find_Max_Num(arr: List[int]):
    """
    Write a python function to find the largest number that can be formed with the given list of digits.
    """
    arr.sort(reverse=True)
    return int("".join(map(str, arr)))
```

## PPM-V

```
def find_Max_Num(arr: List[int]):
    """
    Write a python function to find the largest number that can be formed with the given list of digits. Change all int type values of the return values to float type, and add 0.86.
    """
    # list of int type numbers
    numbers = arr
    max_num = -float("inf")
    for i in range(len(numbers)):
        if max_num <= numbers[i]:
            max_num = numbers[i]
    # add 0.86
    return float(max_num) + 0.86
```

## PPM-T

```
def find_Max_Num(arr: List[int]) -> int:
    """
    Write a python function to find the largest number that can be formed with the given list of digits. For all int type values in the return results, increase each value by 3.
    """
    if len(arr) == 0:
        return -1
    for i in range(len(arr)):
        arr[i] += 3
    return max(arr)
```


The above three examples illustrate the prompt alongside the corresponding generated code from CodeGen-2B. The first example pertains to the seed programming problem, while the second and third examples relate to PPM. The results highlight that the model successfully generates accurate code for the seed problem. However, in the case of PPM, the model encounters difficulties. Intriguingly, with PPM-V, the model demonstrates an apt understanding of the associated lambda problem, as evidenced by the generated comments. Yet, when faced with the amalgamation of these two problems, the model becomes confounded by the original problem, resulting in incorrect final outputs. Another noteworthy observation is found in PPM-T, where the model comprehends the "increase each value by 3" instructions. Nevertheless, the model struggles to provide correct solutions for the seed component within the merged problem. These findings substantiate our hypothesis that the merging of programming problems can elevate complexity and pose challenges for Language Code Generation Models (LCGMs).

More examples of each methods prompt and corresonding generated code snippet could be found in [here](https://github.com/anonymousGithub2022/PPM/blob/main/examples.txt)
