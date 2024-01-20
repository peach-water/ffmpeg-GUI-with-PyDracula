import subprocess
import os
import time

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QFileDialog
import ffmpeg

from .constants import *
from .utils import commandRunner, readCacheFile, saveCacheFile

# 监控线程模块
# ///////////////////////////////////////////////////////////////

class VideoConvert(QThread):
    """
    创建一个线程开始转码工作
    
    Input:
    ---
        i_batch_Mode - (bool)      
            是否启用批量处理
        i_convert_Command - (str)
            统一的处理命令
        i_home_dir - (str)
            待处理文件位置
        i_output_dir - (str)
            处理完的文件保存位置
        i_output_ext - (str)
            处理成什么格式
        i_process_Time - (str)
            给文件名添加一个额外的信息防止重名（一般是时间信息）
    """
    finishSignal = Signal(str)
    progressSignal = Signal(int)
    def __init__(self, i_batch_Mode=False, 
                 i_convert_Command=None, 
                 i_home_dir=None, 
                 i_output_dir=None, 
                 i_output_ext=None,
                 i_process_Time=None
                ):
        super(VideoConvert, self).__init__()
        self.command = ""
        self.duration = 0.0
        self.thread1 = None
        # 批处理模式
        self.g_batch_Mode = i_batch_Mode
        if i_batch_Mode:
            assert i_home_dir is not None
            assert i_output_dir is not None
            assert i_output_ext is not None
            assert i_convert_Command is not None
            self.g_home_Dir = i_home_dir
            self.g_output_Dir = i_output_dir
            self.g_output_Ext = i_output_ext
            self.g_convert_Command = i_convert_Command
            self.g_process_Time = i_process_Time

    def run(self):
        """
        开始转码工作，先检查是否为批处理模式
        """
        if not self.g_batch_Mode:
            self.thread1 = subprocess.Popen(self.command,
                             stdout=subprocess.PIPE, 
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=False, 
                             universal_newlines=True,
                             encoding="utf-8"
                            )
            l_runner = commandRunner(self.thread1, duration=self.duration, progressSignal=self.progressSignal)
            l_info = ""
            for l_info in l_runner:
                self.finishSignal.emit(l_info)
            
            # 检查转码结果
            if self.thread1 is None:
                # 任务取消
                self.finishSignal.emit(CANCEL)
            elif self.thread1.returncode not in [0, None]:
                # 转码出错
                self.finishSignal.emit("Error:\t" + l_info.split("\n")[-2])
                # 在终端打印错误信息
                print(l_info)
            elif self.thread1.returncode in [0, None]:
                # 转码成功
                self.finishSignal.emit(DONE)
            else:
                # 其他意料之外的事情，理论上这里不应该会被执行
                self.finishSignal.emit(l_info)
                print("videoconvert class 不应该执行到这里")
            return 

        # 批处理模式
        l_home_dir = self.g_home_Dir
        l_count = 0
        l_unprocessed_file = os.listdir(l_home_dir)
        l_process_failure_file = [] # 记录下转码执行失败的信息和对应的文件信息
        for lo_file in l_unprocessed_file:
            lo_fileExt = lo_file.split(".")[-1]
            lo_fileName = lo_file[:-len(lo_fileExt)-1] + self.g_process_Time
            lo_file = os.path.join(l_home_dir, lo_file)
            lo_command = f"ffmpeg -i \"{lo_file}\" {self.g_convert_Command}"
            lo_command += f" \"{os.path.join(self.g_output_Dir, lo_fileName)}.{self.g_output_Ext}\""
            # 创建线程开始转码
            lo_duration = float(ffmpeg.probe(lo_file)["format"]["duration"])
            self.thread1 = subprocess.Popen(lo_command,
                             stdout=subprocess.PIPE, 
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=False,
                             universal_newlines=True,
                             encoding="utf-8"
                            )
            l_runner = commandRunner(self.thread1, duration=lo_duration, progressSignal=self.progressSignal)
            lo_info = ""
            for lo_info in l_runner:
                lo_info += "处理进度 %4d/%4d" % (l_count+1, len(l_unprocessed_file))
                self.finishSignal.emit(lo_info)
            if self.thread1 is None:
                # 表示任务已经取消
                self.finishSignal.emit(CANCEL)
                return
            elif self.thread1.returncode not in [0, None]:
                l_process_failure_file.append(lo_file + "\t:\t" + lo_file.split("\n")[-2])
            l_count += 1
            self.thread1.wait()
        # 如果有错误信息则展示错误信息
        if l_process_failure_file.__len__() != 0:
            l_err_info = ""
            for i in l_process_failure_file:
                l_err_info += i + "\n"
            self.finishSignal.emit(l_err_info)
            return
        self.finishSignal.emit(DONE)
    
    def close(self):
        """
        关闭实际干事的子进程，这个类本身是一个监控进程。
        """
        if self.thread1 is not None:
            self.thread1.terminate()
            self.thread1.wait()
            self.thread1 = None
        self.deleteLater()

# 功能实现模块
# /////////////////////////////////////////////////////

class ConvertVideoFactory(QWidget):
    def __init__(self, widgets):
        super().__init__()
        self.absPath, self.g_dict_Cache = readCacheFile()
        if self.g_dict_Cache.get("fileName"):
            widgets.input_Edit1.setPlainText(self.g_dict_Cache["fileName"])
        if self.g_dict_Cache.get("OutputDirName"):
            widgets.input_Edit3.setPlainText(self.g_dict_Cache["OutputDirName"])

        self.widgets = widgets
        self.thread1 = None
        # self.widgets.input_Edit3.setPlainText(os.path.join(os.path.expanduser("~"), "Desktop"))
        self.g_convert_Mode = {}
        self.g_bitrate_Control = ""
        self.g_preset_Mode = "fast"
        self.g_file_Ext = "mp4"
        self.g_batch_Mode = False # 是否启用批量处理模式
        # 为了保证生成指令格式的正确性，下面字典的value值需要依据参数实际情况保留空格。
        self.g_dict_Mode = {
                "转码H264": {"-c:v": " h264"}, 
                "转码H265": {"-c:v": " libx265"}, 
                "转MP3": {"-vn":" ", "-f": " mp3"},
                "提取视频":{"-an":" ", "-c:v": " copy"},
                "转GIF": {"-f": " gif"},
                "内挂字幕": {"-c": " copy", "-c:s": " copy"},
                "内嵌字幕": {"-qscale": " 0", "-vf \"subtitles=":""},
                "视频两倍速" : {"-r":" 120", "-filter:a": " \"atempo=2.0\"", "-filter:v": " \"setpts=0.5*PTS\""}
        }

    def closeThread(self):
        """
        无论之前的任务是否完成，都退出并释放资源
        """
        if self.thread1:
            self.thread1.close()
            self.thread1.wait()
            self.thread1.deleteLater()
            self.thread1 = None


    def selectFile(self, btn_Name):
        """
        选择一个本地文件，因为两个选择文件按钮都是采用同一个处理逻辑，需要区分是哪个按钮
        
        Input:
        ---
            btn_Name - (str)
                按钮名字，用来区分不同的按钮
        """
        l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
        if btn_Name == "btn_input1":
            # 输入框有上次留下的内容，就沿用
            if self.widgets.input_Edit1.toPlainText() != "":
                l_home_dir = self.widgets.input_Edit1.toPlainText()
            l_fileName = QFileDialog.getOpenFileName(self, "选择文件", l_home_dir)[0]
    
            if l_fileName != "":
                self.widgets.input_Edit1.setPlainText(l_fileName)
                l_home_dir = os.path.dirname(l_fileName)
                self.widgets.input_Edit3.setPlainText(str(l_home_dir))
        elif btn_Name == "btn_input2":
            if self.widgets.input_Edit3.toPlainText() != "":
                l_home_dir = self.widgets.input_Edit3.toPlainText()
            l_fileName = QFileDialog.getOpenFileName(self, "选择文件", l_home_dir)[0]
            if l_fileName != "":
                self.widgets.input_Edit2.setPlainText(l_fileName)
        self.updateCommandText()
        # 更新缓存
        if l_fileName != "":
            self.g_dict_Cache["fileName"] = os.path.dirname(l_fileName)
            self.g_dict_Cache["OutputDirName"] = l_home_dir

    def selectDirectory(self, i_btn_Name):
        """
        选择输出文件夹位置

        Input:
        ---
            i_btn_Name - (str)
                按下按钮的名字
        """
        if self.widgets.input_Edit3.toPlainText() == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
        else:
            l_home_dir = self.widgets.input_Edit3.toPlainText()

        l_fileName = QFileDialog.getExistingDirectory(self, "输出位置", l_home_dir)
        if l_fileName != "":
            # 更新缓存
            self.g_dict_Cache["OutputDirName"] = l_fileName
            
            if i_btn_Name == "btn_input3":
                # 单文件处理模式
                self.widgets.input_Edit3.setPlainText(l_fileName)
            elif i_btn_Name == "btn_input1":
                # 批处理模式
                self.widgets.input_Edit1.setPlainText(l_fileName)
                self.widgets.input_Edit3.setPlainText(os.path.abspath(os.path.join(l_fileName, "..")))
        # 更新一下文本框展示的预览指令
        self.updateCommandText()

    def selectMode(self, mode, listBoxIndex):
        """
        确定选择使用的预设
        
        Input:
        ---
            mode - (str)
                选择的选项
            listBoxIndex - (str)
                传入激活的是哪个选项框
        """
        l_item = mode
        if listBoxIndex == "modeBox":
            self.g_convert_Mode = self.g_dict_Mode.get(l_item)
            if self.g_convert_Mode is None:
                self.g_convert_Mode = {}
            elif l_item == "转MP3":
                # 禁用输出格式
                self.widgets.list_video_type.setEnabled(False)
                self.g_file_Ext = "mp3"
            elif l_item == "转GIF":
                self.widgets.list_video_type.setEnabled(False)
                self.g_file_Ext = "gif"
            elif l_item == "内挂字幕":
                self.widgets.list_video_type.setEnabled(False)
                self.g_file_Ext = "mkv"
            else:
                self.widgets.list_video_type.setEnabled(True)
                self.g_file_Ext = "mp4"
        elif listBoxIndex == "typeBox":
            self.g_file_Ext = l_item
        # 最后更新一下预览命令框里面的命令
        self.updateCommandText()

    def selectPresetMode(self):
        """
        控制转码速度的滑块，设置不同挡位显示的内容
        """
        l_mode_dict = {0: "placebo", 1: "veryslow", 2: "slower", 3: "slow", 4: "medium",
                        5: "fast", 6:"faster", 7:"veryfast", 8: "superfast", 9: "ultrafast"}
        self.g_preset_Mode = l_mode_dict.get(self.widgets.perset_set_Slider.value())

        self.updateCommandText()

    def selectBitrateMode(self):
        """
        码率控制模块，具体码率不做限制，之间采用用户输入作为码率参数
        """
        if self.widgets.bitrate_mode_Combo.currentText() != "无":
            self.g_bitrate_Control = self.widgets.bitrate_mode_Combo.currentText()
        else:
            self.g_bitrate_Control = ""
        self.updateCommandText()

    def selectBatchProcessMode(self):
        """
        控制是否启用批处理模式，批量转码文件
        """
        self.g_batch_Mode = self.widgets.batch_mode_Check.isChecked()
        if self.g_batch_Mode:
            self.widgets.btn_input1.setText("选择文件夹")
            self.widgets.btn_input1.clicked.disconnect()
            self.widgets.btn_input1.clicked.connect(lambda: self.selectDirectory("btn_input1"))
        else:
            self.widgets.btn_input1.setText("选择文件")
            self.widgets.btn_input1.clicked.disconnect()
            self.widgets.btn_input1.clicked.connect(lambda: self.selectFile("btn_input1"))
        return 
        
    def updateCommandText(self):
        """
        更新命令框显示的内容，预览命令
        """
        if self.widgets.input_Edit1.toPlainText() == "":
            self.widgets.output_command_Edit.setPlainText("指定输入文件")
            return
        l_command = f"ffmpeg -i \"{self.widgets.input_Edit1.toPlainText()}\""
        # 取出文件名
        l_fileName, _ = os.path.splitext(self.widgets.input_Edit1.toPlainText()) # 去掉文件拓展名
        l_fileName = os.path.basename(l_fileName)

        l_fileName += time.strftime("_%m-%d_%H-%M-%S", time.localtime()) # 生成文件输出名
        # 反馈展示
        # ////////////////////////////////////////////////////////////
        # 指定第二个输入文件
        if self.widgets.input_Edit2.toPlainText() != "":
            # 特别指定非内嵌字幕模式的处理方式
            if self.g_convert_Mode.get("-vf \"subtitles=") is None:
                l_command += f" -i \"{self.widgets.input_Edit2.toPlainText()}\""
        # 选择输出位置和输出文件名
        l_home_dir = self.widgets.input_Edit3.toPlainText()
        if l_home_dir == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
        # 控制命令生成
        l_control_command = self.convertCommandGenerate()
        if type(l_control_command) == dict:
            self.widgets.output_command_Edit.setPlainText(l_control_command[1])
            return
        l_command += l_control_command
        # 指定输出文件
        l_command += f" -y \"{l_home_dir}/{l_fileName}.{self.g_file_Ext}\""
        # 在指令文本框展示命令
        self.widgets.output_command_Edit.setPlainText(l_command)

    def convertCommandGenerate(self):
        """
        生成转码命令，指不包括输入输出以外的转码命令

        Input:
        ---
            None

        Output:
        ---
            l_control_command - (str)
                根据 self.g_convert_Mode 生成可执行的转码指令
        """
        l_command = {}
        # 检查码率设置
        if self.g_bitrate_Control != "":
            l_command = {"-"+self.g_bitrate_Control:" "+self.widgets.bitrate_Edit.toPlainText()}
        # 出现内嵌字幕时处理方法
        if self.g_convert_Mode == self.g_dict_Mode.get("内嵌字幕"):
            l_input_Edit2 = self.widgets.input_Edit2.toPlainText()
            # 未指定字幕文件报错
            if l_input_Edit2 == "":
                l_command = {1:"在输入处理文件2处指定字幕文件"}
                return l_command
            self.g_convert_Mode["-vf \"subtitles="] = "\'" + l_input_Edit2.replace(":","\\:") + "\'\""
        # 最后是处理速度和默认覆盖原文件
        l_command["-preset"] = " "+self.g_preset_Mode 
        # 剩下的其他固定指令
        for i in self.g_convert_Mode.keys():
            l_command[i] = self.g_convert_Mode[i]
        l_control_command = ""
        for i in l_command.keys():
            l_control_command += " " + i + l_command[i]
        return l_control_command

    def runCommand(self):
        """
        新建一个终端运行指令框的命令，如果是批量处理
        """
        # 先终止前面未运行完的任务，然后恢复先前的指令
        if self.thread1:
            self.closeThread()
            self.widgets.btn_command_run.setText(START_BTN)
            self.widgets.progressBar.setMaximumHeight(0) # 关闭进度条
            self.updateCommandText()
            return
        # 单个文件处理
        if not self.g_batch_Mode:
            # 没有指令就不执行任务
            if self.widgets.output_command_Edit.toPlainText() in ["", CANCEL, DONE]:
                return
            self.thread1 = VideoConvert()
            self.thread1.command = self.widgets.output_command_Edit.toPlainText()
            # 创建Qthread监控线程执行转码任务
            try:
                self.thread1.duration = float(ffmpeg.probe(self.widgets.input_Edit1.toPlainText())["format"]["duration"])
            except ffmpeg._run.Error as e:
                print("ERROR:\t" + str(e))
                self.widgets.btn_command_run.setText(END_BTN)
                return

        else:
            l_output_Dir = self.widgets.input_Edit3.toPlainText()
            l_home_Dir = self.widgets.input_Edit1.toPlainText()
            if l_output_Dir == "":
                l_output_Dir = os.path.abspath(os.path.join(self.absPath, ".."))
            # 生成统一的转码指令
            l_convert_Command = self.convertCommandGenerate()
            # 创建Qthread监控线程执行转码任务
            self.thread1 = VideoConvert(True, 
                                        i_convert_Command=l_convert_Command,
                                        i_home_dir=l_home_Dir,
                                        i_output_dir=l_output_Dir,
                                        i_output_ext=self.g_file_Ext,
                                        i_process_Time=time.strftime("_%m-%d_%H-%M-%S", time.localtime())
                                        )
        # 启动线程
        self.thread1.finishSignal.connect(self.runCommandTextShow)
        self.thread1.progressSignal.connect(self.progressBarShow)
        self.thread1.start()
        self.widgets.btn_command_run.setText(END_BTN)
        self.widgets.progressBar.setMaximumHeight(120) # 打开进度条
        # 保存本次运行的路径，方便下次快速使用
        saveCacheFile(self.g_dict_Cache)
    
    def runCommandTextShow(self, signal_str:str):
        """
        在命令框展示运行结果
        
        Input:
        ---
            stgnal_str - (str)
                需要展示的信息
        """
        if signal_str == DONE:
            self.closeThread()
            self.widgets.btn_command_run.setText(START_BTN)
            
        self.widgets.output_command_Edit.setPlainText(signal_str)

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
        self.widgets.progressBar.setValue(value)
