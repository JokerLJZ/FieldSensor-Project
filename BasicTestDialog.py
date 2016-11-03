"""docstring..."""
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class TestDialog(QDialog):
    """class docstring."""

    def __init__(self):
        """__init__ docstring."""
        super(TestDialog, self).__init__()
        self.setWindowTitle("测试程序")
        self.setWindowIcon(QIcon("images/WindowIcon.png"))
        self.setAutoFillBackground(True)
        pic = "images/Back2.jpg"
        background_pic = QPixmap(pic)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background_pic))
        self.setPalette(palette)
        self.setModal(False)
        self.InitDialog()
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stder = EmittingStream(textWritten=self.normalOutputWritten)
        self.closeEvent = self.CloseEvent

    def CloseEvent(self, event):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        cursor = self.textedit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textedit.setTextCursor(cursor)
        self.textedit.ensureCursorVisible()

    def InitDialog(self):
        """Initial the test dialog."""
        self.main_layout = QVBoxLayout()
        self.textedit = QTextEdit()
        self.main_layout.addWidget(self.textedit)
        self.setLayout(self.main_layout)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ex = TestDialog()
    ex.show()
    sys.exit(app.exec_())
