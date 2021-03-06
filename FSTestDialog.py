"""FSTestDialog create a Test dialog for FSMainWindow.

Copyright (C) 2016 CTTL and TMC.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).

You could read the sorce code of this programme.
Commercial use was not allowed.
"""
import time
import threading

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QRadioButton, QTextEdit,
                             QVBoxLayout, QInputDialog)

from Access import Access
from BasicTestDialog import EmittingStream, TestDialog
from ProbeTest import ProbeTest

__author__ = "Joker.Liu"


class FSTestDialog(TestDialog):
    """
    FSTestDialog create a dialog for setting.

    The test dialog include the test option of the test programme.
    """
    _valuesentsignal = pyqtSignal(float)

    def __init__(self, dbname=None):
        """Initial the setting dialog with modal mode."""
        super(FSTestDialog, self).__init__(dbname=dbname)
        self.dbname = dbname

    def InitDialog(self):
        """init_dialog docstring."""
        self.main_layout = QGridLayout()
        textedit_box, self.textedit = self.CreateTextEditBox()
        freq_select_box = self.CreateFreqSelectBox()
        freq_disp_box = self.CreateFreqDispBox()
        freq_mode_box = self.CreateFreqModeBox()
        intens_mode_box = self.CreateIntensityModeBox()
        intensity_disp_box = self.CreateIntensityDispBox()
        test_box = self.CreateTestBox()
        isotropy_select_box = self.CreateIsotropySelectBox()
        instrument_addr_box = self.CreateInstrumentAddrBox()
        probe_type_box = self.CreateProbeTypeBox()
        self.main_layout.addWidget(freq_select_box, 0, 0, 1, 2)
        self.main_layout.addWidget(freq_mode_box, 1, 0, 1, 2)
        self.main_layout.addWidget(freq_disp_box, 0, 4, 3, 4)
        self.main_layout.addWidget(intensity_disp_box, 0, 8, 3, 4)
        self.main_layout.addWidget(probe_type_box, 2, 0, 1, 2)
        self.main_layout.addWidget(isotropy_select_box, 0, 2, 1, 2)
        self.main_layout.addWidget(intens_mode_box, 1, 2, 1, 2)
        self.main_layout.addWidget(test_box, 3, 12, 6, 4)
        self.main_layout.addWidget(textedit_box, 3, 0, 4, 12)
        self.main_layout.addWidget(instrument_addr_box, 0, 12, 3, 4)
        self.StretchSet()
        self.setLayout(self.main_layout)

    def StretchSet(self):
        """StretchSet docstring."""
        self.setMinimumHeight(580)
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(1, 1)
        self.main_layout.setRowStretch(2, 1)
        self.main_layout.setRowStretch(3, 4)

    def CreateTextEditBox(self):
        textedit = QTextEdit()
        textedit.setReadOnly(True)
        textedit_box = QGroupBox("实时信息监控")
        layout = QVBoxLayout()
        layout.addWidget(textedit)
        textedit_box.setLayout(layout)
        return textedit_box, textedit

    def CreateTestBox(self):
        """CreateTestBox docstring."""
        self.start_test_button = QPushButton("开始测试")
        self.pause_test_button = QPushButton("暂停测试")
        self.stop_test_button = QPushButton("停止测试")
        self.start_test_button.clicked.connect(self.StartTest)
        self.stop_test_button.clicked.connect(self.StopTest)
        self.start_test_button.setEnabled(True)
        self.stop_test_button.setEnabled(False)
        test_box_layout = QVBoxLayout()
        test_box_layout.addWidget(self.start_test_button)
        test_box_layout.addWidget(self.pause_test_button)
        test_box_layout.addWidget(self.stop_test_button)
        test_box = QGroupBox()
        test_box.setLayout(test_box_layout)
        return test_box

    def CreateFreqSelectBox(self):
        """CreateFreqSelectBox docstring."""

        self.high_freq_radiobutton = QRadioButton("1GHz-18GHz", self)
        self.low_freq_radiobutton = QRadioButton("10MHz-1GHz", self)
        self.high_freq_radiobutton.setChecked(True)
        self.high_freq_radiobutton.clicked.connect(
            lambda *args: self.FreqSelMode())
        self.low_freq_radiobutton.clicked.connect(
            lambda *args: self.FreqSelMode())
        self.high_freq_radiobutton.clicked.connect(
            lambda *args: self.IntensSelMode())
        self.low_freq_radiobutton.clicked.connect(
            lambda *args: self.IntensSelMode())
        freq_select_layout = QVBoxLayout()
        freq_select_layout.addWidget(self.high_freq_radiobutton)
        freq_select_layout.addWidget(self.low_freq_radiobutton)
        freq_select_box = QGroupBox("频率选择")
        freq_select_box.setMaximumWidth(110)
        freq_select_box.setLayout(freq_select_layout)

        return freq_select_box

    def CreateIsotropySelectBox(self):
        self.isotropy_false_radiobutton = QRadioButton("非全向性测试", self)
        self.isotropy_true_radiobutton = QRadioButton("全向性测试", self)
        self.isotropy_false_radiobutton.setChecked(True)
        self.isotropy_true_radiobutton.clicked.connect(
            self.SelectIsotropy)
        self.isotropy_false_radiobutton.clicked.connect(
            self.UnSelectedIsotropy)
        isotropy_select_layout = QVBoxLayout()
        isotropy_select_layout.addWidget(self.isotropy_false_radiobutton)
        isotropy_select_layout.addWidget(self.isotropy_true_radiobutton)
        isotropy_select_box = QGroupBox("全向性测试")
        isotropy_select_box.setMaximumWidth(110)
        isotropy_select_box.setLayout(isotropy_select_layout)

        return isotropy_select_box

    def SelectIsotropy(self):
        self.freq_norm_mode.setEnabled(False)
        self.freq_ets_mode.setEnabled(False)
        # self.freq_opt_mode.setEnabled(False)
        self.low_freq_radiobutton.disconnect()
        self.low_freq_radiobutton.clicked.connect(self.SetIsotropy)
        self.high_freq_radiobutton.disconnect()
        self.high_freq_radiobutton.clicked.connect(self.SetIsotropy)
        self.intens_freqres_mode.setEnabled(False)
        self.intens_linear_mode.setEnabled(False)
        # self.intens_opt_mode.setEnabled(False)
        for obj in self.freq_lineedit_box:
            obj.clear()
            obj.setEnabled(False)
        self.freq_lineedit_box[0].setEnabled(True)
        for obj in self.intensity_lineedit_box:
            obj.clear()
            obj.setEnabled(False)
        self.intensity_lineedit_box[0].setEnabled(True)
        self.SetIsotropy()

    def SetIsotropy(self):
        if self.high_freq_radiobutton.isChecked():
            self.freq_lineedit_box[0].setText("1000")
        elif self.low_freq_radiobutton.isChecked():
            self.freq_lineedit_box[0].setText("800")
        self.intensity_lineedit_box[0].setText("20")

    def UnSelectedIsotropy(self):
        self.freq_norm_mode.setEnabled(True)
        self.freq_ets_mode.setEnabled(True)
        # self.freq_opt_mode.setEnabled(True)
        self.low_freq_radiobutton.disconnect()
        self.low_freq_radiobutton.clicked.connect(self.FreqSelMode)
        self.low_freq_radiobutton.clicked.connect(self.IntensSelMode)
        self.high_freq_radiobutton.disconnect()
        self.high_freq_radiobutton.clicked.connect(self.FreqSelMode)
        self.high_freq_radiobutton.clicked.connect(self.IntensSelMode)
        self.intens_freqres_mode.setEnabled(True)
        self.intens_linear_mode.setEnabled(True)
        # self.intens_opt_mode.setEnabled(True)
        for obj in self.freq_lineedit_box:
            obj.setEnabled(True)
        for obj in self.intensity_lineedit_box:
            obj.setEnabled(True)
        self.FreqSelMode()
        self.IntensSelMode()

    def CreateFreqModeBox(self):
        """CreateFreqModeBox."""
        self.freq_norm_mode = QRadioButton("常规频点")
        self.freq_ets_mode = QRadioButton("ETS定制频点")
        self.freq_opt_mode = QRadioButton("自定义频点")
        self.freq_norm_mode.setChecked(True)
        self.freq_norm_mode.clicked.connect(
            lambda *args: self.FreqSelMode())
        self.freq_ets_mode.clicked.connect(
            lambda *args: self.FreqSelMode())
        self.freq_opt_mode.clicked.connect(
            lambda *args: self.FreqSelMode())

        freq_mode_layout = QVBoxLayout()
        freq_mode_layout.addWidget(self.freq_norm_mode)
        freq_mode_layout.addWidget(self.freq_ets_mode)
        freq_mode_layout.addWidget(self.freq_opt_mode)
        freq_mode_box = QGroupBox("频点设置")
        freq_mode_box.setMaximumWidth(110)
        freq_mode_box.setLayout(freq_mode_layout)

        return freq_mode_box

    def CreateIntensityModeBox(self):
        """CreateFreqModeBox."""
        self.intens_linear_mode = QRadioButton("线性度")
        self.intens_freqres_mode = QRadioButton("频率响应")
        # self.intens_opt_mode = QRadioButton("自定义场强")
        self.intens_linear_mode.setChecked(True)
        self.intens_linear_mode.clicked.connect(
            lambda *args: self.IntensSelMode())
        self.intens_freqres_mode.clicked.connect(
            lambda *args: self.IntensSelMode())
        # self.intens_opt_mode.clicked.connect(
        # lambda *args: self.IntensSelMode())
        intens_mode_layout = QVBoxLayout()
        intens_mode_layout.addWidget(self.intens_linear_mode)
        intens_mode_layout.addWidget(self.intens_freqres_mode)
        # intens_mode_layout.addWidget(self.intens_opt_mode)
        intens_mode_box = QGroupBox("测试模式设置")
        intens_mode_box.setMaximumWidth(110)
        intens_mode_box.setLayout(intens_mode_layout)

        return intens_mode_box

    def CreateProbeTypeBox(self):
        """CreateProbeTypeBox."""
        self.ets_mode = QRadioButton("ETS自动读数")
        self.manual_mode = QRadioButton("手动读数")
        self.manual_mode.setChecked(True)
        probe_type_layout = QVBoxLayout()
        probe_type_layout.addWidget(self.manual_mode)
        probe_type_layout.addWidget(self.ets_mode)
        probe_type_box = QGroupBox("探头模式")
        probe_type_box.setMaximumWidth(110)
        probe_type_box.setLayout(probe_type_layout)

        return probe_type_box

    def ProbeType(self):
        """Return probe type."""
        if self.manual_mode.isChecked():
            probe_type = "Manual"
        elif self.ets_mode.isChecked():
            probe_type = "ETS"
        else:
            probe_type = "Manual"
        return probe_type

    def CreateInstrumentAddrBox(self):
        """Create the inst visa address lineedit groupbox."""
        basicinfo = Access("/Data/Basicinfo.accdb")
        high_sg_addr_label = QLabel("高频信号源")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '高频信号源'").fetchone()[0]
        self.high_sg_addr_lineedit = QLineEdit(addr)
        high_pa_addr_label = QLabel("高频功放")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '高频功放'").fetchone()[0]
        self.high_pa_addr_lineedit = QLineEdit(addr)
        high_pm_addr_label = QLabel("高频功率计")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '高频功率计'").fetchone()[0]
        self.high_pm_addr_lineedit = QLineEdit(addr)
        high_ct_addr_label = QLabel("暗室转台")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '暗室转台'").fetchone()[0]
        self.high_ct_addr_lineedit = QLineEdit(addr)
        low_sg_addr_label = QLabel("低频信号源")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '低频信号源'").fetchone()[0]
        self.low_sg_addr_lineedit = QLineEdit(addr)
        pa_250MHz_addr_label = QLabel("250MHz功放")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '250MHz功放'").fetchone()[0]
        self.pa_250MHz_addr_lineedit = QLineEdit(addr)
        pa_1GHz_addr_label = QLabel("1GHz功放")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '1GHz功放'").fetchone()[0]
        self.pa_1GHz_addr_lineedit = QLineEdit(addr)
        low_pm_addr_label = QLabel("低频功率计")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '低频功率计'").fetchone()[0]
        self.low_pm_addr_lineedit = QLineEdit(addr)
        zeta_addr_label = QLabel("电机COM口")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '电机COM口'").fetchone()[0]
        self.zeta_addr_lineedit = QLineEdit(addr)
        probe_addr_label = QLabel("探头COM口")
        addr = basicinfo.cursor.execute(
            "SELECT Address From InstrumentVisaAddr WHERE Instrument"
            " = '探头COM口'").fetchone()[0]
        self.probe_addr_lineedit = QLineEdit(addr)
        self.save_instr_addr_button = QPushButton("保存仪表地址信息")
        self.inst_addr_lineedit_list = [
            [high_sg_addr_label, self.high_sg_addr_lineedit],
            [high_pa_addr_label, self.high_pa_addr_lineedit],
            [high_ct_addr_label, self.high_ct_addr_lineedit],
            [high_pm_addr_label, self.high_pm_addr_lineedit],
            [low_sg_addr_label, self.low_sg_addr_lineedit],
            [pa_250MHz_addr_label, self.pa_250MHz_addr_lineedit],
            [pa_1GHz_addr_label, self.pa_1GHz_addr_lineedit],
            [low_pm_addr_label, self.low_pm_addr_lineedit],
            [zeta_addr_label, self.zeta_addr_lineedit],
            [probe_addr_label, self.probe_addr_lineedit],
        ]
        inst_addr_box = QGroupBox("仪表连接地址")
        inst_layout = QGridLayout()
        for obj in self.inst_addr_lineedit_list:
            index = self.inst_addr_lineedit_list.index(obj)
            inst_layout.addWidget(obj[0], index, 0, 1, 1)
            inst_layout.addWidget(obj[1], index, 1, 1, 1)
        inst_layout.addWidget(
            self.save_instr_addr_button,
            len(self.inst_addr_lineedit_list), 1, 1, 1)
        inst_addr_box.setLayout(inst_layout)
        self.save_instr_addr_button.clicked.connect(
            self.SaveInstrAddr)
        basicinfo.ConnClose()
        return inst_addr_box

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
        validator = QDoubleValidator()
        for i in self.freq_lineedit_box:
            i.setValidator(validator)
            freq_disp_layout.addWidget(i, self.freq_lineedit_box.index(i), 1)
        freq_label_seq = [QLabel("频率" + str(i)) for i in range(1, 15)]
        for i in freq_label_seq:
            freq_disp_layout.addWidget(i, freq_label_seq.index(i), 0)
        basicinfo = Access("//Data//BasicInfo.accdb")
        sql = "SELECT NormModeHigh FROM FrequencyList"
        frequency_list = basicinfo.cursor.execute(sql).fetchall()
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
        intensity_lineedit1.setText("10")
        intensity_lineedit2.setText("20")
        return intensity_disp_box

    def FreqSelMode(self):
        """FreqSelMode set a frequency box status."""
        basicinfo = Access("//Data//BasicInfo.accdb")
        mode_checkbox = [
            self.freq_norm_mode.isChecked(),
            self.freq_ets_mode.isChecked(),
            self.freq_opt_mode.isChecked()]
        freq_checkbox = [
            self.high_freq_radiobutton.isChecked(),
            self.low_freq_radiobutton.isChecked()]
        if mode_checkbox[0] and freq_checkbox[0]:
            sql = "SELECT NormModeHigh FROM FrequencyList"
            frequency_list = basicinfo.cursor.execute(sql).fetchall()
            frequency_list = list(zip(*frequency_list))[0]
        elif mode_checkbox[0] and freq_checkbox[1]:
            sql = "SELECT NormModeLow FROM FrequencyList"
            frequency_list = basicinfo.cursor.execute(sql).fetchall()
            frequency_list = list(zip(*frequency_list))[0]
        elif mode_checkbox[1] and freq_checkbox[0]:
            sql = "SELECT ETSModeHigh FROM FrequencyList"
            frequency_list = basicinfo.cursor.execute(sql).fetchall()
            frequency_list = list(zip(*frequency_list))[0]
        elif mode_checkbox[1] and freq_checkbox[1]:
            sql = "SELECT ETSModeLow FROM FrequencyList"
            frequency_list = basicinfo.cursor.execute(sql).fetchall()
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

    def IntensSelMode(self):
        """InrensSelMode set a intensity box status."""
        basicinfo = Access("//Data//BasicInfo.accdb")
        mode_checkbox = [
            self.intens_linear_mode.isChecked(),
            self.intens_freqres_mode.isChecked()]
        # self.intens_opt_mode.isChecked()]
        intens_checkbox = [
            self.high_freq_radiobutton.isChecked(),
            self.low_freq_radiobutton.isChecked()]
        if mode_checkbox[0] and intens_checkbox[0]:
            sql = "SELECT LinearModeHigh FROM IntensityList"
            intensity_list = basicinfo.cursor.execute(sql).fetchall()
            intensity_list = list(zip(*intensity_list))[0]
        elif mode_checkbox[0] and intens_checkbox[1]:
            sql = "SELECT LinearModeLow FROM IntensityList"
            intensity_list = basicinfo.cursor.execute(sql).fetchall()
            intensity_list = list(zip(*intensity_list))[0]
        elif mode_checkbox[1] and intens_checkbox[0]:
            sql = "SELECT FreqResModeHigh FROM IntensityList"
            intensity_list = basicinfo.cursor.execute(sql).fetchall()
            intensity_list = list(zip(*intensity_list))[0]
        elif mode_checkbox[1] and intens_checkbox[1]:
            sql = "SELECT FreqResModeLow FROM IntensityList"
            intensity_list = basicinfo.cursor.execute(sql).fetchall()
            intensity_list = list(zip(*intensity_list))[0]
        else:
            intensity_list = [None]
        for i in range(len(intensity_list)):
            if intensity_list[i] is not None:
                self.intensity_lineedit_box[i].setText(str(intensity_list[i]))
            else:
                self.intensity_lineedit_box[i].clear()
        for i in range(len(intensity_list), len(self.intensity_lineedit_box)):
            self.intensity_lineedit_box[i].clear()

    def StartTest(self):
        intensity = [
            float(obj.text()) for obj in self.intensity_lineedit_box
            if obj.text().__len__() > 0]
        frequency = [
            float(obj.text()) for obj in self.freq_lineedit_box
            if obj.text().__len__() > 0]
        self.start_test_button.setEnabled(False)
        self.stop_test_button.setEnabled(True)
        # True is isotropy, False is not isotropy
        isisotropy = self.isotropy_true_radiobutton.isChecked()
        # True is high frequency, Flase is low frequency
        freqselect = self.high_freq_radiobutton.isChecked()
        # True is frequency response, False is linearity
        freqres = self.intens_freqres_mode.isChecked()
        # Manual is manual mode ETS is ETS mode
        probetype = self.ProbeType()
        print(probetype)
        self.test = ProbeTest(
            dbname=self.dbname, isisotropy=isisotropy,
            freqselect=freqselect, freqres=freqres,
            probetype=probetype,
            frequency=frequency, intensity=intensity,
            highsgaddr=self.high_sg_addr_lineedit.text(),
            highpaaddr=self.high_pa_addr_lineedit.text(),
            ctaddr=self.high_ct_addr_lineedit.text(),
            pmhighaddr=self.high_pm_addr_lineedit.text(),
            lowsgaddr=self.low_pm_addr_lineedit.text(),
            pa250MHzaddr=self.pa_250MHz_addr_lineedit.text(),
            pa1GHzaddr=self.pa_1GHz_addr_lineedit.text(),
            pmlowaddr=self.low_pm_addr_lineedit.text(),
            probeaddr=self.probe_addr_lineedit.text(),
            zetaaddr=self.zeta_addr_lineedit.text())
        self.test._messagesignal.connect(self.SetThread)
        self.test._valuedialogsignal.connect(self.SetThreadValueDialog)
        self.test._testcompletesignal.connect(self.StopTest)
        self._valuesentsignal.connect(self.test.GetValue)
        self.test.start()

    def SaveInstrAddr(self):
        basicinfo = Access("/Data/Basicinfo.accdb")
        for obj in self.inst_addr_lineedit_list:
            name = obj[0].text()
            addr = obj[1].text()
            sql = (
                "UPDATE InstrumentVisaAddr SET Address = '%s' "
                "WHERE Instrument = '%s'" % (addr, name))
            basicinfo.Execute(sql)
        print("仪表地址信息已保存")
        basicinfo.ConnClose()

    @pyqtSlot()
    def StopTest(self):
        self.start_test_button.setEnabled(True)
        self.stop_test_button.setEnabled(False)

    @pyqtSlot(threading.Event, str)
    def SetThread(self, event, s):
        QMessageBox.information(
            None, "提示", "%s" % s)
        event.set()

    @pyqtSlot(threading.Event)
    def SetThreadValueDialog(self, event):
        value, ok1 = QInputDialog.getDouble(
            None, "标题", "场强值:", value=0, min=0, max=1000, decimals=2)
        self._valuesentsignal.emit(value)
        event.set()
        return value


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mainWin = FSTestDialog("TestDB")
    mainWin.show()
    sys.exit(app.exec_())
