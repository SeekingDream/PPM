import random
from .abstract_method import AbstractMethods


class constract_prompt(AbstractMethods):
    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)

    def add_demo(self):
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
            else :
                raise NameError


        else:
            return self.prompt

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




    def rep_demo(self):
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



        # Divide the test cases in test
        # end_index = self.test.index('\n\n')
        # tests = self.test[:end_index]
        # assert_statements = tests.split('assert candidate')[1:]
        # if assert_statements:
        #     random_statement = random.choice(assert_statements)
        #     rep_test = '>>> ' + self.entry_point + random_statement
        #     rep_test = rep_test.replace(' == ', "\n\t")
        #     new_prompt = prompt.replace(org_test, rep_test)
        #     return new_prompt
        # else:
        #     print("rep_demo fail,please check the test")
