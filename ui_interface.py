# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface violencesVcPAI.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)
import ressources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(817, 532)
        MainWindow.setMinimumSize(QSize(30, 30))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setFamilies([u"NovaFlat"])
        font.setPointSize(4)
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet(u" *{ color: #fff;\n"
"  border: nine;\n"
"   background: none;\n"
"}\n"
"#centralwidget{\n"
"  background-color:#000000;\n"
"}\n"
"#left_menu_widget{\n"
" background-color:#000000 ;\n"
"}\n"
"#stackedWidget{\n"
" background-color:#FFFFFF ;\n"
"}\n"
"#header_frame, #frame_3{\n"
"background-color: #800000;\n"
"}\n"
"#frame_4 QPushButton{\n"
" padding: 10px;\n"
"  background-color:#800000; \n"
"}\n"
"\n"
"#header_nav QPushButton{\n"
"background-color: (61, 80, 95);\n"
"}\n"
"#header_nav QPushButton:hover{\n"
"background-color: rgb(120, 157, 186);\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, 0)
        self.left_menu_widget = QFrame(self.centralwidget)
        self.left_menu_widget.setObjectName(u"left_menu_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_menu_widget.sizePolicy().hasHeightForWidth())
        self.left_menu_widget.setSizePolicy(sizePolicy)
        self.left_menu_widget.setMaximumSize(QSize(200, 16777215))
        self.left_menu_widget.setFrameShape(QFrame.StyledPanel)
        self.left_menu_widget.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.left_menu_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.left_menu_widget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(250, 16777215))
        font1 = QFont()
        font1.setPointSize(8)
        self.frame_4.setFont(font1)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 0, 171, 50))
        self.frame_3.setMaximumSize(QSize(200, 50))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(30, 30))
        self.label_2.setMaximumSize(QSize(35, 35))
        self.label_2.setPixmap(QPixmap(u":/newPrefix/icones/analytics.png"))
        self.label_2.setScaledContents(True)

        self.horizontalLayout_6.addWidget(self.label_2)

        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(60, 20))
        self.label.setMaximumSize(QSize(130, 50))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        self.label.setFont(font2)
        self.label.setTextFormat(Qt.RichText)
        self.label.setScaledContents(True)
        self.label.setWordWrap(True)
        self.label.setMargin(0)
        self.label.setIndent(-1)

        self.horizontalLayout_6.addWidget(self.label)

        self.map = QPushButton(self.frame_4)
        self.map.setObjectName(u"map")
        self.map.setGeometry(QRect(10, 160, 171, 51))
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.map.sizePolicy().hasHeightForWidth())
        self.map.setSizePolicy(sizePolicy2)
        font3 = QFont()
        font3.setPointSize(13)
        font3.setBold(True)
        self.map.setFont(font3)
        icon = QIcon()
        icon.addFile(u":/newPrefix/icones/maps.png", QSize(), QIcon.Normal, QIcon.Off)
        self.map.setIcon(icon)
        self.map.setIconSize(QSize(35, 35))
        self.map.setAutoDefault(False)
        self.graphes = QPushButton(self.frame_4)
        self.graphes.setObjectName(u"graphes")
        self.graphes.setGeometry(QRect(10, 240, 171, 51))
        sizePolicy2.setHeightForWidth(self.graphes.sizePolicy().hasHeightForWidth())
        self.graphes.setSizePolicy(sizePolicy2)
        self.graphes.setFont(font2)
        icon1 = QIcon()
        icon1.addFile(u":/newPrefix/icones/bar char.png", QSize(), QIcon.Normal, QIcon.Off)
        self.graphes.setIcon(icon1)
        self.graphes.setIconSize(QSize(35, 35))
        self.moregraphes = QPushButton(self.frame_4)
        self.moregraphes.setObjectName(u"moregraphes")
        self.moregraphes.setEnabled(True)
        self.moregraphes.setGeometry(QRect(10, 320, 171, 51))
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.moregraphes.sizePolicy().hasHeightForWidth())
        self.moregraphes.setSizePolicy(sizePolicy3)
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(True)
        self.moregraphes.setFont(font4)
        icon2 = QIcon()
        icon2.addFile(u":/newPrefix/icones/more.png", QSize(), QIcon.Normal, QIcon.Off)
        self.moregraphes.setIcon(icon2)
        self.moregraphes.setIconSize(QSize(30, 30))

        self.verticalLayout.addWidget(self.frame_4)


        self.horizontalLayout.addWidget(self.left_menu_widget)

        self.frame_6 = QWidget(self.centralwidget)
        self.frame_6.setObjectName(u"frame_6")
        self.verticalLayout_4 = QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy2.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy2)
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_8)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.frame_8)
        self.header_frame.setObjectName(u"header_frame")
        sizePolicy2.setHeightForWidth(self.header_frame.sizePolicy().hasHeightForWidth())
        self.header_frame.setSizePolicy(sizePolicy2)
        self.header_frame.setMaximumSize(QSize(16777215, 50))
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.header_frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_5 = QPushButton(self.header_frame)
        self.pushButton_5.setObjectName(u"pushButton_5")
        icon3 = QIcon()
        icon3.addFile(u":/newPrefix/icones/menu open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon3)
        self.pushButton_5.setIconSize(QSize(35, 35))

        self.horizontalLayout_4.addWidget(self.pushButton_5, 0, Qt.AlignLeft)

        self.label_3 = QLabel(self.header_frame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setMinimumSize(QSize(42, 49))
        font5 = QFont()
        font5.setFamilies([u"NovaFlat"])
        font5.setPointSize(16)
        font5.setBold(True)
        self.label_3.setFont(font5)
        self.label_3.setScaledContents(False)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.label_5 = QLabel(self.header_frame)
        self.label_5.setObjectName(u"label_5")
        sizePolicy2.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy2)
        font6 = QFont()
        font6.setFamilies([u"NovaFlat"])
        font6.setPointSize(14)
        font6.setBold(True)
        self.label_5.setFont(font6)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.header_nav = QFrame(self.header_frame)
        self.header_nav.setObjectName(u"header_nav")
        self.header_nav.setFrameShape(QFrame.StyledPanel)
        self.header_nav.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.header_nav)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.minimize_window_button = QPushButton(self.header_nav)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        icon4 = QIcon()
        icon4.addFile(u":/newPrefix/icones/remove.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_window_button.setIcon(icon4)
        self.minimize_window_button.setIconSize(QSize(25, 25))

        self.horizontalLayout_3.addWidget(self.minimize_window_button)

        self.restore_widow_button = QPushButton(self.header_nav)
        self.restore_widow_button.setObjectName(u"restore_widow_button")
        icon5 = QIcon()
        icon5.addFile(u":/newPrefix/icones/open is full.png", QSize(), QIcon.Normal, QIcon.Off)
        self.restore_widow_button.setIcon(icon5)
        self.restore_widow_button.setIconSize(QSize(25, 25))

        self.horizontalLayout_3.addWidget(self.restore_widow_button)

        self.close_window_button = QPushButton(self.header_nav)
        self.close_window_button.setObjectName(u"close_window_button")
        icon6 = QIcon()
        icon6.addFile(u":/newPrefix/icones/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window_button.setIcon(icon6)
        self.close_window_button.setIconSize(QSize(25, 25))

        self.horizontalLayout_3.addWidget(self.close_window_button)


        self.horizontalLayout_4.addWidget(self.header_nav, 0, Qt.AlignRight)


        self.verticalLayout_5.addWidget(self.header_frame, 0, Qt.AlignTop)

        self.frame_7 = QFrame(self.frame_8)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.stackedWidget = QStackedWidget(self.frame_7)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_6 = QVBoxLayout(self.page)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_7 = QVBoxLayout(self.page_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.stackedWidget.addWidget(self.page_3)

        self.horizontalLayout_5.addWidget(self.stackedWidget)


        self.verticalLayout_5.addWidget(self.frame_7)


        self.verticalLayout_4.addWidget(self.frame_8)


        self.horizontalLayout.addWidget(self.frame_6)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"VIOLENCE", None))
        self.map.setText(QCoreApplication.translate("MainWindow", u"MAPS", None))
        self.graphes.setText(QCoreApplication.translate("MainWindow", u"GRAPHES", None))
        self.moregraphes.setText(QCoreApplication.translate("MainWindow", u"MORE GRAPHES", None))
        self.pushButton_5.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"DASHBOARD", None))
        self.minimize_window_button.setText("")
        self.restore_widow_button.setText("")
        self.close_window_button.setText("")
    # retranslateUi

