"""FSTestDialog create a Test dialog for FSMainWindow.

Copyright (C) 2016 CTTL and TMC.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).

You could read the sorce code of this programme.
Commercial use was not allowed.
"""

from PyQt5.QtWidgets import (QRadioButton, QGridLayout, QGroupBox, QLineEdit,
                             QVBoxLayout, QLabel, QPushButton)
from BasicUI.TestDialog import TestDialog
__author__ = "Joker.Liu"


class FSTestDialog(TestDialog):
    """
    FSTestDialog create a dialog for setting.

    The test dialog include the test option of the test programme.
    """

    def __init__(self):
        """Initial the setting dialog with modal mode."""
        super(FSTestDialog, self).__init__()
        self.init_dialog()

    def init_dialog(self):
        """init_dialog docstring."""
        self.main_layout = QGridLayout()
        freq_select_box = self.create_freq_select_box()
        freq_disp_box = self.create_freq_disp_box()
        freq_mode_box = self.create_freq_mode_box()
        test_box = self.create_test_box()
        self.main_layout.addWidget(freq_select_box, 0, 0, 1, 2)
        self.main_layout.addWidget(freq_mode_box, 1, 0, 1, 2)
        self.main_layout.addWidget(freq_disp_box, 0, 2, 2, 4)
        self.main_layout.addWidget(test_box, 1, 7, 1, 2)
        self.setLayout(self.main_layout)

    def create_test_box(self):
        """create_test_box docstring."""
        self.start_test_button = QPushButton("开始测试")
        self.pause_test_button = QPushButton("暂停测试")
        self.stop_test_button = QPushButton("停止测试")
        test_box_layout = QVBoxLayout()
        test_box_layout.addWidget(self.start_test_button)
        test_box_layout.addWidget(self.pause_test_button)
        test_box_layout.addWidget(self.stop_test_button)
        test_box = QGroupBox()
        test_box.setLayout(test_box_layout)
        # test_box.setMaximumWidth(100)
        return test_box

    def create_freq_select_box(self):
        """create_freq_select_box docstring."""
        self.high_freq_radiobutton = QRadioButton("1GHz-18GHz", self)
        self.low_freq_radiobutton = QRadioButton("10MHz-1GHz", self)
        self.high_freq_radiobutton.setChecked(True)
        self.high_freq_radiobutton.clicked.connect(
            lambda *args: self.norm_mode())
        self.low_freq_radiobutton.clicked.connect(
            lambda *args: self.norm_mode())

        freq_select_layout = QVBoxLayout()
        freq_select_layout.addWidget(self.high_freq_radiobutton)
        freq_select_layout.addWidget(self.low_freq_radiobutton)
        freq_select_box = QGroupBox("频率选择")
        freq_select_box.setMaximumWidth(110)
        freq_select_box.setLayout(freq_select_layout)

        return freq_select_box

    def create_freq_mode_box(self):
        """create_freq_mode_box."""
        self.freq_norm_mode = QRadioButton("常规频点")
        self.freq_ets_mode = QRadioButton("ETS定制频点")
        self.freq_opt_mode = QRadioButton("自定义频点")
        self.freq_norm_mode.setChecked(True)
        self.freq_norm_mode.clicked.connect(
            lambda *args: self.norm_mode())
        self.freq_ets_mode.clicked.connect(
            lambda *args: self.norm_mode())
        self.freq_opt_mode.clicked.connect(
            lambda *args: self.norm_mode())

        freq_mode_layout = QVBoxLayout()
        freq_mode_layout.addWidget(self.freq_norm_mode)
        freq_mode_layout.addWidget(self.freq_ets_mode)
        freq_mode_layout.addWidget(self.freq_opt_mode)
        freq_mode_box = QGroupBox("频点设置")
        freq_mode_box.setMaximumWidth(110)
        freq_mode_box.setLayout(freq_mode_layout)

        return freq_mode_box

    def create_freq_disp_box(self):
        """Create the frequency display lineedit groupbox."""
        self.freq_lineedit1 = QLineEdit()
        self.freq_lineedit2 = QLineEdit()
        self.freq_lineedit3 = QLineEdit()
        self.freq_lineedit4 = QLineEdit()
        self.freq_lineedit5 = QLineEdit()
        self.freq_lineedit6 = QLineEdit()
        self.freq_lineedit7 = QLineEdit()
        self.freq_lineedit8 = QLineEdit()
        self.freq_lineedit9 = QLineEdit()
        self.freq_lineedit10 = QLineEdit()
        self.freq_lineedit11 = QLineEdit()
        self.freq_lineedit12 = QLineEdit()
        self.freq_lineedit13 = QLineEdit()
        self.freq_lineedit14 = QLineEdit()
        freq_disp_box = QGroupBox("频率设置")
        freq_disp_layout = QGridLayout()
        freq_disp_box.setLayout(freq_disp_layout)
        self.freq_lineedit_box = [
            self.freq_lineedit1, self.freq_lineedit2,
            self.freq_lineedit3, self.freq_lineedit4,
            self.freq_lineedit5, self.freq_lineedit6,
            self.freq_lineedit7, self.freq_lineedit8,
            self.freq_lineedit9, self.freq_lineedit10,
            self.freq_lineedit11, self.freq_lineedit12,
            self.freq_lineedit13, self.freq_lineedit14]
        for i in self.freq_lineedit_box:
            freq_disp_layout.addWidget(i, self.freq_lineedit_box.index(i), 1)
        freq_label_seq = [QLabel("频率" + str(i)) for i in range(1, 15)]
        for i in freq_label_seq:
            freq_disp_layout.addWidget(i, freq_label_seq.index(i), 0)

        return freq_disp_box

    def norm_mode(self):
        """norm_mode docstring.

           ==============   ============================================
           **Argument:**
           freq_sel:        default is True
                            when set True frequency list is 1GHz-18GHz
                            when set False frequency list is 10MHz-1GHz
           ==============   ============================================

        """
        mode_checkbox = [
            self.freq_norm_mode.isChecked(),
            self.freq_ets_mode.isChecked(),
            self.freq_opt_mode.isChecked()]
        freq_checkbox = [
            self.high_freq_radiobutton.isChecked(),
            self.low_freq_radiobutton.isChecked()]
        if mode_checkbox[0] and freq_checkbox[0]:
            frequency_list = [
                1800, 2450, 4800, 5800, 8000,
                10000, 12000, 15000, 18000, None]
        elif mode_checkbox[0] and freq_checkbox[1]:
            frequency_list = [
                30, 50, 100, 200, 300, 400,
                500, 600, 700, 790, 910]
        elif mode_checkbox[1] and freq_checkbox[0]:
            frequency_list = [
                1800, 2450, 4800, 5800, 8000,
                10000, 12000, 15000, 18000]
        elif mode_checkbox[1] and freq_checkbox[1]:
            frequency_list = [
                20, 50, 100, 200, 300, 400,
                500, 600, 700, 790, 910]
        elif mode_checkbox[2] and freq_checkbox[0]:
            frequency_list = [
                1800, 2450, 4800, 5800, 8000,
                10000, 12000, 15000, 18000]
        elif mode_checkbox[2] and freq_checkbox[1]:
            frequency_list = [
                20, 50, 100, 200, 300, 400,
                500, 600, 700, 790, 910]
        else:
            frequency_list = [1]
        for i in range(len(frequency_list)):
            self.freq_lineedit_box[i].setText(str(frequency_list[i]))
        self.freq_lineedit_box[1].clear()
