import time
import psutil
import os
import sys
import subprocess
from PySide6.QtCharts import QLineSeries, QChart, QDateTimeAxis, QValueAxis
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .vad_functions import format_timestamp

from .whisper.transcribe import transcribe
from .whisper.model import load_model
from .whisper.utils import write_srt, write_txt, write_vtt
import numpy as np
import json
import re, ffmpeg

DONE = "done" # 表示任务完成
CANCEL = "cancel" # 表示任务被取消

# 监控线程模块
# ///////////////////////////////////////////////////////////////
class CPUInfoCapture(QThread):
    """
    实现CPU和内存占用信息的获取并发送给主进程
    """
    # 自定义信号申明
    finishSignal = Signal(str)

    def __init__(self, parent=None):
        super(CPUInfoCapture, self).__init__(parent)
        self.stop_statu = False

    def run(self):
        while not self.stop_statu:
            cpu_percent = psutil.cpu_percent(interval=1)
            virtual_memory = psutil.virtual_memory()
            memory_percent = virtual_memory.percent
            
            self.finishSignal.emit(f"{cpu_percent}, {memory_percent}\n")

class VideoConvert(QThread):
    """
    创建一个线程开始转码工作
    ---
    输入:
        * i_batch_Mode:       是否启用批量处理
        * i_convert_Command:  统一的处理命令（这一批做什么）
        * i_home_dir:         待处理文件位置
        * i_output_dir:       处理完的文件保存位置
        * i_output_ext:       处理成什么格式
        * i_process_Time:     给文件名添加一个额外的信息防止重名（一般是时间信息）
    """
    finishSignal = Signal(str)
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

        if not self.g_batch_Mode:
            self.thread1 = subprocess.Popen(self.command,
                             stdout=subprocess.PIPE, 
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=False, 
                             universal_newlines=True,
                             encoding="utf-8"
                            )
            l_runner = commandRunner(self.thread1, duration=self.duration)
            l_info = ""
            for l_info in l_runner:
                self.finishSignal.emit(l_info)
            
            # 检查转码结果
            if self.thread1 is None:
                # 任务取消
                self.finishSignal.emit(CANCEL)
            elif self.thread1.returncode != 0:
                # 转码出错
                self.finishSignal.emit("Error:\t" + l_info.split("\n")[-2])
                # 在终端打印错误信息
                print(l_info)
            else:
                # 转码成功
                self.finishSignal.emit(DONE)
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
            l_runner = commandRunner(self.thread1, duration=lo_duration)
            lo_info = ""
            for lo_info in l_runner:
                lo_info += "处理进度 %4d/%4d" % (l_count+1, len(l_unprocessed_file))
                self.finishSignal.emit(lo_info)
            if self.thread1 is None:
                # 表示任务已经取消
                self.finishSignal.emit(CANCEL)
                return
            elif self.thread1.returncode != 0:
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
        实际上是关闭创建的干事的子进程，这个类本身是一个监控进程。
        """
        if self.thread1 is not None:
            self.thread1.terminate()
            self.thread1.wait()
            self.thread1 = None
        self.exit(0)

def formatTimeToSecond(time: str) -> float:
    """
    格式化时间 hh:mm:ss.mm 转持续时间。

    输入：
        time:       字符串，格式化的时间
    输出:
        seconds:    浮点数，返回time对应的秒数
    """
    time = time.split(":")
    h = int(time[0])
    m = int(time[1])
    time = time[-1].split(".")
    s = int(time[0])
    ms = int(time[1])
    seconds = (h*60*60) + (m * 60) + s + (ms/100)
    return seconds

def commandRunner(p, duration=None, buffer=4):       
        lines = []
        for line in p.stderr:
            lines.append(line)            
            if len(lines) > buffer:
                lines.pop(0)
            string = ""
            for i in lines:
                string += i
            time = re.search(r"\stime=(?P<time>\S+)", line)
            if time and duration:
                line = line[time.start():time.end()].split("=")
                percent = formatTimeToSecond(line[-1])/duration
                string += f"\n处理进度：{round(percent*100, ndigits=2)}%\t"
            yield string
        # 老方法
        # l_buffer = p.stdout.read(128)
        # l_buffer_str = ""

        # while l_buffer:
        #     l_buffer = l_buffer.decode("utf-8", "ignore").strip()
        #     l_buffer_str += l_buffer
        #     temp = l_buffer_str.replace("\n", "").split("\r")

        #     for i in range(len(temp)-1):
        #         # if temp[i].find("frame") == -1:
        #         #     continue
        #         lines.append(temp[i] + "\n")
        #     while len(lines) > buffer:
        #         lines.pop(0)
        #     string = ""
        #     for i in lines:
        #         string += i
        #     yield string
        #     l_buffer_str = temp[-1]
        #     l_buffer = p.stdout.read(128)

class VADRunner(QThread):
    """
    实现视频的自动分割，并获得处理好的结果
    """
    processSignal = Signal(str) # 传递预处理进度信息
    finishSignal = Signal(str)
    def __init__(self, i_file:str=None, i_output_dir:str=None, parent=None):
        super(VADRunner, self).__init__(parent)
        if i_file is None:
            raise ValueError(f"No file input")
        self.g_file = i_file
        if i_output_dir is None:
            raise ValueError(f"no output diectory")
        self.g_output_dir = i_output_dir
        self.thread1 = None
        
    def run(self):
        """
        利用模型得到分割时间戳
        """
        from . vad_functions import get_transcribe_timestamps, get_audio_duration
        
        result = get_transcribe_timestamps(
            audio=self.g_file,
            start_time=0,
            end_time=get_audio_duration(self.g_file),
            progress_tracking_callback=self.processSignal
        )
        self.autoCutVideo(result)

    def autoCutVideo(self, dict_signal: list):  
        """
        根据模型划分的时间节点，循环创建剪辑指令交给子进程执行
        """      
        l_fileHome = self.g_file
        l_fileName, l_fileExt = os.path.splitext(self.g_file)
        l_fileName = os.path.basename(l_fileName)
        l_fileExt = l_fileExt[1:] # os的splitExt会带有 "." 需要去掉
        l_fileHome = os.path.dirname(self.g_file)

        for i, timestamp in enumerate(dict_signal):
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
            l_runner = commandRunner(self.thread1, buffer=8)

            for res in l_runner:
                res += "处理进度 %4d/%4d" % (i+1, len(dict_signal))
                self.finishSignal.emit(res)
            self.thread1.wait()

        self.close()
        self.finishSignal.emit(DONE)
    
    def close(self):
        """
        实际上是关闭创建的干事的子进程，这个类本身是一个监控进程。
        """
        if self.thread1 is not None:
            self.thread1.terminate()
            self.thread1.wait()
            self.thread1 = None
        self.terminate()

class SubTitleRunner(QThread):
    """
    调用Whisper配字幕
    """
    processSignal = Signal(str)
    finishSignal = Signal(str)
    def __init__(self, args: dict, parent=None):
        super(SubTitleRunner, self).__init__(parent)
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
        l_audio_path = self.args.pop("audio")
        result = transcribe(
            model=self.g_model,
            audio=l_audio_path,
            temperature=self.g_temperature,
            signal_return=self.processSignal,
            cancel=self.g_cancel_signal,
            **self.args
        )
        if not self.g_cancel_signal[0]:
            # 任务取消，就不需要保存现有的文件
            self.finishSignal.emit("任务取消")
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
        self.g_information.append(i_processSignal)
        while len(self.g_information) > 8:
            self.g_information.pop(0)
        string = ""
        for i in self.g_information:
            string += i + "\n"
        self.finishSignal.emit(string)

    def close(self):
        """
        关闭本监控线程，核心是关闭run中的transcribe函数调用。
        """
        self.g_cancel_signal[0] = False
        pass
        
# 功能实现模块
# //////////////////////////////////////////////////////////////

def readCacheFile():
    """
    读取文件所在绝对路径，读取上次操作缓存文件
    输入：

    输出：
    l_absPath:      文件绝对路径，str格式
    l_FileName:     缓存文件，dict格式
    """
    l_absPath = os.path.dirname(os.path.abspath(__file__))
    l_fileName = {}
    if os.path.exists(os.path.join(l_absPath, "..", "config.json")):
        with open(os.path.join(l_absPath, "..", "config.json"), "r") as f:
            l_fileName = json.load(f)
    return l_absPath, l_fileName

class CPUInfoCaptureFactory():
    def __init__(self, graphicsView):
        super().__init__()
        # 初始化一些变量
        assert graphicsView is not None
        self.graphicsView = graphicsView
        self.seriesS = QLineSeries()
        self.seriesL = QLineSeries()
        self.chart = QChart()
        self.initChart()

        self.thread1 = None
        # 自动开始记录
        self.startDataDisplay()

    def initChart(self):
        """
        初始化图像数据
        """
        # 设置曲线名字
        self.seriesS.setName("CPU")
        self.seriesL.setName("RAM")
        self.seriesMaxSize = 60
        self.chart.setTitle("设备资源图")
        self.chart.addSeries(self.seriesS)
        self.chart.addSeries(self.seriesL)
        # 设置坐标轴
        self.axisX = QDateTimeAxis()
        self.axisY = QValueAxis()
        # 设置显示范围
        self.axisX.setRange(QDateTime.currentDateTime().addSecs(-60), QDateTime.currentDateTime())
        self.axisX.setReverse(False)
        self.axisY.setMin(0)
        self.axisY.setMax(100)
        # 设置刻度
        self.axisX.setTickCount(11)
        self.axisY.setTickCount(11)
        # 设置显示名字
        self.axisX.setTitleText("时间(s)")
        self.axisX.setFormat("hh:mm:ss")
        self.axisY.setTitleText("占用率(%)")
        # 设置网格显示，为灰色
        self.axisX.setGridLineVisible(True)
        self.axisX.setGridLineColor(Qt.gray)
        self.axisY.setGridLineVisible(True)
        self.axisY.setGridLineColor(Qt.gray)
        # 添加坐标轴
        self.chart.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        # 绑定坐标，否则不会显示
        self.seriesL.attachAxis(self.axisX)
        self.seriesL.attachAxis(self.axisY)
        self.seriesS.attachAxis(self.axisX)
        self.seriesS.attachAxis(self.axisY)

        self.graphicsView.setChart(self.chart)

    def closeThread(self):
        self.clearDataDisplay()

    def startDataDisplay(self):
        """
        启动线程检测CPU和内存信息
        """
        # 开始监听记录信号
        if self.thread1 is not None:
            return
        self.thread1 = CPUInfoCapture()
        # 线程thread的信号和UI主线程中的槽函数data_display进行连接
        self.thread1.finishSignal.connect(self.dataDisplay)
        self.thread1.start()
    def clearDataDisplay(self):
        """
        清除已经记录的数据
        """
        # 终止线程
        if self.thread1 is None:
            return
        setattr(self.thread1,"stop_statu", True)
        self.thread1.wait()
        self.thread1.deleteLater()
        self.seriesS.clear()
        self.seriesL.clear()
        self.thread1 = None

    def dataDisplay(self, str_signal):
        """
        展示电脑CPU和内存信息
        :return:
        """
        # 读取数据并展示
        data = str_signal.replace("\n","").split(",")
        col = float(QDateTime.currentDateTime().toMSecsSinceEpoch())
        if self.seriesL.count() > self.seriesMaxSize:
            self.seriesL.remove(0)
            self.seriesS.remove(0)
        # cpu
        cpu = float(data[0])
        # RAM
        memory = float(data[1])
        
        self.seriesS.append(col, cpu)
        self.seriesL.append(col, memory)
        self.axisX.setMin(QDateTime.currentDateTime().addSecs(-60))
        self.axisX.setMax(QDateTime.currentDateTime().addSecs(0))

class OpenFileFactory(QWidget):
    def __init__(self, widgets) -> None:
        super().__init__()
        if getattr(sys, "frozen", False):
            absPath = os.path.dirname(os.path.abspath(sys.executable))
        elif __file__:
            absPath = os.path.dirname(os.path.abspath(__file__))
        self.absPath = absPath
        self.widgets = widgets
        self.pic_path = os.path.abspath(os.path.join(self.absPath, ".."))
        self.pic_path = os.path.join(self.pic_path, "image")
        pass

    def openFile(self):
        """
        打开一个本地文件
        :return:
        """
        home_dir = os.path.abspath(os.path.join(self.absPath, ".."))

        f_name = QFileDialog.getOpenFileName(self, "Open file", home_dir)
        print(f_name)
        
    def switchPicture(self):
        """
        在label标签展示图片，实际未启用。
        :return:
        """
        path = self.pic_path
        lab1 = self.widgets.label
        pic_list = os.listdir(path)

        from random import randint
        
        index = randint(0, len(pic_list))

        pix = QPixmap(os.path.join(path , pic_list[index])).scaled(lab1.size(), aspectMode=Qt.KeepAspectRatio)
        lab1.setPixmap(pix)
        lab1.repaint()

    def openUrl(self):
        """
        打开一个指定网页
        """
        import webbrowser
        webbrowser.open("www.bing.com")
        pass

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
                "内嵌字幕": {"-qscale": " 0", "-vf subtitles=":""},
                "视频两倍速" : {"-r":" 120", "-filter:a": " \"atempo=2.0\"", "-filter:v": " \"setpts=0.5*PTS\""}
        }
        
    def closeThread(self):
        if self.thread1:
            self.thread1.close()
            self.thread1.wait()
            self.thread1.deleteLater()
            self.thread1 = None


    def selectFile(self, btn_Name):
        """
        选择一个本地文件，因为两个选择文件按钮都是采用同一个处理逻辑，需要区分是哪个按钮
        输入:
            btn_Name:       按下的按钮是哪个
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
        self.updateCommandText()

    def selectMode(self, mode, listBoxIndex):
        """
        确定选择使用的预设
        输入：
            mode:           传入选择的内容
            listBoxIndex:   传入激活的是哪个选项卡
        """
        l_item = mode.currentItem().text()
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
        码率控制模块
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
            if self.g_convert_Mode.get("-vf subtitles=") is None:
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
        self.widgets.output_command_Edit.setPlainText(l_command)

    def convertCommandGenerate(self):
        """
        生成转码命令，指不包括输入输出以外的所有命令
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
            self.g_convert_Mode["-vf subtitles="] = f"\"{l_input_Edit2}\""
        # 最后是处理速度和默认覆盖原文件
        l_command["-preset"] = " "+self.g_preset_Mode 
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
            self.widgets.btn_command_run.setText("运行命令")
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
            self.thread1.duration = float(ffmpeg.probe(self.widgets.input_Edit1.toPlainText())["format"]["duration"])

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
        self.thread1.start()
        self.widgets.btn_command_run.setText("取消命令")
        # 保存本次运行的路径，方便下次快速使用
        with open(os.path.join(self.absPath, "..", "config.json"), "w") as f:
            json.dump(self.g_dict_Cache, f, indent=4)
        
    
    def runCommandTextShow(self, signal_str):
        """
        在命令框展示运行结果
        输入: 
            stgnal_str:     需要展示的信息
        """
        if signal_str == DONE or signal_str == CANCEL:
            self.closeThread()
            self.widgets.btn_command_run.setText("运行命令")
            
        self.widgets.output_command_Edit.setPlainText(signal_str)

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
        if self.thread1 is not None:
            self.thread1.close()
            self.thread1.wait()
            self.thread1.deleteLater()
            self.thread1 = None

    def selectFile(self, btn_Name: str=None):
        """
        选择一个文件
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
            self.widgets.autoCut_run_Btn.setText("运行命令")
            self.updateCommandText()
            return
        l_home_dir = self.widgets.autoCut_input_Edit.toPlainText()
        l_output_dir = self.widgets.autoCut_input2_Edit.toPlainText()
        # 创建一个新的监控进程对象
        self.thread1 = VADRunner(l_home_dir, l_output_dir)
        self.thread1.processSignal.connect(self.runCommandTextShow)
        self.thread1.finishSignal.connect(self.runCommandTextShow)
        
        self.thread1.start()
    
        # 保存缓存
        with open(os.path.join(self.absPath, "..", "config.json"), "w") as f:
            json.dump(self.g_dict_Cache, f, indent=4)
        self.widgets.autoCut_run_Btn.setText("取消命令")

    def updateCommandText(self):
        """
        更新界面，提高交互性
        """
        return

    def runCommandTextShow(self, str_signal):
        """
        在文本框展示程序运行进度和运行结果
        """
        self.widgets.autoCut_output_Edit.setPlainText(str_signal)

class AutoSubtitleFactory(QWidget):
    """
    配字幕功能实现类
    """
    def __init__(self, widgets):
        super().__init__()
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
        if self.thread1:
            self.thread1.close()
            self.thread1.wait()
            self.thread1.deleteLater()
            self.thread1=None

    def selectFile(self):
        """
        选择一个本地文件
        """
        l_home_dir = self.widgets.autoTitle_input_Edit.toPlainText()
        if l_home_dir == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))

        l_fileName = QFileDialog.getOpenFileName(self, "选择文件", l_home_dir)[0]
        if l_fileName == "":
            return
            
        self.args["audio"] = l_fileName
        self.widgets.autoTitle_input_Edit.setPlainText(l_fileName)
        
        if self.widgets.autoTitle_input2_Edit.toPlainText() == "":
            l_home_dir = os.path.dirname(l_fileName)
            self.widgets.autoTitle_input2_Edit.setPlainText(l_home_dir)
            self.args["output_dir"] = l_home_dir
            self.g_dict_Cache["OutputDirName"] = l_home_dir
        self.updateCommandText()
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
        self.updateCommandText()
        self.g_dict_Cache["OutputDirName"] = l_fileName

    def selectLanguage(self):
        """
        选择字幕语言
        """
        self.args.update({"language": self.widgets.autoTitle_comboBox.currentText()})
        self.updateCommandText()

    def selectSubTitleExt(self):
        """
        选择输出字幕格式
        """
        self.args["output_ext"] = self.widgets.autoTitle_comboBox2.currentText()
        self.updateCommandText()

    def runCommand(self):
        """
        创建线程，调用whisper配字幕
        """
        # 先结束之前的进程
        if self.thread1 is not None:
            self.closeThread()
            self.updateCommandText()
            self.widgets.autoTitle_run_Btn.setText("运行命令")
            return
        # 创建新监控进程
        self.thread1 = SubTitleRunner(self.args.copy())
        # 设置新监控进程的数据信息
        self.thread1.finishSignal.connect(self.updateCommandText)
        self.thread1.start()
        # 保存缓存
        with open(os.path.join(self.absPath, "..", "config.json"), "w") as f:
            json.dump(self.g_dict_Cache, f, indent=4)
        self.widgets.autoTitle_run_Btn.setText("取消命令")

    def updateCommandText(self, i_text=None):
        """
        更新文本框展示参数，给定内容则展示内容，否则展示默认配字幕使用的参数。
        输入:
            i_text:     需要显示的内容
        """
        string = i_text
        if string is None:
            string = ""
            string += "输入文件 : " + self.args["audio"] + "\n"
            string += "输出位置 : " + self.args["output_dir"] + "\n"
            string += "字幕格式 : " + self.args["output_ext"] + "\n"
            string += "字幕语言 : " + self.args["language"] + "\n"
        self.widgets.autoTitle_output_Edit.setPlainText(string)