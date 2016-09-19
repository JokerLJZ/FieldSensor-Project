"""A MicroSoft Office word class."""

import os
import win32com.client

__author__ = 'JokerLiu'


class Word(object):
    "Word print application."

    def __init__(self, filename="校准报告", report=True, language=0):
        """initialise the word application.

           ==============  ===================================================
           **Argument:**

           filename        Defalt is "校准报告", the name of the report.
           report          Defalt is True, True: Create a report doc.
                                           False: Create a orginal record doc.
           language        Defalt is 0, 0: Chinese
                                        1: Eglish
                                        2: Chinese and Eglish.
           ==============  ===================================================
        """
        self.language = 0
        self.report = True
        if report:
            self.filename = os.getcwd() + "\\TestResult\\Report\\" + filename
        else:
            self.filename = os.getcwd() + "\\TestResult\\Original\\" + filename
        self.wordapp = win32com.client.Dispatch("Word.Application")
        self.wordapp.Visible = 1
        self.doc = self.CreateReport(report, language)

    def CreateReport(self, report=True, language=0):
        """initialise the word application.

           ==============  ===================================================
           **Argument:**

           report          Defalt is True, True: Create a report doc.
                                           False: Create a orginal record doc.
           language        Defalt is 0, 0: Chinese
                                        1: Eglish
                                        2: Chinese and Eglish.
           ==============  ===================================================
        """
        if report:
            if language == 0:
                templatepath = '\\Data\\Report_cn.dotx'
            elif language == 1:
                templatepath = '\\Data\\Report_en.dotx'
            else:
                templatepath = '\\Data\\Report_encn.dotx'
        else:
            templatepath = '\\Data\\Original.dotx'
        templatepath = os.getcwd() + templatepath
        doc = self.wordapp.Documents.Add(Template=templatepath)
        return doc

    def DocSave(self, path=None):
        """Save the word doc to the path, self.filename is a good path."""
        self.doc.SaveAs(path)

    def TableInsert(self, rng, row, column):
        """Insert the table into the range and set the row and column num.

           ==============  ===================================================
           **Argument:**

           rng             Defalt is True, True: Create a report doc.
                                           False: Create a orginal record doc.
           language        Defalt is 0, 0: Chinese
                                        1: Eglish
                                        2: Chinese and Eglish.
           ==============  ===================================================
        """
        self.doc.Tables.Add(rng, row, column)

    def TableContent(self, tablenum, cellrow, cellcolum, insertcontent):
        """Insert the content to the specific table cell.

           ==============  ===================================================
           **Argument:**

           tablenum        The number of the table in doc.

           ==============  ===================================================
        """
        tab = self.doc.Tables[tablenum]
        cel = tab.Cell(cellrow, cellcolum)
        rng = cel.Range
        rng.Text = insertcontent

    def TableAddRow(self, tablenum=None, row=None):
        """Add one row to the table."""
        for i in range(row):
            self.doc.Tables(tablenum).Rows.Add()

    def CellDownMerge(self, tablenum=None, row=None, col=None, mergenum=None):
        self.doc.Tables(tablenum).Cell(row, col).Select()
        self.doc.Application.Selection.MoveDown(5, mergenum, 1)
        self.doc.Application.Selection.Cells.Merge()

    def CellRightMerge(self, tablenum=None, row=None, col=None, mergenum=None):
        self.doc.Tables(tablenum).Cell(row, col).Select()
        self.doc.Application.Selection.MoveRight(1, mergenum, 1)
        self.doc.Application.Selection.Cells.Merge()

    def InsertHeader(self, content="None", language=0, report=True):
        """Insert header to the document."""
        self.wordapp.ActiveWindow.ActivePane.View.SeekView = 9
        if language == 0:
            offset = 0
        elif language == 1:
            offset = 0
        elif language == 2:
            offset = 0
        if report:
            count = 3
            section = 1
        else:
            count = 3
            section = 0
        self.doc.Sections[section].Headers[0].Range.Select()
        sel = self.wordapp.Selection
        sel.MoveLeft(1)
        sel.MoveRight(count + offset)
        sel.InsertAfter(content)
        self.wordapp.ActiveWindow.ActivePane.View.SeekView = 0


if __name__ == "__main__":
    word = Word(report=True)
    # word.TableContent(2, 4, 1, "测试")
    # word.TableAddRow(2, 10)
    # word.CellDownMerge(2, 2, 1, 1)
    word.InsertHeader()
    # sel = word.doc.Tables(2).Cell(2, 1).Select()
    # word.doc.Application.Selection.MoveDown(5, 1, 1)
    # word.doc.Application.Selection.Cells.Merge()
    # word.DocSave(word.filename)
