"""FSTestDialog create a Test dialog for FSMainWindow.

Copyright (C) 2016 CTTL and TMC.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).

You could read the sorce code of this programme.
Commercial use was not allowed.
"""

from PyQt5.QtWidgets import (QRadioButton, QGridLayout, QGroupBox, QLineEdit,
                             QVBoxLayout, QLabel, QPushButton)
from BasicUI.TestDialog import TestDialog
from Access import Access
__author__ = "Joker.Liu"


class FSTestDialog(TestDialog):
    """
    FSTestDialog create a dialog for setting.

    The test dialog include the test option of the test programme.
    """

    def __init__(self):
        """Initial the setting dialog with modal mode."""
        super(FSTestDialog, self).__init__()
        self.basicinfo = Access("//Data//BasicInfo.accdb")
        self.InitDialog()

    def InitDialog(self):
        """init_dialog docstring."""
        self.main_layout = QGridLayout()
        freq_select_box = self.CreateFreqSelectBox()
        freq_disp_box = self.CreateFreqDispBox()
        freq_mode_box = self.CreateFreqModeBox()
        test_box = self.CreateTestBox()
        intensity_dist_box = self.CreateIntensityDispBox()
        self.main_layout.addWidget(freq_select_box, 0, 0, 1, 2)
        self.main_layout.addWidget(freq_mode_box, 1, 0, 1, 2)
        self.main_layout.addWidget(freq_disp_box, 0, 2, 2, 4)
        self.main_layout.addWidget(intensity_dist_box, 0, 6, 2, 4)
        self.main_layout.addWidget(test_box, 1, 11, 1, 2)
        self.setLayout(self.main_layout)

    def CreateTestBox(self):
        """CreateTestBox docstring."""
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

    def CreateFreqSelectBox(self):
        """CreateFreqSelectBox docstring."""
        self.high_freq_radiobutton = QRadioButton("1GHz-18GHz", self)
        self.low_freq_radiobutton = QRadioButton("10MHz-1GHz", self)
        self.high_freq_radiobutton.setChecked(True)
        self.high_freq_radiobutton.clicked.connect(
            lambda *args: self.NormMode())
        self.low_freq_radiobutton.clicked.connect(
            lambda *args: self.NormMode())

        freq_select_layout = QVBoxLayout()
        freq_select_layout.addWidget(self.high_freq_radiobutton)
        freq_select_layout.addWidget(self.low_freq_radiobutton)
        freq_select_box = QGroupBox("频率选择")
        freq_select_box.setMaximumWidth(110)
        freq_select_box.setLayout(freq_select_layout)

        return freq_select_box

    def CreateFreqModeBox(self):
        """CreateFreqModeBox."""
        self.freq_NormMode = QRadioButton("常规频点")
        self.freq_ets_mode = QRadioButton("ETS定制频点")
        self.freq_opt_mode = QRadioButton("自定义频点")
        self.freq_NormMode.setChecked(True)
        self.freq_NormMode.clicked.connect(
            lambda *args: self.NormMode())
        self.freq_ets_mode.clicked.connect(
            lambda *args: self.NormMode())
        self.freq_opt_mode.clicked.connect(
            lambda *args: self.NormMode())

        freq_mode_layout = QVBoxLayout()
        freq_mode_layout.addWidget(self.freq_NormMode)
        freq_mode_layout.addWidget(self.freq_ets_mode)
        freq_mode_layout.addWidget(self.freq_opt_mode)
        freq_mode_box = QGroupBox("频点设置")
        freq_mode_box.setMaximumWidth(110)
        freq_mode_box.setLayout(freq_mode_layout)

        return freq_mode_box

    def CreateFreqDispBox(self):
        """Create the frequency display lineedit groupbox."""
        freq_lineedit1 = QLineEdit()
        freq_lineedit2 = QLineEdit()
        freq_lineedit3 = QLineEdit()
        freq_lineedit4 = QLineEdit()
        freq_lineedit5 = QLineEdit()
        freq_lineedit6 = QLineEdit()
        freq_lineedit7 = QLineEdit()
        freq_lineedit8 = QLineEdit()
        freq_lineedit9 = QLineEdit()
        freq_lineedit10 = QLineEdit()
        freq_lineedit11 = QLineEdit()
        freq_lineedit12 = QLineEdit()
        freq_lineedit13 = QLineEdit()
        freq_lineedit14 = QLineEdit()
        freq_disp_box = QGroupBox("频率设置")
        freq_disp_layout = QGridLayout()
        freq_disp_box.setLayout(freq_disp_layout)
        self.freq_lineedit_box = [
            freq_lineedit1, freq_lineedit2,
            freq_lineedit3, freq_lineedit4,
            freq_lineedit5, freq_lineedit6,
            freq_lineedit7, freq_lineedit8,
            freq_lineedit9, freq_lineedit10,
            freq_lineedit11, freq_lineedit12,
            freq_lineedit13, freq_lineedit14]
        for i in self.freq_lineedit_box:
            freq_disp_layout.addWidget(i, self.freq_lineedit_box.index(i), 1)
        freq_label_seq = [QLabel("频率" + str(i)) for i in range(1, 15)]
        for i in freq_label_seq:
            freq_disp_layout.addWidget(i, freq_label_seq.index(i), 0)
        sql = "SELECT NormModeHigh FROM FrequencyList"
        frequency_list = self.basicinfo.cursor.execute(sql).fetchall()
        frequency_list = list(zip(*frequency_list))[0]
        for i in range(len(frequency_list)):
            if frequency_list[i] is not None:
                self.freq_lineedit_box[i].setText(str(frequency_list[i]))
            else:
                self.freq_lineedit_box[i].clear()
        return freq_disp_box

    def CreateIntensityDispBox(self):
        """Create the intensity select box."""
        intensity_lineedit1 = QLineEdit()
        intensity_lineedit2 = QLineEdit()
        intensity_lineedit3 = QLineEdit()
        intensity_lineedit4 = QLineEdit()
        intensity_lineedit5 = QLineEdit()
        intensity_lineedit6 = QLineEdit()
        intensity_lineedit7 = QLineEdit()
        intensity_lineedit8 = QLineEdit()
        intensity_lineedit9 = QLineEdit()
        intensity_lineedit10 = QLineEdit()
        intensity_lineedit11 = QLineEdit()
        intensity_lineedit12 = QLineEdit()
        intensity_lineedit13 = QLineEdit()
        intensity_lineedit14 = QLineEdit()
        intensity_disp_box = QGroupBox("场强设置")
        intensity_disp_layout = QGridLayout()
        intensity_disp_box.setLayout(intensity_disp_layout)
        self.intensity_lineedit_box = [
            intensity_lineedit1, intensity_lineedit2,
            intensity_lineedit3, intensity_lineedit4,
            intensity_lineedit5, intensity_lineedit6,
            intensity_lineedit7, intensity_lineedit8,
            intensity_lineedit9, intensity_lineedit10,
            intensity_lineedit11, intensity_lineedit12,
            intensity_lineedit13, intensity_lineedit14]
        for i in self.intensity_lineedit_box:
            intensity_disp_layout.addWidget(
                i, self.intensity_lineedit_box.index(i), 1)
        intensity_label_seq = [
            QLabel("场强" + str(i)) for i in range(1, 15)]
        for i in intensity_label_seq:
            intensity_disp_layout.addWidget(i, intensity_label_seq.index(i), 0)
        return intensity_disp_box

    def NormMode(self):
        """NormMode docstring.

           ==============   ============================================
           **Argument:**
           freq_sel:        default is True
                            when set True frequency list is 1GHz-18GHz
                            when set False frequency list is 10MHz-1GHz
           ==============   ============================================

        """
        mode_checkbox = [
            self.freq_NormMode.isChecked(),
            self.freq_ets_mode.isChecked(),
            self.freq_opt_mode.isChecked()]
        freq_checkbox = [
            self.high_freq_radiobutton.isChecked(),
            self.low_freq_radiobutton.isChecked()]
        if mode_checkbox[0] and freq_checkbox[0]:
            sql = "SELECT NormModeHigh FROM FrequencyList"
            frequency_list = self.basicinfo.cursor.execute(sql).fetchall()
            frequency_list = list(zip(*frequency_list))[0]
        elif mode_checkbox[0] and freq_checkbox[1]:
            sql = "SELECT NormModeLow FROM FrequencyList"
            frequency_list = self.basicinfo.cursor.execute(sql).fetchall()
            frequency_list = list(zip(*frequency_list))[0]
        elif mode_checkbox[1] and freq_checkbox[0]:
            sql = "SELECT ETSModeHigh FROM FrequencyList"
            frequency_list = self.basicinfo.cursor.execute(sql).fetchall()
            frequency_list = list(zip(*frequency_list))[0]
        elif mode_checkbox[1] and freq_checkbox[1]:
            sql = "SELECT ETSModeLow FROM FrequencyList"
            frequency_list = self.basicinfo.cursor.execute(sql).fetchall()
            frequency_list = list(zip(*frequency_list))[0]
        else:
            frequency_list = [None]
        for i in range(len(frequency_list)):
            if frequency_list[i] is not None:
                self.freq_lineedit_box[i].setText(str(frequency_list[i]))
            else:
                self.freq_lineedit_box[i].clear()
        for i in range(len(frequency_list), len(self.freq_lineedit_box)):
            self.freq_lineedit_box[i].clear()
