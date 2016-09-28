"""docstring..."""
# -*- coding: utf-8 -*-

import os
from Access import Access
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton,
                             QGridLayout, QGroupBox, QListWidget)
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
        self.main_layout.addWidget(self.list_box, 1, 6, 6, 3)
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

    def ItemChanged(self):
        db = Access(
            "TestResult\\DataBase\\%s" % self.list_box.currentItem().text())
        sql = ("SELECT TestDate FROM TestDate")
        date = db.cursor.execute(sql).fetchone()[0]
        sql = ("SELECT 设备名称, 制造厂家,客户名称,客户地址, 型号规格, 出厂编号,"
               "资产编号, 温度高频, 相对湿度高频, 温度低频, 相对湿度低频")

    def CreateWidget(self):
        """CreateWidget docstring."""
        cert_num_label = QLabel("证书编号")
        device_serial_label = QLabel("设备序号")
        manufacturer_label = QLabel("生产厂家")
        device_name_label = QLabel("设备名称")
        device_type_label = QLabel("设备型号")
        custom_addr_label = QLabel("客户地址")
        custom_name_label = QLabel("客户名称")
        cal_addr_label = QLabel("校准地点")
        temperature_high_label = QLabel("温度高频")
        humidity_high_label = QLabel("湿度高频")
        temperature_low_label = QLabel("温度低频")
        humidity_low_label = QLabel("湿度低频")
        tester_label = QLabel("测试人员")
        date_label = QLabel("测试日期")
        self.cert_num_lineedit = QLineEdit()  # 证书编号
        self.device_serial_lineedit = QLineEdit()  # 设备序号
        self.manufacturer_lineedit = QLineEdit()    # 生产厂家
        self.device_name_lineedit = QLineEdit()    # 设备名称
        self.custom_addr_lineedit = QLineEdit()    # 客户地址
        self.custom_name_lineedit = QLineEdit()    # 客户名称
        self.device_type_lineedit = QLineEdit()    # 设备型号
        self.cal_addr_lineedit = QLineEdit()    # 校准地点
        self.temperature_high_lineedit = QLineEdit()    # 温度
        self.humidity_high_lineedit = QLineEdit()    # 湿度
        self.temperature_low_lineedit = QLineEdit()    # 温度
        self.humidity_low_lineedit = QLineEdit()    # 湿度
        self.tester_lineedit = QLineEdit()    # 测试人员
        self.date_lineedit = QLineEdit()    # 测试日期
        self.save_basicinfo_pushbutton = QPushButton("保存基本信息")
        self.get_serial_num_pushbutton = QPushButton("获取序列号")
        line_box = [
            cert_num_label, self.cert_num_lineedit,
            manufacturer_label, self.manufacturer_lineedit,
            device_name_label, self.device_name_lineedit,
            device_type_label, self.device_type_lineedit,
            device_serial_label, self.device_serial_lineedit,
            custom_addr_label, self.custom_addr_lineedit,
            custom_name_label, self.custom_name_lineedit,
            cal_addr_label, self.cal_addr_lineedit,
            temperature_high_label, self.temperature_high_lineedit,
            humidity_high_label, self.humidity_high_lineedit,
            temperature_low_label, self.temperature_low_lineedit,
            humidity_low_label, self.humidity_low_lineedit,
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
