# FFMPEG GUI PyDracula 
# 

# 😊Introduction

> ❌**Important：** This project does not have FFMPEG environment installed in, and you need to solve FFMPEG environmental problems by yourself. The ffmpeg command can be recognized at the shell is ok.❌

Currently implemented features:
* Preview the command on the textbox, and you can modify the command if you learned how to use FFMPEG.
* Convert video in preset mode
* Extract videos
* Extract audio and save in mp3
* Batch transcoding(not include subtitle)
* Setting transcoding bitrate
* Setting transcoding speed mode
* Merge subtitle
* Auto Cut the video (Automatically cut out the corresponding video based on the audio)
* Use Whisper to automatically generate subtitles for videos
* Use Paraformer to automatically generate chinese subtitles for videos

features will be implemented in future:
* More preset mode
* Multi-segment video stitching (Maybe not so important for this tiny project)
* Choose and Download Whisper model
* cuda acceleration 

# Multiple Themes
![PyDracula_Default_Dark](https://github.com/peach-water/ffmpeg-GUI-with-PyDracula/blob/master/gallery/dark_theme.png?raw=true)
![PyDracula_Light](https://github.com/peach-water/ffmpeg-GUI-with-PyDracula/blob/master/gallery/light_theme.png?raw=true)


# 🛠 For developer

> 💥**Warning**: this project was created using PySide6 and Python 3.10, using previous versions can cause compatibility problems.

## YouTube - Presentation And Tutorial
Presentation and tutorial video with the main functions of the user interface.
> 🔗 https://youtu.be/9DnaHg4M_AM

## High DPI
> Qt Widgets is an old technology and does not have a good support for high DPI settings, making these images look distorted when your system has DPI applied above 100%.
You can minimize this problem using a workaround by applying this code below in "main.py" just below the import of the Qt modules.
```python
# ADJUST QT FONT DPI FOR HIGHT SCALE
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96"
```

## Running
> Inside your preferred terminal run the commands below depending on your system, remembering before installing Python 3.9> and requirements "pip install -r requirements.txt".
> ### **Windows**:
```console
python main.py
```
> ### **MacOS and Linux**:
```console
python3 main.py
```
## Compiling
> ### **Using Pyinstaller**
```console
pyinstaller -Dw ./main.py --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --copy-metadata huggingface-hub --copy-metadata safetensors --copy-metadata pyyaml
```

After successful compilation, the "./dist/main/main.exe" file can be found in the current directory, and you need to copy the theme directory to "./dist/main" before starting, otherwise an error will be reported because the theme file cannot be found. Follows similarly:
* Copy the model directory to the './dist/main/_internal' directory, which is required by auto cut and auto subtitle function.
* Copy the modules/whisper/ folder to the './dist/main/modules/' directory, this file is required by subtitles.

## Error Fix

### Build error

if error info `tuple index out of range` raised when build with pyinstaller under the python3.10.
Please modify the function `_unpack_opargs` from file `src/python3.10/Lib/dis.py` as follows.

```python
def _unpack_opargs(code):
    extended_arg = 0
    for i in range(0, len(code), 2):
        op = code[i]
        if op >= HAVE_ARGUMENT:
            arg = code[i+1] | extended_arg
            extended_arg = (arg << 8) if op == EXTENDED_ARG else 0
        else:
            arg = None
            extended_arg = 0
        yield (i, op, arg)

```

### Execute error

Get an error like the one shown below when you start the program.
```shell
File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "PyInstaller\loader\pyimod02_importers.py", line 385, in exec_module
  File "transformers\utils\import_utils.py", line 37, in <module>
    logger = logging.get_logger(__name__)  # pylint: disable=invalid-name
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "transformers\utils\logging.py", line 124, in get_logger
    _configure_library_root_logger()
  File "transformers\utils\logging.py", line 88, in _configure_library_root_logger
    _default_handler.flush = sys.stderr.flush
                             ^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'flush'
```

Please open the `[path to]/transformers/utils/logging.py` and add the follow code, then rebuild the program again.

```python
def _configure has already_library_root_logger() -> None:
    ...
    _default_handler = logging.StreamHandler()
    + if sys.stderr is None:
    +     sys.stderr = open(os.devnull, "w")
    
    _default_handler.flush = sys.stderr.flush
    ...
```

## Project Files And Folders
> **main.py**: application initialization file.

> **main.ui**: Qt Designer project.

> **resouces.qrc**: Qt Designer resoucers, add here your resources using Qt Designer. Use version 6 >

> **setup.py**: cx-Freeze setup to compile your application (configured for Windows).

> **themes/**: add here your themes (.qss).

> **modules/**: module for running PyDracula GUI.

> **modules/app_funtions.py**: add your application's functions here.

> **modules/app_settings.py**: global variables to configure user interface.

> **modules/auto_cut.py**: auto cut function implementation.

> **modules/auto_subtitle.py**: Call the whisper subtitle function implement file.

> **modules/btn_functions.py**: Software feature implementation files.

> **modules/video_convert.py**: Transcode the video.

> **modules/vad_functions.py**: Vocal recognition module, from SERR4/SILERO-VAD.

> **modules/resources_rc.py**: "resource.qrc" file compiled for python using the command: ```pyside6-rcc resources.qrc -o resources_rc.py```.

> **modules/ui_functions.py**: add here only functions related to the user interface / GUI.

> **modules/ui_main.py**: file related to the user interface exported by Qt Designer. You can compile it manually using the command: ```pyside6-uic main.ui> ui_main.py ```.
After expoting in .py and change the line "import resources_rc" to "from. Resoucers_rc import *" to use as a module.

> **images/**: put all your images and icons here before converting to Python (resources_re.py) ```pyside6-rcc resources.qrc -o resources_rc.py```.

# Projects Created Using PyDracula
**See the projects that were created using PyDracula.**
> To participate create a "Issue" with the name beginning with "#pydracula_project", leaving the link of your project on Github, name of the creator and what is its functionality. Your project will be added and this list will be deleted from "Issue".
**Malicious programs will not be added**!

# Acknowledgment

> This Project is modified from https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6 .

> thanks Wanderson M. Pimenta for open-source repository [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6) .

> thanks snakers4 for open-source repository [Silero-vad](https://github.com/snakers4/silero-vad) .

> thanks PINTO0309 for open source repository [whisper-onnx-cpu](https://github.com/PINTO0309/whisper-onnx-cpu) .

> thanks RapidAI for open-source repository [RapidASR](https://github.com/RapidAI/RapidASR) .
