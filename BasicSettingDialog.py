"""docstring..."""
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon


class SettingDialog(QDialog):
    """class docstring."""

    def __init__(self):
        """__init__ docstring."""
        super(SettingDialog, self).__init__()
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon("images/WindowIcon.png"))
        self.setModal(True)
