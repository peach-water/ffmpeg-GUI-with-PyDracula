import re
import json
import os
import ffmpeg
import logging
import subprocess
from logging.handlers import RotatingFileHandler

from PySide6.QtCore import Signal

def logInitialize():
    """
    初始化一个日志器
    """
    logging.basicConfig(level=logging.INFO)
    l_log_Handle = RotatingFileHandler("log.txt", maxBytes=1024*1024, backupCount=5, encoding="utf-8")
    l_formatter = logging.Formatter("%(asctime)s - %(name)s %(levelname)s - %(message)s- from : %(funcName)s,")
    # 设置日志记录格式
    l_log_Handle.setFormatter(l_formatter)
    logging.getLogger().addHandler(l_log_Handle)
    

def formatTimeToSecond(time: str) -> float:
    """
    格式化时间 hh:mm:ss.mm 转持续时间。

    Input：
        time - (str)
            字符串，格式化的时间
    Output:
        seconds - (float)
            浮点数，返回time对应的秒数
    """
    time = time.split(":")
    h = int(time[0])
    m = int(time[1])
    time = time[-1].split(".")
    s = int(time[0])
    ms = int(time[1])
    seconds = (h*60*60) + (m * 60) + s + (ms/100)
    return seconds

def commandRunner(p, duration=None, buffer=4, progressSignal:Signal=None):
    """
    调用ffmpeg进行转码工作的自进程，并且格式化ffmpeg打印的日志信息返回给程序以追踪处理进度。
    进程对象不由本函数创建。

    Input:
    ---
        p - (subprocess.Popen)
            进程对象
        duration - (float)
            视频总时长，换算成秒
        buffer - (int)
            格式化信息包含ffmpeg的日志最近几行的内容，越大可以追踪的信息越多
    
    Output:
    ---
        string - (generator(str))
            函数以 generator 形式返回格式化的日志信息，
            信息以 str 的数据类型存储
    """
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
            if line[-1] == "N/A":
                # 经过检查发现出现 N/A 输出的原因是转码任务较容易时ffmpeg处理太快，例如视频只有 1s 。
                pass
            else:
                try:
                    percent = formatTimeToSecond(line[-1])/duration
                    if progressSignal:
                        progressSignal.emit(int(percent*100))
                except BaseException as e:
                    logging.error(f"{e}")
            # string += f"\n处理进度：{round(percent*100, ndigits=2)}%\t"
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

def readCacheFile():
    """
    读取文件所在绝对路径，读取上次操作缓存文件
    
    Input:
    ---
        None

    Output:
    ---
        l_absPath - (str)
            缓存文件绝对路径
        l_FileName: - (str)
            缓存文件，保存上次处理的文件信息
    """
    l_absPath = os.path.dirname(os.path.abspath(__file__))
    l_fileName = {}
    if os.path.exists(os.path.join(l_absPath, "..", "config.json")):
        with open(os.path.join(l_absPath, "..", "config.json"), "r") as f:
            l_fileName = json.load(f)
    return l_absPath, l_fileName

def saveCacheFile(cache:dict):
    """
    保存上次操作的缓存数据

    Input:
    ---
        cache - (dict)
            字典类型的缓存信息
    
    Output:
    ---
        None
    """
    l_absPath = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(l_absPath, "..", "config.json"), "w") as f:
        json.dump(cache, f, indent=4)
    return 

def getVideoFramsPerSecond(file:str):
    """
    获得视频文件的帧率

    Input:
    ---
        file - (str)
            文件位置
    
    Output:
    ---
        l_fps - (float)
            帧率
    """
    if not os.path.exists(file):
        print("文件不存在")
        return
    try:
        l_fps = ffmpeg.probe(file)["streams"][0]["avg_frame_rate"]
        l_fps = eval(l_fps)
    except ffmpeg.Error as e:
        logging.debug(f"{file} 无法读取")
        return 0.0
    except ZeroDivisionError as e:
        logging.debug(f"{file} 没有视频信息")
        return 0.0
    return l_fps

def hidenTerminal():
    """
    如果是 windows 环境下，用于关闭 subprocess 执行命令时弹出的窗口
    """
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return startupinfo
    return None