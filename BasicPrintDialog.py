"""docstring..."""
# -*- coding: utf-8 -*-

import threading
import os
import time
from Access import Access
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QGroupBox,
    QListWidget, QDateTimeEdit, QTextEdit)
from PyQt5.QtGui import QIcon


class PrintDialog(QDialog):
    """class string."""

    def __init__(self):
        """__init__ string."""
        super(PrintDialog, self).__init__()
        self.setWindowTitle("打印")
        self.setWindowIcon(QIcon("images/WindowIcon.png"))
        self.setModal(True)
        self.InitDialog()

    def InitDialog(self):
        """InitDialog docstring."""
        self.main_layout = QGridLayout()
        self.CreateWidget()
        self.list_box = self.CreateListBox()
        self.main_layout.addWidget(self.list_box, 0, 6, 8, 4)
        self.start_print_button = QPushButton("打印报告")
        self.start_print_button.clicked.connect(self.StartPrint)
        self.save_basicinfo_pushbutton.clicked.connect(self.SaveInfo)
        self.main_layout.addWidget(self.start_print_button, 14, 7, 3, 2)
        self.textedit = QTextEdit()
        self.main_layout.addWidget(self.textedit, 0, 11, 12, 6)
        self.setLayout(self.main_layout)

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

    def StartPrintThread(self):
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
