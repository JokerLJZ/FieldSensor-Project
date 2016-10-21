"""docstring..."""
# -*- coding: utf-8 -*-


from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMessageBox)
from Access import Access
from BasicPrintDialog import PrintDialog


class MainWindow(QMainWindow):
    """class string."""

    version = "1.0.0"

    def __init__(self, setting_dialog, central_box, test_dialog):
        """__init__ docstring.

           ==============  ====================
           **Argument:**
           setting_dialog  A dialog object inherit from SettingDialog.
           print_dialog    A dialog object inherit from PrintDialog.
           central_box     A QtWidget object inherit from CentralBox.
           test_dialog     A dialog object inherit from TestDialog.
           ==============  ===================
        """
        super(MainWindow, self).__init__()
        self.central_box = central_box
        self.setting_dialog = setting_dialog
        self.test_dialog = test_dialog
        self.CreateMainWindow()

    def CreateMainWindow(self):
        """CreateMainWindow string."""
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon("images/WindowIcon.png"))
        self.setAutoFillBackground(True)
        pic = "images/Back2.jpg"
        background_pic = QPixmap(pic)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_pic))
        self.setPalette(palette)
        self.statusBar()
        self.CreateMenu()
        self.CreateCentralWidget()

    def CreateMenu(self):
        """CreateMenu string."""
        self.file_menu = self.menuBar().addMenu("文件")

        self.setting_menu = self.menuBar().addMenu("设置")
        self.setting_menu.addAction(QAction("&选项", self,
                                            triggered=self.setting))

        self.printing_menu = self.menuBar().addMenu("打印")
        self.printing_menu.addAction(QAction("&打印报告", self,
                                             triggered=self.printing))

        self.about_menu = self.menuBar().addMenu("&About")
        self.about_menu.addAction(QAction("&About", self,
                                  statusTip="Show the application's About box",
                                  triggered=self.about))

        self.about_menu.addAction(QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=QApplication.instance().aboutQt))

        self.central_box.start_test_pushbutton.clicked.connect(self.start)

    def CreateCentralWidget(self):
        """CreateCentralWidget string."""
        self.setCentralWidget(self.central_box)

    def CreateDb(self):
        cert_num = self.central_box.cert_num_lineedit.text() + "_"
        device_serial = self.central_box.device_serial_lineedit.text() + "_"
        custom_name = self.central_box.custom_name_lineedit.text()
        datetime = (
            self.central_box.date_lineedit.dateTime().toString(
                "#yyyy-MM-dd HH:MM:ss#"))
        self.dbname = cert_num + device_serial + custom_name
        db = Access("TestResult\\DataBase\\%s.accdb" % self.dbname)
        basicdb = Access("Data\\BasicInfo.accdb")
        db.CreateSerial(datetime)
        namelist = basicdb.cursor.execute(
            "SELECT * FROM Infoname").fetchall()
        try:
            basicdb.Close()
        except:
            pass
        namelist = list(zip(*namelist))[0]
        db.CreateTable(
            tablename="TestInfo", columnnamelist=namelist,
            typelist=(["VARCHAR 30"] * namelist.__len__()))
        self.InsertDbInfo(db=db)

    def InsertDbInfo(self, db=None):
        basicdb = Access("/Data/BasicInfo.accdb")
        infolist = basicdb.cursor.execute(
            "SELECT Name FROM InfoName").fetchall()
        infolist = tuple(zip(*infolist))[0]
        lineeditlist = [
            obj.text() for obj in self.central_box.linebox[1::2]]
        lineeditlist.pop(len(lineeditlist) - 1)

    def start(self):
        """start docstring."""
        self.central_box.start_test_pushbutton.setEnabled(False)
        self.test_dialog.closeEvent = self.close_event
        self.test_dialog.show()
        self.CreateDb()

    def close_event(self, event):
        """close_event docstring."""
        self.central_box.start_test_pushbutton.setEnabled(True)

    def setting(self):
        """Setting string."""
        self.setting_dialog.show()

    def printing(self):
        """Printing string."""
        self.printing_dialog = PrintDialog()
        self.printing_dialog.show()

    def about(self):
        """About string."""
        QMessageBox.about(
            self, "About programme of CTTL",
            "<p><b>The test programme uses the python version of 3.4.4</p></b>"
            "<p>a recently used file menu in a Qt application.</p>")


if __name__ == '__main__':
    import sys
    from BasicSettingDialog import SettingDialog
    from BasicPrintDialog import PrintDialog
    from BasicCentralBox import CentralBox
    from BasicTestDialog import TestDialog
    app = QApplication(sys.argv)
    setting_dialog = SettingDialog()
    central_box = CentralBox()
    test_dialog = TestDialog()
    mainWin = MainWindow(
        setting_dialog=setting_dialog,
        central_box=central_box,
        test_dialog=test_dialog)
    mainWin.show()
    sys.exit(app.exec_())
