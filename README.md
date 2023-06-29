# 1.codeGen

    python generate.py --model "codegen-2b" --bs 1 --temperature 0.8 --constract_prompt "base"
##More
+ --constract_prompt {"base", "add_demo", "del_demo","rep_demo"}
+ --model {"gpt-4","chatgpt","codegen-2b","codegen-6b","codegen-6b-hf","codegen-16b","codegen2-16b","polycoder","vicuna-7b","vicuna-13b","santacoder","incoder-1b","incoder-6b","stablelm-7b","gptneo-2b","gpt-j","starcoder"}
+ --n_samples  #Number of generated samples
# 2.codeEval

    cd evaluation/src
    python main.py --dir "../../workdir/codegen/humaneval/add_demo" --recursive --output-dir "./output/humaneval/add_demo"
# 3. Eval_pass@k
    python pass_k.py --dir "./evaluation/src/output/humaneval/add_demo"


# File Structure

    generate.py			            Generate code using a specified large language model
    model.py				    load LLMS
    utils.py                                    load HumanEval dataset   return {task["task_id"]: task for task in human_eval}
  
