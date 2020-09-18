#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: YangJingWei  PHPNOTE.CN
# Date: 2020-07-02 13:24:19  Python: 3.7

import os
import sys
from PIL import Image
import filetype
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, PYQT_VERSION_STR, QT_VERSION_STR, QSize
import threading
import types


class Main(QMainWindow):
    scriptTitle = 'WEBP TO JPG 图片格式批量转换工具'

    importPath = ''
    outputPath = ''
    fileList = []
    results = []

    # 设置载入文件路径
    def setImportPath(self, importPath):
        self.importPath = importPath
        return self.importPath

    # 设置导出文件路径
    def setOutputPath(self, outputPath):
        self.outputPath = outputPath
        return self.outputPath

    # 检查配置
    def checkConf(self):
        if os.path.isdir(self.importPath) and os.path.isdir(self.outputPath):
            return 1
        return 0

    # 转换
    def webp2jpg(self):
        print('webp2jpg...')
        self.fileList = os.listdir(self.importPath)
        for item in self.fileList:
            src = os.path.join(os.path.abspath(self.importPath), item)
            if os.path.isfile(src):
                kind = filetype.guess(src)
                if hasattr(kind, 'extension'):
                    if kind.extension == 'webp':
                        img = Image.open(src)
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        img.load()
                        save_name = '{}/{}'.format(self.outputPath, item)
                        img.save('{}'.format(save_name), 'JPEG')
                        msg = '文件: {}, 类型: {}, 状态: {}'.format(src, kind.extension, '已转换')
                    else:
                        msg = '文件: {}, 类型: {}, 状态: {}'.format(src, kind.extension, '未转换')
                    self.results.append(msg)
        return self.results

    def __init__(self):
        super().__init__()
        self.mainLayout()
        self.initMsg()

    def initMsg(self):
        msg = '''
---------------------------------------------
软件功能: 
批量将WEBP图片转换为JPG图片,
只针对WEBP格式, 导入文件夹中的其他文件不会受到影响,
文件转换后, 后缀不做修改, 
如果导入导出文件夹相同, 则会覆盖源文件! 
---------------------------------------------
        '''
        # self.textEdit.append(msg)
        # self.textBrowser.setText("<font color='red'>" + msg + "</font>")
        # self.textBrowser.setText(msg)
        self.textBrowser.append(msg)

    # 主界面布局
    def mainLayout(self):
        self.resize(600, 400)
        self.center()
        self.setWindowTitle(self.scriptTitle)
        self.createWidget()
        self.createMenuBar()
        self.statusBar().showMessage('上海微看文化传媒有限公司')

    # 构造菜单栏
    def createMenuBar(self):
        menubar = self.menuBar()
        toolMenu = menubar.addMenu('关于')
        doDesc = toolMenu.addAction('关于本软件')
        doDesc.triggered.connect(self.alert)
        doDesc.setStatusTip('关于本软件')
        doExit = QAction('&Exit', self)
        doExit.setShortcut('Ctrl+Q')
        doExit.setStatusTip('退出快捷键: Ctrl+Q')
        doExit.triggered.connect(qApp.quit)
        toolMenu.addAction(doExit)
        self.statusBar()


    def alert(self):
        title = '关于本软件'
        msg = '本软件出自: 上海微看文化传媒有限公司 技术组           '
        # QMessageBox.information(self, title, msg, QMessageBox.Close)
        QMessageBox.about(self, title, msg)
        # QMessageBox.information(self, title, msg, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        # wgt_tmp = QDialog()
        # wgt_tmp.setWindowModality(Qt.ApplicationModal)
        # wgt_tmp.setMinimumWidth(200)
        # wgt_tmp.setMinimumSize(QSize(200, 200))
        # # wgt_tmp.setStyleSheet('background-color: red;')
        # wgt_tmp.exec_()

    # 构建页面组件
    def createWidget(self):
        _widget = QWidget(self)
        self.setCentralWidget(_widget)
        # pyinstaller打包的话, 这里要用绝对路径,
        # self.setWindowIcon(QIcon('./static/imgs/favicon1.ico'))
        self.setWindowIcon(QIcon("D:/Projects/Python/Tools/webp2jpg/static/imgs/favicon1.ico"))

        self.importButton = QPushButton("导入文件夹")
        self.outputButton = QPushButton("导出文件夹")
        self.conversionButton = QPushButton("开始转换")

        hbox = QHBoxLayout()
        hbox.addWidget(self.importButton)
        hbox.addWidget(self.outputButton)
        hbox.addWidget(self.conversionButton)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        # self.textEdit = QTextEdit()
        # vbox.addWidget(self.textEdit)

        self.textBrowser = QTextBrowser(self)
        vbox.addWidget(self.textBrowser)

        _widget.setLayout(vbox)
        self.bindButtonClick()

    # 绑定按钮
    def bindButtonClick(self):
        self.importButton.clicked.connect(self.openImportDialog)
        self.outputButton.clicked.connect(self.openOutputDialog)
        self.conversionButton.clicked.connect(self.doConversion)

    # 转换
    def doConversion(self):
        check = self.checkConf()
        if check == 0:
            QMessageBox.warning(self, 'Warning', '请先设置文件夹    ')
            return
        t = threading.Thread(target=self.doStart)
        t.start()

    def doStart(self):
        self.textBrowser.append('转换中...')
        res = self.webp2jpg()
        # if len(res) > 0:
        #     for item in res:
        #         self.textBrowser.append(item)
        self.textBrowser.append('转换结束...')
        self.textBrowser.append('导出路径为: {}'.format(self.outputPath))


    # 导入文件夹弹窗
    def openImportDialog(self):
        default = './'
        get_directory_path = QFileDialog.getExistingDirectory(self, "选择导入文件夹", default)
        if get_directory_path:
            self.importPath = get_directory_path
            self.setImportPath(self.importPath)
            str = '导入路径为: {}'.format(self.importPath)
            self.textBrowser.append(str)
            # self.textEdit.append(str)
            # self.textBrowser.setText(str)


    # 导出文件夹弹窗 webp
    def openOutputDialog(self):
        default = self.importPath
        get_directory_path = QFileDialog.getExistingDirectory(self, "选择导出文件夹", default)
        if get_directory_path:
            self.outputPath = get_directory_path
            self.setOutputPath(self.outputPath)
            str = '导出路径为: {}'.format(self.outputPath)
            self.textBrowser.append(str)
            # self.textBrowser.append(str)
            # self.textEdit.append(str)


    # def textPush(self, str):
    #     self.textBrowser.append(str)
        # self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    # 设置居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    # 解决高分屏字体缩放的问题
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    font = QFont("宋体")
    pointsize = font.pointSize()
    font.setPixelSize(pointsize * 90 / 72)
    app.setFont(font)

    main = Main()
    main.show()
    sys.exit(app.exec_())
