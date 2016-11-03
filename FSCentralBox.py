"""FSCentralBox create a CentralBox for FSMainWindow.

Copyright (C) 2016 CTTL and TMC.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).

You could read the sorce code of this programme.
Commercial use was not allowed.
"""
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QDateTime
from BasicCentralBox import CentralBox
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QRadioButton,
                             QVBoxLayout, QGridLayout, QGroupBox, QDateTimeEdit
                             )
from Access import Access
__author__ = "Joker.Liu"


class FSCentralBox(CentralBox):
    """Class String."""

    def __init__(self):
        """__init__ docstring."""
        super(FSCentralBox, self).__init__()

    def CreateInfoBox(self):
        """CreateTestBox docstring."""
        self.defalt_info_radiobutton = QRadioButton("Defalt", self)
        self.ets_info_radiobutton = QRadioButton("ETS", self)
        self.safety_info_radiobutton = QRadioButton("Safety", self)
        self.narda_info_radiobutton = QRadioButton("Narda", self)
        self.cttl_info_radiobutton = QRadioButton("CTTL", self)
        self.defalt_info_radiobutton.setChecked(True)
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.defalt_info_radiobutton)
        info_layout.addWidget(self.ets_info_radiobutton)
        info_layout.addWidget(self.safety_info_radiobutton)
        info_layout.addWidget(self.narda_info_radiobutton)
        info_layout.addWidget(self.cttl_info_radiobutton)
        self.defalt_info_radiobutton.clicked.connect(self.InfoSelect)
        self.ets_info_radiobutton.clicked.connect(self.InfoSelect)
        self.safety_info_radiobutton.clicked.connect(self.InfoSelect)
        self.narda_info_radiobutton.clicked.connect(self.InfoSelect)
        self.cttl_info_radiobutton.clicked.connect(self.InfoSelect)
        info_box = QGroupBox("客户信息")
        info_box.setMaximumWidth(150)
        info_box.setLayout(info_layout)
        self.main_layout.addWidget(info_box, 0, 5, 6, 4)
        self.DefaltInfo()
        return info_box

    def DefaltInfo(self):
        sql = ("SELECT 证书编号, 客户地址, 客户名称, 设备名称, 电源电压, 校准地点"
               ",温度高频, 相对湿度高频, 温度低频, 相对湿度低频, 校准人, 核验人, "
               "制造厂家 FROM DefaltInfo WHERE 客户标识='Defalt'")
        basicdb = Access("Data\\BasicInfo.accdb")
        info = basicdb.cursor.execute(sql).fetchone()
        try:
            basicdb.Close()
        except:
            pass
        self.cert_num_lineedit.setText(info[0])
        self.custom_addr_lineedit.setText(info[1])
        self.custom_name_lineedit.setText(info[2])
        self.device_name_lineedit.setText(info[3])
        self.power_voltage_lineedit.setText(info[4])
        self.cal_addr_lineedit.setText(info[5])
        self.temperature_high_lineedit.setText(info[6])
        self.humidity_high_lineedit.setText(info[7])
        self.temperature_low_lineedit.setText(info[8])
        self.humidity_low_lineedit.setText(info[9])
        self.tester_lineedit.setText(info[10])
        self.verifier_lineedit.setText(info[11])
        self.manufacturer_lineedit.setText(info[12])

    def InfoSelect(self):
        if self.defalt_info_radiobutton.isChecked():
            custom = "Defalt"
        elif self.ets_info_radiobutton.isChecked():
            custom = "ETS"
        elif self.safety_info_radiobutton.isChecked():
            custom = "Safety"
        elif self.narda_info_radiobutton.isChecked():
            custom = "Narda"
        elif self.cttl_info_radiobutton.isChecked():
            custom = "CTTL"
        sql = ("SELECT 证书编号, 客户地址, 客户名称, 设备名称, 电源电压, 校准地点"
               ",温度高频, 相对湿度高频, 温度低频, 相对湿度低频, 校准人, 核验人, "
               "制造厂家 FROM DefaltInfo WHERE 客户标识='%s'" % custom)
        basicdb = Access("Data\\BasicInfo.accdb")
        info = basicdb.cursor.execute(sql).fetchone()
        self.cert_num_lineedit.setText(info[0])
        self.custom_addr_lineedit.setText(info[1])
        self.custom_name_lineedit.setText(info[2])
        self.device_name_lineedit.setText(info[3])
        self.power_voltage_lineedit.setText(info[4])
        self.cal_addr_lineedit.setText(info[5])
        self.temperature_high_lineedit.setText(info[6])
        self.humidity_high_lineedit.setText(info[7])
        self.temperature_low_lineedit.setText(info[8])
        self.humidity_low_lineedit.setText(info[9])
        self.tester_lineedit.setText(info[10])
        self.verifier_lineedit.setText(info[11])
        self.manufacturer_lineedit.setText(info[12])

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
        temperature_high_label = QLabel("温度高频")
        humidity_high_label = QLabel("湿度高频")
        temperature_low_label = QLabel("温度低频")
        humidity_low_label = QLabel("湿度低频")
        power_voltage_label = QLabel("电源电压")
        tester_label = QLabel("校准人员")
        verifier_label = QLabel("核验人员")
        date_label = QLabel("测试日期")
        self.cert_num_lineedit = QLineEdit()  # 证书编号
        self.device_serial_lineedit = QLineEdit()  # 出厂编号
        self.manufacturer_lineedit = QLineEdit()    # 制造厂家
        self.device_name_lineedit = QLineEdit()    # 设备名称
        self.custom_addr_lineedit = QLineEdit()    # 客户地址
        self.custom_name_lineedit = QLineEdit()    # 客户名称
        self.device_type_lineedit = QLineEdit()    # 型号规格
        self.cal_addr_lineedit = QLineEdit()    # 校准地点
        self.temperature_high_lineedit = QLineEdit()    # 温度
        self.humidity_high_lineedit = QLineEdit()    # 湿度
        self.temperature_low_lineedit = QLineEdit()    # 温度
        self.humidity_low_lineedit = QLineEdit()    # 湿度
        self.power_voltage_lineedit = QLineEdit()    # 电源电压
        self.tester_lineedit = QLineEdit()    # 测试人员
        self.verifier_lineedit = QLineEdit()    # 核验人员
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
            temperature_high_label, self.temperature_high_lineedit,
            humidity_high_label, self.humidity_high_lineedit,
            temperature_low_label, self.temperature_low_lineedit,
            humidity_low_label, self.humidity_low_lineedit,
            power_voltage_label, self.power_voltage_lineedit,
            tester_label, self.tester_lineedit,
            verifier_label, self.verifier_lineedit,
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
