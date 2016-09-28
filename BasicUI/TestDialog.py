"""docstring..."""
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush


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
        # self.setMinimumWidth(700)
        # self.setMinimumHeight(490)
        self.setPalette(palette)
        self.setModal(False)

    def init_dialog(self):
        """Initial the test dialog."""
        self.create_widget()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ex = TestDialog()
    ex.show()
    sys.exit(app.exec_())
