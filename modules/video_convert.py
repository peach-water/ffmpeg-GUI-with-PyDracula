import subprocess
import os
import time
import logging

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QFileDialog
import ffmpeg

from .constants import *
from .utils import commandRunner, readCacheFile, saveCacheFile, getVideoFramsPerSecond, logInitialize, hidenTerminal

# 监控线程模块
# ///////////////////////////////////////////////////////////////

class VideoConvert(QThread):
    """
    创建一个线程开始转码工作
    
    Input:
    ---
        i_batch_Mode - (bool)      
            是否启用批量处理
        i_convert_Command - (dict)
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
                 i_convert_Command:dict=None, 
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
                                encoding="utf-8",
                                startupinfo=hidenTerminal()
                            )
            l_runner = commandRunner(self.thread1, duration=self.duration, progressSignal=self.progressSignal)
            l_info = ""
            logging.debug("执行: " + self.command)
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
                logging.error(l_info)
            elif self.thread1.returncode in [0, None]:
                # 转码成功
                self.finishSignal.emit(DONE)
            else:
                # 其他意料之外的事情，理论上这里不应该会被执行
                self.finishSignal.emit(l_info)
                logging.error(l_info)
            return 

        # 批处理模式
        l_home_dir = self.g_home_Dir
        l_count = 0
        l_unprocessed_file = os.listdir(l_home_dir)

        for lo_file in l_unprocessed_file:
            lo_fileName, lo_fileExt = os.path.splitext(lo_file)
            lo_fileExt = lo_fileExt[1:]
            lo_fileName += self.g_process_Time
            lo_file = os.path.join(l_home_dir, lo_file)
            lo_command = f"ffmpeg -i \"{lo_file}\""
            for i in self.g_convert_Command.keys():
                if i == "-r":
                    # 如果启用了“视频二倍速”功能
                    lo_fps = getVideoFramsPerSecond(lo_file)
                    self.g_convert_Command[i] = str(lo_fps * 2)
                lo_command += " " + i + " " + self.g_convert_Command[i]
            
            lo_command += f" -y \"{os.path.join(self.g_output_Dir, lo_fileName)}.{self.g_output_Ext}\""
            if os.path.exists(f"{os.path.join(self.g_output_Dir, lo_fileName)}.{self.g_output_Ext}"):
                logging.info(f"{lo_file} 存在同名文件但不同后缀文件，转码将保留后者")
            # 创建线程开始转码
            logging.debug("执行: " + lo_command)

            try:
                lo_probe = ffmpeg.probe(lo_file)
            except ffmpeg.Error:
                # 非视频音频跳过
                logging.info(f"{lo_file} 无法识别，跳过")
                continue
            if lo_probe["streams"][0]["codec_type"] == "subtitle":
                # 字幕文件跳过
                logging.info(f"{lo_file} 是字幕文件，跳过")
                continue
            lo_duration = float(lo_probe["format"]["duration"])

            self.thread1 = subprocess.Popen(lo_command,
                                stdout=subprocess.PIPE, 
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=False,
                                universal_newlines=True,
                                encoding="utf-8",
                                startupinfo=hidenTerminal()
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

            l_count += 1
            self.thread1.wait()

        self.finishSignal.emit(DONE)
    
    def close(self):
        """
        关闭实际干事的子进程，这个类本身是一个监控进程。
        """
        if self.thread1 is not None:
            # self.thread1.terminate() # 去掉危险的 terminate 使用。
            self.thread1.kill()
            self.thread1.wait()
            self.thread1 = None
        self.deleteLater()

# 功能实现模块
# /////////////////////////////////////////////////////

class ConvertVideoFactory(QWidget):
    def __init__(self, widgets):
        super().__init__()
        self.absPath, self.g_dict_Cache = readCacheFile()
        self.g_input1_file = "" # 输入的第一个文件位置
        if self.g_dict_Cache.get("fileName"):
            widgets.input_Edit1.setPlainText(self.g_dict_Cache["fileName"])
            self.g_input1_file = self.g_dict_Cache["fileName"] 
        if self.g_dict_Cache.get("OutputDirName"):
            widgets.input_Edit3.setPlainText(self.g_dict_Cache["OutputDirName"])

        self.widgets = widgets
        self.thread1 = None
        # self.widgets.input_Edit3.setPlainText(os.path.join(os.path.expanduser("~"), "Desktop"))
        self.g_convert_Mode = {} # 保存具体的转码指令
        self.g_convert_Mode_Name = "" # 标记转码模式
        self.g_bitrate_Control = "" # 码率控制
        self.g_preset_Mode = "fast" # 转码速率控制
        self.g_file_Ext = "mp4" # 输出格式
        self.g_batch_Mode = False # 是否启用批量处理模式
        # 为了保证生成指令格式的正确性，下面字典的value值需要依据参数实际情况保留空格。
        self.g_dict_Mode = {
                "转码H264": {"-c:v": "h264"}, 
                "转码H265": {"-c:v": "libx265"}, 
                "转MP3": {"-vn":"", "-acodec": "mp3_mf"},
                "提取视频": {"-an":"", "-c:v": "copy"},
                "转GIF": {"-f": "gif"},
                "内挂字幕": {"-c": "copy", "-c:s": "copy"},
                "内嵌字幕": {"-qscale": "0", "-vf \"subtitles=":""},
                "视频两倍速" : {"-r":"0", "-filter:a": "\"atempo=2.0\"", "-filter:v": "\"setpts=0.5*PTS\""}
        }
        logInitialize()

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
            self.g_dict_Cache["fileName"] = l_fileName
            self.g_dict_Cache["OutputDirName"] = l_home_dir
            self.g_input1_file = l_fileName

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
            self.g_convert_Mode_Name = l_item
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
        self.g_input1_file = self.widgets.input_Edit1.toPlainText()
        l_command = f"ffmpeg -i \"{self.g_input1_file}\""
        # 取出文件名
        l_fileName, _ = os.path.splitext(self.g_input1_file) # 去掉文件拓展名
        l_fileName = os.path.basename(l_fileName)

        l_fileName += time.strftime("_%m-%d_%H-%M-%S", time.localtime()) # 生成文件输出名
        # 反馈展示
        # ////////////////////////////////////////////////////////////
        # 指定第二个输入文件
        if self.widgets.input_Edit2.toPlainText() != "":
            # 特别指定非内嵌字幕模式的处理方式
            if self.g_convert_Mode_Name != "内嵌字幕":
                l_command += f" -i \"{self.widgets.input_Edit2.toPlainText()}\""
        # 选择输出位置和输出文件名
        l_home_dir = self.widgets.input_Edit3.toPlainText()
        if l_home_dir == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
        # 控制命令生成
        l_control_command = self.convertCommandGenerate()
        # 通过返回值是否为 dict 类型判断控制指令是否生成出错
        if False in l_control_command.keys():
            self.widgets.output_command_Edit.setPlainText(str(l_control_command.popitem()))
            return
        for i in l_control_command.keys():
            l_command += " " + i + " " + l_control_command.get(i)
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
            l_control_command - (dict)
                根据 self.g_convert_Mode 生成可执行的转码指令
        """
        l_command = {}
        # 检查码率设置
        if self.g_bitrate_Control != "":
            l_command = {"-"+self.g_bitrate_Control:" "+self.widgets.bitrate_Edit.toPlainText()}
        # 出现字幕处理时操作逻辑
        if self.g_convert_Mode_Name in ["内嵌字幕", "内挂字幕"]:
            l_input_Edit2 = self.widgets.input_Edit2.toPlainText()
            # 未指定字幕文件报错
            if l_input_Edit2 == "":
                return {False:"在“输入处理文件 2” 处指定字幕文件"}
            if self.g_convert_Mode_Name == "内嵌字幕":
                self.g_convert_Mode["-vf \"subtitles="] = "\'" + os.path.abspath(l_input_Edit2) + "\'\""
            else: # 内挂字幕处理，新开一条轨道加入字幕
                l_input_info = ffmpeg.probe(self.g_input1_file)
                l_input_tracker_count = len(l_input_info["streams"]) # 统计轨道数量
                if l_input_tracker_count > 2:
                    l_command["-map"] = "0:v -map 0:a -map 0:s -map 1"
                else:
                    l_command["-map"] = "0:v -map 0:a -map 1"
        if self.g_convert_Mode_Name == "视频两倍速" and os.path.isfile(self.g_input1_file):
            l_fps = getVideoFramsPerSecond(self.g_input1_file)
            self.g_convert_Mode["-r"] = str(l_fps * 2)
        # 处理速度和默认覆盖原文件设置
        l_command["-preset"] = self.g_preset_Mode 
        # 剩下的其他固定指令
        for i in self.g_convert_Mode.keys():
            l_command[i] = self.g_convert_Mode[i]
        return l_command

    def runCommand(self):
        """
        新建一个终端运行指令框的命令，如果是批量处理，则创建一个批处理任务较给子函数执行。
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
            # 创建Qthread监控线程执行转码任务
            self.thread1 = VideoConvert()
            self.thread1.command = self.widgets.output_command_Edit.toPlainText()
            l_file = self.widgets.input_Edit1.toPlainText()
            # 检查输入文件是否可以为可识别音频或视频文件
            try:
                l_file_Info = ffmpeg.probe(l_file)["format"]
            except ffmpeg.Error:
                logging.error(f"{l_file} 不可识别")
                self.widgets.btn_command_run.setText(END_BTN)
                return
            if "duration" not in l_file_Info.keys():
                logging.info(f"{l_file} 不是音频或视频")
                return
            self.thread1.duration = float(l_file_Info["duration"])

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
            self.widgets.progressBar.setMaximumHeight(0) # 关闭进度条
            
        self.widgets.output_command_Edit.setPlainText(signal_str)

    def progressBarShow(self, value:int):
        """
        更新进度条的进度

        Input:
        ---
            value - (int)
                更新的数值
        """
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self.widgets.progressBar.setValue(value)
