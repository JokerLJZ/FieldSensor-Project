"""The field sensor probe test programme. All units is Mhz and dBm."""

import logging
import traceback
import time
import visa
from Access import Access
from SG8257D import SG8257D as SGHigh
from PABonn import PABonn as PAHigh
from PMNRP import PMNRP as PM
from CoupleNew import CalHighFreq
from Controller import Controller as CT
from PyQt5.QtWidgets import QMessageBox, QApplication, QInputDialog
from ETSProbe import ETSProbe


class ProbeTest(object):
    """Define a test class."""
    def __init__(self, dbname="TestDB", probetype=None,
                 highsgaddr=19, highpaaddr=7, ctaddr=10,
                 pmhighaddr='RSNRP::0x0003::102279::INSTR'):
        """initialise the test class."""
        self.rm = visa.ResourceManager()
        self.highsgaddr = highsgaddr
        self.highpaaddr = highpaaddr
        self.ctaddr = ctaddr
        self.pmhighaddr = pmhighaddr
        self.probetype = probetype
        self.Log()
        dbname = "\\TestResult\\Database\\" + dbname + ".accdb"
        dbinfoname = "\\Data\\BasicInfo.accdb"
        self.db = Access(dbname)
        self.info = Access(dbinfoname)
        self.serial = self.db.CreateSerial()

    def Log(self):
        """Initialise the log function."""
        self.logger = logging.getLogger()
        handler = logging.FileHandler("Data\\TestLog.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s -%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

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
        # Initial the instrument
        sg = SGHigh(self.Highsgaddr, self.rm)
        pa = PAHigh(self.Highpaaddr, self.rm)
        pm = PM(self.pmhighaddr, self.rm)
        ct = CT(self.ctaddr, self.rm)
        couple = CalHighFreq(freq / 1e3, fieldintensity, dist)
        QMessageBox.information(
            None, "提示", "请连接好电场探头")
        QMessageBox.information(
            None, "提示", "请连接%s天线进行测试" % couple["Antenna"])
        ct.CTAntennaRoll(couple["Antenna"])
        powertarget = couple["PowerMeter"]
        self.PowerIter(target=powertarget, freq=freq, sg=sg, pa=pa, pm=pm)
        value = self.ReadValue()
        sg.SGPowerOut("OFF")
        pa.PAPowerOut("OFF")
        sg.SGClose()
        pa.PAClose()
        pm.PMClose()
        return value

    def LinearityHighFreq(self, freq=None, field=None):
        """Test the Linearity of probe in specific frequency and field
           intensity.

        ===============   =====================================================
        **Argument:**
        freq              Defalt is None. freq should be a list if not will
                          raise a assertion error. Unit should be MHz.
        field             Defalt is None, should be a list, if not will raise
                          a assertion error, the unit is V/m.
        ===============   =====================================================
        """
        column = ("Frequency__MHz, Field__V_per_m, FieldResult__V_per_m,"
                  " TestSeries")
        self.db.CreateTable(
            tablename="场强线性度",
            columnnamelist=column.split(", "),
            typelist=["DOUBLE", "DOUBLE", "DOUBLE", "DOUBLE"])
        assert type(freq) == list
        assert type(field) == list
        for frequency in freq:
            for intensity in field:
                QMessageBox.information(
                    None, "提示", "将要开始进行%sMHz强度%sV/m的测试"
                    % (freq, intensity))
                value = self.ProbeTestHighFreq(
                    freq=frequency, fieldintensity=intensity)
                self.db.cursor.execute(
                    "INSERT INTO 场强线性度 (%s) VALUES (%f, %f, %f, %d)"
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

    def PowerIter(self, powertarget=None, freq=None,
                  sg=None, pa=None, pm=None, highfreq=True):
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
        if self.probetype is None:
            value, ok1 = QInputDialog.getDouble(
                None, "标题", "场强值:", value=0, min=0, max=1000, decimals=2)
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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    try:
        test = ProbeTest()
        test.FieldTestHighFreq([10, 20], [20, 34])
        # test.ProbeTestHighFreq(freq=18000, fieldintensity=10, dist=0.7)
    except:
        logger = logging.getLogger()
        handler = logging.FileHandler("Data\\TestLog.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s -%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(traceback.format_exc())
