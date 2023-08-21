# FFMPEG GUI PyDracula 
# 

> 本项目从[PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)修改而来
> 感谢 Wanderson M. Pimenta 的 repository [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)
> 感谢 snakers4 的 repository [Silero-vad](https://github.com/snakers4/silero-vad) 。
> 感谢 PINTO0309 的 repository [whisper-onnx-cpu](https://github.com/PINTO0309/whisper-onnx-cpu) 。

# 多种主题
![PyDracula_Default_Dark](https://github.com/peach-water/ffmpeg-GUI-with-PyDracula/blob/master/gallery/dark_theme.png?raw=true)
![PyDracula_Light](https://github.com/peach-water/ffmpeg-GUI-with-PyDracula/blob/master/gallery/light_theme.png?raw=true)

# ✔简介

🤣界面还没有整理🤣部分按钮目前没有实际作用🤣其实暂时作为一个ffmpeg的命令生成GUI工具也是可以的。
🤣又不是不能用🤣。

> ❌**重要：** 本项目没有ffmpeg环境安装，需要用户自行解决ffmpeg的环境问题。能够在命令行识别到ffmpeg命令即可。❌

目前实现的功能：
* 命令窗口预览将要执行的命令，可以修改（懂ffmpeg命令的话，就可以自己修改指令实现目的）
* 转码视频文件
* 提取视频
* 视频二倍速
* 视频转MP3
* 批量转码功能
* 转码码率设置
* 转码速度设置
* 内挂字幕（仅限mkv格式）
* 内嵌字幕
* 自动切片（根据音频自动切出对应音频）
* 接入 Whisper 实现视频自动生成字幕（Whisper似乎对中文识别不是很好，容易识别成繁体中文）

未来期望实现功能：
* 更多的目标格式
* 多段视频拼接
* ffmpeg错误提示和反馈（目前ffmpeg出错是没有提示和反馈的）
* whisper模型选择和下载
* whisper可以使用GPU加速

> Pyside打包是真的大啊，不知道有没有什么可以压缩这部分的方法。

> 默认会显示后台终端，方便查看GUI报错。

# 🛠 以下为开发人员内容

## YouTube - 教程与帮助
关于修改用户界面以及理解项目的教程。
> 🔗 https://youtu.be/9DnaHg4M_AM

> 💥**警告**: 本项目使用 PySide6 和 Python 3.9 开发，使用较早的版本可能会出现兼容性问题。

## 高分辨率设置

> QT 控件是一项比较老的技术，不能较好的支持高DPI的设置。如果你的系统DPI设置高于100%，GUI界面的图像会被扭曲。
> 你可以用下面的方法，通过在"main.py"的Qt控件导入后加入这段代码来避免这个问题。

```python
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96"
```

## 启动
> 在你的系统上按照'requirements.txt'安装环境，然后就可以使用下面的代码在终端中启动这个项目。
> ### **Windows**:
```console
python main.py
```
> ### **MacOS and Linux**:
```console
python3 main.py
```
## 编译
> ### **Windows**:
```console
python setup.py build
```
> ### 使用 Pyinstaller 编译 exe 项目
```console
pyinstaller -Dw ./main.py --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --copy-metadata huggingface-hub --copy-metadata safetensors --copy-metadata pyyaml
```
在那之前还需要使用命令 pip install pyinstaller==5.13 来安装打包环境。
更新的pyinstaller没有尝试。
编译成功后，在当前目录下可以找到"./dist/main/main.exe"文件，在启动之前还需要复制theme主题文件到"./dist/main"，否则会因为找不到主题文件报错。类似的还有：
* 复制model文件到'./dist/main'目录下，自动剪辑功能需要这个模型。
* 复制modules/whisper/assets文件夹到'./dist/main/modules/whisper'目录下，配字幕需要这个功能

> transformer库打包需要这一溜的metadata数据才可以正常运行，所以需要加上。

## 项目文件及文件夹
> **main.py**: 程序主文件.

> **main.ui**: 使用 Qt Designer GUI界面设计文件.

> **resouces.qrc**: Qt Designer 加载"main.ui"使用的图片资源（例如背景图，图标等），也需要加载以保证程序正确运行。使用 version 6 >

> **setup.py**: 编译项目为 Windows 可执行程序。

> **themes/**: 放你的主题文件 (.qss)。

> **modules/**: 本项目功能实现模块。

> **modules/app_funtions.py**: 原来的功能实现文件。

> **modules/btn_functions.py**: ffmpeg功能实现文件。

> **modules/vad_functions.py**: 人声识别模块，来自snakers4/silero-vad。

> **modules/app_settings.py**: 用户交互界面全局设置文件。

> **modules/resources_rc.py**: "resource.qrc" 需要使用这条命令编译得到 ```pyside6-rcc resources.qrc -o resources_rc.py```。

> **modules/ui_functions.py**: 和用户交互界面相关函数实现。

> **modules/ui_main.py**: 由 Qt Designer 编译导出用户界面得到。你可以使用下面的命令手动导出本文件 ```pyside6-uic main.io -o ui_main.py```。导出以后需要把代码 "import resources_rc" 修改成 "from . resources_rc import *" 来导入资源文件。或者直接修改resources_rc.py文件的位置能够被python解释器找到也可以。

> **images/**: 在编译成资源文件resource_rc.py之前把项目需要使用的图像资源全部放到这里。



