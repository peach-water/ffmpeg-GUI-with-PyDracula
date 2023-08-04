import time
import psutil
import os
import sys
from PySide6.QtCharts import QLineSeries, QChart, QDateTimeAxis, QValueAxis
# from main import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# 线程创建实现
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

class CommandRunner(QThread):
    """
    创建一个线程开始转码工作
    ~~~~~~~~~~~~~~~~~~
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
        super(CommandRunner, self).__init__()
        self.command = ""
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
            l_runner = self.commandRunner(self.command)
            for i in l_runner:
                self.finishSignal.emit(i)
            return 

        l_home_dir = self.g_home_Dir
        l_count = 0
        l_unprocessed_file = os.listdir(l_home_dir)
        for lo_file in l_unprocessed_file:
            lo_fileExt = lo_file.split(".")[-1]
            lo_fileName = lo_file[:-len(lo_fileExt)-1] + self.g_process_Time
            lo_file = os.path.join(l_home_dir, lo_file)
            lo_command = f"ffmpeg -i \"{lo_file}\" {self.g_convert_Command}"
            lo_command += f" \"{os.path.join(self.g_output_Dir, lo_fileName)}.{self.g_output_Ext}\""

            l_runner = self.commandRunner(lo_command)
            for i in l_runner:
                i += "progressd %4d/%4d" % (l_count+1, len(l_unprocessed_file))
                self.finishSignal.emit(i)
            time.sleep(2)
            l_count += 1

    def commandRunner(self, command):
        import subprocess
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE, 
                             stdin=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=False, 
                             universal_newlines=True
                            )
            
        lines = []
        for line in p.stdout:
            lines.append(line)
            string = ""
            for i in lines:
                string += i
            if len(lines) > 4:
                lines.pop(0)
            yield string
# 功能实现模块
# //////////////////////////////////////////////////////////////

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
        if getattr(sys, "frozen", False):
            absPath = os.path.dirname(os.path.abspath(sys.executable))
        elif __file__:
            absPath = os.path.dirname(os.path.abspath(__file__))
        self.absPath = absPath
        self.widgets = widgets
        self.thread1 = None
        # self.widgets.input_Edit3.setPlainText(os.path.join(os.path.expanduser("~"), "Desktop"))
        self.g_convert_Mode = ""
        self.g_bitrate_Control = ""
        self.g_preset_Mode = "fast"
        self.g_file_Ext = "mp4"
        self.g_batch_Mode = False # 是否启用批量处理模式
        self.g_dict_Mode = {"转码H264": "-c:v h264", 
                         "转码H265": "-c:v libx265", 
                         "转MP3": "-vn -f mp3",
                         "转GIF": "-f gif",
                         "内挂字幕": "-c copy -c:s copy",
                        #  "内嵌字幕": "-qscale 0 -c:h264 -vf subtitles",
                         "视频两倍速" : "-r 120 -filter:a \"atempo=2.0\" -filter:v \"setpts=0.5*PTS\""
                        }
    def closeThread(self):
        if self.thread1:
            self.thread1.terminate()
            self.thread1.wait()
            self.thread1 = None
            self.widgets.input_Edit3.setPlainText("已停止")

    def selectFile(self, btn_Name):
        """
        选择一个本地文件，因为两个选择文件按钮都是采用同一个处理逻辑，需要区分是哪个按钮
        输入:
            btn_Name:       按下的按钮是哪个
        """
        l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
        l_fileName = QFileDialog.getOpenFileName(self, "选择文件", l_home_dir)[0]
        if btn_Name == "btn_input1":
            self.widgets.input_Edit1.setPlainText(l_fileName)
            l_fileName = l_fileName.split("/")
            l_home_dir = l_fileName[0]
            for i in range(1, len(l_fileName)-1):
                l_home_dir += "/" + l_fileName[i]
            self.widgets.input_Edit3.setPlainText(str(l_home_dir))
        elif btn_Name == "btn_input2":
            self.widgets.input_Edit2.setPlainText(l_fileName)
        self.updateCommandText()

    def selectDirectory(self, i_btn_Name):
        """
        选择输出文件夹位置
        """
        
        if self.widgets.input_Edit3.toPlainText() == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
        else:
            l_home_dir = self.widgets.input_Edit3.toPlainText()
        l_fileName = QFileDialog.getExistingDirectory(self, "输出位置", l_home_dir)
        if i_btn_Name == "btn_input3":
            self.widgets.input_Edit3.setPlainText(l_fileName)
        elif i_btn_Name == "btn_input1":
            self.widgets.input_Edit1.setPlainText(l_fileName)
            self.widgets.input_Edit3.setPlainText(os.path.abspath(os.path.join(l_fileName, "..")))
        self.updateCommandText()

    def selectMode(self, mode, listBoxIndex):
        """
        确定选择使用的预设
        输入：
            mode:           传入选择的模式
            listBoxIndex:   传入选择的输出视频格式
        """
        l_item = mode.currentItem().text()
        if listBoxIndex == "modeBox":
            self.g_convert_Mode = self.g_dict_Mode.get(l_item)
            if self.g_convert_Mode is None:
                self.g_convert_Mode = ""
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
        l_mode_dict = {0: "placebo", 1: "veryslow", 2: "slower", 3: "slow", 4: "medium",
                        5: "fast", 6:"faster", 7:"veryfast", 8: "superfast", 9: "ultrafast"}
        self.g_preset_Mode = l_mode_dict.get(self.widgets.perset_set_Slider.value())

        self.updateCommandText()

    def selectBitrateMode(self):
        if self.widgets.bitrate_mode_Combo.currentText() != "无":
            self.g_bitrate_Control = self.widgets.bitrate_mode_Combo.currentText()
        else:
            self.g_bitrate_Control = ""
        self.updateCommandText()

    def selectBatchProcessMode(self):
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
        更新命令框
        """
        if self.widgets.input_Edit1.toPlainText() == "":
            self.widgets.output_command_Edit.setPlainText("指定输入文件")
            return
        l_command = f"ffmpeg -i \"{self.widgets.input_Edit1.toPlainText()}\""
        # 取出文件名和拓展名
        temp = self.widgets.input_Edit1.toPlainText().split("/")[-1]
        l_fileExt = temp.split(".")[-1]
        l_fileName = temp[:-len(l_fileExt)-1]

        l_fileName += time.strftime("_%m-%d_%H-%M-%S", time.localtime())
        del temp
        # 反馈展示
        # ////////////////////////////////////////////////////////////
        # 指定第二个输入文件
        if self.widgets.input_Edit2.toPlainText() != "":
            l_command += f" -i \"{self.widgets.input_Edit2.toPlainText()}\""
        # 指定码率控制
        if self.g_bitrate_Control != "":
            l_command += f" -{self.g_bitrate_Control} {self.widgets.bitrate_Edit.toPlainText()}"
        # 选择输出位置和输出文件名
        l_home_dir = self.widgets.input_Edit3.toPlainText()
        if l_home_dir == "":
            l_home_dir = os.path.abspath(os.path.join(self.absPath, ".."))
            
        l_command += f" {self.g_convert_Mode} -preset {self.g_preset_Mode}"
        l_command += f" -y \"{l_home_dir}/{l_fileName}.{self.g_file_Ext}\""
        self.widgets.output_command_Edit.setPlainText(l_command)

    def runCommandText(self):
        """
        新建一个终端运行指令框的命令，如果是批量处理
        """
        # 单个文件处理
        if not self.g_batch_Mode:
            self.thread1 = CommandRunner()
            self.thread1.command = self.widgets.output_command_Edit.toPlainText()
        else:
            l_convert_Command = ""
            if self.g_bitrate_Control != "":
                l_convert_Command += f" -{self.g_bitrate_Control} {self.widgets.bitrate_Edit.toPlainText()}"
            l_output_Dir = self.widgets.input_Edit3.toPlainText()
            l_home_Dir = self.widgets.input_Edit1.toPlainText()
            if l_output_Dir == "":
                l_output_Dir = os.path.abspath(os.path.join(self.absPath, ".."))
            
            l_convert_Command += f" {self.g_convert_Mode} -preset {self.g_preset_Mode}"
            l_convert_Command += f" -y"
            self.thread1 = CommandRunner(True, 
                                        i_convert_Command=l_convert_Command,
                                        i_home_dir=l_home_Dir,
                                        i_output_dir=l_output_Dir,
                                        i_output_ext=self.g_file_Ext,
                                        i_process_Time=time.strftime("_%m-%d_%H-%M-%S", time.localtime())
                                        )
        # 启动线程
        self.thread1.finishSignal.connect(self.runCommandTextShow)
        self.thread1.start()
    
    def runCommandTextShow(self, signal_str):
        """
        在命令框展示运行结果
        输入: 
            stgnal_str:     需要展示的信息
        """
        self.widgets.output_command_Edit.setPlainText(signal_str)
