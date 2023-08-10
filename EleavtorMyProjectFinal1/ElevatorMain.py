from PyQt5.QtWidgets import QMainWindow
import ElevatorUI
import sys
from PyQt5.QtWidgets import QApplication

class Elevator(QMainWindow, ElevatorUI.Ui_Window):
    def __init__(self):
        super().__init__()
        self.setupUI(self)
        self.setWindowTitle("Elevator Dispatch")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Elevator()
    win.show()
    sys.exit(app.exec_())
