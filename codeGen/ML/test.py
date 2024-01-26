# from src.methods.demo_mutate import constract_prompt
# from utils import get_human_eval,get_human_eval_cleaned_doc,get_humaneval_cs,get_humaneval_cpp,get_humaneval_java
# human_eval_cleaned_doc = get_human_eval_cleaned_doc()
# human_eval = get_human_eval()
# data_test = human_eval['HumanEval/4']
# methods = constract_prompt(data_test['prompt'],data_test['test'],data_test['entry_point'])
#
# del_prompt = methods.del_demo()
# add_prompt = methods.add_demo()
# rep_prompt = methods.rep_demo()

# import json
# # 读取JSON文件
# with open('./workdir/Dataset/humaneval-py-transform.json', 'r') as f:
#     data_list = json.load(f)
#
# for data in data_list:
#     name = data['name']
#     pos = name.find("_", name.find("_") + 1)
#     data['task_id'] = name[:pos]
#     data['entry_point'] = name[pos+1:]

# pos = name.find("_", name.find("_") + 1)
# if pos != -1:
#     string = name[:pos]
#
# fun = name[pos+1:]

# for task_id, task in get_human_eval_cleaned_doc().items():
#     methods = constract_prompt(task['prompt'],task['tests'],task['entry_point'])
#     print(task['prompt'])
#     print(methods.del_demo())

# for task_id, task in get_human_eval_cleaned_doc().items():
#     methods = constract_prompt(task['prompt'], task['tests'], task['entry_point'])
#     print(task['prompt'])
#     print(methods.rep_demo(task['language']))


import os
from abc import ABC, abstractmethod
from typing import List
from warnings import warn
# Communism
os.environ["HF_HOME"] = os.environ.get("HF_HOME", "/home/simin/Project/CodeModel/workdir/huggingface")
import torch
from fastchat.serve.inference import load_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
)
from evalplus.gen.util.api_request import create_chatgpt_config, request_chatgpt_engine

HUMANEVAL_EOS = ["\nclass", "\ndef", "\n#", "\n@", "\nprint", "\nif"]
NON_CODE_EOS = ["<|endoftext|>", "\n```", "\n</s>", "<|endofmask|>"]
EOS = HUMANEVAL_EOS + NON_CODE_EOS
class DecoderBase(ABC):
    def __init__(
        self,
        name: str,
        batch_size: int = 1,
        temperature: float = 0.8,
        max_new_tokens: int = 512,
    ) -> None:
        print("Initializing a decoder model: {} ...".format(name))
        self.name = name
        self.batch_size = batch_size
        self.temperature = temperature
        self.eos = EOS
        self.skip_special_tokens = False
        self.max_new_tokens = max_new_tokens

    @abstractmethod
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        pass

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
class HFTorchDecoder(DecoderBase):
    def __init__(self, name: str, batch_size: int = 1, temperature: float = 0.8):
        super().__init__(name=name, batch_size=batch_size, temperature=temperature)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        kwargs = {
            "trust_remote_code": name
            in {
                "bigcode/santacoder",
                "Salesforce/codegen2-1B",
                "Salesforce/codegen2-3_7B",
                "Salesforce/codegen2-7B",
                "Salesforce/codegen2-16B",
            }
        }
        if "codegen-" in name:  # use fp16 for codegen models
            kwargs["torch_dtype"] = torch.float16
        if "codegen2-" in name:  # avoid warning of trust remote code
            kwargs["revision"] = "main"
            kwargs["torch_dtype"] = torch.float16
            if "16b" in name.lower():
                kwargs["device_map"] = "auto"
                # Not working... # int8 acceleration
                # kwargs["load_in_8bit"] = True
        if "starcoder" in name:
            kwargs["torch_dtype"] = torch.bfloat16

        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.model = AutoModelForCausalLM.from_pretrained(name, **kwargs)
        if name in {"StabilityAI/stablelm-base-alpha-7b"}:
            print("Switching to float16 ...")
            self.model = self.model.half()
            self.skip_special_tokens = True
        self.model = self.model.to(self.device)

    # Assumption is that all inputs should probably fit under maximum context. but can add a checking function
    # just in case. TODO: think about
    @torch.inference_mode()
    def codegen(
        self, prompt: str, do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        input_tokens = self.tokenizer.encode(prompt, return_tensors="pt").to(
            self.device
        )
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            output_scores=True,
            return_dict_in_generate=True,
            num_return_sequences=min(self.batch_size, num_samples),
            pad_token_id=self.tokenizer.eos_token_id,
        )  # remove warning
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    # could be multiple eos in outputs, better pick minimum one
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs

class Codegen2Decoder(HFTorchDecoder):
    def __init__(
        self, name: str, batch_size: int = 1, temperature: float = 0.8
    ) -> None:
        super().__init__(name, batch_size, temperature)
        self.infill_ph = "<mask_1>"
        # taken from: https://huggingface.co/Salesforce/codegen2-16B
        self.extra_end = "<|endoftext|><sep><mask_1>"
        self.extra_eos = ["<eom>"]
        self.eos = self.eos + self.extra_eos

    @torch.inference_mode()
    def codegen(
        self, prompt: "def hello_world():", do_sample: bool = True, num_samples: int = 200
    ) -> List[str]:
        input = prompt + self.infill_ph + self.extra_end
        input_tokens = self.tokenizer.encode(input, return_tensors="pt").to(self.device)
        scores = StoppingCriteriaList(
            [
                EndOfFunctionCriteria(
                    start_length=len(input_tokens[0]),
                    eos=self.eos,
                    tokenizer=self.tokenizer,
                )
            ]
        )
        raw_outputs = self.model.generate(
            input_tokens,
            max_new_tokens=self.max_new_tokens,
            stopping_criteria=scores,
            do_sample=do_sample,
            top_p=0.95,
            top_k=None,
            temperature=self.temperature,
            output_scores=True,
            return_dict_in_generate=True,
            num_return_sequences=min(self.batch_size, num_samples),
            pad_token_id=self.tokenizer.eos_token_id,
        )
        gen_seqs = raw_outputs.sequences[:, len(input_tokens[0]) :]
        gen_strs = self.tokenizer.batch_decode(
            gen_seqs, skip_special_tokens=self.skip_special_tokens
        )
        outputs = []
        # removes eos tokens.
        for output in gen_strs:
            min_index = 10000
            for eos in self.eos:
                if eos in output:
                    min_index = min(min_index, output.index(eos))
            outputs.append(output[:min_index])
        return outputs


def make_model(name: str, batch_size: int = 1, temperature: float = 0.8):
    return Codegen2Decoder(
        batch_size=batch_size,
        name="bigcode/starcoder",
        temperature=temperature,
    )

make_model("bigcode/starcoder")
