import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 680, 480)
        self.setWindowTitle("Optimal Path Finder")
        self.initUI()

    def initUI(self):
        self.open_file_lb = QtWidgets.QLabel(self)
        self.open_file_lb.setText("Open File: ")
        self.open_file_lb.move(10, 10)

        self.file_path_lb = ""

        self.browse_bt = QtWidgets.QPushButton(self)
        self.browse_bt.setText("Browse")
        self.browse_bt.move(450, 10)

        self.browse_bt.clicked.connect(self.browse_file)
        self bt = QtWidgets.QPushButton(self)
        self.bt.setText("Click Me")
        self.bt.move(100, 100)
        self.bt.clicked.connect(self.clicked)

        # self.b1 = QtWidgets.QPushButton(self)
        # self.b1.setText("Click Me")
        # self.b1.clicked.connect(self.clicked)

    def clicked(self):
        # self.label.setText("You pressed the button")
        self.update()


    def browse_file(self):
        self.file_path = QFileDialog.getOpenFileName(self, "Open File", "/", "Text Files (*.txt)")
        self.file_path_lb.setText(self.file_path[0])
        self.update()
        QMessageBox.about(self, "File Path", self.file_path[0])

    def update(self):
        self.label.adjustSize()

class MyWindow2(QMainWindow):
    def __init__(self):
        super(MyWindow2, self).__init__()
        self.setGeometry(200, 200, 680, 480)
        self.setWindowTitle("Optimal Path Finder2")
        self.initUI()

    def initUI(self):
        self.open_file_lb = QtWidgets.QLabel(self)
        self.open_file_lb.setText("Open File: ")
        self.open_file_lb.move(10, 10)

        self.file_path_lb = ""

        self.browse_bt = QtWidgets.QPushButton(self)
        self.browse_bt.setText("Browse")
        self.browse_bt.move(450, 10)

        self.browse_bt.clicked.connect(self.browse_file)
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())

window()


