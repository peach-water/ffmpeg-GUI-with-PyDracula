# FFMPEG GUI PyDracula 
# 

> 本项目从[PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)修改而来
> 感谢 Wanderson M. Pimenta 的 repository [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)

> **警告**: 本项目使用 PySide6 和 Python 3.9 开发，使用较早的版本可能会出现兼容性问题。

# YouTube - 教程与帮助
关于修改用户界面以及理解项目的教程。
> 🔗 https://youtu.be/9DnaHg4M_AM

# 多种主题
![PyDracula_Default_Dark](https://user-images.githubusercontent.com/60605512/112993874-0b647700-9140-11eb-8670-61322d70dbe3.png)
![PyDracula_Light](https://user-images.githubusercontent.com/60605512/112993918-18816600-9140-11eb-837c-e7a7c3d2b05e.png)

# 高分辨率设置
> QT 控件是一项比较老的技术，不能较好的支持高DPI的设置。如果你的系统DPI设置高于100%，GUI界面的图像会被扭曲。
> 你可以用下面的方法，通过在"main.py"的Qt控件导入后加入这段代码来避免这个问题。

```python
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96"
```

# 启动
> 在你的系统上安装 Python 3.9> 和 PySide6，然后就可以使用下面的代码在终端中启动这个项目。
> ## **Windows**:
```console
python main.py
```
> ## **MacOS and Linux**:
```console
python3 main.py
```
# 编译
> ## **Windows**:
```console
python setup.py build
```
> ## 使用 Pyinstaller 编译 exe 项目
```
pyinstaller -F main.py
```
在那之前还需要使用命令 pip install pyinstaller==5.13 来安装打包环境。
更新的pyinstaller没有尝试。
编译成功后，在当前目录下可以找到"./dist/main.exe"文件，在启动之前还需要复制theme主题文件到"./dist/"，否则会因为找不到主题文件报错。

# 项目文件及文件夹
> **main.py**: 程序主文件.

> **main.ui**: 使用 Qt Designer GUI界面设计文件.

> **resouces.qrc**: Qt Designer 加载"main.ui"使用的图片资源（例如背景图，图标等），也需要加载以保证程序正确运行。使用 version 6 >

> **setup.py**: 编译项目为 Windows 可执行程序。

> **themes/**: 放你的主题文件 (.qss)。

> **modules/**: 本项目功能实现模块。

> **modules/app_funtions.py**: 原来的功能实现文件。

> **modules/btn_functions.py**: ffmpeg功能实现文件。

> **modules/app_settings.py**: 用户交互界面全局设置文件。

> **modules/resources_rc.py**: "resource.qrc" 需要使用这条命令编译得到 ```pyside6-rcc resources.qrc -o resources_rc.py```。

> **modules/ui_functions.py**: 和用户交互界面相关函数实现。

> **modules/ui_main.py**: 由 Qt Designer 编译导出用户界面得到。你可以使用下面的命令手动导出本文件 ```pyside6-uic main.io -o ui_main.py```。导出以后需要把代码 "import resources_rc" 修改成 "from . resources_rc import *" 来导入资源文件。或者直接修改resources_rc.py文件的位置能够被python解释器找到也可以。

> **images/**: 在编译成资源文件resource_rc.py之前把项目需要使用的图像资源全部放到这里。



