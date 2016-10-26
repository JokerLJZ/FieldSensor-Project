"""docstring..."""
# -*- coding: utf-8 -*-

import threading
import os
import sys
import time
from Access import Access
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QGroupBox,
    QListWidget, QDateTimeEdit, QTextEdit, QRadioButton, QVBoxLayout)
from PyQt5.QtGui import QIcon


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class PrintDialog(QDialog):
    """class string."""

    def __init__(self):
        """__init__ string."""
        super(PrintDialog, self).__init__()
        self.setWindowTitle("打印")
        self.setWindowIcon(QIcon("images/WindowIcon.png"))
        self.setModal(True)
        self.InitDialog()
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stder = EmittingStream(textWritten=self.normalOutputWritten)
        self.closeEvent = self.CloseEvent

    def CloseEvent(self, event):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def InitDialog(self):
        """InitDialog docstring."""
        self.main_layout = QGridLayout()
        self.setMinimumWidth(1100)
        self.CreateWidget()
        self.list_box = self.CreateListBox()
        self.main_layout.addWidget(self.list_box, 0, 6, 12, 4)
        self.language_box = self.CreateLanguageBox()
        self.main_layout.addWidget(self.language_box, 13, 6, 3, 1)
        self.start_print_button = QPushButton("打印报告")
        self.start_print_button.setFont(
            QFont("黑体", 20))
        self.start_print_button.clicked.connect(
            lambda *args: self.StartPrintThread(report=True))
        self.start_print_original_button = QPushButton("打印原始记录")
        self.start_print_original_button.clicked.connect(
            lambda *args: self.StartPrintThread(report=False))
        self.start_print_original_button.setFont(
            QFont("黑体", 20))
        self.save_basicinfo_pushbutton.clicked.connect(self.SaveInfo)
        self.main_layout.addWidget(self.start_print_button, 13, 8)
        self.main_layout.addWidget(
            self.start_print_original_button, 15, 8)
        self.textedit = self.CreateTextEdit()
        self.main_layout.addWidget(self.textedit, 0, 11, 12, 10)
        self.setLayout(self.main_layout)

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textedit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textedit.setTextCursor(cursor)
        self.textedit.ensureCursorVisible()

    def CreateTextEdit(self):
        textedit = QTextEdit()
        textedit.setReadOnly(True)
        return textedit

    def CreateLanguageBox(self):
        language_ch_radiobutton = QRadioButton("中文")
        language_en_radiobutton = QRadioButton("英文")
        # language_chen_radiobutton = QRadioButton("中英文")
        language_ch_radiobutton.setChecked(True)
        language_box = QGroupBox("语言选择")
        language_box_layout = QVBoxLayout()
        language_box_layout.addWidget(language_ch_radiobutton)
        language_box_layout.addWidget(language_en_radiobutton)
        # language_box_layout.addWidget(language_chen_radiobutton)
        language_box.setLayout(language_box_layout)
        return language_box

    def CreateListBox(self):
        "Return the database object into a list box."
        list_box = QListWidget()
        dir = ("TestResult\\DataBase")
        filename = [
            obj for obj in list(os.walk(dir))[0][2]
            if (".mdb" in obj or ".accdb" in obj)]
        for obj in filename:
            list_box.addItem(obj)
        list_box.currentItemChanged.connect(self.ItemChanged)
        return list_box

    def StartPrint(self):
        th = threading.Thread(target=self.StartPrintThread)
        th.start()

    def StartPrintThread(self, report=True):
        self.start_print_button.setEnabled(False)
        time.sleep(10)
        self.start_print_button.setEnabled(True)

    def ItemChanged(self):
        db = Access(
            "TestResult\\DataBase\\%s" % self.list_box.currentItem().text())
        sql = ("SELECT TestDate FROM TestDate")
        date = db.cursor.execute(sql).fetchone()[0]
        sql = ("SELECT 设备名称, 制造厂家, 客户名称,客户地址, 型号规格, 出厂编号,"
               "资产编号, 温度高频, 相对湿度高频, 温度低频, 相对湿度低频")
        self.dbname = self.list_box.currentItem().text()

    def SaveInfo(self):
        pass

    def CreateWidget(self):
        """CreateWidget docstring."""
        cert_num_label = QLabel("证书编号")
        device_serial_label = QLabel("出厂编号")
        manufacturer_label = QLabel("制造厂家")
        device_name_label = QLabel("设备名称")
        device_type_label = QLabel("型号规格")
        custom_addr_label = QLabel("客户地址")
        custom_name_label = QLabel("客户名称")
        cal_addr_label = QLabel("校准地点")
        temperature_label = QLabel("温    度")
        humidity_label = QLabel("湿    度")
        tester_label = QLabel("测试人员")
        date_label = QLabel("测试日期")
        self.cert_num_lineedit = QLineEdit()  # 证书编号
        self.device_serial_lineedit = QLineEdit()  # 出厂编号
        self.manufacturer_lineedit = QLineEdit()    # 制造厂家
        self.device_name_lineedit = QLineEdit()    # 设备名称
        self.custom_addr_lineedit = QLineEdit()    # 客户地址
        self.custom_name_lineedit = QLineEdit()    # 客户名称
        self.device_type_lineedit = QLineEdit()    # 型号规格
        self.cal_addr_lineedit = QLineEdit()    # 校准地点
        self.temperature_lineedit = QLineEdit()    # 温度
        self.humidity_lineedit = QLineEdit()    # 湿度
        self.tester_lineedit = QLineEdit()    # 测试人员
        self.date_lineedit = QDateTimeEdit(QDateTime.currentDateTime())
        self.save_basicinfo_pushbutton = QPushButton("保存基本信息")
        self.save_basicinfo_pushbutton.setFont(
            QFont("黑体", 20))
        line_box = [
            cert_num_label, self.cert_num_lineedit,
            manufacturer_label, self.manufacturer_lineedit,
            device_name_label, self.device_name_lineedit,
            device_type_label, self.device_type_lineedit,
            device_serial_label, self.device_serial_lineedit,
            custom_addr_label, self.custom_addr_lineedit,
            custom_name_label, self.custom_name_lineedit,
            cal_addr_label, self.cal_addr_lineedit,
            temperature_label, self.temperature_lineedit,
            humidity_label, self.humidity_lineedit,
            tester_label, self.tester_lineedit,
            date_label, self.date_lineedit]
        widget_box = QGroupBox()
        widget_box_layout = QGridLayout()
        for i in range(len(line_box)):
            if i % 2 == 0:
                widget_box_layout.addWidget(
                    line_box[i], (i / 2), 0, 1, 1)
            else:
                widget_box_layout.addWidget(
                    line_box[i], (i - 1) / 2, 1, 1, 4)
        widget_box_layout.addWidget(
            self.save_basicinfo_pushbutton, len(line_box) / 2 + 1, 1, 1, 2)
        widget_box.setLayout(widget_box_layout)
        self.main_layout.addWidget(
            widget_box, 0, 0, len(line_box) / 2 + 1, 5)
        widget_box.setMinimumWidth(400)
        widget_box.setMaximumWidth(400)
        widget_box.setMinimumHeight(600)
        widget_box.setMaximumHeight(600)
