import argparse
from utils import get_dataset
from src.methods.demo_mutate import DemoMutation
from src.methods.description_mute import CharacterMutation, TokenMutation
from src.methods.semantic_mute import OutputTypeMutation, OutputValueMutation

from src.methods.func_name import FuncNameMutation
from src.methods.sytanx_mute import CommentMutation, InsertLineMutation
from codeGen.model import make_model


def prompt_generate(args):
    # 该函数的作用是生成代码。它接受三个参数：args（命令行参数）、workdir（工作目录的路径）和model（模型对象）。

    input_type_dict, output_type_dict = {}, {}
    total_fail = 0
    for task_id, task in get_dataset(args.dataset).items():
        # print(task["prompt"])
        if args.construct_prompt == "base":
            prompt = task["prompt"]
        elif args.construct_prompt == "add_demo":
            methods = DemoMutation(task['prompt'], task['tests'], task['entry_point'])
            prompt = methods.add_demo(task['language'])
        elif args.construct_prompt == "del_demo":
            methods = DemoMutation(task['prompt'], task['tests'], task['entry_point'])
            prompt = methods.del_demo(task['language'])
        elif args.construct_prompt == "rep_demo":
            methods = DemoMutation(task['prompt'], task['tests'], task['entry_point'])
            prompt = methods.rep_demo(task['language'])
        elif args.construct_prompt == "char_mutation":
            methods = CharacterMutation(task['prompt'], task['tests'], task['entry_point'])
            prompt = methods.mutate(task['language'])
        elif args.construct_prompt == "token_mutation":
            methods = TokenMutation(task['prompt'], task['tests'], task['entry_point'])
            prompt = methods.mutate(task['language'])

        elif args.construct_prompt == "func_name":
            methods = FuncNameMutation(task['prompt'], task['tests'], task['entry_point'])
            prompt, entry_point,new_test = methods.mutate(task['language'])
        elif args.construct_prompt == 'insert_line':
            methods = InsertLineMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.mutate(task['language'])
        elif args.construct_prompt == 'comment':
            methods = CommentMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.mutate(task['language'])

        elif args.construct_prompt == 'output_v_mutation':
            methods = OutputValueMutation(task['prompt'], task['tests'], task['entry_point'])
            is_success, new_prompt, new_test, src_type, tgt_type, op = methods.mutate(task['language'])
            if is_success == False:
                total_fail += 1

        elif args.construct_prompt == 'output_mutation':
            methods = OutputTypeMutation(task['prompt'], task['tests'], task['entry_point'])
            is_success, new_prompt, new_test, src_type, tgt_type, op = methods.mutate(task['language'])
            if is_success == False:
                total_fail += 1
        else:
            raise NotImplementedError
        print(new_prompt)
        
        #for k in input_type_dict:
        #    print(k, ":", input_type_dict[k])
        #print('-----------------------------------')
        #for k in output_type_dict:
        #    print(k, ":", output_type_dict[k])
        #print('-----------------------------------')
    #print("total_fail:", total_fail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--temperature", default=0.7, type=float)
    parser.add_argument("--construct_prompt", default="comment", type=str)
    parser.add_argument("--dataset", default="humaneval", type=str) #humaneval
    parser.add_argument("--root", default="./workdir/codegen", type=str)
    parser.add_argument("--n_samples", default=200, type=int)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--greedy", action="store_true")
    args = parser.parse_args()

    prompt_generate(args)



if __name__ == '__main__':
    main()
