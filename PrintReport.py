"""A MicroSoft Office access class."""

import os
import re
from math import log10, sqrt

import matplotlib.pyplot as plt

from Access import Access
from Word import Word

__author__ = 'JokerLiu'


class FSPrintReport(object):
    """A print report class print the report."""

    def __init__(self, filename="校准报告", report=True, language=0,
                 dbname=None):
        """Initial the fs print report class.

           ==============  ===================================================
           **Argument:**

           filename        Defalt is "校准报告", the name of the report.
           report          Defalt is True, True: Create a report doc.
                                           False: Create a orginal record doc.
           language        Defalt is 0, 0: Chinese
                                        1: Eglish
                                        2: Chinese and Eglish.
           dbname          Defalt is None, the database should save in the
                           \\TestResult\\DataBase folder
           ==============  ===================================================
        """
        self.doc = Word(filename=filename, report=report, language=language)
        self.db = Access("\\TestResult\\DataBase\\" + dbname)
        self.basicinfo = Access("\\Data\\Test.accdb")
        if report:
            self.position = "ReportPosition"
        else:
            self.position = "OriginalPosition"
        self.report = report
        self.language = language
        self.PrintInfo()

    def PrintFrequencyResponse(self):
        """Print the frequency response."""
        sql = ("SELECT Frequency__GHz * 1000, Field__V_per_m, "
               "FieldResult__V_per_m FROM 场强频率响应 ORDER BY Frequency__GHz")
        testdata = list(self.db.cursor.execute(sql).fetchall())
        testdata = [list(obj) for obj in testdata]
        rownum = testdata.__len__()
        for obj in testdata:
            obj[2] = "%0.2f" % obj[2]
            obj += ("%0.2f" % (float(obj[1]) / float(obj[2])), )
            sql = ("SELECT Uncertainty FROM Uncertainty WHERE %s < FreqUpper "
                   "AND %s >= FreqLower" % ((obj[0] / 1000), (obj[0] / 1000)))
            obj += ("%0.1f"
                    % (self.basicinfo.cursor.execute(sql).fetchone()[0]), )
        sql = ("SELECT TableNum FROM %s WHERE "
               "TestItems='场强频率响应'" % self.position)
        tablenum = self.basicinfo.cursor.execute(sql).fetchone()[0]
        self.doc.TableAddRow(tablenum=tablenum, row=rownum)
        # 打印不确定度k值
        if not self.report:
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=1, cellcolum=5,
                insertcontent="测量不确定度(k=2) (dB)")
        for i in range(rownum):
            for j in range(5):
                self.doc.TableContent(
                    tablenum=tablenum - 1, cellrow=i + 2, cellcolum=j + 1,
                    insertcontent=testdata[i][j])

    def PrintFieldLinearity(self):
        """Print the field linearity."""
        sql = ("SELECT Frequency__GHz, Field__V_per_m, FieldResult__V_per_m"
               " FROM 场强线性度 ORDER BY Frequency__GHz, Field__V_per_m")
        testdata = list(self.db.cursor.execute(sql).fetchall())
        testdata = [list(obj) for obj in testdata]
        rownum = testdata.__len__()
        sql = ("SELECT TableNum FROM %s WHERE "
               "TestItems='场强线性度'" % self.position)
        tablenum = self.basicinfo.cursor.execute(sql).fetchone()[0]
        self.doc.TableAddRow(tablenum=tablenum, row=rownum)
        for obj in testdata:
            obj[2] = "%0.2f" % obj[2]
            obj += ("%0.2f" % (float(obj[1]) / float(obj[2])), )
            sql = ("SELECT Uncertainty FROM Uncertainty WHERE %s < FreqUpper "
                   "AND %s >= FreqLower" % (obj[0], obj[0]))
            obj += ("%0.1f"
                    % (self.basicinfo.cursor.execute(sql).fetchone()[0]), )
        # 打印不确定度k值
        if not self.report:
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=1, cellcolum=5,
                insertcontent="测量不确定度(k=2) (dB)")
        for i in range(rownum):
            if i % 2 == 1:
                self.doc.CellDownMerge(
                    tablenum=tablenum, row=i + 1, col=1, mergenum=1)
                self.doc.CellDownMerge(
                    tablenum=tablenum, row=i + 1, col=5, mergenum=1)
            if i % 2 == 0:
                assert testdata[i][0] == testdata[i + 1][0]
                assert testdata[i][1] != testdata[i + 1][1]
                self.doc.TableContent(
                    tablenum=tablenum - 1, cellrow=i + 2, cellcolum=1,
                    insertcontent=testdata[i][0])
                self.doc.TableContent(
                    tablenum=tablenum - 1, cellrow=i + 2, cellcolum=5,
                    insertcontent=testdata[i][4])
            for j in range(1, 4):
                self.doc.TableContent(
                    tablenum=tablenum - 1, cellrow=i + 2, cellcolum=j + 1,
                    insertcontent=testdata[i][j])

    def PrintIsotrophy(self, dbname=None):
        """Print isotrophy."""
        freqname = re.search(r'\d+\.{0,1}\d{0,}(e-\d+)?MHz', dbname).group(0)
        freq = freqname[:-3]
        intensity = re.search(r"\d+V", dbname).group(0)
        sql = "SELECT MAX(TestSeriesNo), MIN(TestSeriesNo) FROM %s" % dbname
        serial = self.db.cursor.execute(sql).fetchone()
        assert serial[0] == serial[1]
        sql = ("SELECT Degree__°, Field__V_per_m FROM %s"
               " ORDER BY Degree__°" % dbname)
        testdata = list(self.db.cursor.execute(sql).fetchall())
        rownum = testdata.__len__()
        sql = ("SELECT TableNum FROM %s WHERE "
               "TestItems='全向性'" % self.position)
        tablenum = self.basicinfo.cursor.execute(sql).fetchone()[0]
        assert rownum == 72
        # 打印标题
        if self.report is not True or self.language == 0:
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=1, cellcolum=1,
                insertcontent="%s各向同性" % freqname)
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=2, cellcolum=1,
                insertcontent="场强值%s/m" % intensity)
        elif self.language == 1:
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=1, cellcolum=1,
                insertcontent="Isotropy at %s" % freqname)
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=2, cellcolum=1,
                insertcontent="Field Strength %s/m" % intensity)
        # 打印不确定度
        sql = ("SELECT Uncertainty FROM Uncertainty WHERE %s < FreqUpper "
               "AND %s >= FreqLower"
               % (float(freq) / 1000, float(freq) / 1000))
        uncertainty = self.basicinfo.cursor.execute(sql).fetchone()[0]
        if self.report is False or self.language == 0:
            uncertsentense = "测量结果的不确定度"
        else:
            uncertsentense = "Measurement uncertainty"
        self.doc.TableContent(tablenum=tablenum - 1, cellrow=23, cellcolum=1,
                              insertcontent="%s (k=2): %0.1f dB"
                              % (uncertsentense, uncertainty))
        # 打印数据
        for i in range(19):
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=i + 4, cellcolum=2,
                insertcontent="%0.2f" % testdata[i][1])
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=i + 4, cellcolum=4,
                insertcontent="%0.2f" % testdata[i + 19][1])
            self.doc.TableContent(
                tablenum=tablenum - 1, cellrow=i + 4, cellcolum=6,
                insertcontent="%0.2f" % testdata[i + 38][1])
            if i < 15:
                self.doc.TableContent(
                    tablenum=tablenum - 1, cellrow=i + 4, cellcolum=8,
                    insertcontent="%0.2f" % testdata[i + 57][1])
        sql = ("SELECT MAX(Field__V_per_m), MIN(Field__V_per_m) FROM %s"
               % dbname)
        [maxdata, mindata] = self.db.cursor.execute(sql).fetchone()
        isotrophy = 20 * log10(maxdata / (sqrt(maxdata * mindata)))
        self.doc.TableContent(
            tablenum=tablenum, cellrow=1, cellcolum=2,
            insertcontent="%0.2f" % maxdata)
        self.doc.TableContent(
            tablenum=tablenum, cellrow=2, cellcolum=2,
            insertcontent="%0.2f" % mindata)
        self.doc.TableContent(
            tablenum=tablenum, cellrow=3, cellcolum=2,
            insertcontent="%0.2f" % isotrophy)
        testdata = list(map(list, zip(*testdata)))
        testdata[1] = list(
            map(lambda x: 20 * log10(x / maxdata), testdata[1]))
        plt.figure(figsize=(8, 5))
        plt.plot(
            testdata[0], testdata[1],
            color="black", linewidth=2)
        plt.xlabel("Angle(°)")
        plt.ylabel("Normalization field strenth(dB)")
        plt.title("Isotrophy(%s)" % freqname)
        plt.xlim(0, 355)
        plt.grid(axis='y')
        plt.savefig(os.getcwd() + '/TestResult/Picture/result.png')
        self.doc.doc.InlineShapes.AddPicture(
            os.getcwd() + "\\TestResult\\Picture\\result.png", False, True,
            self.doc.doc.Tables(tablenum + 2).Cell(1, 1).Range)

    def PrintInfo(self):
        """Print the basic info of the report."""
        infoname = list(zip(*self.basicinfo.cursor.execute(
            "SELECT Name FROM Infoname").fetchall()))[0]
        for obj in infoname:
            s = ("SELECT Col, Row, TableNum FROM %s WHERE "
                 "TestItems=%s" % (self.position, "'" + obj + "'"))
            [col, row, tablenum] = self.basicinfo.cursor.execute(s).fetchone()
            s = "SELECT %s FROM TestInfo" % obj
            content = self.db.cursor.execute(s).fetchone()[0]
            if tablenum is not None:
                self.doc.TableContent(
                    tablenum=tablenum, cellrow=row, cellcolum=col,
                    insertcontent=content)

    def PrintDate(self, testseries=1):
        """Print the date of the report."""
        sql = ("SELECT FORMAT(TestDate, 'yyyy年mm月dd日'), "
               "FORMAT(TestDate, 'mmmm dd, yyyy') FROM TestDate "
               "WHERE TestSeriesNo=%s" % testseries)
        [datecn, dateen] = self.db.cursor.execute(sql).fetchone()
        if self.report is not True:
            date = datecn
            s = ("SELECT TableNum, row, Col FROM %s WHERE "
                 "TestItems='日期2'" % self.position)
            [tablenum, row, col] = self.basicinfo.cursor.execute(s).fetchone()
            self.doc.TableContent(
                tablenum=tablenum, cellrow=row, cellcolum=col,
                insertcontent=date)
        elif self.language == 0:
            date = datecn
        elif self.language == 1:
            date = dateen
        s = ("SELECT TableNum, row, Col FROM %s WHERE "
             "TestItems='日期1'" % self.position)
        [tablenum, row, col] = self.basicinfo.cursor.execute(s).fetchone()
        self.doc.TableContent(
            tablenum=tablenum, cellrow=row, cellcolum=col,
            insertcontent=date)

    def PrintCertNum(self):
        """Print certificate number."""
        sql = ("SELECT TableNum FROM %s WHERE "
               "TestItems='证书编号'" % self.position)
        sql = ("SELECT 证书编号 FROM TestInfo")
        certnum = self.db.cursor.execute(sql).fetchone()[0]
        print(certnum)
        self.doc.InsertHeader(
            "%s" % certnum, language=self.language, report=self.report)

    def PrintInstrument(self):
        """Print instrument info."""
        sql = ("SELECT TableNum FROM %s WHERE "
               "TestItems='设备列表'" % self.position)
        tablenum = self.basicinfo.cursor.execute(sql).fetchone()[0]
        if self.report is not True:
            sql = ("SELECT Instrument, Model, SerialNum, Uncertainty,"
                   "StateBefore, StateAfter FROM InstrumentCn")
            testdata = self.basicinfo.cursor.execute(sql).fetchall()
            rownum = testdata.__len__()
            for i in range(rownum):
                for j in range(len(testdata[0])):
                    self.doc.TableContent(
                        tablenum=tablenum, cellrow=i + 2, cellcolum=j + 2,
                        insertcontent=testdata[i][j])
        elif self.language == 0:
            sql = ("SELECT Instrument, Uncertainty, Certificate, DueDate"
                   " FROM InstrumentCn")
            testdata = self.basicinfo.cursor.execute(sql).fetchall()
            rownum = testdata.__len__()
            for i in range(rownum):
                for j in range(len(testdata[0])):
                    self.doc.TableContent(
                        tablenum=tablenum, cellrow=i + 5, cellcolum=j + 1,
                        insertcontent=testdata[i][j])
        elif self.language == 1:
            sql = ("SELECT Instrument, Uncertainty, Certificate, DueDate"
                   " FROM InstrumentEn")
            testdata = self.basicinfo.cursor.execute(sql).fetchall()
            rownum = testdata.__len__()
            for i in range(rownum):
                for j in range(len(testdata[0])):
                    self.doc.TableContent(
                        tablenum=tablenum, cellrow=i + 5, cellcolum=j + 1,
                        insertcontent=testdata[i][j])


if __name__ == "__main__":
    a = FSPrintReport(dbname="2016-9-8 ETS.mdb", report=False, language=0)
    a.PrintFieldLinearity()
    a.PrintFrequencyResponse()
    a.PrintIsotrophy("全向性_1000MHz_20V")
    a.PrintInstrument()
    a.PrintCertNum()
    a.PrintDate()
    # a.doc.DocSave()
