"""FSMainWindow create a interface for Field sensor caliberation programme.

Copyright (C) 2016 CTTL and TMC.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).

You could read the sorce code of this programme.
Commercial use was not allowed.
"""
# -*- coding: utf-8 -*-
from BasicMainWindow import MainWindow
from FSCentralBox import FSCentralBox
from FSSettingDialog import FSSettingDialog
from FSPrintDialog import FSPrintDialog
from FSTestDialog import FSTestDialog
from Access import Access

__author__ = "Joker.Liu"


class FSMainWindow(MainWindow):
    """The FSMainWindow class."""

    def __init__(self):
        """docstring."""

        self.setting_dialog = FSSettingDialog()
        self.central_box = FSCentralBox()
        self.test_dialog = FSTestDialog()

        super(FSMainWindow, self).__init__(
            setting_dialog=self.setting_dialog,
            central_box=self.central_box,
            test_dialog=self.test_dialog)

    def printing(self):
        """Printing string."""
        self.printing_dialog = FSPrintDialog()
        self.printing_dialog.show()

    def InsertDbInfo(self, db=None):
        lineeditlist = [
            obj.text() for obj in self.central_box.linebox[1::2]]
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
                if "温度" in infoname[i]:
                    infocontent = lineeditlist[i] + "℃"
                elif "湿度" in infoname[i]:
                    infocontent = lineeditlist[i] + "%"
                else:
                    infocontent = lineeditlist[i]
                content = (infoname[i], infocontent, flag[0], flag[1])
                db.cursor.execute(
                    "UPDATE TestInfo SET %s = '%s' WHERE %s = '%s'" % (
                        content))
                db.Commit()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mainWin = FSMainWindow()
    mainWin.show()
    sys.exit(app.exec_())
