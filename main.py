# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # 软件标题
        # APP title
        # ///////////////////////////////////////////////////////////////
        title = "PyDracula - Modern GUI"
        description = "工具箱"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        # widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_autoTitle.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_autoCut.clicked.connect(self.buttonClick)

        
        # 自己加入菜单项一个新内容
        widgets.btn_computer.clicked.connect(self.buttonClick)
      
        # 这一段无用，测试接口函数的
        widgets.btn_message.clicked.connect(self.buttonClick)
        # 子模块激活
        # ///////////////////////////////////////////////////////////////
        # 测试页
        self.OpenFile = None
        # CPU和内存监控页
        self.CPUMonitor = None
        # 转换视频页(主页)
        self.ConvertVideo = None
        # 自动剪辑主页
        self.AutoCut = None
        # 配字幕主页
        self.AutoTitle = None

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        if getattr(sys, "frozen", False):
            absPath = os.path.dirname(os.path.abspath(sys.executable))
        elif __file__:
            absPath = os.path.dirname(os.path.abspath(__file__))
        useCustomTheme = True
        self.useCustomTheme = useCustomTheme
        self.absPath = absPath
        themeFile = os.path.abspath(os.path.join(absPath, "themes\py_dracula_dark.qss"))

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        if self.ConvertVideo is None:
            self.ConvertVideo = ConvertVideoFactory(widgets)
            # 设置主页按钮功能
            widgets.btn_input1.clicked.connect(lambda: self.ConvertVideo.selectFile("btn_input1"))
            widgets.btn_input2.clicked.connect(lambda: self.ConvertVideo.selectFile("btn_input2"))
            widgets.btn_input3.clicked.connect(lambda: self.ConvertVideo.selectDirectory("btn_input3"))
            widgets.list_mode.clicked.connect(lambda: self.ConvertVideo.selectMode(widgets.list_mode, "modeBox"))
            widgets.list_video_type.clicked.connect(lambda: self.ConvertVideo.selectMode(widgets.list_video_type, "typeBox"))
            widgets.btn_command_run.clicked.connect(self.ConvertVideo.runCommand)
            widgets.perset_set_Slider.valueChanged.connect(self.ConvertVideo.selectPresetMode)
            widgets.bitrate_mode_Combo.activated.connect(self.ConvertVideo.selectBitrateMode)
            widgets.bitrate_Edit.textChanged.connect(self.ConvertVideo.selectBitrateMode)
            widgets.batch_mode_Check.stateChanged.connect(self.ConvertVideo.selectBatchProcessMode)
            # 提高交互性，文本框更新时触发
            widgets.input_Edit1.textChanged.connect(self.ConvertVideo.updateCommandText)
            widgets.input_Edit2.textChanged.connect(self.ConvertVideo.updateCommandText)
            widgets.input_Edit3.textChanged.connect(self.ConvertVideo.updateCommandText)
            # 设置关闭按钮
            widgets.closeAppBtn.clicked.connect(self.ConvertVideo.closeThread)  

        widgets.stackedWidget.setCurrentWidget(widgets.convert_video)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.convert_video)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_autoTitle":
            if self.AutoTitle is None:
                self.AutoTitle = AutoSubtitleFactory(widgets)
                # 设置主页按钮功能
                widgets.autoTitle_comboBox.activated.connect(self.AutoTitle.selectLanguage)
                widgets.autoTitle_comboBox2.activated.connect(self.AutoTitle.selectSubTitleExt)
                widgets.autoTitle_input_Btn.clicked.connect(self.AutoTitle.selectFile)
                widgets.autoTitle_input2_Btn.clicked.connect(self.AutoTitle.selectDirectory)
                widgets.autoTitle_run_Btn.clicked.connect(self.AutoTitle.runCommand)
                
                # 设置关闭按钮
                widgets.closeAppBtn.clicked.connect(self.AutoTitle.closeThread)

            widgets.stackedWidget.setCurrentWidget(widgets.auto_subtitle_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            if self.OpenFile is None:
                self.OpenFile = OpenFileFactory(widgets)
                # 打开文件
                widgets.btn_open_file.clicked.connect(self.OpenFile.openFile)
                # 打开外部网页
                widgets.btn_open_url.clicked.connect(self.OpenFile.openUrl)
                # 切换图片功能
                widgets.btn_switch_picture.clicked.connect(self.OpenFile.switchPicture)

            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_autoCut":
            # 给出功能未实现的提示
            # QMessageBox.information(self, "提示", "功能未实现", QMessageBox.Yes)
            if self.AutoCut is None:
                self.AutoCut = AutoCutFactory(widgets)
                widgets.autoCut_input_Btn.clicked.connect(self.AutoCut.selectFile)
                widgets.autoCut_input2_Btn.clicked.connect(self.AutoCut.selectDirectory)
                widgets.autoCut_run_Btn.clicked.connect(self.AutoCut.runCommand)
                # 关闭按钮
                widgets.closeAppBtn.clicked.connect(self.AutoCut.closeThread)
                
            widgets.stackedWidget.setCurrentWidget(widgets.auto_cut_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_computer":
            if self.CPUMonitor is None:
                self.CPUMonitor = CPUInfoCaptureFactory(widgets.graphicsView)
                # 加入监控CPU和内存信息功能
                widgets.btn_draw.clicked.connect(self.CPUMonitor.startDataDisplay)
                # 开始记录CPU和内存占用信息
                widgets.btn_graphic_clear.clicked.connect(self.CPUMonitor.clearDataDisplay)
                # 设置关闭按钮
                widgets.closeAppBtn.clicked.connect(self.CPUMonitor.closeThread)
        
            # 切换页面
            widgets.stackedWidget.setCurrentWidget(widgets.computer_info) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # 切换主题黑夜/白天
        if btnName == "btn_message":
            if self.useCustomTheme:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_dark.qss"))
                UIFunctions.theme(self, themeFile, True)
                # SET HACKS
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = False
            else:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_light.qss"))
                UIFunctions.theme(self, themeFile, True)
                # SET HACKS
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = True

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
