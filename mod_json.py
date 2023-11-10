
import json
import os
import argparse


def mod_json(subfolders):
    # 遍历每个子文件夹
    for subfolder_path in subfolders:
        # 遍历文件夹中的所有文件
       # json_file_path = os.path.join(subfolder_path, os.path.basename(subfolder_path) + '.json')
        #with open(json_file_path, 'r') as json_file:
        #    data = json.load(json_file)
        py_completions = []
        for file_name in os.listdir(subfolder_path):
            if file_name.endswith('.py'):
                #find .py path
                file_path = os.path.join(subfolder_path, file_name)
                with open(file_path, 'r',encoding='UTF-8') as py_file:
                    content = py_file.read()
                    split1 = content.split('"""\n', 2)
                    if(len(split1)==2):
                        content_after_first_occurrence = split1[1]
                    elif(len(split1)==3):
                        content_after_first_occurrence = split1[2]
                    else:
                        print(len(split1))
                    split2 = content_after_first_occurrence.split('def check', 1)
                    desired_content = split2[0]
                    py_completions.append(desired_content)
                    #assert data["prompt"]+desired_content+data["tests"]==content

        json_file_path = os.path.join(subfolder_path, os.path.basename(subfolder_path) + '.json')
        # 读取json文件内容
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            # 修改特定内容
        data['completions'] = py_completions
        # 将修改后的内容写入json文件，覆盖原有内容
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, type=str)
    args = parser.parse_args()

    parent_folder_path = args.path  # 替换为父级目录的路径
    subfolders = [f.path for f in os.scandir(parent_folder_path) if f.is_dir()]
    mod_json(subfolders)

if __name__ == "__main__":
    main()


