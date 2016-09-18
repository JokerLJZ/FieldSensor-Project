__author__ = 'TheJoker'

from Visa8257D import Visa8257D
from VisaBONN import VisaBONN
from VisaNRP import VisaNRP
from VisaController import VisaController
from ETSProbe import ETSProbe
from Zeta import Zeta
from EasyDatabase import EasyDatabase
from Couple import cal_field
from math import log10
import tkinter.messagebox
import visa
import time


class FieldSensor(object):

    def __init__(self, dbname='Test', fieldread=None, sgaddr='GPIB0::19::INSTR', paaddr='GPIB0::7::INSTR',
                 pmaddr='RSNRP::0x0003::102279::INSTR', ctaddr='GPIB0::10::INSTR', zetaaddr='ASRL10::INSTR'):
        """initialise the test programme"""
        self.resourcemanager = visa.ResourceManager()
        try:
            self.sg = Visa8257D(sgaddr, self.resourcemanager)
        except:
            tkinter.messagebox.showinfo(title='提示', message="无信号源连接")
        try:
            self.pa = VisaBONN(paaddr, self.resourcemanager)
        except:
            tkinter.messagebox.showinfo(title='提示', message="无功放连接")
        try:
            self.pm = VisaNRP(pmaddr, self.resourcemanager)
        except:
            tkinter.messagebox.showinfo(title='提示', message="无功率计连接")
        try:
            self.ct = VisaController(ctaddr, self.resourcemanager)
        except:
            tkinter.messagebox.showinfo(title='提示', message="无转台连接")
        try:
            self.zeta = Zeta(zetaaddr, self.resourcemanager)
        except:
            tkinter.messagebox.showinfo(title='提示', message="无电机连接")
        try:
            self.db = EasyDatabase(dbname)
        except:
            tkinter.messagebox.showinfo(title='提示', message="无数据库连接")
        self.fieldintensityRange = [0, 100]
        self.fieldread = fieldread
        if self.fieldread == 'ETS':
            print('ETS探头状态为%s' % self.fieldread)
        else:
            self.ETS = None

    def __del__(self):
        """Delete the test object"""
        try:
            self.sg.SGPowerOut('OFF')
        except:
            pass
        try:
            self.pa.PAPowerOut('OFF')
        except:
            pass
        try:
            self.sg.SGClose()
        except:
            pass
        try:
            self.pa.PAClose()
        except:
            pass
        try:
            self.ct.CTClose()
        except:
            pass
        try:
            self.zeta.ZetaClose()
        except:
            pass

    def FieldProb(self, freq, fieldintensity, transfer=False):
        """Produce the fieldintensity of specified frequency
        :param transfer:
        :param fieldintensity:
        :param freq:
        """
        global powersg
        sg_output_limit = -5  # unit is dBm set the signal generator output limit
        tkinter.messagebox.showinfo(title='提示', message='请连接好电场探头\n')
        field = cal_field(freq, fieldintensity)
        print(field)
        if transfer:
            self.db.BasicCursor.execute("SELECT PowerCal FROM FieldTransfer WHERE Frequency=%f AND Field=%f"
                                    % (freq, fieldintensity))
            powertarget = self.db.BasicCursor.fetchall()[0][0]
            if powertarget == 0:
                tkinter.messagebox.showinfo(title='提示', message='输入场强无法传递\n')
                return
        else:
            powertarget = field[0]
        # change cable module to be updated #
        # angel = self.ct.CTReadAngel()
        # antennachange = ['ETS3160-0316001', 'ETS3160-0316002', 'ETS3160-0316003']
        # if antenna not in antennachange and angel != 90:
        #     self.ct.CTRoll(180)
        tkinter.messagebox.showinfo(title='提示', message="请确定天线更换完毕并且射频线连接正确")
        if transfer:
            self.ct.CTRoll(90)
        else:
            antenna = field[2]
            tkinter.messagebox.showinfo(title='提示', message="请连接%s天线进行测试" % antenna)
            self.ct.CTAntennaRoll(antenna)
        sg_initial = -30
        self.sg.SGPowerSet(sg_initial)  # set the initial power unit dBm
        # frequency set
        frequency = freq * 1e9
        self.sg.SGCWFrec(frequency)
        self.pm.PMSetFreq(frequency)
        self.pa.PAPowerOut('OFF')
        time.sleep(5)
        self.pa.PABand(frequency)
        self.sg.SGPowerOut('On')
        self.pa.PAPowerOut('ON')
        time.sleep(5)
        for i in range(0, 4):  # iterate the power output
            time.sleep(2)  # delay 1 second
            if i == 0:
                powercoup = self.pm.PMFetch()
                print('当前第%d循环的功率计读数为%f' % (i + 1, powercoup))
                powerdiff = powertarget - powercoup
                powersg = sg_initial + powerdiff
                if self.sg.SGInRange(powersg) and powersg < sg_output_limit:
                    self.sg.SGPowerSet(powersg)
                else:
                    tkinter.messagebox.showinfo(title='Alert', message="Error input signal generator power")
                    return "Error input signal generator power"
            else:
                powercoup = self.pm.PMFetch()
                print('当前第%d循环的功率计读数为%f' % (i + 1, powercoup))
                powerdiff = powertarget - powercoup
                powersg += powerdiff
                if self.sg.SGInRange(powersg) and powersg < sg_output_limit:
                    self.sg.SGPowerSet(powersg)
                else:
                    tkinter.messagebox.showinfo(title='Alert', message="Error input signal generator power")
                    return "Error input signal generator power"
        if self.fieldread == 'ETS':
            try:
                self.ETS = ETSProbe()
            except:
                tkinter.messagebox.showinfo(title='提示', message="无ETS探头连接")
            fieldreading = self.ETS.ProbeField()[3]
            # fieldreading = self.ETS.ProbeField()[0]
            self.ETS.RemoveProbe()
        else:
            try:
                fieldreading = float(input('请输入电场探头示值:'))
            except:
                print('输入数据有误')
                try:
                    fieldreading = float(input('请重新输入电场探头示值:'))
                except:
                    print('输入数据有误')
                    fieldreading = float(input('请重新输入电场探头示值:'))
        try:
            self.db.Cursor.execute("INSERT INTO 场强线性度 (Frequency__GHz, Field__V_per_m, FieldResult__V_per_m,"
                                   " TestSeries) "
                               "VALUES (%f, %f, %f, %f)" % (freq, fieldintensity, fieldreading, self.db.TestSeriesNo))
            self.db.Cursor.commit()
        except:
            print('结果写入数据库失败')
        # set return value
        if fieldreading:
            return fieldreading
        else:
            return 'wrong output'

    def FieldTest(self, specfreq=None, field=None, transfer=False):
        """
        :param field:
        :param transfer:
        :param specfreq:
        """
        # Create result table
        if not self.db.Cursor.tables(table='FieldTransfer1G').fetchone():
            try:
                self.db.Cursor.execute("Create TABLE 场强线性度")
                self.db.Cursor.commit()
            except:
                pass
            try:
                self.db.Cursor.execute("alter table 场强线性度 add Frequency__GHz DOUBLE ")
                self.db.Cursor.commit()
            except:
                pass
            try:
                self.db.Cursor.execute("alter table 场强线性度 add Field__V_per_m DOUBLE ")
                self.db.Cursor.commit()
            except:
                pass
            try:
                self.db.Cursor.execute("alter table 场强线性度 add FieldResult__V_per_m DOUBLE ")
                self.db.Cursor.commit()
            except:
                pass
            try:
                self.db.Cursor.execute("alter table 场强线性度 add TestSeries DOUBLE ")
                self.db.Cursor.commit()
            except:
                pass

        specfreq = list(specfreq)
        field = list(field)
        iterationfreq = len(specfreq)
        iterationfield = len(field)
        if specfreq is not None:
            for i in range(iterationfreq):
                for j in range(iterationfield):
                    self.FieldProb(specfreq[i], field[j], transfer)
                    self.sg.SGPowerOut('OFF')
                    self.pa.PAPowerOut('OFF')

    def fieldomni(self, freq, fieldintensity, degreestep=5, transfer=False):
        if not self.db.Cursor.tables(table='全向性_%sGHz_%sV' % (freq, fieldintensity)).fetchone():
            try:
                self.db.Cursor.execute("Create TABLE 全向性_%sGHz_%sV" % (freq, fieldintensity))
                self.db.Cursor.commit()
            except:
                pass
            try:
                self.db.Cursor.execute('alter table 全向性_%sGHz_%sV add %s DOUBLE '
                                       % (freq, fieldintensity, 'Degree__°'))
                self.db.Cursor.commit()
            except:
                pass
            try:
                self.db.Cursor.execute("alter table 全向性_%sGHz_%sV add Field__V_per_m DOUBLE "
                                       % (freq, fieldintensity))
                self.db.Cursor.commit()
            except:
                pass
            try:
                self.db.Cursor.execute("alter table 全向性_%sGHz_%sV add TestSeriesNo DOUBLE "
                                       % (freq, fieldintensity))
                self.db.Cursor.commit()
            except:
                pass
        sg_output_limit = -5  # unit is dBm set the signal generator output limit
        degree = 0
        tkinter.messagebox.showinfo(title='提示', message='将要进行频率%f场强%f的各向同性测试, 请连接好探头和电机\n'
                                    % (freq, fieldintensity))
        times = int(360 / degreestep)
        if transfer is False:
            field = cal_field(freq, fieldintensity)
            print(field)
            antenna = field[2]
            powertarget = field[0]
            self.ct.CTAntennaRoll(antenna)
        else:
            self.db.BasicCursor.execute("SELECT PowerCal FROM FieldTransfer WHERE Frequency=%f AND Field=%f"
                                    % (freq, fieldintensity))
            powertarget = self.db.BasicCursor.fetchall()[0][0]
            if powertarget == 0:
                tkinter.messagebox.showinfo(title='提示', message='输入场强无法传递\n')
                return
            self.ct.CTRoll(89)
        frequency = freq * 1e9
        powersignal = -30
        self.sg.SGPowerSet(powersignal)
        self.sg.SGCWFrec(frequency)
        self.pm.PMSetFreq(frequency)
        self.pa.PABand(frequency)
        self.sg.SGPowerOut('ON')
        self.pa.PAPowerOut('ON')
        time.sleep(5)
        for i in range(5):
            time.sleep(2)
            pmpower = self.pm.PMFetch()
            print('当前第%d循环的功率计读数为%f' % (i + 1, pmpower))
            powerdiff = powertarget - pmpower
            powersignal += powerdiff
            if self.sg.SGInRange(powersignal) and powersignal < sg_output_limit:
                self.sg.SGPowerSet(powersignal)
            else:
                self.sg.SGPowerOut('OFF')
                self.pa.PAPowerOut('OFF')
                return "Error input signal generator power"
        for i in range(times):
            pmpower = self.pm.PMFetch()
            print('当前第%d循环的功率计读数为%f' % (i + 1, pmpower))
            powerdiff = powertarget - pmpower
            powersignal += powerdiff
            self.sg.SGPowerSet(powersignal)
            time.sleep(3)
            if self.fieldread == 'ETS':
                try:
                    self.ETS = ETSProbe()
                except:
                    tkinter.messagebox.showinfo(title='提示', message="无ETS探头连接")
                fieldreading = self.ETS.ProbeField()[3]
                self.ETS.RemoveProbe()
            else:
                try:
                    fieldreading = float(input('请输入电场探头示值:'))
                except:
                    print('输入数据有误')
                    try:
                        fieldreading = float(input('请重新输入电场探头示值:'))
                    except:
                        print('输入数据有误')
                        fieldreading = float(input('请重新输入电场探头示值:'))
            if degree == 0:
                try:
                    self.db.Cursor.execute("INSERT INTO 全向性_%sGHz_%sV (%s, Field__V_per_m, TestSeriesNo) VALUES"
                                           " (%f, %f, %d)"
                                           % (freq, fieldintensity, 'Degree__°', degree, fieldreading,
                                              self.db.TestSeriesNo))
                    self.db.Cursor.commit()
                except:
                    print('结果写入数据库失败')
                degree += 5
            else:
                try:
                    self.db.Cursor.execute("INSERT INTO 全向性_%sGHz_%sV (%s, Field__V_per_m, TestSeriesNo) VALUES"
                                           " (%f, %f, %d)"
                                           % (freq, fieldintensity, 'Degree__°', degree, fieldreading,
                                              self.db.TestSeriesNo))
                    self.db.Cursor.commit()
                    self.zeta.ZetaRoll(degreestep)
                except:
                    print('结果写入数据库失败')
                degree += 5

    def fieldtransfer(self, cal=0, specfreq=None, field=None):
        if self.fieldread == 'ETS':
            try:
                self.ETS = ETSProbe()
            except:
                tkinter.messagebox.showinfo(title='提示', message="无ETS探头连接")
        if not self.db.BasicCursor.tables(table='FieldTransfer').fetchone():
            try:
                self.db.BasicCursor.execute("Create TABLE FieldTransfer")
                self.db.BasicCursor.commit()
            except:
                pass
            try:
                self.db.BasicCursor.execute("alter table FieldTransfer add Frequency DOUBLE ")
                self.db.BasicCursor.commit()
            except:
                pass
            try:
                self.db.BasicCursor.execute("alter table FieldTransfer add Field DOUBLE ")
                self.db.BasicCursor.commit()
            except:
                pass
            try:
                self.db.BasicCursor.execute("alter table FieldTransfer add Cal DOUBLE ")
                self.db.BasicCursor.commit()
            except:
                pass
            try:
                self.db.BasicCursor.execute("alter table FieldTransfer add PowerCal DOUBLE ")
                self.db.BasicCursor.commit()
            except:
                pass
            try:
                self.db.BasicCursor.execute("alter table FieldVerify add FieldVerify DOUBLE ")
                self.db.BasicCursor.commit()
            except:
                pass
        field = list(field)
        specfreq = list(specfreq)
        iterationfreq = len(specfreq)
        iterationfield = len(field)
        if cal == 0 and specfreq is not None:
            for i in range(iterationfreq):
                for j in range(iterationfield):
                    self.TransferInit(specfreq[i], field[j])
        elif cal == 1 and specfreq is not None:
            frequency = list(specfreq)
            iterationfreq = len(specfreq)
            for i in range(iterationfreq):
                for j in range(iterationfield):
                    self.db.BasicCursor.execute("SELECT * FROM FieldTransfer WHERE Frequency=%f "
                                             "AND Field=%f" % (frequency[i], field[j]))
                    table = self.db.BasicCursor.fetchall()
                    tkinter.messagebox.showinfo(title='提示',
                                                message='将要进行频率%f场强%f的测试\n' % (frequency[i], field[j]))
                    print(self.TransferIteration(table[0][0], table[0][2]))
        self.ETS.RemoveProbe()

    def TransferInit(self, freq, fieldtarget):
        result = self.FieldProb(freq, fieldtarget)
        print(result)
        self.db.BasicCursor.execute("SELECT * FROM FieldTransfer WHERE Frequency=%f AND Field=%f" % (freq, fieldtarget))
        update = self.db.BasicCursor.fetchall()
        if not update and result != "Error input signal generator power":
            self.db.BasicCursor.execute("INSERT INTO FieldTransfer (Frequency, Field, Cal) "
                                     "VALUES (%f, %f, %f)" % (freq, fieldtarget, result[1]))
            self.db.BasicCursor.commit()
            self.db.BasicCursor.execute("SELECT * FROM FieldTransfer ORDER BY Frequency, Field")
            table = self.db.BasicCursor.fetchall()
            self.db.BasicCursor.execute("DELETE FROM FieldTransfer")
            self.db.BasicCursor.commit()
            for i in range(len(table)):
                self.db.BasicCursor.execute("INSERT INTO FieldTransfer (Frequency, Field, Cal) "
                                         "VALUES (%f, %f, %f)" % (table[i][0], table[i][1], table[i][2]))
                self.db.BasicCursor.commit()
        elif update and result != "Error input signal generator power":
            self.db.BasicCursor.execute(
                "UPDATE FieldTransfer SET Cal=%f WHERE Frequency=%f AND Field=%f" % (result[1], freq, fieldtarget))
            self.db.BasicCursor.commit()
        elif not update and result == "Error input signal generator power":
            self.db.BasicCursor.execute("INSERT INTO FieldTransfer (Frequency, Field, Cal) "
                                     "VALUES (%f, %f, %f)" % (freq, fieldtarget, 0))
            self.db.BasicCursor.commit()
            self.db.BasicCursor.execute("SELECT * FROM FieldTransfer ORDER BY Frequency, Field")
            table = self.db.BasicCursor.fetchall()
            self.db.BasicCursor.execute("DELETE FROM FieldTransfer")
            self.db.BasicCursor.commit()
            for i in range(len(table)):
                self.db.BasicCursor.execute("INSERT INTO FieldTransfer (Frequency, Field, Cal) "
                                         "VALUES (%f, %f, %f)" % (table[i][0], table[i][1], table[i][2]))
                self.db.BasicCursor.commit()
        elif update and result == "Error input signal generator power":
            self.db.BasicCursor.execute(
                "UPDATE FieldTransfer SET Cal=%f WHERE Frequency=%f AND Field=%f" % (0, freq, fieldtarget))
            self.db.BasicCursor.commit()

    # noinspection PyGlobalUndefined
    def TransferIteration(self, freq, fieldtarget):
        global powerpm_am, powercouple, powertemp
        frequency = freq * 1e9
        sg_output_limit = -5
        kdmoniter = []
        flag = 0
        if fieldtarget == 0:
            self.db.BasicCursor.execute("UPDATE FieldTransfer SET PowerCal=%f WHERE Frequency=%f "
                                     "AND Cal=%f" % (0, freq, fieldtarget))
            self.db.BasicCursor.execute("UPDATE FieldTransfer SET FieldVerify=%f WHERE Frequency=%f "
                                     "AND Cal=%f" % (0, freq, fieldtarget))
            self.db.BasicCursor.commit()
            return 'Field target is 0'
        # iteration first time, power is -10 dBm
        self.sg.SGPowerSet(-10)
        self.ct.CTRoll(90)
        self.sg.SGCWFrec(frequency)
        self.pm.PMSetFreq(frequency)
        self.pa.PABand(frequency)
        self.sg.SGPowerOut('ON')
        self.pa.PAPowerOut('ON')
        time.sleep(10)
        powerpm = self.pm.PMFetch()
        fieldinit = self.ETS.ProbeField()[3]
        # calculate the kd first time
        kd = powerpm - 20 * log10(fieldinit)
        print('当前k值为%s, 功率计读数为%s, 初始电场显示值为%s' % (kd, powerpm, fieldinit))
        kdmoniter.append(kd)
        # enter the iteration
        for i in range(3):
            time.sleep(5)
            if flag == 1:
                break
            powerpm_am = kd + 20 * log10(fieldtarget)
            print('当前功率计读数目标值为%f, 目标场强值为%f' % (powerpm_am, fieldtarget))
            sg_initial = -30
            self.sg.SGPowerSet(sg_initial)  # set the initial power unit dBm
            for j in range(0, 5):  # iterate the power output
                time.sleep(3)  # delay 2 second
                if j == 0:
                    powercouple = self.pm.PMFetch()
                    print('当前第%d循环的功率计读数为%f' % (j + 1, powercouple))
                    powerdiff = powerpm_am - powercouple
                    powertemp = sg_initial + powerdiff
                    if self.sg.SGInRange(powertemp) and powertemp < sg_output_limit:
                        self.sg.SGPowerSet(powertemp)
                    else:
                        flag = 1
                        break
                elif j <= 9:
                    powercouple = self.pm.PMFetch()
                    print('当前第%d循环的功率计读数为%f' % (j + 1, powercouple))
                    powerdiff = powerpm_am - powercouple
                    powertemp += powerdiff
                    if self.sg.SGInRange(powertemp) and powertemp < sg_output_limit:
                        self.sg.SGPowerSet(powertemp)
                    elif 3 > powerdiff > 1:
                        break
                    else:
                        self.sg.SGPowerOut('OFF')
                        self.pa.PAPowerOut('OFF')
                        flag = 1
                        break
            print('当前的flag值为%d' % flag)
            fieldinit = self.ETS.ProbeField()[3]
            print('当前电场探头数值为%f' % fieldinit)
            if fieldinit != 0:
                kd = powercouple - 20 * log10(fieldinit)
                kdmoniter.append(kd)
        if flag == 1:
            print('Flag 1')
            self.db.BasicCursor.execute("UPDATE FieldTransfer SET PowerCal=%f WHERE Frequency=%f "
                                     "AND Cal=%f" % (0, freq, fieldtarget))
            self.db.BasicCursor.execute("UPDATE FieldTransfer SET FieldVerify=%f WHERE Frequency=%f "
                                     "AND Cal=%f" % (0, freq, fieldtarget))
            self.db.BasicCursor.commit()
            return "Error input signal generator power"
        elif flag == 0:
            print('Flag 0')
            if fieldinit == 0:
                self.db.BasicCursor.execute("UPDATE FieldTransfer SET PowerCal=%f WHERE Frequency=%f "
                                         "AND Cal=%f" % (0, freq, fieldtarget))
                self.db.BasicCursor.execute("UPDATE FieldTransfer SET FieldVerify=%f WHERE Frequency=%f "
                                         "AND Cal=%f" % (0, freq, fieldtarget))
                self.db.BasicCursor.commit()
                return 'Wrong Probe reading'
            else:
                self.db.BasicCursor.execute("UPDATE FieldTransfer SET PowerCal=%f WHERE Frequency=%f "
                                         "AND Cal=%f" % (powerpm_am, freq, fieldtarget))
                self.db.BasicCursor.execute("UPDATE FieldTransfer SET FieldVerify=%f WHERE Frequency=%f "
                                         "AND Cal=%f" % (fieldinit, freq, fieldtarget))
                self.db.BasicCursor.commit()
                return kdmoniter
        else:
            return 'WTF'


if __name__ == '__main__':
    test = FieldSensor('2016-3-3 ETS', fieldread='ETS')
    # freq1 = [17, 17.5, 18]
    # freq1 = [2, 2.5, 3, 3.5, 3.7, 3.8, 3.85, 3.9, 3.95]
    # freq2 = [4, 4.05, 4.1, 4.15, 4.5, 5, 5.5]
    # freq3 = [6]
    # test.FieldTest(specfreq=freq1 + freq2 + freq3, field=[5, 10])
    # print(test.FieldProd(18, 20, fieldread电场='ETS'))
    # freq1 = [1.05, 19, 20, 18.4]
    # test.fieldtransfer(3, 1.6, 18)
    # test.FieldProb(1, 10)
    #for i in range(10, 35):
     #   freq = 0.5 * i + 1
    test.FieldTest(specfreq=[18], field=[10, 20], transfer=False)
    #test.fieldomni(1, 20, 5)
    # test.FieldTest(specfreq=[10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18], transfer=True)
    # test.fieldtransfer(cal=1, specfreq=[2])
    # test.fieldomni(6, 10, 5, transfer=False)
    # print(test.TransferIteration(6, 8.996188))

