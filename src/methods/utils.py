from typing import List
import ast
import astor


def parse_assertion(assert_statement):
    # Parse the function call into an AST
    tree = ast.parse(assert_statement)

    # Find the function call node
    call_node = next(
        node for node in ast.walk(tree) if isinstance(node, ast.Call)
    )

    # Extract the arguments
    args = []
    for arg in call_node.args:
        args.append(eval(astor.to_source(arg)))

    output_node = tree.body[0].test.comparators[0]
    if isinstance(output_node, ast.List):
        output_vars = [[eval(astor.to_source(d)) for d in output_node.elts]]
    else:
        output_vars = eval(astor.to_source(output_node))
    # print(args, output_vars)
    return args, output_vars


def replace_assertion_output(assertion_code, desired_output: List):
    # Parse the assertion statement
    parsed_ast = ast.parse(assertion_code)

    # Find the assertion statement and replace the expected output
    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.Assert):
            node.test.comparators = [ast.Constant(value=output) for output in desired_output]

    # Recompile the modified AST into Python code
    modified_code = astor.to_source(parsed_ast)

    return modified_code


def concat_move_non_english(a, b):
    non_english = ""
    # Find the non-English character at the end of string a
    for char in reversed(a):
        if char != ".":
            non_english = char + non_english
        else:
            break

    # Concatenate a and b, moving the non-English character to the end
    result = a[:-len(non_english)] + " " + b + non_english
    return result


def replace_asserts_in_function(function_code, assert_replacements):
    # Parse the function code
    parsed_ast = ast.parse(function_code)

    # Traverse the AST to find assert statements within the function
    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.Assert):
            # Replace the original assert statements with new statements
            node.test = ast.parse(assert_replacements[0]).body[0].test
            assert_replacements = assert_replacements[1:]

    # Recompile the modified AST into Python code
    modified_code = astor.to_source(parsed_ast)

    return modified_code


def get_list_element_type(list_a):
    possible_types = summarize_types(list_a)
    possible_type_str = ','.join(possible_types)
    return f"list[{possible_type_str}]"


def get_tuple_element_type(tuple_a):
    possible_types = summarize_types(tuple_a)
    possible_type_str = ','.join(possible_types)
    return f"tuple[{possible_type_str}]"


def get_dict_element_type(dict_a):
    map_list = set()
    for k in dict_a:
        v = dict_a[k]
        map_list.add(type(v).__name__)
    possible_type_str = ','.join(list(map_list))
    return f"dict[{possible_type_str}]"


def summarize_types(val_list):
    possible_types = set()
    for v in val_list:
        if v is None:
            continue
        type_name = type(v).__name__
        if type_name in ['bool', 'int', 'str', 'float']:
            possible_types.add(type_name)
        elif type_name == 'list':
            new_type_name = get_list_element_type(v)
            possible_types.add(new_type_name)
        elif type_name == 'tuple':
            new_type_name = get_tuple_element_type(v)
            possible_types.add(new_type_name)
        elif type_name == 'dict':
            new_type_name = get_dict_element_type(v)
            possible_types.add(new_type_name)
        else:
            raise NotImplementedError
    return list(possible_types)


def modify_list_output_values(v_list, src_type, op):
    new_list = []
    for v in v_list:
        new_list.append(modify_output_values(v, src_type, op))
    return new_list


def modify_dict_output_values(v_dict, src_type, op):
    new_dict = {}
    for v in v_dict:
        new_dict[v] = modify_output_values(v_dict[v], src_type, op)
    return new_dict


def modify_tuple_output_values(v_tuple, src_type, op):
    new_tuple = []
    for v in v_tuple:
        new_tuple.append(modify_output_values(v, src_type, op))
    return tuple(new_tuple)


def modify_output_values(v, src_type, op):
    if v is None:
        return None
    type_name = type(v).__name__
    if type_name in ['bool', 'int', 'str', 'float']:
        if isinstance(v, eval(src_type)):
            return op(v)
        else:
            return v
    elif type_name == 'list':
        return modify_list_output_values(v, src_type, op)
    elif type_name == 'tuple':
        return modify_tuple_output_values(v, src_type, op)
    elif type_name == 'dict':
        return modify_dict_output_values(v, src_type, op)
    else:
        raise NotImplementedError

