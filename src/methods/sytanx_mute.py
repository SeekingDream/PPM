import random
from .abstract_method import AbstractMethods


class SyntaxMutation(AbstractMethods):
    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)


def doc2comments_general_python(code, entry_point=None):
    """ change \"\"\" to # comments
    This function is general, perturbing all of \"\"\" to # comments
    """
    
    new_code = str(code)

    #The following line is for mbpp
    new_code = new_code.replace('\t','    ')
    #===============================
    doc_types = ["\"\"\"", "\'\'\'"]
    for doc_type in doc_types:
        doc_start = new_code.find(doc_type)
        while doc_start != -1:
            if doc_start > 0:
                # get all the indent before """
                doc_line_start = doc_start - 1
                indent = ""
                while doc_line_start >= 0:
                    ch = new_code[doc_line_start]
                    if ch in [" ", "\t"]:
                        doc_line_start -= 1
                        indent = ch + indent
                    else:
                        break
                # if new_code[doc_line_start] != "\n": import pdb; pdb.set_trace()
                # assert new_code[doc_line_start] == "\n"
                doc_line_start += 1
            else:
                indent = ""
                doc_line_start = doc_start

            doc_end = new_code.find(doc_type, doc_start + len(doc_type))
            if doc_end == -1: break  # some times appear text/strings...
            # in case there are spaces after doc_end of """
            doc_line_end = doc_end + len(doc_type)
            for ch in new_code[doc_end:]:
                if ch in [" ", "\t"]:
                    doc_line_end += 1
                else:
                    break
            # if new_code[doc_line_end] != "\n": import pdb; pdb.set_trace()
            # assert new_code[doc_line_end] == "\n"

            doc_lines = new_code[doc_line_start: doc_line_end]
            # print(doc_lines)
            # import pdb; pdb.set_trace()

            lines = doc_lines.split("\n")

            new_lines = []
            for line in lines:
                new_line = str(line)
                if line.replace(" ", "").replace("\t", "").replace("\n", "") == doc_type:
                    # remove these lines
                    new_lines.append(new_line.replace(f"{doc_type} ", "").replace(doc_type, ""))
                    continue
                if doc_type in line:
                    new_line = new_line.replace(f"{doc_type} ", "").replace(doc_type, "")
                space_ahead = ""
                ch_idx = 0
                for ch_idx, ch in enumerate(line):
                    if ch in [" ", "\t"]:
                        space_ahead += ch
                    else:
                        break

                # new_line = space_ahead.replace(indent, indent + "# ") + new_line[ch_idx:]
                if indent in space_ahead:
                    new_line = space_ahead[: len(indent)] + "# " + space_ahead[len(indent):] + new_line[ch_idx:]
                new_lines.append(new_line)

            new_code = new_code[:doc_line_start] + "\n".join(new_lines) + "\n" + new_code[doc_line_end + 1:]
            last_doc_start = doc_start
            doc_start = new_code.find(doc_type)  # need to refind the doc end idx, previous ones already removed
            if last_doc_start == doc_start: print("Warning: doc start repeated!")

    return new_code


class CommentMutation(SyntaxMutation):
    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)

    def mutate(self, lang):
        if lang == 'py':
            return self.mutate_py()

    def mutate_py(self):
        return doc2comments_general_python(self.prompt, self.entry_point)


class InsertLineMutation(SyntaxMutation):
    def __init__(self, prompt, test, entry_point):
        super().__init__(prompt, test, entry_point)

    def mutate(self, lang):
        if lang == 'py':
            return self.mutate_py()

    def mutate_py(self):
        func_entry, comments, test_demo = self.split_desc_testcases_py()
        if random.random() < 0.5:
            new_comments = '\n' + comments
        else:
            new_comments = comments + '\n'
        new_prompt = self.combine_desc_testcases_py(func_entry, new_comments, test_demo)
        return new_prompt


