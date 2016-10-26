"""FSPrintDialog create a Print dialog for FSMainWindow.

Copyright (C) 2016 CTTL and TMC.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).

You could read the sorce code of this programme.
Commercial use was not allowed.
"""
# -*- coding: utf-8 -*-
import os
from BasicPrintDialog import PrintDialog
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QDateTimeEdit, QPushButton, QGroupBox, QGridLayout,
    QListWidget, QMessageBox)
from Access import Access
from PrintReport import FSPrintReport
__author__ = "Joker.Liu"


class FSPrintDialog(PrintDialog):
    """
    FSPrintDialog create a dialog for setting.

    The setting dialog include the configuration option of the test programme.
    """

    def __init__(self):
        """Initial the setting dialog with modal mode."""
        super(FSPrintDialog, self).__init__()

    def StartPrintThread(self, report=True):
        self.start_print_button.setEnabled(False)
        for i in range(1, len(self.language_box.children())):
            if self.language_box.children()[i].isChecked():
                language = i - 1
        try:
            if ".mdb" in self.dbname:
                filename = self.dbname[: len(self.dbname) - 4]
            elif ".accdb" in self.dbname:
                filename = self.dbname[: len(self.dbname) - 6]
            else:
                filename = "校准报告"
            report = FSPrintReport(
                filename=filename, dbname=self.dbname, report=report,
                language=language)
        except:
            print("数据库有误, 请重新选择")
            self.start_print_button.setEnabled(True)
            return None
        try:
            report.PrintInfo()
        except:
            print("打印基础信息错误")
        try:
            report.PrintDate()
        except:
            print("打印日期错误")
        try:
            report.PrintCertNum()
        except:
            print("打印证书序列号错误")
        try:
            report.PrintInstrument()
        except:
            print("打印设备信息错误")
        try:
            report.PrintFrequencyResponse()
        except:
            print("打印频率响应错误")
        try:
            report.PrintFieldLinearity()
        except:
            print("打印场强线性度错误")
        try:
            report.PrintIsotropy()
        except:
            print("打印全向性错误")
        report.doc.DocSave(report.doc.filename)
        self.start_print_button.setEnabled(True)

    def SaveInfo(self):
        db = Access("TestResult\\DataBase\\%s" % self.dbname)
        lineeditlist = [
            obj.text() for obj in self.linebox[1::2]]
        lineeditlist.pop(len(lineeditlist) - 1)
        infoname = ["证书编号", "制造厂家", "设备名称", "型号规格", "出厂编号",
                    "客户地址", "客户名称", "校准地点", "温度高频",
                    "相对湿度高频", "温度低频", "相对湿度低频", "电源电压",
                    "校准人", "核验人"]
        if db.IsTableContentExist("TestInfo"):
            db.cursor.execute("DELETE FROM TestInfo")
        for i in range(len(infoname)):
            if i == 0:
                content = (infoname[i], lineeditlist[i])
                flag = content
                db.cursor.execute(
                    "INSERT INTO TestInfo (%s) VALUES ('%s')" % content)
                db.Commit()
            else:
                if "温度" in infoname[i] and "℃" not in lineeditlist[i]:
                    infocontent = lineeditlist[i] + "℃"
                elif "湿度" in infoname[i] and "%" not in lineeditlist[i]:
                    infocontent = lineeditlist[i] + "%"
                else:
                    infocontent = lineeditlist[i]
                content = (infoname[i], infocontent, flag[0], flag[1])
                db.cursor.execute(
                    "UPDATE TestInfo SET %s = '%s' WHERE %s = '%s'" % (
                        content))
                db.Commit()
        db.cursor.execute("DELETE FROM TestDate")
        datetime = self.date_lineedit.dateTime().toString(
            "#yyyy-MM-dd HH:MM:ss#")
        db.CreateSerial(datetime)

    def ItemChanged(self):
        db = Access(
            "TestResult\\DataBase\\%s" % self.list_box.currentItem().text())
        sql = ("SELECT * FROM TestDate")
        date = db.cursor.execute(sql).fetchone()[0]
        sql = ("SELECT 证书编号, 客户地址, 客户名称, 设备名称, 电源电压, 校准地点"
               ",温度高频, 相对湿度高频, 温度低频, 相对湿度低频, 校准人, 核验人, "
               "制造厂家, 型号规格, 出厂编号 FROM TestInfo")
        info = db.cursor.execute(sql).fetchone()
        infobox = [
            self.cert_num_lineedit,
            self.custom_addr_lineedit,
            self.custom_name_lineedit,
            self.device_name_lineedit,
            self.power_voltage_lineedit,
            self.cal_addr_lineedit,
            self.temperature_high_lineedit,
            self.humidity_high_lineedit,
            self.temperature_low_lineedit,
            self.humidity_low_lineedit,
            self.tester_lineedit,
            self.verifier_lineedit,
            self.manufacturer_lineedit,
            self.device_type_lineedit,
            self.device_serial_lineedit]
        for i in range(len(infobox)):
            infobox[i].setText(info[i])
        date = db.cursor.execute("SELECT TestDate FROM TestDate").fetchone()[0]
        self.date_lineedit.setDate(date)
        db.ConnClose()
        self.dbname = self.list_box.currentItem().text()
        self.infobox = infobox
        self.infocolumn = (
            "证书编号, 客户地址, 客户名称, 设备名称, 电源电压, 校准地点, "
            "温度高频, 相对湿度高频, 温度低频, 相对湿度低频, 校准人, 核验人, "
            "制造厂家, 型号规格, 出厂编号")

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
        self.linebox = line_box
