# 这个文件用于自动打包项目，并复制相关文件到合适位置
import os
import argparse

parser = argparse.ArgumentParser()

md5sum_map = {}
from hashlib import md5
def file_depulicate(path):
    """
    用 md5 值检查 path 路径下文件重复情况，这个为附加组件，与构建脚本无关
    """
    global md5sum_map
    for filenames in os.listdir(path):
        filename = os.path.join(path, filenames)
        if os.path.isdir(filename):
            file_depulicate(filename)
        else:
            with open(filename, "rb") as f:
                content = f.read()
            file_md5 = md5(content).hexdigest()
            # print(file_md5)
            if md5sum_map.get(file_md5, None) is None:
                md5sum_map[file_md5] = filename
            else:
                print(f"file {md5sum_map[file_md5]} \nfile {filename} duplicated")
                print(os.path.getsize(filename), end=" Bytes\n\n")


def copyDir(src, tar):
    # 文件夹复制，保持原目录树的形式
    source_path = os.path.abspath(src)
    target_path = os.path.abspath(tar)
    dirs = os.listdir(source_path)
    for dir in dirs:
        source_path_new = source_path + "\\" + dir
        target_path_new = target_path + "\\" + dir

        if os.path.isdir(source_path_new):
            if not os.path.exists(target_path_new):
                os.makedirs(target_path_new)
            copyDir(source_path_new, target_path_new)
        else:
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            os.system(f"copy \"{source_path_new}\" \"{target_path}\"")
            print(target_path_new)

def build(arg:dict):
    # 一些必要的构建参数
    parameter = "-y "
    # parameter += "--copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata pyyaml"
    # parameter += " --add-data model:./model --add-data resources:./resources"

    if arg.g:
        os.system("pyinstaller -D ./main.py " + parameter)
    else:
        os.system("pyinstaller -Dw ./main.py " + parameter)

    if not os.path.exists("./dist"):
        print("发生错误，请检查构建日志")
        exit(-1)

    print("处理剩余配置...")
    print("拷贝主题文件")
    copyDir("./resources/themes", "./dist/main/resources/themes")
    print("拷贝配置文件")
    print("拷贝模型文件")
    copyDir("./model", "./dist/main/model")
    print("清理文件...")

if __name__ == "__main__":

    parser.add_argument("-g", action="store_true",
                        default=False, help="表示需要调试窗口")

    arg = parser.parse_args()
    
    build(arg)
    # 检查 pyinstaller 是否重复复制了部分文件
    # file_depulicate("./dist/main")
