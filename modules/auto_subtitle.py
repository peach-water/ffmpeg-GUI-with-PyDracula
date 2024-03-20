import os

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QFileDialog
import numpy as np

from .constants import *
from .whisper.transcribe import transcribe
from .whisper.model import load_model
from .whisper.utils import write_srt, write_txt, write_vtt
from .utils import readCacheFile, saveCacheFile

# 监控线程模块
# ///////////////////////////////////////////////////////////////

class SubTitleRunner(QThread):
    """
    调用Whisper配字幕，使用 onnx 封装的 whisper 神经网络模型
    """
    processSignal = Signal(str)
    finishSignal = Signal(str)
    def __init__(self, args: dict, parent=None):
        super(SubTitleRunner, self).__init__(parent)
        """
        初始化信息控制类，
        TODO args 目前是以一个字典的形式传入参数，可读性低，未来改为一个 class 类形式

        Input:
        ---
            args - (dict(str:str))
                参数字典
        """
        self.g_model_name: str = args.pop("model")
        self.g_output_dir: str = args.pop("output_dir")
        self.g_mode = args.pop("mode")

        if self.g_model_name.endswith(".en") and args["language"] not in {"en", "English"}:
            self.finishSignal.emit(f"{self.g_model_name} is an English-only model but receipted '{args['language']}'; using English instead.")
            args["language"] = "en"
        
        self.g_temperature = args.pop("temperature")
        self.g_temperature_increment_on_fallback = args.pop("temperature_increment_on_fallback")
        if self.g_temperature_increment_on_fallback is not None:
            self.g_temperature = tuple(np.arange(self.g_temperature, 1.0+1e-6, self.g_temperature_increment_on_fallback))
        else:
            self.g_temperature = [self.g_temperature]
        
        self.g_model = load_model(self.g_model_name)

        self.args = args
        self.g_output_ext = self.args.pop("output_ext")
        self.processSignal.connect(self.signalHandle)
        self.g_information = []
        self.g_cancel_signal = [True] # 用来结束transcribe函数调用，取消任务。使用list数据类型可以保证参数引用而不是值引用。TODO需要更高级的实现方式。
    
    def run(self):
        """
        开始任务，重载 qthread 的 run 方法
        """
        l_audio_path = self.args.pop("audio")
        try:
            result = transcribe(
                model=self.g_model,
                audio=l_audio_path,
                temperature=self.g_temperature,
                signal_return=self.processSignal,
                cancel=self.g_cancel_signal,
                **self.args
            )
        except RuntimeError as e:
            self.finishSignal.emit(str(e))
            return

        if not self.g_cancel_signal[0]:
            # 任务取消，就不需要保存现有的文件
            self.finishSignal.emit(CANCEL)
            return
        l_audio_base = os.path.basename(l_audio_path)
        if self.g_output_ext == "txt":
            with open(os.path.join(self.g_output_dir, l_audio_base+".txt"), "w", encoding="utf-8") as txt:
                write_txt(result["segments"], txt)
        elif self.g_output_ext == "vtt":
            with open(os.path.join(self.g_output_dir, l_audio_base+".vtt"), "w", encoding="utf-8") as vtt:
                write_vtt(result["segments"], vtt)
        else:
            with open(os.path.join(self.g_output_dir, l_audio_base+".srt"), "w", encoding="utf-8") as srt:
                write_srt(result["segments"], srt)
        self.finishSignal.emit(DONE)

    def signalHandle(self, i_processSignal):
        """
        消息传递，把从whisper内部处理日志发送到 UI 做进度跟踪

        Input:
        ---
            i_processSignal - (str)
                信号传递的 str 格式化日志信息
        """
        self.g_information.append(i_processSignal)
        while len(self.g_information) > MAX_LOG_LENGTH:
            self.g_information.pop(0)
        string = ""
        for i in self.g_information:
            string += i + "\n"
        self.finishSignal.emit(string)

    def close(self, info=None):
        """
        关闭本监控线程，核心是退出run中的transcribe函数调用。
        """
        self.g_cancel_signal[0] = False
        pass

# 功能实现模块
# //////////////////////////////////////////////////////////////

class AutoSubtitleFactory(QWidget):
    """
    配字幕功能实现类
    """
    def __init__(self, widgets):
        super().__init__()
        # TODO 用一个 class 来管理这个类
        self.args = {
            "mode": "audio",
            "audio": None, # 必须指定配字幕文件名
            "model": "tiny", # [tiny, base, small, medium]
            "output_dir": ".", # 输出位置
            "output_ext": "srt", # 输出格式 srt, vtt, txt 三选一
            "verbose": True, # 显示处理进度
            "task": "transcribe", # 还有translate模式
            "language": "zh",
            "temperature": 0, # 采样使用的温度
            "best_of": 5, # 候选采样数，基于一定温度的
            "beam_size": 3, # beam search 采样数，当temperature为0生效
            "patience": None,
            "length_penalty": None,
            "suppress_tokens": "-1",
            "initial_prompt": None,
            "condition_on_previous_text": True,
            "temperature_increment_on_fallback": 0.2,
            "compression_ratio_threshold": 2.4,
            "logprob_threshold": -1.0,
            "no_speech_threshold": 0.6
        }
        absPath, self.g_dict_Cache = readCacheFile()
        if self.g_dict_Cache.get("fileName"):
            widgets.autoTitle_input_Edit.setPlainText(self.g_dict_Cache["fileName"])
            self.args["audio"] = self.g_dict_Cache["fileName"]
        if self.g_dict_Cache.get("OutputDirName"):
            widgets.autoTitle_input2_Edit.setPlainText(self.g_dict_Cache["OutputDirName"])
            self.args["output_dir"] = self.g_dict_Cache["OutputDirName"]
        self.absPath = absPath
        self.widgets = widgets
        self.thread1 = None
    
    def closeThread(self):
        """
        无论上一个任务是否完成，都结束进程并释放资源
        """
        if self.thread1:
            self.thread1.close()
            self.thread1.wait()
            self.thread1.deleteLater()
            self.thread1=None

    def selectFile(self):
        """
        选择一个本地文件
        """
        l_home_dir = self.args.get("output_dir")
        if l_home_dir == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))

        l_fileName = QFileDialog.getOpenFileName(self, "选择文件", l_home_dir)[0]
        if l_fileName == "":
            return
            
        self.args["audio"] = l_fileName
        self.args["output_dir"] = os.path.dirname(l_fileName)
        self.widgets.autoTitle_input2_Edit.setPlainText(self.args.get("output_dir"))
        self.widgets.autoTitle_input_Edit.setPlainText(l_fileName)
        
        if self.widgets.autoTitle_input2_Edit.toPlainText() == "":
            l_home_dir = os.path.dirname(l_fileName)
            self.widgets.autoTitle_input2_Edit.setPlainText(l_home_dir)
            self.args["output_dir"] = l_home_dir
            self.g_dict_Cache["OutputDirName"] = l_home_dir
        self.showCurrentInformation()
        self.g_dict_Cache["fileName"] = l_fileName

    def selectDirectory(self):
        """
        选择字幕文件输出配置
        """
        l_home_dir = self.widgets.autoTitle_input2_Edit.toPlainText()
        if l_home_dir == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
        
        l_fileName = QFileDialog.getExistingDirectory(self, "输出位置", l_home_dir)
        if l_fileName == "":
            return
        
        self.widgets.autoTitle_input2_Edit.setPlainText(l_fileName)
        self.args["output_dir"] = l_fileName
        self.showCurrentInformation()
        self.g_dict_Cache["OutputDirName"] = l_fileName

    def selectLanguage(self):
        """
        选择字幕语言
        """
        self.args["language"] = self.widgets.autoTitle_comboBox.currentText()
        self.showCurrentInformation()

    def selectSubTitleExt(self):
        """
        选择输出字幕格式
        """
        self.args["output_ext"] = self.widgets.autoTitle_comboBox2.currentText()
        self.showCurrentInformation()

    def selectModelSize(self):
        """
        选择模型大小
        """
        self.args["model"] = self.widgets.autoTitle_comboBox_modelSize.currentText()
        self.showCurrentInformation()

    def showCurrentInformation(self):
        """
        展示当前选择的whisper配置
        """
        string = ""
        string += "输入文件 : " + self.args["audio"] + "\n"
        string += "输出位置 : " + self.args["output_dir"] + "\n"
        string += "字幕格式 : " + self.args["output_ext"] + "\n"
        string += "字幕语言 : " + self.args["language"] + "\n"
        string += "选择模型 : " + self.args["model"] + "\n"
        self.updateCommandText(string)

    def runCommand(self):
        """
        创建线程，调用whisper配字幕
        """
        # 先结束之前的进程
        if self.thread1 is not None:
            self.closeThread()
            self.showCurrentInformation()
            self.widgets.autoTitle_run_Btn.setText(START_BTN)
            return
        # 创建新监控进程
        self.thread1 = SubTitleRunner(self.args.copy())
        # 设置新监控进程的数据信息
        self.thread1.finishSignal.connect(self.updateCommandText)
        self.thread1.start()

        # 保存缓存
        saveCacheFile(self.g_dict_Cache)
        self.widgets.autoTitle_run_Btn.setText(END_BTN)

    def updateCommandText(self, i_text=None):
        """
        更新文本框展示参数，给定内容则展示内容，否则展示默认配字幕使用的参数。
        
        Input:
        ---
            i_text - (str)
                需要显示的内容
        """
        string = i_text
        if string == DONE:
            self.closeThread()
            self.widgets.autoTitle_run_Btn.setText(START_BTN)
        self.widgets.autoTitle_output_Edit.setPlainText(string)
