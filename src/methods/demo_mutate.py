import random
from .abstract_method import AbstractMethods


class DemoMutation(AbstractMethods):
    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)

    def add_demo(self, language):
        if language == 'py':
            return self.add_demo_py()
        elif language == 'cs':
            return self.add_demo_cs()
        elif language == 'cpp':
            return self.add_demo_cpp()
        elif language == 'java':
            return self.add_demo_java()
        else:
            raise ValueError(
                "language error"
            )

    def del_demo(self, language):
        if language == 'py':
            return self.del_demo_py()
        elif language == 'cs':
            return self.del_demo_cs()
        elif language == 'cpp':
            return self.del_demo_cpp()
        elif language == 'java':
            return self.del_demo_java()
        else:
            raise ValueError(
                "language error"
            )

    def rep_demo(self, language):
        if language == 'py':
            return self.rep_demo_py()
        elif language == 'cs':
            return self.rep_demo_cs()
        elif language == 'cpp':
            return self.rep_demo_cpp()
        elif language == 'java':
            return self.rep_demo_java()
        else:
            raise ValueError(
                "language error"
            )

    def add_demo_py(self):
        # Divide the test cases in test
        end_index = self.test.index('\n\n')
        tests = self.test[:end_index]
        assert_statements = tests.split('assert candidate')[1:]
        # Randomly choose one
        if assert_statements:
            random_statement = random.choice(assert_statements)
            add_test = '>>> ' + self.entry_point + random_statement
            add_test = add_test.replace(' == ', "\n\t")

            # Find the position of the last """
            last_quote_index1 = self.prompt.rfind('"""')
            last_quote_index2 = self.prompt.rfind("'''")
            if last_quote_index1 >= 0:
                # add_demo
                updated_prompt = self.prompt[:last_quote_index1] + add_test + self.prompt[last_quote_index1:]
                return updated_prompt
            elif last_quote_index2 >= 0:
                # add_demo
                updated_prompt = self.prompt[:last_quote_index2] + add_test + self.prompt[last_quote_index2:]
                return updated_prompt
            else:
                raise NameError
        else:
            return self.prompt

    def del_demo_py(self):
        prompt = self.prompt
        # find all tests from prompt
        test_demo = prompt.split('>>> ')[1:]
        test_num = len(test_demo)
        # If there is only one test case, not delete
        if test_num <= 1:
            return prompt
        else:
            # delete a demo randomly
            quote_index1 = test_demo[test_num - 1].find('"""')
            quote_index2 = test_demo[test_num - 1].find("'''")
            if quote_index1 != -1:
                test_demo[test_num - 1] = test_demo[test_num - 1][:quote_index1]
            elif quote_index2 != -1:
                test_demo[test_num - 1] = test_demo[test_num - 1][:quote_index2]
            random_statement = random.choice(test_demo)
            del_test = '>>> ' + random_statement
            new_prompt = prompt.replace(del_test, "")
            return new_prompt

    def rep_demo_py(self):
        prompt = self.prompt
        # find all tests from prompt
        test_demo = prompt.split('>>> ')[1:]
        test_num = len(test_demo)
        if test_num <= 0:
            return prompt
        else:
            # Find the position of the last """
            quote_index1 = test_demo[test_num - 1].find('"""')
            quote_index2 = test_demo[test_num - 1].find("'''")
            if quote_index1 != -1:
                test_demo[test_num - 1] = test_demo[test_num - 1][:quote_index1]
            elif quote_index2 != -1:
                test_demo[test_num - 1] = test_demo[test_num - 1][:quote_index2]
            random_statement = random.choice(test_demo)
            org_test = '>>> ' + random_statement

            # Divide the test cases in test
            end_index = self.test.index('\n\n')
            tests = self.test[:end_index]
            assert_statements = tests.split('assert candidate')[1:]
            # Randomly choose one
            if assert_statements:
                random_statement = random.choice(assert_statements)
                rep_test = '>>> ' + self.entry_point + random_statement
                rep_test = rep_test.replace(' == ', "\n\t")
                new_prompt = prompt.replace(org_test, rep_test)
                return new_prompt
            else:
                # print("rep_demo fail,please check the test")
                raise NameError

    def add_demo_cs(self):
        # Divide the test cases in test
        lines = self.test.splitlines()
        assert_lines = []
        for line in lines:
            trimmed_line = line.strip()
            if trimmed_line.startswith("Debug.Assert"):
                assert_lines.append(trimmed_line)
        if assert_lines:
            s = random.choice(assert_lines)
            if " == " in s:
                parts = s.split(" == ", maxsplit=1)
                parts[0] = parts[0][13:]
                parts[1] = parts[1][:-2]
            elif ".Equals" in s:
                parts = s.split(".Equals(", maxsplit=1)
                parts[0] = parts[0][13:]
                # parts[1] = parts[1][:parts[1].rfind(")")]
                parts[1] = parts[1][:-3]
            else:
                parts = [s]
            index = self.prompt.find("// >>>")
            if index == -1:
                return self.prompt
            insert = '// >>> ' + parts[0] + '\n\t// ' + parts[1] + "\n\t"
            new_prompt = self.prompt[:index] + insert + self.prompt[index:]
        return new_prompt

    def del_demo_cs(self):
        test_demo = self.prompt.split('// >>> ')[1:]
        length = len(test_demo)
        if length <= 1:
            return self.prompt
        else:
            last_index = test_demo[length - 1].rfind('\n')
            second_last_index = test_demo[length - 1].rfind('\n', 0, last_index)
            test_demo[length - 1] = test_demo[length - 1][:second_last_index]
            test_demo[length - 1] = test_demo[length - 1] + '\n    '

            s = random.choice(test_demo)
            del_test = '// >>> ' + s
            new_prompt = self.prompt.replace(del_test, "")
            return new_prompt

    def rep_demo_cs(self):
        # find all tests from prompt
        test_demo = self.prompt.split('// >>> ')[1:]
        length = len(test_demo)
        if length <= 0:
            return self.prompt
        else:
            last_index = test_demo[length - 1].rfind('\n')
            second_last_index = test_demo[length - 1].rfind('\n', 0, last_index)
            test_demo[length - 1] = test_demo[length - 1][:second_last_index]
            test_demo[length - 1] = test_demo[length - 1] + '\n    '

            s = random.choice(test_demo)
            org_test = '// >>> ' + s

        # Divide the test cases in test

        lines = self.test.splitlines()
        assert_lines = []
        for line in lines:
            trimmed_line = line.strip()
            if trimmed_line.startswith("Debug.Assert"):
                assert_lines.append(trimmed_line)
        if assert_lines:
            s = random.choice(assert_lines)
            if " == " in s:
                parts = s.split(" == ", maxsplit=1)
                parts[0] = parts[0][13:]
                parts[1] = parts[1][:-2]
            elif ".Equals" in s:
                parts = s.split(".Equals(", maxsplit=1)
                parts[0] = parts[0][13:]
                # parts[1] = parts[1][:parts[1].rfind(")")]
                parts[1] = parts[1][:-3]
            else:
                parts = [s]
            index = self.prompt.find("// >>>")
            if index == -1:
                return self.prompt
            rep_test = '// >>> ' + parts[0] + '\n\t// ' + parts[1] + "\n\t"

        new_prompt = self.prompt.replace(org_test, rep_test)
        return new_prompt

    def add_demo_cpp(self):
        # Divide the test cases in test
        lines = self.test.splitlines()
        assert_lines = []
        for line in lines:
            trimmed_line = line.strip()
            if trimmed_line.startswith("assert"):
                assert_lines.append(trimmed_line)
        if assert_lines:
            s = random.choice(assert_lines)
            if " == " in s:
                parts = s.split(" == ", maxsplit=1)
                parts[0] = parts[0][7:]
                parts[0] = parts[0].replace('candidate', self.entry_point)
                parts[1] = parts[1][:-2]
            elif ".Equals" in s:
                parts = s.split(".Equals(", maxsplit=1)
                parts[0] = parts[0][7:]
                parts[0] = parts[0].replace('candidate', self.entry_point)
                # parts[1] = parts[1][:parts[1].rfind(")")]
                parts[1] = parts[1][:-3]
            else:
                parts = [s]
            index = self.prompt.find("// >>>")
            if index == -1:
                return self.prompt
            insert = '// >>> ' + parts[0] + '\n// ' + parts[1] + '\n'
            new_prompt = self.prompt[:index] + insert + self.prompt[index:]
        return new_prompt

    def del_demo_cpp(self):
        test_demo = self.prompt.split('// >>> ')[1:]
        length = len(test_demo)
        if length <= 1:
            return self.prompt
        else:
            last_index = test_demo[length - 1].rfind('\n')
            second_last_index = test_demo[length - 1].rfind('\n', 0, last_index)
            test_demo[length - 1] = test_demo[length - 1][:second_last_index]
            test_demo[length - 1] = test_demo[length - 1] + '\n'

            s = random.choice(test_demo)
            del_test = '// >>> ' + s
            new_prompt = self.prompt.replace(del_test, "")
            return new_prompt

    def rep_demo_cpp(self):
        # Divide the test cases in test
        lines = self.test.splitlines()
        assert_lines = []
        for line in lines:
            trimmed_line = line.strip()
            if trimmed_line.startswith("assert"):
                assert_lines.append(trimmed_line)
        if assert_lines:
            s = random.choice(assert_lines)
            if " == " in s:
                parts = s.split(" == ", maxsplit=1)
                parts[0] = parts[0][7:]
                parts[0] = parts[0].replace('candidate', self.entry_point)
                parts[1] = parts[1][:-2]
            elif ".Equals" in s:
                parts = s.split(".Equals(", maxsplit=1)
                parts[0] = parts[0][7:]
                parts[0] = parts[0].replace('candidate', self.entry_point)
                # parts[1] = parts[1][:parts[1].rfind(")")]
                parts[1] = parts[1][:-3]
            else:
                parts = [s]
            index = self.prompt.find("// >>>")
            if index == -1:
                return self.prompt
            rep_test = '// >>> ' + parts[0] + '\n// ' + parts[1] + '\n'

        # find all tests from prompt
        test_demo = self.prompt.split('// >>> ')[1:]
        length = len(test_demo)
        if length <= 0:
            return self.prompt
        else:
            last_index = test_demo[length - 1].rfind('\n')
            second_last_index = test_demo[length - 1].rfind('\n', 0, last_index)
            test_demo[length - 1] = test_demo[length - 1][:second_last_index]
            test_demo[length - 1] = test_demo[length - 1] + '\n'

            s = random.choice(test_demo)
            org_test = '// >>> ' + s
        new_prompt = self.prompt.replace(org_test, rep_test)
        return new_prompt

    def add_demo_java(self):
        # Divide the test cases in test
        lines = self.test.splitlines()
        assert_lines = []
        for line in lines:
            trimmed_line = line.strip()
            if trimmed_line.startswith("assert"):
                assert_lines.append(trimmed_line)
        if assert_lines:
            s = random.choice(assert_lines)
            if " == " in s:
                parts = s.split(" == ", maxsplit=1)
                parts[0] = parts[0][7:]
                parts[1] = parts[1][:-2]
            elif ".equals" in s:
                parts = s.split(".equals(", maxsplit=1)
                parts[0] = parts[0][7:]
                # parts[1] = parts[1][:parts[1].rfind(")")]
                parts[1] = parts[1][:-3]
            else:
                parts = [s]
            index = self.prompt.find("// >>>")
            if index == -1:
                return self.prompt
            insert = '// >>> ' + parts[0] + '\n\t// ' + parts[1] + "\n\t"
            new_prompt = self.prompt[:index] + insert + self.prompt[index:]
        return new_prompt

    def del_demo_java(self):
        test_demo = self.prompt.split('// >>> ')[1:]
        length = len(test_demo)
        if length <= 1:
            return self.prompt
        else:
            last_index = test_demo[length - 1].rfind('\n')
            second_last_index = test_demo[length - 1].rfind('\n', 0, last_index)
            test_demo[length - 1] = test_demo[length - 1][:second_last_index]
            test_demo[length - 1] = test_demo[length - 1] + '\n    '

            s = random.choice(test_demo)
            del_test = '// >>> ' + s
            new_prompt = self.prompt.replace(del_test, "")
            return new_prompt

    def rep_demo_java(self):
        # find all tests from prompt
        test_demo = self.prompt.split('// >>> ')[1:]
        length = len(test_demo)
        if length <= 0:
            return self.prompt
        else:
            last_index = test_demo[length - 1].rfind('\n')
            second_last_index = test_demo[length - 1].rfind('\n', 0, last_index)
            test_demo[length - 1] = test_demo[length - 1][:second_last_index]
            test_demo[length - 1] = test_demo[length - 1] + '\n    '

            s = random.choice(test_demo)
            org_test = '// >>> ' + s

        # Divide the test cases in test
        lines = self.test.splitlines()
        assert_lines = []
        for line in lines:
            trimmed_line = line.strip()
            if trimmed_line.startswith("assert"):
                assert_lines.append(trimmed_line)
        if assert_lines:
            s = random.choice(assert_lines)
            if " == " in s:
                parts = s.split(" == ", maxsplit=1)
                parts[0] = parts[0][7:]
                parts[1] = parts[1][:-2]
            elif ".equals" in s:
                parts = s.split(".equals(", maxsplit=1)
                parts[0] = parts[0][7:]
                # parts[1] = parts[1][:parts[1].rfind(")")]
                parts[1] = parts[1][:-3]
            else:
                parts = [s]
            index = self.prompt.find("// >>>")
            if index == -1:
                return self.prompt
            rep_test = '// >>> ' + parts[0] + '\n\t// ' + parts[1] + "\n\t"

        new_prompt = self.prompt.replace(org_test, rep_test)
        return new_prompt
