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
        self.print_dialog = FSPrintDialog()
        self.central_box = FSCentralBox()
        self.test_dialog = FSTestDialog()

        super(FSMainWindow, self).__init__(
            setting_dialog=self.setting_dialog,
            print_dialog=self.print_dialog,
            central_box=self.central_box,
            test_dialog=self.test_dialog)

    def start(self):
        """start docstring."""
        self.central_box.start_test_pushbutton.setEnabled(False)
        self.test_dialog.closeEvent = self.close_event
        self.test_dialog.show()
        self.CreateDb()

    def CreateDb(self):
        cert_num = self.central_box.cert_num_lineedit.text() + "_"
        device_serial = self.central_box.device_serial_lineedit.text() + "_"
        custom_name = self.central_box.custom_name_lineedit.text()
        date = self.central_box.date_lineedit.date().toString("yyyy-MM-dd")
        self.dbname = cert_num + device_serial + custom_name
        db = Access("TestResult\\DataBase\\%s.accdb" % self.dbname)
        basicdb = Access("Data\\BasicInfo.accdb")
        namelist = basicdb.cursor.execute(
            "SELECT * FROM Infoname").fetchall()
        namelist = list(zip(*namelist))[0]
        db.CreateTable(
            tablename="TestInfo", columnnamelist=namelist,
            typelist=(["VARCHAR 30"] * namelist.__len__()))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mainWin = FSMainWindow()
    mainWin.show()
    sys.exit(app.exec_())
