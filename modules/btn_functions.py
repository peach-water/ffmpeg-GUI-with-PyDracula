import psutil
import os
import sys

from PySide6.QtCharts import QLineSeries, QChart, QDateTimeAxis, QValueAxis
from PySide6.QtCore import QThread, Signal, QDateTime
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QFileDialog

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
        """
        不断读取最新的CPU和内存使用信息
        """
        while not self.stop_statu:
            cpu_percent = psutil.cpu_percent(interval=1)
            virtual_memory = psutil.virtual_memory()
            memory_percent = virtual_memory.percent
            
            self.finishSignal.emit(f"{cpu_percent}, {memory_percent}\n")

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
        """
        TODO本类还没有一个实现目标
        """
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
        """
        home_dir = os.path.abspath(os.path.join(self.absPath, ".."))

        f_name = QFileDialog.getOpenFileName(self, "Open file", home_dir)
        print(f_name)
        
    def switchPicture(self):
        """
        在label标签展示图片，实际未启用。
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
