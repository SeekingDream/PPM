# codeModel

    python generate.py --model "codegen-2b" --bs 1 --temperature 0.8


# File Structure

    generate.py			            Generate code using a specified large language model
    model.py				    load LLMS
    utils.py                            load HumanEval dataset   return {task["task_id"]: task for task in human_eval}

## LLMS
    {"gpt-4","chatgpt","codegen-2b","codegen-6b","codegen-6b-hf","codegen-16b","codegen2-16b","polycoder","vicuna-7b","vicuna-13b","santacoder","incoder-1b","incoder-6b","stablelm-7b","gptneo-2b","gpt-j","starcoder"}
