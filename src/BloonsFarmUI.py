import os
import sys
import time
import pyautogui
import threading
import keyboard
import json
import cv2
import pyscreeze
from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont, QAction, QIcon, QFontMetrics
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMenuBar, \
    QMainWindow, QMenu
from pynput import mouse

from towerInfo import towerData
from menuNavInfo import menuNavData
import CoordinateHandler

#TODO: rework actual bloons interface to run as a while-loop that interfaces with a json file full of data
#TODO: rework json file construction
#TODO: add functionality to the secondary windows to edit Tower Positions

class BloonsUIPopup(QMainWindow):
    def __init__(self, title, popupmessage):
        super().__init__()
        # Error Window setup junk
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(self.resolve_path('Resources/UI/farmicon.ico')))
        self.setGeometry(550, 250, 300, 100)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.popupwindow = QWidget()
        self.popuplayout = QVBoxLayout()
        self.popuphbox = QHBoxLayout()

        # Font setup
        self.font_id = QFontDatabase.addApplicationFont(self.resolve_path('Resources/UI/LuckiestGuy-Regular.ttf'))
        self.font_name = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_name)

        # Add error window label widget
        self.popuplabel = QLabel(popupmessage, parent=self)
        self.custom_font.setPointSize(13)
        self.popuplabel.setFont(self.custom_font)

        # Add Widgets and set up layout of error window
        self.popuphbox.addWidget(self.popuplabel)
        self.popuplayout.addLayout(self.popuphbox)

        # Finalize error window setup
        self.popupwindow.setLayout(self.popuplayout)
        self.setCentralWidget(self.popupwindow)



    # Finding file path for assets
    def resolve_path(self, path):
        if getattr(sys, "frozen", False):
            # If the 'frozen' flag is set, we are in bundled-app mode!
            resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
        else:
            # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
            resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))

        return resolved_path

class BloonsUICoords(QMainWindow):
    def __init__(self, title, button_labels, fileName):
        super().__init__()
        # Secondary Window UI setup junk
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(self.resolve_path('Resources/UI/btdfarmicon.ico')))
        self.setGeometry(550, 250, 400, 300)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.sub = QWidget()
        self.outvbox = QVBoxLayout()
        self.sublayout = QHBoxLayout()
        self.subvbox = QVBoxLayout()

        # Font setup
        self.font_id = QFontDatabase.addApplicationFont(self.resolve_path('Resources/UI/LuckiestGuy-Regular.ttf'))
        self.font_name = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_name)

        # Add sub window label widgets
        self.subwinlab = QLabel("Select a option to change it's position:", parent=self)
        self.custom_font.setPointSize(15)
        self.subwinlab.setFont(self.custom_font)

        self.subwinlab2 = QLabel("Click where you want the new mouse click position to be", parent=self)
        self.custom_font.setPointSize(15)
        self.subwinlab2.setFont(self.custom_font)
        self.subwinlab2.hide()

        # Add Widgets and set up layout of sub windows
        self.outvbox.addWidget(self.subwinlab)

        # Create sub window buttons and add them to layout
        self.buttons = []
        for labels in button_labels:
            button = QPushButton(labels, parent=self)
            button.setFixedSize(200, 50)
            self.custom_font.setPointSize(13)
            button.setFont(self.custom_font)
            button.clicked.connect(self.resetPos)
            self.subvbox.addWidget(button)
            self.buttons.append(button)

        # Finalize and setup of sub windows
        self.padding = QWidget()
        self.sublayout.addWidget(self.padding)
        self.sublayout.addLayout(self.subvbox)
        self.sublayout.addWidget(self.padding)
        self.outvbox.addLayout(self.sublayout)
        self.sub.setLayout(self.outvbox)
        self.setCentralWidget(self.sub)

        # Current File Denoted by the menu option chosen
        self.currentFile = fileName

    # Function for finding file path for assets
    def resolve_path(self, path):
        if getattr(sys, "frozen", False):
            # If the 'frozen' flag is set, we are in bundled-app mode!
            resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
        else:
            # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
            resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))

        return resolved_path

    # Function for resetting Tower Positions
    def resetPos(self):
        try:
            with open('Tower Positions/' + self.currentFile + '.json') as f:
                def on_click(x,y,button,pressed):
                    self.x = x
                    self.y = y
                    if pressed:
                        return False

                with mouse.Listener(on_click=on_click) as listener:
                    listener.join()


                button_name = self.sender().text().lower().replace(' ', '_')
                with open('Tower Positions/deflation.json', 'r+') as f:
                    pos = json.load(f)
                    pos["towers"][button_name]["x"] = self.x
                    pos["towers"][button_name]["y"] = self.y
                    f.seek(0)
                    f.truncate()
                    json.dump(pos, f)
                self.success = BloonsUIPopup("Success", "Position successfully changed!")
                self.success.show()
        except FileNotFoundError:
            self.error = BloonsUIPopup("No File Found", "Error! coordinate file not found! (Run one of the default farms first)")
            self.error.show()

class BloonsUIMain(QMainWindow):
    def __init__(self):
        self.BloonsUI = QApplication([])
        super().__init__()
        # Tower setup
        self.deflationTowers = [towerData('d', 824, 366, 4, 0, 2),
                                towerData('f', 831, 307, 4, 2, 0),
                                towerData('f', 834, 764, 4, 2, 0),
                                towerData('d', 835, 696, 4, 0, 2)]

        self.deflation2xTowers = [towerData('z', 1608, 501, 2, 0, 5),
                                  towerData('f', 1551, 544, 4, 2, 0),
                                  towerData('k', 1581, 622, 2, 3, 0)]

        self.deflationMenuNav = menuNavData("expert", "inferno", "easy", "deflation")
        self.deflation2xMenuNav = menuNavData("expert", "inferno", "easy", "deflation")

        # Gen the Pre-made .json Files
        if not os.path.exists('Tower Positions'):
            os.mkdir('Tower Positions')
        if not os.path.exists('Tower position/deflation.json'):
            CoordinateHandler.gen(self.deflationTowers, self.deflationMenuNav, "deflation")
        if not os.path.exists('Tower position/deflation_2x_cash.json'):
            CoordinateHandler.gen(self.deflation2xTowers, self.deflation2xMenuNav, "deflation_2x_cash")

        # Main Window UI setup junk
        self.setWindowTitle('Bloons Auto Farm')
        self.setWindowIcon(QtGui.QIcon(self.resolve_path('Resources/UI/btdfarmicon.ico')))
        self.setGeometry(550, 250, 800, 600)
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.mainhboxtop = QHBoxLayout()
        self.mainhboxbotrows = []
        self.mainhboxbot = QHBoxLayout()
        self.runninghbox = QHBoxLayout()
        self.runningvbox = QVBoxLayout()
        self.runninglabelhbox = QHBoxLayout()
        self.runningbuttonhbox = QHBoxLayout()

        # Font setup
        self.font_id = QFontDatabase.addApplicationFont(self.resolve_path('Resources/UI/LuckiestGuy-Regular.ttf'))
        self.font_name = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_name)

        # Add main window label widgets
        self.mainlabel = QLabel('Choose your desired farming method', parent=self.window)
        self.mainlabel.setFixedSize(600,50)
        self.custom_font.setPointSize(24)
        self.mainlabel.setFont(self.custom_font)

        self.activeLabel = QLabel('', parent=self.window)
        self.custom_font.setPointSize(17)
        self.activeLabel.setFont(self.custom_font)
        self.activeLabel.setAlignment(Qt.AlignCenter)
        self.activeLabel.hide()


        # Add a menu bar
        self.menubar = QMenuBar()
        self.editmenu = QMenu("Edit", self.menubar)

        #Add menu options to menu bar
        for file in os.listdir('Tower Positions'):
            if file.endswith('.json'):
                self.editcoords_action = QAction(file.replace('_', ' ').title().replace('.Json', ''), self)
                self.editmenu.addAction(self.editcoords_action)
                self.editcoords_action.triggered.connect(self.editcoords)

        self.menubar.addMenu(self.editmenu)

        # Build Farming Buttons
        self.farm_button_list = []
        self.buttonnum = 0
        self.buttonrow = -1

        for file in os.listdir('Tower Positions'):
            if file.endswith('.json'):
                if self.buttonnum % 4 == 0:
                    self.mainhboxbotrows.append(QHBoxLayout())
                    self.buttonrow += 1
                self.startLoopbutton = QPushButton(file.replace('_', ' ').title().replace('.Json', ''), parent=self.window)
                self.startLoopbutton.setFixedSize(200, 100)
                self.custom_font.setPointSize(20)
                self.startLoopbutton.setFont(self.custom_font)
                self.set_max_font_size(self.startLoopbutton, 20)
                self.startLoopbutton.clicked.connect(self.startLoop)
                self.mainhboxbotrows[self.buttonrow].addWidget(self.startLoopbutton)
                self.farm_button_list.append(self.startLoopbutton)
                self.buttonnum += 1

        # Build Quit Button
        self.quitbutton = QPushButton('Quit to Menu', parent=self.window)
        self.quitbutton.hide()
        self.custom_font.setPointSize(20)
        self.quitbutton.setFont(self.custom_font)
        self.quitbutton.setFixedSize(200, 100)
        self.quitbutton.clicked.connect(self.quit)

        # Add Widgets and set up layout of main UI page
        self.mainhboxtop.addWidget(self.mainlabel)
        self.layout.setAlignment(self.mainhboxtop, Qt.AlignCenter)
        self.layout.setAlignment(self.mainhboxbot, Qt.AlignCenter)
        self.layout.addLayout(self.mainhboxtop)
        for rows in self.mainhboxbotrows:
            self.layout.addLayout(rows)

        # Add Widgets and set up layout of Deflation/Deflation 2x Cash pages
        self.runningvbox.addWidget(self.activeLabel)
        self.runningvbox.addWidget(self.quitbutton)
        self.runningvbox.setAlignment(self.quitbutton, Qt.AlignCenter)
        self.runningvbox.setAlignment(self.activeLabel, Qt.AlignCenter)
        self.runninghbox.addLayout(self.runningvbox)
        self.layout.addLayout(self.runninghbox)

        # Finalize UI setup and open the window
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)
        self.setMenuBar(self.menubar)
        self.show()

        # Reset Coordinates
        self.x = 0
        self.y = 0
        
        # Thread setup
        self.running = False

        # Active File being used by the program
        self.activeFile = None

    # Function used in the loop to handle menu navigation
    def menuNav(self, fileName):
        with open(self.resolve_path('Tower Positions/' + fileName + '.json')) as f:
            menuData = json.load(f)
        mapDifficulty = menuData["menuNav"]["mapDifficulty"]
        map = menuData["menuNav"]["map"]
        difficulty = menuData["menuNav"]["difficulty"]
        mode = menuData["menuNav"]["mode"]
        found = False
        x, y = 0, 0
        clock = 0
        imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Maps/' + map + '.png')), confidence=0.9)
        while imageToFind is None and clock is not 3:
            if not self.running:
                print("We're not running anymore, exit!")
                return
            else:
                print(f"We're still running, keep sleeping...")
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Maps/' + map + '.png')), confidence=0.9)
                clock += 1
        if (imageToFind is None):
            while not found:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping...")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MapDifficulty/' + mapDifficulty + '.png')), confidence=0.9)
                    while imageToFind is None:
                        if not self.running:
                            print("We're not running anymore, exit!")
                            return
                        else:
                            print(f"We're still running, keep sleeping...")
                            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MapDifficulty/' + mapDifficulty + '.png')), confidence=0.9)
                    x, y, _, _ = imageToFind
                    pyautogui.click(x, y)
                    clock = 0
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Maps/' + map + '.png')), confidence=0.9)
                    while imageToFind is None and clock is not 5:
                        if not self.running:
                            print("We're not running anymore, exit!")
                            return
                        else:
                            print(f"We're still running, keep sleeping...")
                            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Maps/' + map + '.png')), confidence=0.9)
                            clock += 1
                    if imageToFind is not None:
                        x, y, _, _ = imageToFind
                        found = True
        else:
            x, y, _, _ = imageToFind
            found = True
        y += 20
        pyautogui.click(x, y)
        imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Difficulty/' + difficulty + '.png')), confidence=0.9)
        while imageToFind is None:
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Difficulty/' + difficulty + '.png')), confidence=0.9)
        x, y, _, _ = imageToFind
        pyautogui.click(x, y)
        imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Mode/' + mode + '.png')), confidence=0.7)
        while imageToFind is None:
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Mode/' + mode + '.png')), confidence=0.7)
        x, y, _, _ = imageToFind
        pyautogui.click(x, y)


    # Function used in the loop to handle tower placement in a given map
    def towerPlacement(self, fileName):
        with open('Tower Positions/' + fileName +'.json', 'r') as f:
            towerData = json.load(f)
        for tower, value in towerData["towers"].items():
            hotkey = towerData["towers"][tower]["hotkey"]
            x = towerData["towers"][tower]["x"]
            y = towerData["towers"][tower]["y"]
            top = towerData["towers"][tower]["top"]
            middle = towerData["towers"][tower]["middle"]
            bottom = towerData["towers"][tower]["bottom"]
            pyautogui.click(x, y)
            time.sleep(0.25)
            keyboard.press_and_release(hotkey)
            time.sleep(0.25)
            pyautogui.click(x, y)
            time.sleep(0.25)
            pyautogui.click(x, y)
            for i in range(top):
                time.sleep(0.25)
                keyboard.press_and_release(',')
            for i in range(middle):
                time.sleep(0.25)
                keyboard.press_and_release('.')
            for i in range(bottom):
                time.sleep(0.25)
                keyboard.press_and_release('/')
            time.sleep(0.25)



    # Looping Farm Function
    def farmLoop(self):
        while self.running:
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/homemenu.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping...")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/homemenu.png')), confidence=0.9)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            self.menuNav(self.activeFile)
            clock = 0
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/existinggame.png')), confidence=0.9)
            while imageToFind is None and clock is not 5:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping...")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/existinggame.png')), confidence=0.9)
                    clock += 1
            if (imageToFind is not None):
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/existingok.png')), confidence=0.9)
                while imageToFind is None:
                    if not self.running:
                        print("We're not running anymore, exit!")
                        return
                    else:
                        print(f"We're still running, keep sleeping...")
                        imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/existingok.png')), confidence=0.9)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/ingame.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping...")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/ingame.png')), confidence=0.9)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/tooltipcheck.png')), confidence=0.9)
            clock = 0
            while imageToFind is None and clock is not 5:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping...")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/tooltipcheck.png')), confidence=0.9)
                    clock += 1
            if (imageToFind is not None):
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/tooltipcheck.png')), confidence=0.9)
                while imageToFind is not None:
                    print("waiting for tooltip to despawn")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/tooltipcheck.png')), confidence=0.9)
            self.towerPlacement(self.activeFile)
            keyboard.press_and_release('space')
            time.sleep(0.25)
            keyboard.press_and_release('space')
            keyboard.press_and_release('esc')
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping...")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame.png')), confidence=0.9)
                    levelup = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/levelup.png')), confidence=0.9)
                    if levelup is not None:
                        pyautogui.click(x, y)
                        pyautogui.click(x, y)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame2.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping...")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame2.png')), confidence=0.9)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            clock = 0
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/collectionevent.png')), confidence=0.9)
            while imageToFind is None and clock is not 10:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping...")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/collectionevent.png')), confidence=0.9)
                    clock += 1
            if (imageToFind is not None):
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/instamonkey.png')), confidence=0.7)
                while imageToFind is None:
                    if not self.running:
                        print("We're not running anymore, exit!")
                        return
                    else:
                        print(f"We're still running, keep sleeping...")
                        imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/instamonkey.png')), confidence=0.7)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.8)
                pyautogui.click(x, y)
                time.sleep(0.8)
                while True:
                    if not self.running:
                        print("We're not running anymore, exit!")
                        return
                    else:
                        print(f"We're still running, keep sleeping...")
                        imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/instamonkey.png')), confidence=0.7)
                        if (imageToFind is None):
                            break
                        x, y, _, _ = imageToFind
                        pyautogui.click(x, y)
                        time.sleep(0.8)
                        pyautogui.click(x, y)
                        time.sleep(0.8)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endcollection.png')), confidence=0.9)
                while imageToFind is None:
                    if not self.running:
                        print("We're not running anymore, exit!")
                        return
                    else:
                        print(f"We're still running, keep sleeping...")
                        imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endcollection.png')), confidence=0.9)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
            print("Done with the loop!")


    def editcoords(self):
        menuoption = self.sender().text().lower().replace(' ', '_')
        with open('Tower Positions/' + menuoption + '.json', 'r') as f:
            tower_names = json.load(f)
            button_labels = [x.replace('_', ' ').title() for x in tower_names["towers"].keys()]
        self.defsubwin = BloonsUICoords(menuoption.replace('_', ' ').title().replace('.Json', '') ,button_labels, menuoption)
        self.defsubwin.show()
        self.defsubwin.raise_()

    # Define button functionality for main window
    def startLoop(self):
        self.running = True
        self.activeFile = self.sender().text().lower().replace(' ', '_')
        self.activeLabel.setText('Program is currently running ' + self.activeFile.replace('_', ' ').title() + ' farm')
        self.activeLabel.show()
        self.quitbutton.show()
        self.mainlabel.hide()
        for button in self.farm_button_list:
            button.hide()
        self.thread = threading.Thread(target=self.farmLoop, daemon=True)
        self.thread.start()

    # Define button functionality for quit button
    def quit(self):
        self.running = False
        self.activeFile = ''
        self.activeLabel.hide()
        self.activeLabel.setText('')
        self.quitbutton.hide()
        self.mainlabel.show()
        for button in self.farm_button_list:
            button.show()
        self.thread.join()


    # Finding file path for assets
    def resolve_path(self, path):
        if getattr(sys, "frozen", False):
            # If the 'frozen' flag is set, we are in bundled-app mode!
            resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
        else:
            # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
            resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))

        return resolved_path

    def set_max_font_size(self, button, max_font_size):
        font = button.font()
        font_metrics = QFontMetrics(font)
        text = button.text()
        width = button.width()
        height = button.height()

        # Decrease font size until the text fits within the button
        while font_metrics.boundingRect(text).width() > width or font_metrics.height() > height:
            max_font_size -= 1
            font.setPointSize(max_font_size)
            font_metrics = QFontMetrics(font)

        button.setFont(font)

    # Run program
    def run(self):
        sys.exit(self.BloonsUI.exec())

if __name__ == "__main__":
    BloonsUI = BloonsUIMain()
    BloonsUI.run()
