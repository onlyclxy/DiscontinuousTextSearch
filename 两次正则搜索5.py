import os
import re
from tqdm import tqdm
from datetime import datetime


def generate_html_file(result_list):
    """
    生成包含搜索结果的 HTML 文件
    """
    with open("search_result.html", 'w',encoding="utf8") as f:
        title = "Search Result"
        f.write(f"<!doctype html>\n<html>\n<head>\n<meta charset='UTF-8'>\n<title>{title}</title>\n</head>\n<body>\n")
        f.write(f"<h1>{title}</h1>\n")
        for file in result_list:
            f.write(f"<p><a href=file://{file}>{file}</a></p>\n")
        f.write("</body>\n</html>\n")
    print(f"结果已保存至 search_result.html 中。")


# 定义文件名和路径
filename = "search_result.txt"
path = ""


while True:
    # 输入扩展名和路径
    extensions = input("请输入要搜索的扩展名（用英文逗号分隔 例如 txt,xml）：")
    extension_list = extensions.split(',')


    paths = input("请输入文件路径（用英文逗号分隔）：")
    path_list = paths.split(',')


    # 输入首个正则表达式和次个正则表达式
    regex_1 = input("请输入首个搜索文本，支持正则表达式：")
    regex_2 = input("请输入次个搜索文本，支持正则表达式：")

    # 遍历路径及子路径，获取满足扩展名条件的文件列表
    file_list = []

    # 遍历每个路径及其子路径，获取满足扩展名条件的文件列表
    for path in path_list:
        for root, dirs, files in tqdm(os.walk(path), desc="正在遍历文件..."):
            for file in files:
                if file.endswith(tuple(extension_list)):
                    file_list.append(os.path.join(root, file))


    result_list = []
    # 对满足扩展名条件的文件进行内容搜索
    for file in tqdm(file_list, desc="正在搜索文件..."):
        with open(file, 'r') as f:
            content = f.read()
            if re.search(regex_1, content) and re.search(regex_2, content):
                result_list.append(file)

    if result_list:
        # 输出搜索到的文件列表
        print("以下文件包含搜索到的内容：")
        for file in result_list:
            print("-", file)

        # 将搜索结果追加到文件，并同时保存为逆序格式
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(filename, 'a') as f:
            f.write(f"\n\n搜索时间：{now}\n")
            for file in reversed(result_list):
                f.write(f"{file}\n")

        # 生成包含搜索结果的 HTML 文件
        generate_html_file(result_list)

    else:
        print("未找到任何符合条件的文件。")

    # 询问是否继续搜索
    choice = input("按回车键继续，退出请关闭窗口：")
    if choice.upper() == 'N':
        break
