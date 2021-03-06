"""docstring..."""
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton,
    QDateTimeEdit, QVBoxLayout, QDateTimeEdit)


class CentralBox(QWidget):
    """class string."""

    def __init__(self):
        """__init__ docstring."""
        super(CentralBox, self).__init__()
        self.init_box()

    def init_box(self):
        """init_box docstring."""
        self.main_layout = QGridLayout()
        self.linebox = self.CreateWidget()
        self.CreateEnterTest()
        self.setLayout(self.main_layout)
        self.StretchSet()
        self.CreateInfoBox()

    def CreateEnterTest(self):
        """CreateEnterTest docstring."""
        self.start_test_pushbutton = QPushButton("开始测试")    # 开始测试
        self.start_test_pushbutton.resize(6, 6)
        self.start_test_pushbutton.setFont(
            QFont("黑体", 30, QFont.Bold))
        self.main_layout.addWidget(
            self.start_test_pushbutton, 9, 5, 3, 3)

    def CreateInfoBox(self):
        """CreateTestBox docstring."""
        info_layout = QVBoxLayout()
        info_box = QGroupBox("客户信息")
        info_box.setMaximumWidth(110)
        info_box.setLayout(info_layout)
        self.main_layout.addWidget(info_box, 0, 5, 4, 3)

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
                line_box[i].setMaximumWidth(70)
            else:
                widget_box_layout.addWidget(
                    line_box[i], (i - 1) / 2, 1, 1, 4)
        widget_box_layout.addWidget(
            self.save_basicinfo_pushbutton, len(line_box) / 2, 1, 1, 2)
        widget_box_layout.addWidget(
            self.get_serial_num_pushbutton, len(line_box) / 2, 3, 1, 2)
        widget_box.setLayout(widget_box_layout)
        widget_box.setMinimumWidth(400)
        widget_box.setMaximumWidth(400)
        widget_box.setMinimumHeight(600)
        widget_box.setMaximumHeight(600)
        self.main_layout.addWidget(widget_box, 1, 1, 12, 4)
        return line_box

    def StretchSet(self):
        """StretchSet docstring."""
        self.main_layout.setColumnStretch(0, 0.5)
        self.main_layout.setColumnStretch(1, 2)
        self.main_layout.setColumnStretch(2, 1)
        self.main_layout.setColumnStretch(3, 1)
