__author__ = 'TheJoker'
from filetools import get_path

from win32com.client import Dispatch


class EasyWord(object):
    """Print word application definition"""

    def __init__(self, filename='校准报告', report=True, language=0):
        """initialise the word application,then return the word handle"""
        if report:
            if language == 0:
                self.reportpath = get_path() + '\Data\Report_cn.dotx'
            elif language == 1:
                self.reportpath = get_path() + '\Data\Report_en.dotx'
            else:
                self.reportpath = get_path() + '\Data\Report_encn.dotx'
        else:
            self.reportpath = get_path() + '\Data\Original.dot'
        self.wordapp = Dispatch('Word.Application')
        self.wordapp.Visible = 1
        self.worddoc = self.wordapp.Documents.Add(Template=self.reportpath)  # import the report template file
        self.myRange = self.worddoc.Range(0, 0)
        self.paragraphcount = self.worddoc.Paragraphs.Count
        self.sectioncount = self.worddoc.Sections.Count
        self.tablecount = self.worddoc.Tables.Count

        if report:
            self.reportpath = get_path() + '/TestResult/' + filename
        else:
            self.reportpath = get_path() + '/TestResult/Original/' + filename + '_Original'

    def DocSave(self):
        self.worddoc.SaveAs(self.reportpath)

    def DocClose(self, changemodel=0):
        self.worddoc.Close(SaveChanges=changemodel)
        self.wordapp.Quit()

    def TableInsert(self, rng, row, column):
        self.worddoc.Tables.Add(rng, row, column)

    def TableContent(self, tablenum, cellrow, cellcolum, insertcontent):
        tab = self.worddoc.Tables[tablenum]
        cel = tab.Cell(cellrow, cellcolum)
        rng = cel.Range
        rng.Text = insertcontent

    def ParagraphsRange(self, paragraphnum=0):
        return self.worddoc.Paragraphs(paragraphnum).Range

    def ParagraphsInsert(self, rng):
        self.worddoc.Paragraphs.Add(rng)

    def TablenumUpdate(self):
        self.tablecount = self.worddoc.Paragraphs.Count

    def TableAutoFit(self, tablecount):
        self.worddoc.Tables(tablecount).AutoFitBehavior(1)

    @staticmethod
    def SetHorizonAlignment(rng, position=1):
        """
        :type rng: win32com word range object input
        :type position: 0, 1 or 2, where 0 means left alignment and 1 is middle 2 is right
        """
        rng.ParagraphFormat.Alignment = position

    @staticmethod
    def SetVerticalAlignment(cellrng, position=1):
        """
        :param cellrng: win32com word table cell object input
        :type position: 0, 1 or 2, where 0 means up alignment and 1 is middle 2 is down
        """
        cellrng.VerticalAlignment.Alignment = position

    def InsertSection(self, rng):
        self.worddoc.Sections.Add(rng)

    def InsertOriginalBlock(self, tablerow, tablecol):
        self.worddoc.Paragraphs.Add(self.worddoc.Paragraphs(21).Range)  # first test result table
        self.worddoc.Paragraphs.Add(self.worddoc.Paragraphs(21).Range)
        self.worddoc.Paragraphs.Add(self.worddoc.Paragraphs(21).Range)
        self.worddoc.Paragraphs(22).Style = '标题 2'
        self.worddoc.Tables.Add(self.worddoc.Paragraphs(23).Range, tablerow, tablecol)
        self.worddoc.Tables(2).Style = '网格型'
        self.TableAutoFit(2)

    def InsertReportBlock(self, tablerow, tablecol):
        self.worddoc.Paragraphs.Add(self.worddoc.Paragraphs(90).Range)  # first test result table
        self.worddoc.Paragraphs.Add(self.worddoc.Paragraphs(90).Range)
        self.worddoc.Paragraphs.Add(self.worddoc.Paragraphs(90).Range)
        self.worddoc.Paragraphs(91).Style = '标题 2'
        self.worddoc.Tables.Add(self.worddoc.Paragraphs(92).Range, tablerow, tablecol)
        self.worddoc.Tables(3).Style = '网格型'
        self.TableAutoFit(3)

    def InsertReportContinuousBlock(self, tablerow, tablecol):
        self.worddoc.Paragraphs.Add(self.worddoc.Paragraphs(90).Range)  # first test result table
        self.worddoc.Paragraphs.Add(self.worddoc.Paragraphs(90).Range)
        self.worddoc.Tables.Add(self.worddoc.Paragraphs(91).Range, tablerow, tablecol)
        self.worddoc.Tables(3).Style = '网格型'
        self.TableAutoFit(3)

    def InertBreak(self, rng):
        self.worddoc.Paragraphs.Add(rng)
        rng.InsertBreak()


if __name__ == '__main__':
    wordprint = EasyWord('123', report=True, language=0)
    wordprint.InsertReportBlock(1, 2)
    wordprint.InsertReportBlock(3, 4)
    # wordprint.InsertOriginalBlock(1, 2)
    # wordprint.InsertOriginalBlock(3, 4)
    wordprint.TableContent(2, 2, 2, '校准频率\nGHz')
    # wordprint.DocSave()
    # wordprint.DocClose()
