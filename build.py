# 这个文件用于自动打包项目，并复制相关文件到合适位置
import os
import argparse

parser = argparse.ArgumentParser()


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


if __name__ == "__main__":

    parser.add_argument("-g", action="store_true",
                        default=False, help="表示需要调试窗口")

    arg = parser.parse_args()

    if arg.g:
        os.system("pyinstaller -D ./main.py --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --copy-metadata huggingface-hub --copy-metadata safetensors --copy-metadata pyyaml")
    else:
        os.system("pyinstaller -Dw ./main.py --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --copy-metadata huggingface-hub --copy-metadata safetensors --copy-metadata pyyaml")

    if not os.path.exists("./dist/main/main.exe"):
        print("errror")
        exit(-1)

    print("处理剩余配置...")
    print("拷贝主题文件")
    copyDir("./themes", "./dist/main/themes")
    print("拷贝配置文件")
    copyDir("./modules/whisper/assets",
            "./dist/main/_internal/modules/whisper/assets")
    print("拷贝模型文件")
    copyDir("./model", "./dist/main/_internal/model")
    print("清理文件...")
