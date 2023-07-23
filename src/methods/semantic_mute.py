import copy
import random
import torch
import string
import nltk
from transformers import BertTokenizer, pipeline
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer
from typing import List
import ast
import astor
import mypy.api
import inspect
from typing import Dict

from .abstract_method import AbstractMethods
from .utils import parse_assertion
from .utils import replace_assertion_output
from .utils import concat_move_non_english
from .utils import replace_asserts_in_function
from .utils import summarize_types
from .utils import modify_output_values


class AbstractSemanticMutation(AbstractMethods):
    basic_types = ['bool', 'float', 'int', 'str']

    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)
        self.assert_statements = self.extract_assert_statements()
        self.ori_test = test
        self.ori_prompt = prompt
        self.input_transfer_op = None
        self.output_transfer_op = None

    def mutate(self, language):
        try:
            func_entry, comments, demo = self.split_desc_testcases(language)
            _, output_types = self.get_input_output_types(language)

            src_type_set = set()
            for output_type in output_types:
                if 'int' in output_type:
                    src_type_set.add('int')
                elif 'bool' in output_type:
                    src_type_set.add('bool')
                elif 'float' in output_type:
                    src_type_set.add('float')
                elif 'str' in output_type:
                    src_type_set.add('str')
                else:
                    pass

            command, src_type, tgt_type, op = self.generate_command(list(src_type_set), language)
            new_comments = concat_move_non_english(comments, command)
            new_demos = self.generate_new_demos(demo, src_type, op, language)
            new_test = self.generate_new_tests(src_type, op, language)

            new_prompt = self.combine_desc_testcases(
                language, func_entry, new_comments, new_demos)

            self.prompt = new_prompt
            self.test = new_test
            is_success = True
            return is_success, self.prompt, self.test, src_type, tgt_type, op
        except:
            is_success = False
            return is_success, self.prompt, self.test, None, None, None

    def generate_new_demos(self, demos, src_type, op, language):
        if language == 'py':
            return self.generate_new_demos_py(demos, src_type, op)
        else:
            raise NotImplementedError

    def generate_new_tests(self, src_type, op, language):
        if language == 'py':
            return self.generate_new_tests_py(src_type, op)
        else:
            raise NotImplementedError

    def generate_command(self, src_type_list, language):
        pass

    def extract_assert_statements(self):
        tree = ast.parse(self.test)
        assert_statements = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                assert_statements.append(astor.to_source(node))
        return assert_statements

    def get_input_output_types(self, language):
        if language == 'py':
            return self.get_input_output_types_py()
        else:
            raise NotImplementedError

    def get_input_output_types_py(self):
        args_list, output_var_list = [], []
        for statement in self.assert_statements:
            arguments, expected_output = parse_assertion(statement)

            args_list.append(arguments)
            output_var_list.append(expected_output)

        args_list = list(zip(*args_list))
        all_input_types = []
        for args in args_list:
            input_types = summarize_types(args)
            all_input_types.append(input_types)
        output_types = summarize_types(output_var_list)
        return all_input_types, output_types

    def generate_new_demos_py(self, demos, src_type, op):
        new_demos = []
        for demo in demos:
            example = demo.split('\n')
            output_values = eval(example[1])

            new_output_values = modify_output_values(output_values, src_type, op)
            output_str = "    " + str(new_output_values)
            example[1] = output_str
            new_demos.append("\n".join(example))
        return new_demos

    def generate_new_tests_py(self, src_type, op):
        new_assert_statements = []
        for statement in self.assert_statements:
            _, expected_output = parse_assertion(statement)
            new_output_values = modify_output_values(expected_output, src_type, op)
            if not isinstance(new_output_values, tuple):
                new_output_values = [new_output_values]
            new_assert = replace_assertion_output(statement, new_output_values)
            new_assert_statements.append(new_assert)
        new_test_code = replace_asserts_in_function(self.test, new_assert_statements)
        return new_test_code


class OutputTypeMutation(AbstractSemanticMutation):

    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)

    def generate_command_py(self, src_type, tgt_type):

        command = f"Change all {src_type} type values of the return values to {tgt_type} type, "

        if src_type == 'bool':
            if tgt_type == 'int':
                offset = random.randint(0, 10)
                command += f"and add {offset}."

                def op(x):
                    return int(x) + offset

            elif tgt_type == 'float':
                offset = round(random.random(), 2)
                command += f"and add {offset}."

                def op(x):
                    return float(x) + offset

            elif tgt_type == 'str':
                offset = random.choice(string.ascii_lowercase)
                next_offset = chr(ord(offset) + 1)
                command += f"and change True to {offset}, and False to {next_offset}."

                def op(x):
                    if x:
                        return offset
                    else:
                        return next_offset

            else:
                raise NotImplementedError
        elif src_type == 'int':
            if tgt_type == 'bool':
                offset = bool(random.randint(0, 1))
                next_offset = not offset
                command += f"change all odd results to {offset}, and all even results to {next_offset}."

                def op(x):
                    if x % 2:
                        return offset
                    else:
                        return next_offset

            elif tgt_type == 'str':
                offset = random.randint(0, 10)
                command += f"return the string value of answer + {offset}."

                def op(x):
                    return str(x + offset)

            elif tgt_type == 'float':
                offset = round(random.random(), 2)
                command += f"and add {offset}."

                def op(x):
                    return x + offset

            else:
                raise NotImplementedError
        elif src_type == 'str':
            if tgt_type == 'bool':
                offset = bool(random.randint(0, 1))
                next_offset = not offset
                command += f"change all odd-length strings to {offset}, and all even-length strings to {next_offset}."

                def op(x):
                    if len(x) % 2:
                        return offset
                    else:
                        return next_offset

            elif tgt_type == 'int':
                offset = random.randint(0, 10)
                command += f"and return the length of the string plus {offset}."

                def op(x):
                    return len(x) + offset

            elif tgt_type == 'float':
                offset = round(random.random(), 2)
                command += f"and return the length of the string plus {offset}."

                def op(x):
                    return len(x) + offset

            else:
                raise NotImplementedError
        elif src_type == 'float':
            if tgt_type == 'bool':
                offset = bool(random.randint(0, 1))
                next_offset = not offset
                command += f"if the answer is larger than 0.0, return {offset}, else return {next_offset}."

                def op(x):
                    return offset if x > 0.0 else next_offset

            elif tgt_type == 'int':
                offset = random.randint(0, 10)
                command += f"keep the integer part of the result plus {offset}."

                def op(x):
                    return int(x) + offset

            elif tgt_type == 'str':
                offset = random.randint(0, 10)
                command += f"return the string value of answer + {offset}."

                def op(x):
                    return str(x + offset)

            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
        return command, op

    def generate_command(self, src_type_list, language):
        if language == 'py':
            src_type = random.choice(src_type_list)
            tgt_types = self.basic_types.copy()
            tgt_types.remove(src_type)
            tgt_type = random.choice(tgt_types)
            command, op = self.generate_command_py(src_type, tgt_type)
        else:
            raise NotImplementedError

        return command, src_type, tgt_type, op


class OutputValueMutation(AbstractSemanticMutation):
    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)

    def generate_command_py(self, src_type):

        if src_type == 'bool':
            def op(x):
                return not x

            command = f"For all {src_type} values in the return results, " \
                      f"invert True to False and False to True."
        elif src_type == 'int':
            def op(x):
                return x + offset

            offset = random.randint(-10, 10)
            command = f"For all {src_type} type values in the return results, " \
                      f"increase each value by {offset}."
        elif src_type == 'str':
            offset = random.randint(1, 3)

            def op(x_str: str):
                new_str = ""
                for i, x in enumerate(x_str):
                    new_str += chr(ord(x) + offset)
                return x_str

            command = f"For all {src_type} values in the return results, " \
                      f"map each character in the {src_type} value to the character " \
                      f"whose ASCII number is the current ASCII value plus {offset}."

        elif src_type == 'float':
            offset = round(random.random() * 2 - 1, 2)

            def op(x):
                return x + offset

            command = f"For all {src_type} type values in the return results, " \
                      f"increase each value by {offset}."

        else:
            raise NotImplementedError
        return command, op

    def generate_command(self, src_type_list, language):
        if language == 'py':
            src_type = random.choice(src_type_list)
            command, op = self.generate_command_py(src_type)
        else:
            raise NotImplementedError
        return command, src_type, src_type, op
