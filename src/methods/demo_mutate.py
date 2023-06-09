import random
from .abstract_method import AbstractMethods


class constract_prompt(AbstractMethods):
    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)

    def add_demo(self):
        # Divide the test cases in test
        assert_statements = self.test.split('assert candidate')[1:]

        # Randomly choose one
        if assert_statements:
            random_statement = random.choice(assert_statements)
            add_test = '>>> ' + self.entry_point + random_statement

            # Find the position of the last """
            last_quote_index = self.prompt.rfind('"""')

            if last_quote_index >= 0:
                # add_demo
                updated_prompt = self.prompt[:last_quote_index] + add_test + self.prompt[last_quote_index:]
                return updated_prompt
            else:
                print("No closing quotes found in the string.")

        else:
            print("add_demo fail,please check the test")

    def del_demo(self):
        prompt = self.prompt
        # find all tests from prompt
        test_demo = prompt.split('>>> ')[1:]
        test_num = len(test_demo)
        # If there is only one test case, not delete
        if test_num <= 1:
            return prompt
        else:
            # delete a demo randomly
            quote_index = test_demo[test_num - 1].find('"""')
            if quote_index != -1:
                test_demo[test_num - 1] = test_demo[test_num - 1][:quote_index]
            random_statement = random.choice(test_demo)
            del_test = '>>> ' + random_statement
            new_prompt = prompt.replace(del_test, "")
            return new_prompt

    def rep_demo(self):
        prompt = self.prompt
        # find all tests from prompt
        test_demo = prompt.split('>>> ')[1:]
        test_num = len(test_demo)
        quote_index = test_demo[test_num - 1].find('"""')
        if quote_index != -1:
            test_demo[test_num - 1] = test_demo[test_num - 1][:quote_index]
        random_statement = random.choice(test_demo)
        org_test = '>>> ' + random_statement

        # Divide the test cases in test
        assert_statements = self.test.split('assert candidate')[1:]
        if assert_statements:
            random_statement = random.choice(assert_statements)
            rep_test = '>>> ' + self.entry_point + random_statement
            new_prompt = prompt.replace(org_test, rep_test)
            return new_prompt
        else:
            print("rep_demo fail,please check the test")



