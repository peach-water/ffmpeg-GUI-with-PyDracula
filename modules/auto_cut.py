import os
import subprocess

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QFileDialog
import ffmpeg

from .constants import *
from .vad_functions import format_timestamp
from .utils import commandRunner, saveCacheFile, readCacheFile

# 监控线程模块
# ///////////////////////////////////////////////////////////////

class VADRunner(QThread):
    """
    实现视频的自动分割，并获得处理好的结果
    """
    processSignal = Signal(int) # 传递预处理进度信息
    finishSignal = Signal(str)
    def __init__(self, i_file:str=None, i_output_dir:str=None, parent=None):
        super(VADRunner, self).__init__(parent)
        if i_file is None:
            raise RuntimeError(f"No file input")
        self.g_file = i_file
        if i_output_dir is None:
            raise RuntimeError(f"no output diectory")
        self.g_output_dir = i_output_dir
        self.thread1 = None
        self.g_cancel_signal = [True] # 用来结束get_transcribe_timestamps函数调用，取消任务。使用list数据类型可以保证参数引用而不是值引用。TODO需要更高级的实现方式。

    def run(self):
        """
        利用模型得到分割时间戳
        """
        from . vad_functions import get_transcribe_timestamps, get_audio_duration
        
        try:
            result = get_transcribe_timestamps(
                audio=self.g_file,
                start_time=0,
                end_time=get_audio_duration(self.g_file),
                progress_tracking_callback=self.processSignal,
                cancel=self.g_cancel_signal
            )
        except ffmpeg._run.Error as e:
            self.finishSignal.emit(str(e) + "\tmaybe no vaild input file")
        if not self.g_cancel_signal[0]:
            self.finishSignal.emit(CANCEL)
            return
        self.autoCutVideo(result)

    def autoCutVideo(self, slice_dict: list):  
        """
        根据模型划分的时间节点，循环创建剪辑指令交给子进程执行

        Input:
            slice_dict - (list(dict))
                list 形式存放 {"start":float,"end":float} 的分割片段
        
        Output:
        ---
            None
        """      
        l_fileHome = self.g_file
        l_fileName, l_fileExt = os.path.splitext(self.g_file)
        l_fileName = os.path.basename(l_fileName)
        l_fileExt = l_fileExt[1:] # os的splitExt会带有 "." 需要去掉
        l_fileHome = os.path.dirname(self.g_file)

        for i, timestamp in enumerate(slice_dict):
            if not self.g_cancel_signal[0]:
                break
            # 这里在生成分割视频的指令
            start = format_timestamp(timestamp["start"], True, ".")
            end = format_timestamp(timestamp["end"], True, ".")
            lo_command = f"ffmpeg -i \"{l_fileHome}/{l_fileName}.{l_fileExt}\""
            lo_command += f" -ss {start} -to {end}"
            start = start.replace(":","-")[:-4]
            end = end.replace(":","-")[:-4]
            lo_command += f" -y \"{self.g_output_dir}/{l_fileName}_{start}_{end}.{l_fileExt}\""
            # print(lo_command)
            self.thread1 = subprocess.Popen(lo_command,
                            stdout=subprocess.PIPE, 
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=False, 
                            universal_newlines=True,
                            encoding="utf-8"
                        )
            l_runner = commandRunner(self.thread1, buffer=MAX_LOG_LENGTH, progressSignal=self.processSignal)

            for res in l_runner:
                res += "处理进度 %4d/%4d" % (i+1, len(slice_dict))
                self.finishSignal.emit(res)

        self.finishSignal.emit(DONE)
    
    def close(self):
        """
        实际是关闭干事的子进程，这个类本身是一个监控进程。
        """
        self.g_cancel_signal[0] = False
        if self.thread1 is not None:
            self.thread1.terminate()
            self.thread1.wait()
            self.thread1 = None
        self.finishSignal.emit(CANCEL)
        pass

# 功能实现模块
# //////////////////////////////////////////////////////////////
    
class AutoCutFactory(QWidget):
    def __init__(self, widgets) -> None:
        super().__init__()
        self.absPath, self.g_dict_Cache = readCacheFile()
        if self.g_dict_Cache["fileName"]:
            widgets.autoCut_input_Edit.setPlainText(self.g_dict_Cache["fileName"])
        if self.g_dict_Cache["OutputDirName"]:
            widgets.autoCut_input2_Edit.setPlainText(self.g_dict_Cache["OutputDirName"])
        self.widgets = widgets
        self.thread1 = None # 调用VAD模型标记音频文件

    def closeThread(self):
        """
        无论上一个任务是否完成都结束进程并释放资源
        """
        if self.thread1 is not None:
            self.thread1.close()
            self.thread1.wait()
            self.thread1.deleteLater()
            self.thread1 = None

    def selectFile(self, btn_Name: str=None):
        """
        选择一个文件

        Input:
            btn_Name - (str)
                标记按下的按钮名称，目前未使用
        """
        l_home_dir = self.widgets.autoCut_input_Edit.toPlainText()
        if l_home_dir == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
        l_fileName = QFileDialog.getOpenFileName(self, "选择文件", l_home_dir)[0]

        if l_fileName == "":
            return
        self.widgets.autoCut_input_Edit.setPlainText(l_fileName)
        self.g_dict_Cache["fileName"] = l_fileName
        l_fileName = os.path.dirname(l_fileName)
        self.widgets.autoCut_input2_Edit.setPlainText(l_fileName)
    
    def selectDirectory(self):
        """
        选择输出位置
        """
        l_home_dir = self.widgets.autoCut_input2_Edit.toPlainText()
        if l_home_dir == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))

        l_home_dir = QFileDialog.getExistingDirectory(self, "输出位置", l_home_dir)
        if l_home_dir == "":
            return
        self.widgets.autoCut_input2_Edit.setPlainText(l_home_dir)
        self.g_dict_Cache["OutputDirName"] = l_home_dir

    def runCommand(self):
        """
        创建线程，调用VAD开始分割视频
        """
        if self.thread1 is not None:
            self.closeThread()
            self.widgets.autoCut_run_Btn.setText(START_BTN)
            self.updateCommandText()
            self.widgets.autoCut_progressBar.setMaximumHeight(0)
            return
        l_home_dir = self.widgets.autoCut_input_Edit.toPlainText()
        l_output_dir = self.widgets.autoCut_input2_Edit.toPlainText()
        # 创建一个新的监控进程对象
        self.thread1 = VADRunner(l_home_dir, l_output_dir)
        self.thread1.processSignal.connect(self.progressBarShow)
        self.widgets.autoCut_progressBar.setMaximumHeight(120)
        self.thread1.finishSignal.connect(self.runCommandTextShow)
        
        self.thread1.start()
        self.widgets.autoCut_run_Btn.setText(END_BTN)
    
        # 保存缓存
        saveCacheFile(self.g_dict_Cache)

    def updateCommandText(self):
        """
        更新界面，提高交互性
        """
        return

    def runCommandTextShow(self, str_signal:str):
        """
        在文本框展示程序运行进度和运行结果

        Input:
        ---
            str_signal - (str)
                需要展示的信息
        """
        string = str_signal
        if string == DONE:
            self.closeThread()
            self.widgets.autoCut_run_Btn.setText(START_BTN)
        self.widgets.autoCut_output_Edit.setPlainText(string)

    def progressBarShow(self, value:int):
        """
        更新进度条的进度

        Input:
        ---
            value - (int)
                更新的数值
        """
        if value < 0 or value > 100 :
            return
        self.widgets.autoCut_progressBar.setValue(value)
