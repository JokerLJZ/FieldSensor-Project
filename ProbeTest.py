"""The field sensor probe test programme. All units is Mhz and dBm."""

import threading
import time

import visa
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox

from Access import Access
from Controller import Controller as CT
from CoupleNew import CalHighFreq
from ETSProbe import ETSProbe
from PABonn import PABonn as PAHigh
from PMNRP import PMNRP as PM
from SG8257D import SG8257D as SGHigh


class ProbeTest(QThread):
    """Define a test class."""
    _messagesignal = pyqtSignal(threading.Event, str)
    _valuedialogsignal = pyqtSignal(threading.Event)
    _testcompletesignal = pyqtSignal()

    def __init__(
            self, dbname="TestDB",
            frequency=[],
            intensity=[],
            isisotropy=False,
            freqselect=True,
            freqres=True,
            probetype=None,
            highsgaddr="GPIB0::19::INSTR",
            highpaaddr="GPIB0::7::INSTR",
            ctaddr="GPIB0::10::INSTR",
            pmhighaddr="RSNRP::0x0003::102279::INSTR",
            lowsgaddr="GPIB0::19::INST",
            pa250MHzaddr="GPIB0::1::INST",
            pa1GHzaddr="GPIB0::2::INST",
            pmlowaddr="RSNRP::0x0021::101975::INSTR",
            probeaddr="2",
            zetaaddr="1"
            ):
        """initialise the test class."""
        super(ProbeTest, self).__init__()
        self.rm = visa.ResourceManager()
        print("当前的探头读数模式为%s" % probetype)
        # print("频率点为%s" % frequency)
        # print("当前高频信号源VISA地址为%s" % highsgaddr)
        # print("当前高频转台VISA地址为%s" % ctaddr)
        # print("当前高频功放VISA地址为%s" % highpaaddr)
        # print("当前高频功率计VISA地址为%s" % pmhighaddr)
        self.frequency = frequency
        self.intensity = intensity
        self.highsgaddr = highsgaddr
        self.highpaaddr = highpaaddr
        self.ctaddr = ctaddr
        self.pmhighaddr = pmhighaddr
        self.lowsgaddr = lowsgaddr
        self.pa250MHzaddr = pa250MHzaddr
        self.pa1GHzaddr = pa1GHzaddr
        self.pmlowaddr = pmlowaddr
        self.probetype = probetype
        self.isisotropy = isisotropy
        self.freqselect = freqselect
        self.freqres = freqres
        self.dbname = "\\TestResult\\Database\\" + dbname + ".accdb"
        self.dbinfoname = "\\Data\\BasicInfo.accdb"
        self.db = Access(self.dbname)
        self.info = Access(self.dbinfoname)
        self.serial = self.db.CreateSerial()

    def run(self):
        self.ThreadMessage("即将开始运行测试程序")
        self.TestProcedure()
        self.db.ConnClose()
        self.info.ConnClose()
        self._testcompletesignal.emit()

    def TestProcedure(self):
        print("进入测试步骤选择")
        time.sleep(1)
        if self.freqselect is True and self.isisotropy is True:
            # print("选择高频全向性")
            time.sleep(1)
            self.IsotropyHighFreq()
        elif self.freqselect is False and self.isisotropy is True:
            # print("选择低频全向性")
            time.sleep(1)
            self.IsotropyLowFreq()
        elif self.freqselect is True and self.freqres is True:
            # print("选择高频频率响应")
            time.sleep(1)
            self.FreqResHighFreq()
        elif self.freqselect is False and self.freqres is True:
            # print("选择低频频率响应")
            time.sleep(1)
            self.FreqResLowFreq()
        elif self.freqselect is True and self.freqres is False:
            # print("选择高频线性度")
            time.sleep(1)
            self.LinearityHighFreq(self.frequency, self.intensity)
        elif self.freqselect is False and self.freqres is False:
            # print("选择低频线性度")
            time.sleep(1)
            self.LinearityLowFreq()

    def ThreadMessage(self, message=None):
        event = threading.Event()
        self._messagesignal.emit(
            event, "%s" % message)
        event.wait()
        event.clear()

    def ThreadValueDialog(self):
        event = threading.Event()
        self._valuedialogsignal.emit(
            event)
        event.wait()
        event.clear()

    def IsotropyLowFreq(self):
        time.sleep(1)
        print("现在即将进行低频全向性测试")

    def FreqResLowFreq(self):
        print("现在即将进行低频频率响应测试")

    def LinearityLowFreq(self):
        print("现在即将进行低频线性度测试")

    def LinearityHighFreq(self, freq=None, intens=None):
        """Test the Linearity of probe in specific frequency and field
           intensity.

        ===============   =====================================================
        **Argument:**
        freq              Defalt is None. freq should be a list if not will
                          raise a assertion error. Unit should be MHz.
        intensity         Defalt is None, should be a list, if not will raise
                          a assertion error, the unit is V/m.
        ===============   =====================================================
        """
        print("现在即将进行高频线性度测试")

        column = ("Frequency__MHz, Field__V_per_m, FieldResult__V_per_m,"
                  " TestSeries")
        self.db.CreateTable(
            tablename="场强线性度",
            columnnamelist=column.split(", "),
            typelist=["DOUBLE", "DOUBLE", "DOUBLE", "DOUBLE"])
        print(intens)
        assert type(freq) == list
        assert type(intens) == list
        for frequency in freq:
            for intensity in intens:
                self.ThreadMessage(
                    "将要开始进行%sMHz强度%sV/m的测试"
                    % (frequency, intensity))
                value = self.ReadValue()
                # value = self.ProbeTestHighFreq(
                #     freq=frequency, fieldintensity=intensity)
                self.db.cursor.execute(
                    "INSERT INTO 场强线性度 (%s) VALUES (%f, %f, %f, %f)"
                    % (column, frequency, intensity, value, self.serial))
                self.db.Commit()

    def IsotropyHighFreq(self, freq=None, field=None, dist=0.7, step=5):
        """Test the isotropy of probe in specific frequency and field
           intensity.

        ===============   =====================================================
        **Argument:**
        freq              Defalt is None. freq should be int or float if not
                          will raise a assertion error. Unit should be MHz.
        field             Defalt is None, should be int or float, if not will
                          raise a assertion error, the unit is V/m.
        ===============   =====================================================
        """
        print("现在即将进行高频全向性测试")
        time.sleep(1)
        return

        assert type(freq) is int or type(field) is float
        assert type(field) is int or type(field) is float
        column = ("Degree__°, Field__V_per_m, TestSeries")
        tablename = "全向性_%sMHz_%sV" % (freq, field)
        self.db.CreateTable(
            tablename=tablename,
            columnnamelist=column.split(", "),
            typelist=["DOUBLE", "DOUBLE", "DOUBLE"])
        degree = 0
        times = int(360 / step)
        sg = SGHigh(self.Highsgaddr, self.rm)
        pa = PAHigh(self.Highpaaddr, self.rm)
        pm = PM(self.pmhighaddr, self.rm)
        ct = CT(self.ctaddr, self.rm)
        couple = CalHighFreq(freq / 1e3, field, dist)
        QMessageBox.information(
            None, "提示", "请连接好电场探头")
        ct.CTAntennaRoll(couple["Antenna"])
        powertarget = couple["PowerMeter"]
        sg_power = self.PowerIter(
            target=powertarget, freq=freq, sg=sg, pa=pa, pm=pm)
        value = list(self.ReadValue())

    def FreqResHighFreq(self, freq=None, field=None):
        """Test the frequency response of probe in specific frequency and
           field intensity.

        ===============   =====================================================
        **Argument:**
        freq              Defalt is None. freq should be a list if not will
                          raise a assertion error. Unit should be MHz.
        fieldintensity    Defalt is None, should be int or float, if not will
                          raise a assertion error, the unit is V/m.
        ===============   =====================================================
        """
        print("现在即将进行高频频率响应测试")
        return

        column = ("Frequency__MHz, Field__V_per_m, FieldResult__V_per_m,"
                  " TestSeries")
        self.db.CreateTable(
            tablename="场强频率响应",
            columnnamelist=column.split(", "),
            typelist=["DOUBLE", "DOUBLE", "DOUBLE", "DOUBLE"])
        assert type(freq) == list
        assert type(field) is int or type(field) is float
        for frequency in freq:
            value = self.ProbeTestHighFreq(
                freq=frequency, fieldintensity=field)
            self.db.cursor.execute(
                "INSERT INTO  (%s) VALUES (%f, %f, %f, %d)"
                % (column, frequency, field, value, self.serial))
            self.db.Commit()

    def ProbeTestHighFreq(self, freq=1000, fieldintensity=10, dist=0.7):
        """The high frequency foundermental probe test procedure.

        ===============   =====================================================
        **Argument:**
        freq              Defalt is 1000MHz.
        fieldintensity    The field intensity of standard field, the unit
                          is V/m.
        dist              The distance of probe and the antenna, defalt is 0.7.
        ===============   =====================================================
        """
        print("现在即将进行高频频率响应测试")
        return
        # Initial the instrument
        sg = SGHigh(self.Highsgaddr, self.rm)
        pa = PAHigh(self.Highpaaddr, self.rm)
        pm = PM(self.pmhighaddr, self.rm)
        ct = CT(self.ctaddr, self.rm)
        couple = CalHighFreq(freq / 1e3, fieldintensity, dist)
        self.ThreadMessage("请连接好电场探头")
        self.ThreadMessage("请连接%s天线进行测试" % couple["Antenna"])
        ct.CTAntennaRoll(couple["Antenna"])
        powertarget = couple["PowerMeter"]
        print(couple)
        self.ThreadMessage("请连接好电场探头")
        poweriteritem = {
            "target": powertarget, "freq": freq, "sg": sg, "pa": pa,
            "pm": pm}
        self.ThreadMessage("请连接好电场探头")
        self.PowerIter(poweriteritem)
        value = self.ReadValue()
        sg.SGPowerOut("OFF")
        pa.PAPowerOut("OFF")
        sg.SGClose()
        pa.PAClose()
        pm.PMClose()
        return value

    def PowerIter(self, poweriteritem=None):
        sg = poweriteritem["sg"]
        pm = poweriteritem["pm"]
        freq = poweriteritem["target"]
        pa = poweriteritem["pa"]
        sg.SGCWFrec(freq)
        pm.PMSetFreq(freq)
        if highfreq:
            pa.PABand(freq)
        else:
            pass
        sg_power = powertarget - 10
        sg.SGPowerSet(sg_power)
        time.sleep(2)
        sg.SGPowerout("ON")
        pa.PAPowerOut("ON")
        diff_limit = 0.01
        for i in range(6):
            time.sleep(2)
            powercoup = pm.PMFetch()
            powerdiff = powertarget - powercoup
            if abs(powerdiff) < diff_limit:
                break
            else:
                sg_power = sg_power + powerdiff
            if sg.SGInRange(sg_power) and sg_power < diff_limit:
                sg.SGPowerOut(sg_power)
            else:
                QMessageBox.information(
                    None, "提示", "信号源将要超过限值，程序即将停止")
                raise ValueError("Wrong power set in signal generator.")
        return sg_power

    def ReadValue(self):
        """Read the value of probe and return the value.

        ===============   =====================================================
        **Argument:**
        type              Defalt is None, read the value of probe handly.
                          Type: "ETS", read the value automatically.
                          Type: "ETSSingle", read the value automatically.
        ===============   =====================================================
        """
        if self.probetype is "Manual":
            self.ThreadValueDialog()
            value = self.value
            print(value)
            time.sleep(2)
        elif self.probetype == "ETS":
            probe = ETSProbe()
            value = probe.ProbeField()[3]
            probe.RemoveProbe()
        elif self.probetype == "ETSSingle":
            probe = ETSProbe()
            value = probe.ProbeField()[0]
            probe.RemoveProbe()
        else:
            self.logging.error(
                "Wrong type selected in ReadValue function of class"
                "ProbeTest.")
            raise AttributeError("Wrong type select in ReadValue.")
        return value

    def ControlerRoll(self, antenna=None):
        ct = CT(self.ctaddr, resourcemanager=self.rm)
        if antenna is not None:
            ct.CTAntennaRoll(antenna)

    @pyqtSlot(float)
    def GetValue(self, value):
        self.value = value


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    test = ProbeTest()
    test.start()
    # test.ProbeTestHighFreq(freq=18000, fieldintensity=10, dist=0.7)
