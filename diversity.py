import nltk
import numpy as np
from datasets import load_dataset
import torch
from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
from nltk.translate.bleu_score import sentence_bleu
from sentence_transformers import SentenceTransformer
import torch.nn.functional as F
from sklearn.metrics.pairwise import cosine_similarity
import os
from utils import get_dataset
from copy import deepcopy
import matplotlib.pyplot as plt
from src.methods.abstract_method import AbstractMethods
from src.methods.demo_mutate import DemoMutation
from src.methods.description_mute import CharacterMutation, TokenMutation
from src.methods.semantic_mute import OutputTypeMutation, OutputValueMutation

from src.methods.func_name import FuncNameMutation
from src.methods.sytanx_mute import CommentMutation, InsertLineMutation

device = torch.device(1)
model_id = "gpt2-large"
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)


prompt_dir = "./final_res/prompt"

if not os.path.isdir(prompt_dir):
    os.mkdir(prompt_dir)


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
            methods = OutputValueMutation(task['prompt'], task['tests'], task['entry_point'])
            is_success, new_prompt, new_test, src_type, tgt_type, op = methods.mutate(task['language'])
        elif method == 'output_mutation':
            methods = OutputTypeMutation(task['prompt'], task['tests'], task['entry_point'])
            is_success, new_prompt, new_test, src_type, tgt_type, op = methods.mutate(task['language'])
        else:
            raise NotImplementedError
        all_prompts[task_id] = new_prompt
    return all_prompts


def compute_bleu(base_sentences, new_sentences):

    new_sentences = [nltk.word_tokenize(text.lower()) for text in new_sentences]
    base_sentences = [nltk.word_tokenize(text.lower()) for text in base_sentences]

    if len(new_sentences) != len(base_sentences):
        return np.nan

    n = len(new_sentences)
    total_bleu_score = 0.0

    for i in tqdm(range(n)):
        ref_sentences = [base_sentences[i]]
        hypothesis = new_sentences[i]
        bleu_score = sentence_bleu(ref_sentences, hypothesis)
        total_bleu_score += bleu_score

    self_bleu_score = total_bleu_score / (n + 1e-12)
    return self_bleu_score


def compute_perplexity(generated_texts):

    encodings = tokenizer("\n\n".join(generated_texts), return_tensors="pt")

    max_length = model.config.n_positions
    stride = 1024
    seq_len = encodings.input_ids.size(1)

    nlls = []
    prev_end_loc = 0
    for begin_loc in tqdm(range(0, seq_len, stride)):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc  # may be different from stride on last loop
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)

            neg_log_likelihood = outputs.loss

        nlls.append(neg_log_likelihood)

        prev_end_loc = end_loc
        if end_loc == seq_len:
            break
    if nlls == []:
        return np.nan
    ppl = torch.exp(torch.stack(nlls).mean())
    return float(ppl)


def compute_embeding_sim(base_sentences, new_sentences):
    model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')
    model = model.to(device).eval()
    vec1 = model.encode(base_sentences)
    vec2 = model.encode(new_sentences)
    if len(vec2) == 0:
        return 0.0
    cos_sim = cosine_similarity(vec1, vec2)
    sim = np.diagonal(cos_sim)
    return np.mean(sim)


def read_prompt(file_path):
    with open(file_path, 'r') as f:
        prompt = f.read()
    return prompt


def read_approach_prompt(dataset_name, approach):
    save_dir = f"./workdir/codegen/{dataset_name}/{approach}/codegen-2b_temp_0.7/"
    results = {}
    for dirpath, dirnames, filenames in os.walk(save_dir):
        for filename in filenames:
            if filename == "prompt.txt":
                file_path = os.path.join(dirpath, filename)
                problem_id = int(dirpath.split('_')[-1])
                results[problem_id] = read_prompt(file_path)
    return results


def compute_diffimp(base_sentences, new_sentences):
    res = []
    for s1, s2 in zip(base_sentences, new_sentences):
        if s1 == s2:
            res.append(0)
        else:
            res.append(1)
    return np.array(res)

def check_implementation_difference(base_sentences, new_sentences):
    res = compute_diffimp(base_sentences, new_sentences)
    return res.mean()


def extract_desc(prompts):
    all_comments = []
    for prompt in prompts:
        m = AbstractMethods(prompt, None, None)
        _, comments, _ = m.split_desc_testcases_py()
        all_comments.append(comments)
    return all_comments


def external_diversity():
    approach_list = [
        "base", "add_demo", "del_demo", "rep_demo",
        "char_mutation", "token_mutation",
        "func_name", "insert_line", "comment",
        "output_v_mutation", "output_mutation",
    ]

    final_res = []
    for dataset_name in ['humaneval', 'mbpp']:
        all_res = []
        base_prompts = read_approach_prompt(dataset_name, "base")  # TODO
        for approach in approach_list:
            new_prompts = read_approach_prompt(dataset_name, approach)

            common_id = set(new_prompts.keys()).intersection(set(base_prompts.keys()))
            common_id = list(common_id)
            base_sents = [base_prompts[k] for k in common_id]
            new_sents = [new_prompts[k] for k in common_id]

            base_sents = extract_desc(base_sents)
            new_sents = extract_desc(new_sents)

            bleu = compute_bleu(base_sents, new_sents)
            perplexity = compute_perplexity(new_sents)
            sim = compute_embeding_sim(base_sents, new_sents)
            all_res.append(np.array([bleu, sim, perplexity]).reshape([1, -1]))
        all_res = np.concatenate(all_res)
        final_res.append(all_res)
    final_res = np.concatenate(final_res, axis=1)
    np.savetxt('final_res/external_diversity.csv', final_res, delimiter=',')
    print()


def internal_diversity():
    approach_list = [
        "base", "add_demo", "del_demo", "rep_demo",
        "char_mutation", "token_mutation",
        "func_name", "insert_line", "comment",
        "output_v_mutation", "output_mutation",
    ]
    random_prompt_dir = "random_prompt"

    final_res = []
    for dataset_name in ['humaneval', 'mbpp']:
        all_res = []
        for approach in approach_list:

            task_name = f"{dataset_name}::::{approach}"
            save_path = os.path.join(random_prompt_dir, task_name)
            all_prompt = torch.load(save_path)
            prompt_1, prompt_2 = all_prompt
            common_id = set(prompt_1.keys()).intersection(set(prompt_2.keys()))
            common_id = list(common_id)
            base_sents = [prompt_1[k] for k in common_id]
            new_sents = [prompt_2[k] for k in common_id]

            base_sents = extract_desc(base_sents)
            new_sents = extract_desc(new_sents)

            bleu = compute_bleu(base_sents, new_sents)
            sim = compute_embeding_sim(base_sents, new_sents)
            is_same_solution = check_implementation_difference(base_sents, new_sents)
            all_res.append(np.array([bleu, sim, is_same_solution]).reshape([1, -1]))
        all_res = np.concatenate(all_res)
        final_res.append(all_res)
    final_res = np.concatenate(final_res, axis=1)
    np.savetxt('final_res/internal_diversity.csv', final_res, delimiter=',')
    print()


def random_prompt_generation():
    random_prompt_dir = "random_prompt"
    if not os.path.isdir(random_prompt_dir):
        os.mkdir(random_prompt_dir)

    approach_list = [
        "base", "add_demo", "del_demo", "rep_demo",
        "char_mutation", "token_mutation",
        "func_name", "insert_line", "comment",
        "output_v_mutation", "output_mutation",
    ]

    for dataset_name in ['humaneval', 'mbpp']:
        for approach in approach_list:
            all_prompt = []
            task_name = f"{dataset_name}::::{approach}"
            save_path = os.path.join(random_prompt_dir, task_name)
            for _ in tqdm(range(2)):
                prompt = prompt_generate(dataset_name, approach)
                all_prompt.append(prompt)
            torch.save(all_prompt, save_path)


def prompt2text():
    approach_list = [
        "base", "add_demo", "del_demo", "rep_demo",
        "char_mutation", "token_mutation",
        "func_name", "insert_line", "comment",
        "output_v_mutation", "output_mutation",
    ]
    random_prompt_dir = "random_prompt"
    prompt_text_dir = "prompt_text"
    if not os.path.isdir(prompt_text_dir):
        os.mkdir(prompt_text_dir)

    for dataset_name in ['humaneval', 'mbpp']:
        for approach in approach_list:
            task_name = f"{dataset_name}::::{approach}"
            save_path = os.path.join(random_prompt_dir, task_name)
            all_prompt = torch.load(save_path)
            prompt_1, prompt_2 = all_prompt
            save_path = os.path.join(prompt_text_dir, task_name + '.txt')
            with open(save_path, 'w') as f:
                for i, k in enumerate(sorted(prompt_1.keys())):
                    if i == 100:
                        break
                    prompt_str = prompt_1[k]
                    f.write(prompt_str)
                    f.write("    pass\n\n\n")


def diffimp_curve():
    approach_list = [
        "output_v_mutation", "output_mutation",
    ]
    final_res = []
    for dataset_name in ['humaneval', 'mbpp']:
        for approach in approach_list:
            base_prompts = prompt_generate(dataset_name, approach)
            is_cover = np.zeros([len(base_prompts)])
            base_id = base_prompts.keys()
            curve = []
            prompt_1 = [base_prompts[p_id] for p_id in base_id]
            for k in tqdm(range(100)):
                prompts = prompt_generate(dataset_name, approach)
                for p_id in base_id:
                    if p_id not in prompts:
                        prompts[p_id] = ""
                prompts = [prompts[p_id] for p_id in base_id]
                cov = compute_diffimp(prompt_1, prompts)
                cov = 1 - cov
                is_cover = is_cover + cov
                is_cover = np.array(is_cover != 0, dtype=np.int32)
                curve.append(deepcopy(is_cover).reshape([1, -1]))
                # print(np.mean(cov))
            curve = np.concatenate(curve).mean(axis=1)
            final_res.append(curve.reshape([-1, 1]))

            # plt.plot(curve)
            # plt.show()
    final_res = np.concatenate(final_res, axis=1)
    final_res = 1 - final_res
    np.savetxt('final_res/curve.csv', final_res, delimiter=',')




if __name__ == '__main__':
    # external_diversity()
    # random_prompt_generation()
    #
    # internal_diversity()
    prompt2text()
    # diffimp_curve()