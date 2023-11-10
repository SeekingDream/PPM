from utils import get_dataset
from src.methods.abstract_method import AbstractMethods
from src.methods.demo_mutate import DemoMutation
from src.methods.description_mute import CharacterMutation, TokenMutation
from src.methods.semantic_mute import OutputTypeMutation, OutputValueMutation

from src.methods.func_name import FuncNameMutation
from src.methods.sytanx_mute import CommentMutation, InsertLineMutation

def prompt_generate(dataset, method):
    all_prompts = {}
    for task_id, task in get_dataset(dataset).items():
        if method == "base":
            new_prompt = task["prompt"]
        elif method == "add_demo":
            methods = DemoMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.add_demo(task['language'])
        elif method == "del_demo":
            methods = DemoMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.del_demo(task['language'])
        elif method == "rep_demo":
            methods = DemoMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.rep_demo(task['language'])
        elif method == "char_mutation":
            methods = CharacterMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.mutate(task['language'])
        elif method == "token_mutation":
            methods = TokenMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.mutate(task['language'])
        elif method == "func_name":
            methods = FuncNameMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt, entry_point, _ = methods.mutate(task['language'])
        elif method == 'insert_line':
            methods = InsertLineMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.mutate(task['language'])
        elif method == 'comment':
            methods = CommentMutation(task['prompt'], task['tests'], task['entry_point'])
            new_prompt = methods.mutate(task['language'])
        elif method == 'output_v_mutation':
            if task['entry_point'] == "fix_spaces":
                print()
            methods = OutputValueMutation(task['prompt'], task['tests'], task['entry_point'])
            is_success, new_prompt, new_test, src_type, tgt_type, op = methods.mutate(task['language'])
            print(new_prompt)

        elif method == 'output_mutation':
            methods = OutputTypeMutation(task['prompt'], task['tests'], task['entry_point'])
            is_success, new_prompt, new_test, src_type, tgt_type, op = methods.mutate(task['language'])
            print(new_prompt)

        else:
            raise NotImplementedError
        all_prompts[task_id] = new_prompt
    return all_prompts


if __name__ == '__main__':
    prompt_generate('humaneval', "output_v_mutation")