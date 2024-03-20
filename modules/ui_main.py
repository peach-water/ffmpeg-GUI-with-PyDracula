# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainXpwRDK.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QPlainTextEdit, QProgressBar,
    QPushButton, QSizePolicy, QSlider, QStackedWidget,
    QTextEdit, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1196, 720)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background"
                        "-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(18"
                        "9, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb("
                        "189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border"
                        "-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-sty"
                        "le: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb"
                        "(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-co"
                        "lor: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-c"
                        "olor: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
""
                        "QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     su"
                        "bcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	back"
                        "ground-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subco"
                        "ntrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    h"
                        "eight: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLi"
                        "nkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Semibold"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_autoCut = QPushButton(self.topMenu)
        self.btn_autoCut.setObjectName(u"btn_autoCut")
        sizePolicy.setHeightForWidth(self.btn_autoCut.sizePolicy().hasHeightForWidth())
        self.btn_autoCut.setSizePolicy(sizePolicy)
        self.btn_autoCut.setMinimumSize(QSize(0, 45))
        self.btn_autoCut.setFont(font)
        self.btn_autoCut.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_autoCut.setLayoutDirection(Qt.LeftToRight)
        self.btn_autoCut.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-library.png);")

        self.verticalLayout_8.addWidget(self.btn_autoCut)

        self.btn_autoTitle = QPushButton(self.topMenu)
        self.btn_autoTitle.setObjectName(u"btn_autoTitle")
        sizePolicy.setHeightForWidth(self.btn_autoTitle.sizePolicy().hasHeightForWidth())
        self.btn_autoTitle.setSizePolicy(sizePolicy)
        self.btn_autoTitle.setMinimumSize(QSize(0, 45))
        self.btn_autoTitle.setFont(font)
        self.btn_autoTitle.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_autoTitle.setLayoutDirection(Qt.LeftToRight)
        self.btn_autoTitle.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-gamepad.png);")

        self.verticalLayout_8.addWidget(self.btn_autoTitle)

        self.btn_computer = QPushButton(self.topMenu)
        self.btn_computer.setObjectName(u"btn_computer")
        self.btn_computer.setMinimumSize(QSize(0, 45))
        self.btn_computer.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_computer.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-devices.png);")

        self.verticalLayout_8.addWidget(self.btn_computer)

        self.btn_new = QPushButton(self.topMenu)
        self.btn_new.setObjectName(u"btn_new")
        sizePolicy.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy)
        self.btn_new.setMinimumSize(QSize(0, 45))
        self.btn_new.setFont(font)
        self.btn_new.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_new.setLayoutDirection(Qt.LeftToRight)
        self.btn_new.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-file.png);")

        self.verticalLayout_8.addWidget(self.btn_new)

        self.btn_exit = QPushButton(self.topMenu)
        self.btn_exit.setObjectName(u"btn_exit")
        sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy)
        self.btn_exit.setMinimumSize(QSize(0, 45))
        self.btn_exit.setFont(font)
        self.btn_exit.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_exit.setLayoutDirection(Qt.LeftToRight)
        self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        self.verticalLayout_8.addWidget(self.btn_exit)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_settings.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)


        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_share = QPushButton(self.extraTopMenu)
        self.btn_share.setObjectName(u"btn_share")
        sizePolicy.setHeightForWidth(self.btn_share.sizePolicy().hasHeightForWidth())
        self.btn_share.setSizePolicy(sizePolicy)
        self.btn_share.setMinimumSize(QSize(0, 45))
        self.btn_share.setFont(font)
        self.btn_share.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_share.setLayoutDirection(Qt.LeftToRight)
        self.btn_share.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-share-boxed.png);")

        self.verticalLayout_11.addWidget(self.btn_share)

        self.btn_adjustments = QPushButton(self.extraTopMenu)
        self.btn_adjustments.setObjectName(u"btn_adjustments")
        sizePolicy.setHeightForWidth(self.btn_adjustments.sizePolicy().hasHeightForWidth())
        self.btn_adjustments.setSizePolicy(sizePolicy)
        self.btn_adjustments.setMinimumSize(QSize(0, 45))
        self.btn_adjustments.setFont(font)
        self.btn_adjustments.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_adjustments.setLayoutDirection(Qt.LeftToRight)
        self.btn_adjustments.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-equalizer.png);")

        self.verticalLayout_11.addWidget(self.btn_adjustments)

        self.btn_more = QPushButton(self.extraTopMenu)
        self.btn_more.setObjectName(u"btn_more")
        sizePolicy.setHeightForWidth(self.btn_more.sizePolicy().hasHeightForWidth())
        self.btn_more.setSizePolicy(sizePolicy)
        self.btn_more.setMinimumSize(QSize(0, 45))
        self.btn_more.setFont(font)
        self.btn_more.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_more.setLayoutDirection(Qt.LeftToRight)
        self.btn_more.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-layers.png);")

        self.verticalLayout_11.addWidget(self.btn_more)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon1)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"background-image: url(:/images/images/images/PyDracula_vertical.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;")
        self.stackedWidget.addWidget(self.home)
        self.convert_video = QWidget()
        self.convert_video.setObjectName(u"convert_video")
        self.convert_video.setFont(font)
        self.verticalLayout_29 = QVBoxLayout(self.convert_video)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_2 = QLabel(self.convert_video)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 60))
        self.label_2.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_23.addWidget(self.label_2)

        self.input_Edit1 = QPlainTextEdit(self.convert_video)
        self.input_Edit1.setObjectName(u"input_Edit1")
        self.input_Edit1.setMinimumSize(QSize(0, 48))
        self.input_Edit1.setMaximumSize(QSize(16777215, 48))
        self.input_Edit1.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.input_Edit1.setStyleSheet(u"")

        self.verticalLayout_23.addWidget(self.input_Edit1)


        self.horizontalLayout_7.addLayout(self.verticalLayout_23)

        self.btn_input1 = QPushButton(self.convert_video)
        self.btn_input1.setObjectName(u"btn_input1")
        self.btn_input1.setMinimumSize(QSize(40, 40))
        self.btn_input1.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_input1.setStyleSheet(u"")

        self.horizontalLayout_7.addWidget(self.btn_input1)


        self.verticalLayout_25.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_3 = QLabel(self.convert_video)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 60))
        self.label_3.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_24.addWidget(self.label_3)

        self.input_Edit2 = QPlainTextEdit(self.convert_video)
        self.input_Edit2.setObjectName(u"input_Edit2")
        self.input_Edit2.setMinimumSize(QSize(0, 48))
        self.input_Edit2.setMaximumSize(QSize(16777215, 48))
        self.input_Edit2.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.input_Edit2.setStyleSheet(u"")

        self.verticalLayout_24.addWidget(self.input_Edit2)


        self.horizontalLayout_8.addLayout(self.verticalLayout_24)

        self.btn_input2 = QPushButton(self.convert_video)
        self.btn_input2.setObjectName(u"btn_input2")
        self.btn_input2.setMinimumSize(QSize(40, 40))
        self.btn_input2.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_input2.setStyleSheet(u"")

        self.horizontalLayout_8.addWidget(self.btn_input2)


        self.verticalLayout_25.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.label_4 = QLabel(self.convert_video)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 60))
        self.label_4.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_26.addWidget(self.label_4)

        self.input_Edit3 = QPlainTextEdit(self.convert_video)
        self.input_Edit3.setObjectName(u"input_Edit3")
        self.input_Edit3.setMinimumSize(QSize(0, 48))
        self.input_Edit3.setMaximumSize(QSize(16777215, 48))
        self.input_Edit3.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.input_Edit3.setStyleSheet(u"")

        self.verticalLayout_26.addWidget(self.input_Edit3)


        self.horizontalLayout_10.addLayout(self.verticalLayout_26)

        self.btn_input3 = QPushButton(self.convert_video)
        self.btn_input3.setObjectName(u"btn_input3")
        self.btn_input3.setMinimumSize(QSize(60, 40))
        self.btn_input3.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_input3.setStyleSheet(u"")

        self.horizontalLayout_10.addWidget(self.btn_input3)


        self.verticalLayout_25.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setSpacing(6)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.verticalLayout_30 = QVBoxLayout()
        self.verticalLayout_30.setSpacing(6)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.batch_mode_Check = QCheckBox(self.convert_video)
        self.batch_mode_Check.setObjectName(u"batch_mode_Check")
        self.batch_mode_Check.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_30.addWidget(self.batch_mode_Check)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_6 = QLabel(self.convert_video)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.horizontalLayout_15.addWidget(self.label_6)

        self.label_7 = QLabel(self.convert_video)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.label_7)


        self.verticalLayout_30.addLayout(self.horizontalLayout_15)

        self.perset_set_Slider = QSlider(self.convert_video)
        self.perset_set_Slider.setObjectName(u"perset_set_Slider")
        self.perset_set_Slider.setCursor(QCursor(Qt.PointingHandCursor))
        self.perset_set_Slider.setMaximum(9)
        self.perset_set_Slider.setValue(5)
        self.perset_set_Slider.setOrientation(Qt.Horizontal)

        self.verticalLayout_30.addWidget(self.perset_set_Slider)


        self.horizontalLayout_16.addLayout(self.verticalLayout_30)

        self.verticalLayout_31 = QVBoxLayout()
        self.verticalLayout_31.setSpacing(6)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.bitrate_mode_Combo = QComboBox(self.convert_video)
        self.bitrate_mode_Combo.addItem("")
        self.bitrate_mode_Combo.addItem("")
        self.bitrate_mode_Combo.addItem("")
        self.bitrate_mode_Combo.addItem("")
        self.bitrate_mode_Combo.setObjectName(u"bitrate_mode_Combo")
        self.bitrate_mode_Combo.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_31.addWidget(self.bitrate_mode_Combo)

        self.bitrate_Edit = QPlainTextEdit(self.convert_video)
        self.bitrate_Edit.setObjectName(u"bitrate_Edit")
        self.bitrate_Edit.setMinimumSize(QSize(0, 48))
        self.bitrate_Edit.setMaximumSize(QSize(16777215, 48))
        self.bitrate_Edit.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))

        self.verticalLayout_31.addWidget(self.bitrate_Edit)


        self.horizontalLayout_16.addLayout(self.verticalLayout_31)


        self.verticalLayout_25.addLayout(self.horizontalLayout_16)


        self.horizontalLayout_12.addLayout(self.verticalLayout_25)

        self.list_mode = QListWidget(self.convert_video)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        QListWidgetItem(self.list_mode)
        self.list_mode.setObjectName(u"list_mode")
        self.list_mode.setMaximumSize(QSize(200, 16777215))
        self.list_mode.viewport().setProperty("cursor", QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_12.addWidget(self.list_mode)

        self.list_video_type = QListWidget(self.convert_video)
        QListWidgetItem(self.list_video_type)
        QListWidgetItem(self.list_video_type)
        QListWidgetItem(self.list_video_type)
        self.list_video_type.setObjectName(u"list_video_type")
        self.list_video_type.setMinimumSize(QSize(100, 0))
        self.list_video_type.setMaximumSize(QSize(100, 16777215))
        self.list_video_type.viewport().setProperty("cursor", QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_12.addWidget(self.list_video_type)


        self.verticalLayout_28.addLayout(self.horizontalLayout_12)

        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.label_5 = QLabel(self.convert_video)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 40))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setBold(False)
        font4.setItalic(False)
        self.label_5.setFont(font4)
        self.label_5.setStyleSheet(u"font-size: 18px;")
        self.label_5.setFrameShape(QFrame.NoFrame)
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_27.addWidget(self.label_5)

        self.output_command_Edit = QPlainTextEdit(self.convert_video)
        self.output_command_Edit.setObjectName(u"output_command_Edit")
        self.output_command_Edit.setMinimumSize(QSize(0, 80))
        self.output_command_Edit.setFont(font4)
        self.output_command_Edit.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.output_command_Edit.setStyleSheet(u"font-size: 14px;")

        self.verticalLayout_27.addWidget(self.output_command_Edit)

        self.progressBar = QProgressBar(self.convert_video)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximumSize(QSize(16777215, 0))
        self.progressBar.setOrientation(Qt.Horizontal)

        self.verticalLayout_27.addWidget(self.progressBar)


        self.verticalLayout_28.addLayout(self.verticalLayout_27)

        self.btn_command_run = QPushButton(self.convert_video)
        self.btn_command_run.setObjectName(u"btn_command_run")
        self.btn_command_run.setMinimumSize(QSize(40, 40))
        self.btn_command_run.setMaximumSize(QSize(1600000, 80))
        self.btn_command_run.setFont(font)
        self.btn_command_run.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_command_run.setStyleSheet(u"")

        self.verticalLayout_28.addWidget(self.btn_command_run)


        self.verticalLayout_29.addLayout(self.verticalLayout_28)

        self.stackedWidget.addWidget(self.convert_video)
        self.blank = QWidget()
        self.blank.setObjectName(u"blank")
        self.blank.setStyleSheet(u"b")
        self.stackedWidget.addWidget(self.blank)
        self.new_page = QWidget()
        self.new_page.setObjectName(u"new_page")
        self.verticalLayout_20 = QVBoxLayout(self.new_page)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.btn_open_file = QPushButton(self.new_page)
        self.btn_open_file.setObjectName(u"btn_open_file")
        self.btn_open_file.setStyleSheet(u"")

        self.verticalLayout_20.addWidget(self.btn_open_file)

        self.btn_open_url = QPushButton(self.new_page)
        self.btn_open_url.setObjectName(u"btn_open_url")
        self.btn_open_url.setStyleSheet(u"")

        self.verticalLayout_20.addWidget(self.btn_open_url)

        self.btn_switch_picture = QPushButton(self.new_page)
        self.btn_switch_picture.setObjectName(u"btn_switch_picture")
        self.btn_switch_picture.setStyleSheet(u"")

        self.verticalLayout_20.addWidget(self.btn_switch_picture)

        self.label = QLabel(self.new_page)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_20.addWidget(self.label)

        self.stackedWidget.addWidget(self.new_page)
        self.auto_cut_page = QWidget()
        self.auto_cut_page.setObjectName(u"auto_cut_page")
        self.verticalLayout_36 = QVBoxLayout(self.auto_cut_page)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_35 = QVBoxLayout()
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.verticalLayout_33 = QVBoxLayout()
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.label_8 = QLabel(self.auto_cut_page)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(60, 40))
        self.label_8.setMaximumSize(QSize(16777215, 60))
        self.label_8.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_33.addWidget(self.label_8)

        self.autoCut_input_Edit = QPlainTextEdit(self.auto_cut_page)
        self.autoCut_input_Edit.setObjectName(u"autoCut_input_Edit")
        self.autoCut_input_Edit.setMinimumSize(QSize(0, 48))
        self.autoCut_input_Edit.setMaximumSize(QSize(16777215, 48))

        self.verticalLayout_33.addWidget(self.autoCut_input_Edit)


        self.horizontalLayout_17.addLayout(self.verticalLayout_33)

        self.autoCut_input_Btn = QPushButton(self.auto_cut_page)
        self.autoCut_input_Btn.setObjectName(u"autoCut_input_Btn")
        self.autoCut_input_Btn.setMinimumSize(QSize(60, 40))

        self.horizontalLayout_17.addWidget(self.autoCut_input_Btn)


        self.verticalLayout_35.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.verticalLayout_34 = QVBoxLayout()
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.label_9 = QLabel(self.auto_cut_page)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(60, 40))
        self.label_9.setMaximumSize(QSize(16777215, 60))
        self.label_9.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_34.addWidget(self.label_9)

        self.autoCut_input2_Edit = QPlainTextEdit(self.auto_cut_page)
        self.autoCut_input2_Edit.setObjectName(u"autoCut_input2_Edit")
        self.autoCut_input2_Edit.setMinimumSize(QSize(0, 48))
        self.autoCut_input2_Edit.setMaximumSize(QSize(16777215, 48))

        self.verticalLayout_34.addWidget(self.autoCut_input2_Edit)


        self.horizontalLayout_18.addLayout(self.verticalLayout_34)

        self.autoCut_input2_Btn = QPushButton(self.auto_cut_page)
        self.autoCut_input2_Btn.setObjectName(u"autoCut_input2_Btn")
        self.autoCut_input2_Btn.setMinimumSize(QSize(60, 40))

        self.horizontalLayout_18.addWidget(self.autoCut_input2_Btn)


        self.verticalLayout_35.addLayout(self.horizontalLayout_18)

        self.autoCut_output_Edit = QPlainTextEdit(self.auto_cut_page)
        self.autoCut_output_Edit.setObjectName(u"autoCut_output_Edit")
        self.autoCut_output_Edit.setStyleSheet(u"font-size: 14px;")

        self.verticalLayout_35.addWidget(self.autoCut_output_Edit)

        self.autoCut_progressBar = QProgressBar(self.auto_cut_page)
        self.autoCut_progressBar.setObjectName(u"autoCut_progressBar")
        self.autoCut_progressBar.setMaximumSize(QSize(16777215, 0))

        self.verticalLayout_35.addWidget(self.autoCut_progressBar)

        self.autoCut_run_Btn = QPushButton(self.auto_cut_page)
        self.autoCut_run_Btn.setObjectName(u"autoCut_run_Btn")
        self.autoCut_run_Btn.setMinimumSize(QSize(60, 40))

        self.verticalLayout_35.addWidget(self.autoCut_run_Btn)


        self.verticalLayout_36.addLayout(self.verticalLayout_35)

        self.stackedWidget.addWidget(self.auto_cut_page)
        self.auto_subtitle_page = QWidget()
        self.auto_subtitle_page.setObjectName(u"auto_subtitle_page")
        self.verticalLayout_32 = QVBoxLayout(self.auto_subtitle_page)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.verticalLayout_38 = QVBoxLayout()
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.label_10 = QLabel(self.auto_subtitle_page)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(60, 40))
        self.label_10.setMaximumSize(QSize(16777215, 60))
        self.label_10.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_38.addWidget(self.label_10)

        self.autoTitle_input_Edit = QPlainTextEdit(self.auto_subtitle_page)
        self.autoTitle_input_Edit.setObjectName(u"autoTitle_input_Edit")
        self.autoTitle_input_Edit.setMinimumSize(QSize(0, 48))
        self.autoTitle_input_Edit.setMaximumSize(QSize(16777215, 48))

        self.verticalLayout_38.addWidget(self.autoTitle_input_Edit)


        self.horizontalLayout_19.addLayout(self.verticalLayout_38)

        self.autoTitle_input_Btn = QPushButton(self.auto_subtitle_page)
        self.autoTitle_input_Btn.setObjectName(u"autoTitle_input_Btn")
        self.autoTitle_input_Btn.setMinimumSize(QSize(60, 40))

        self.horizontalLayout_19.addWidget(self.autoTitle_input_Btn)


        self.verticalLayout_19.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_11 = QLabel(self.auto_subtitle_page)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(60, 40))
        self.label_11.setMaximumSize(QSize(16777215, 60))
        self.label_11.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout.addWidget(self.label_11)

        self.autoTitle_input2_Edit = QPlainTextEdit(self.auto_subtitle_page)
        self.autoTitle_input2_Edit.setObjectName(u"autoTitle_input2_Edit")
        self.autoTitle_input2_Edit.setMinimumSize(QSize(0, 48))
        self.autoTitle_input2_Edit.setMaximumSize(QSize(16777215, 48))

        self.verticalLayout.addWidget(self.autoTitle_input2_Edit)


        self.horizontalLayout_9.addLayout(self.verticalLayout)

        self.autoTitle_input2_Btn = QPushButton(self.auto_subtitle_page)
        self.autoTitle_input2_Btn.setObjectName(u"autoTitle_input2_Btn")
        self.autoTitle_input2_Btn.setMinimumSize(QSize(60, 40))

        self.horizontalLayout_9.addWidget(self.autoTitle_input2_Btn)


        self.verticalLayout_19.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_12 = QLabel(self.auto_subtitle_page)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_16.addWidget(self.label_12)

        self.autoTitle_comboBox = QComboBox(self.auto_subtitle_page)
        self.autoTitle_comboBox.addItem("")
        self.autoTitle_comboBox.addItem("")
        self.autoTitle_comboBox.setObjectName(u"autoTitle_comboBox")

        self.verticalLayout_16.addWidget(self.autoTitle_comboBox)


        self.horizontalLayout_11.addLayout(self.verticalLayout_16)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_13 = QLabel(self.auto_subtitle_page)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_17.addWidget(self.label_13)

        self.autoTitle_comboBox2 = QComboBox(self.auto_subtitle_page)
        self.autoTitle_comboBox2.addItem("")
        self.autoTitle_comboBox2.addItem("")
        self.autoTitle_comboBox2.addItem("")
        self.autoTitle_comboBox2.setObjectName(u"autoTitle_comboBox2")

        self.verticalLayout_17.addWidget(self.autoTitle_comboBox2)


        self.horizontalLayout_11.addLayout(self.verticalLayout_17)

        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.label_14 = QLabel(self.auto_subtitle_page)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setStyleSheet(u"color: rgb(113, 126, 149);font-size: 18px;")

        self.verticalLayout_18.addWidget(self.label_14)

        self.autoTitle_comboBox_modelSize = QComboBox(self.auto_subtitle_page)
        self.autoTitle_comboBox_modelSize.addItem("")
        self.autoTitle_comboBox_modelSize.addItem("")
        self.autoTitle_comboBox_modelSize.addItem("")
        self.autoTitle_comboBox_modelSize.addItem("")
        self.autoTitle_comboBox_modelSize.addItem("")
        self.autoTitle_comboBox_modelSize.addItem("")
        self.autoTitle_comboBox_modelSize.addItem("")
        self.autoTitle_comboBox_modelSize.addItem("")
        self.autoTitle_comboBox_modelSize.setObjectName(u"autoTitle_comboBox_modelSize")

        self.verticalLayout_18.addWidget(self.autoTitle_comboBox_modelSize)


        self.horizontalLayout_11.addLayout(self.verticalLayout_18)


        self.verticalLayout_19.addLayout(self.horizontalLayout_11)

        self.autoTitle_output_Edit = QPlainTextEdit(self.auto_subtitle_page)
        self.autoTitle_output_Edit.setObjectName(u"autoTitle_output_Edit")
        self.autoTitle_output_Edit.setStyleSheet(u"font-size: 14px;")

        self.verticalLayout_19.addWidget(self.autoTitle_output_Edit)

        self.autoTitle_run_Btn = QPushButton(self.auto_subtitle_page)
        self.autoTitle_run_Btn.setObjectName(u"autoTitle_run_Btn")
        self.autoTitle_run_Btn.setMinimumSize(QSize(60, 40))

        self.verticalLayout_19.addWidget(self.autoTitle_run_Btn)


        self.verticalLayout_32.addLayout(self.verticalLayout_19)

        self.stackedWidget.addWidget(self.auto_subtitle_page)
        self.computer_info = QWidget()
        self.computer_info.setObjectName(u"computer_info")
        self.verticalLayout_22 = QVBoxLayout(self.computer_info)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.graphicsView = QChartView(self.computer_info)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_21.addWidget(self.graphicsView)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_draw = QPushButton(self.computer_info)
        self.btn_draw.setObjectName(u"btn_draw")
        self.btn_draw.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.btn_draw)

        self.btn_graphic_clear = QPushButton(self.computer_info)
        self.btn_graphic_clear.setObjectName(u"btn_graphic_clear")
        self.btn_graphic_clear.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.btn_graphic_clear)


        self.verticalLayout_21.addLayout(self.horizontalLayout_6)


        self.verticalLayout_22.addLayout(self.verticalLayout_21)

        self.stackedWidget.addWidget(self.computer_info)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btn_message = QPushButton(self.topMenus)
        self.btn_message.setObjectName(u"btn_message")
        sizePolicy.setHeightForWidth(self.btn_message.sizePolicy().hasHeightForWidth())
        self.btn_message.setSizePolicy(sizePolicy)
        self.btn_message.setMinimumSize(QSize(0, 45))
        self.btn_message.setFont(font)
        self.btn_message.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_message.setLayoutDirection(Qt.LeftToRight)
        self.btn_message.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-envelope-open.png);")

        self.verticalLayout_14.addWidget(self.btn_message)

        self.btn_print = QPushButton(self.topMenus)
        self.btn_print.setObjectName(u"btn_print")
        sizePolicy.setHeightForWidth(self.btn_print.sizePolicy().hasHeightForWidth())
        self.btn_print.setSizePolicy(sizePolicy)
        self.btn_print.setMinimumSize(QSize(0, 45))
        self.btn_print.setFont(font)
        self.btn_print.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_print.setLayoutDirection(Qt.LeftToRight)
        self.btn_print.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-print.png);")

        self.verticalLayout_14.addWidget(self.btn_print)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)


        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        self.creditsLabel.setFont(font4)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"PyDracula", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"Modern GUI / Flat Style", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9875", None))
#if QT_CONFIG(tooltip)
        self.btn_autoCut.setToolTip(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u89c6\u9891\uff0c\u6839\u636e\u662f\u5426\u6709\u58f0\u97f3\u81ea\u52a8\u622a\u53d6\u5bf9\u5e94\u7684\u97f3\u9891\u548c\u89c6\u9891\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.btn_autoCut.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u526a\u8f91", None))
#if QT_CONFIG(tooltip)
        self.btn_autoTitle.setToolTip(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u89c6\u9891\uff0c\u4f7f\u7528Whisper\u6a21\u578b\u8bc6\u522b\u58f0\u97f3\u8f93\u51fa\u5b57\u5e55\u6587\u4ef6\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.btn_autoTitle.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u914d\u5b57\u5e55", None))
        self.btn_computer.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u8d44\u6e90\u76d1\u63a7", None))
        self.btn_new.setText(QCoreApplication.translate("MainWindow", u"\u7a7a\u767d\u9875", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"Left Box", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Left Box", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.btn_share.setText(QCoreApplication.translate("MainWindow", u"Share", None))
        self.btn_adjustments.setText(QCoreApplication.translate("MainWindow", u"Adjustments", None))
        self.btn_more.setText(QCoreApplication.translate("MainWindow", u"More", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">PyDracula</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">An interface created using Python and PySide (support for PyQt), and with colors based on the Dracula theme created by Zen"
                        "o Rocha.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">MIT License</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#bd93f9;\">Created by: Wanderson M. Pimenta</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert UI</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-uic main.ui &gt; ui_main.py</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-in"
                        "dent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert QRC</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-rcc resources.qrc -o resources_rc.py</span></p></body></html>", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u5904\u7406\u5de5\u5177\u7bb1", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u5904\u7406\u6587\u4ef61", None))
#if QT_CONFIG(tooltip)
        self.input_Edit1.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_input1.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u5904\u7406\u6587\u4ef62", None))
#if QT_CONFIG(tooltip)
        self.input_Edit2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_input2.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u4f4d\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.input_Edit3.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_input3.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.batch_mode_Check.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u5904\u7406", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u6700\u6162\uff08\u8d28\u91cf\u597d\uff09", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u6700\u5feb", None))
#if QT_CONFIG(tooltip)
        self.perset_set_Slider.setToolTip(QCoreApplication.translate("MainWindow", u"\u8f6c\u6362\u901f\u5ea6\u6a21\u5f0f\u9009\u62e9", None))
#endif // QT_CONFIG(tooltip)
        self.bitrate_mode_Combo.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0", None))
        self.bitrate_mode_Combo.setItemText(1, QCoreApplication.translate("MainWindow", u"crf", None))
        self.bitrate_mode_Combo.setItemText(2, QCoreApplication.translate("MainWindow", u"vbr", None))
        self.bitrate_mode_Combo.setItemText(3, QCoreApplication.translate("MainWindow", u"abr", None))

#if QT_CONFIG(whatsthis)
        self.bitrate_mode_Combo.setWhatsThis(QCoreApplication.translate("MainWindow", u"\u7801\u7387\u63a7\u5236\u6a21\u5f0f", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(tooltip)
        self.bitrate_Edit.setToolTip(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u63a7\u5236\u6a21\u5f0f\u5bf9\u5e94\u7684\u547d\u4ee4", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.bitrate_Edit.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)

        __sortingEnabled = self.list_mode.isSortingEnabled()
        self.list_mode.setSortingEnabled(False)
        ___qlistwidgetitem = self.list_mode.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u4f7f\u7528\u9884\u8bbe", None));
        ___qlistwidgetitem1 = self.list_mode.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u7801H264", None));
        ___qlistwidgetitem2 = self.list_mode.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u7801H265", None));
        ___qlistwidgetitem3 = self.list_mode.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u53d6\u89c6\u9891", None));
        ___qlistwidgetitem4 = self.list_mode.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u8f6cMP3", None));
        ___qlistwidgetitem5 = self.list_mode.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u8f6cGIF", None));
        ___qlistwidgetitem6 = self.list_mode.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u4e24\u500d\u901f", None));
        ___qlistwidgetitem7 = self.list_mode.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u5185\u6302\u5b57\u5e55", None));
        ___qlistwidgetitem8 = self.list_mode.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u5185\u5d4c\u5b57\u5e55", None));
        ___qlistwidgetitem9 = self.list_mode.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u5f85\u6dfb\u52a0", None));
        self.list_mode.setSortingEnabled(__sortingEnabled)


        __sortingEnabled1 = self.list_video_type.isSortingEnabled()
        self.list_video_type.setSortingEnabled(False)
        ___qlistwidgetitem10 = self.list_video_type.item(0)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("MainWindow", u"mp4", None));
        ___qlistwidgetitem11 = self.list_video_type.item(1)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("MainWindow", u"mkv", None));
        ___qlistwidgetitem12 = self.list_video_type.item(2)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("MainWindow", u"avi", None));
        self.list_video_type.setSortingEnabled(__sortingEnabled1)

        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u547d\u4ee4\u9884\u89c8", None))
        self.output_command_Edit.setPlaceholderText("")
        self.btn_command_run.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u547d\u4ee4", None))
        self.btn_open_file.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u672c\u5730\u6587\u4ef6", None))
        self.btn_open_url.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u7f51\u9875", None))
        self.btn_switch_picture.setText(QCoreApplication.translate("MainWindow", u"\u5207\u6362\u56fe\u7247", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"NEW PAGE TEST", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u6587\u4ef6", None))
        self.autoCut_input_Btn.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u4f4d\u7f6e", None))
        self.autoCut_input2_Btn.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.autoCut_run_Btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u526a\u8f91", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u6587\u4ef6", None))
        self.autoTitle_input_Btn.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u4f4d\u7f6e", None))
        self.autoTitle_input2_Btn.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u8bed\u8a00", None))
        self.autoTitle_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"zh", None))
        self.autoTitle_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"en", None))

#if QT_CONFIG(tooltip)
        self.autoTitle_comboBox.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bc6\u522b\u6587\u672c\uff0c\u5982\u679c\u89c6\u9891\u6216\u97f3\u9891\u8bed\u79cd\u4e0d\u662f\u6307\u5b9a\u8bed\u79cd\uff0c\u8fd8\u4f1a\u8fdb\u884c\u7ffb\u8bd1\u5de5\u4f5c\uff08\u8c28\u614e\u4f7f\u7528\u7ffb\u8bd1\u529f\u80fd\uff09\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u5b57\u5e55\u683c\u5f0f", None))
        self.autoTitle_comboBox2.setItemText(0, QCoreApplication.translate("MainWindow", u"srt", None))
        self.autoTitle_comboBox2.setItemText(1, QCoreApplication.translate("MainWindow", u"txt", None))
        self.autoTitle_comboBox2.setItemText(2, QCoreApplication.translate("MainWindow", u"vtt", None))

#if QT_CONFIG(tooltip)
        self.autoTitle_comboBox2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8f93\u51fa\u5b57\u5e55\u6587\u4ef6\u683c\u5f0f</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u5927\u5c0f", None))
        self.autoTitle_comboBox_modelSize.setItemText(0, QCoreApplication.translate("MainWindow", u"tiny", None))
        self.autoTitle_comboBox_modelSize.setItemText(1, QCoreApplication.translate("MainWindow", u"tiny.en", None))
        self.autoTitle_comboBox_modelSize.setItemText(2, QCoreApplication.translate("MainWindow", u"base", None))
        self.autoTitle_comboBox_modelSize.setItemText(3, QCoreApplication.translate("MainWindow", u"base.en", None))
        self.autoTitle_comboBox_modelSize.setItemText(4, QCoreApplication.translate("MainWindow", u"small", None))
        self.autoTitle_comboBox_modelSize.setItemText(5, QCoreApplication.translate("MainWindow", u"small.en", None))
        self.autoTitle_comboBox_modelSize.setItemText(6, QCoreApplication.translate("MainWindow", u"medium", None))
        self.autoTitle_comboBox_modelSize.setItemText(7, QCoreApplication.translate("MainWindow", u"medium.en", None))

#if QT_CONFIG(tooltip)
        self.autoTitle_comboBox_modelSize.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u9009\u62e9\u6a21\u578b\u5927\u5c0f\uff0c\u540e\u7f00\u5e26 en \u8868\u793a\u4ec5\u652f\u6301\u82f1\u6587\u8bc6\u522b\u6a21\u578b\u3002\u5982\u679c\u76ee\u5f55\u4e0b\u6ca1\u6709\u6a21\u578b\u4f1a\u81ea\u52a8\u4ece\u7f51\u7edc\u4e0b\u8f7d\uff0c\u4e0b\u8f7d\u65f6\u95f4\u8f83\u957f\u8bf7\u8010\u5fc3\u7b49\u5f85\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.autoTitle_run_Btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u8bc6\u522b", None))
        self.btn_draw.setText(QCoreApplication.translate("MainWindow", u"\u7ed8\u56fe", None))
        self.btn_graphic_clear.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.btn_message.setText(QCoreApplication.translate("MainWindow", u"Message", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"Peach Water", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v0.2.1", None))
    # retranslateUi

