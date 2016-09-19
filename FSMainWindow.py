"""FSMainWindow create a interface for Field sensor caliberation programme.

Copyright (C) 2016 CTTL and TMC.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).

You could read the sorce code of this programme.
Commercial use was not allowed.
"""
# -*- coding: utf-8 -*-
from BasicUI.MainWindow import MainWindow
from FSCentralBox import FSCentralBox
from FSSettingDialog import FSSettingDialog
from FSPrintDialog import FSPrintDialog
from FSTestDialog import FSTestDialog
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


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mainWin = FSMainWindow()
    mainWin.show()
    sys.exit(app.exec_())
