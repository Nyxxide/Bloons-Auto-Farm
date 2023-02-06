import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import WorkingUI
import mainwindow

app = QApplication(sys.argv)
window = QMainWindow()
ui = WorkingUI.Ui_BloonsFarm()
ui.setupUi(window)
window.show()
sys.exit(app.exec_())