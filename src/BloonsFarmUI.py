# -*- coding: utf-8 -*-
import os
import sys
# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import time
import pyautogui
import threading
import keyboard
import json
import cv2
import pyscreeze
from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont, QAction, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMenuBar, \
    QMainWindow, QMenu
from pynput import mouse

import CoordinateHandler

#TODO: rework actual bloons interface to run as a while-loop that interfaces with a json file full of data
#TODO: rework json file construction
#TODO: add functionality to the secondary windows to edit tower positions

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

class BloonsUISub(QMainWindow):
    def __init__(self, title, button_labels):
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

    # Function for finding file path for assets
    def resolve_path(self, path):
        if getattr(sys, "frozen", False):
            # If the 'frozen' flag is set, we are in bundled-app mode!
            resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
        else:
            # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
            resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))

        return resolved_path

    # Function for resetting tower positions
    def resetPos(self):
        try:
            with open('towerpos.json') as f:
                def on_click(x,y,button,pressed):
                    self.x = x
                    self.y = y
                    if pressed:
                        return False

                with mouse.Listener(on_click=on_click) as listener:
                    listener.join()


                button_name = self.sender().text().lower().replace(' ', '_')
                with open('towerpos.json', 'r+') as f:
                    pos = json.load(f)
                    pos[button_name] = self.x, self.y
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
        # Main Window UI setup junk
        self.setWindowTitle('Bloons Auto Farm')
        self.setWindowIcon(QtGui.QIcon(self.resolve_path('Resources/UI/btdfarmicon.ico')))
        self.setGeometry(550, 250, 800, 600)
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.mainhboxtop = QHBoxLayout()
        self.mainhboxbot = QHBoxLayout()
        self.defhboxtop = QHBoxLayout()
        self.defhboxbot = QHBoxLayout()
        self.def2xhboxtop = QHBoxLayout()
        self.def2xhboxbot = QHBoxLayout()

        # Font setup
        self.font_id = QFontDatabase.addApplicationFont(self.resolve_path('Resources/UI/LuckiestGuy-Regular.ttf'))
        self.font_name = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font = QFont(self.font_name)

        # Add main window label widgets
        self.mainlabel = QLabel('Choose your desired farming method', parent=self.window)
        self.mainlabel.setFixedSize(600,50)
        self.custom_font.setPointSize(24)
        self.mainlabel.setFont(self.custom_font)

        self.deflationlabel = QLabel('Program is currently running Deflation farm', parent=self.window)
        self.deflationlabel.setFixedSize(618,50)
        self.custom_font.setPointSize(20)
        self.deflationlabel.setFont(self.custom_font)
        self.deflationlabel.hide()

        self.deflation2xlabel = QLabel('Program is currently running 2x Cash Deflation farm', parent=self.window)
        self.deflation2xlabel.setFixedSize(615,50)
        self.custom_font.setPointSize(17)
        self.deflation2xlabel.setFont(self.custom_font)
        self.deflation2xlabel.hide()

        # Add a menu bar
        self.menubar = QMenuBar()
        self.editmenu = QMenu("Edit", self.menubar)

        self.deflation_action = QAction('Deflation', self)
        self.editmenu.addAction(self.deflation_action)

        self.deflation2x_action = QAction('Deflation 2x Cash', self)
        self.editmenu.addAction(self.deflation2x_action)

        self.menubar.addMenu(self.editmenu)

        self.deflation_action.triggered.connect(self.editdeflation)
        self.deflation2x_action.triggered.connect(self.editdeflation2x)

        # Add button widgets to main window
        self.defbutton = QPushButton('Deflation', parent=self.window)
        self.defbutton.setFixedSize(200, 100)
        self.custom_font.setPointSize(20)
        self.defbutton.setFont(self.custom_font)
        self.defbutton.clicked.connect(self.deflationpress)

        self.def2xbutton = QPushButton('Deflation 2x Cash', parent=self.window)
        self.custom_font.setPointSize(15)
        self.def2xbutton.setFont(self.custom_font)
        self.def2xbutton.setFixedSize(200, 100)
        self.def2xbutton.clicked.connect(self.deflation2xpress)

        self.quitbutton = QPushButton('Quit to Menu', parent=self.window)
        self.quitbutton.hide()
        self.custom_font.setPointSize(20)
        self.quitbutton.setFont(self.custom_font)
        self.quitbutton.setFixedSize(200, 100)
        self.quitbutton.clicked.connect(self.quit)

        # Add Widgets and set up layout of main UI page
        self.mainhboxtop.addWidget(self.mainlabel)
        self.mainhboxbot.addWidget(self.defbutton)
        self.mainhboxbot.addWidget(self.def2xbutton)
        self.layout.addLayout(self.mainhboxtop)
        self.layout.addLayout(self.mainhboxbot)

        # Add Widgets and set up layout of Deflation/Deflation 2x Cash pages
        self.defhboxtop.addWidget(self.deflationlabel)
        self.layout.addLayout(self.defhboxtop)
        self.layout.addLayout(self.defhboxbot)

        self.def2xhboxtop.addWidget(self.deflation2xlabel)
        self.def2xhboxbot.addWidget(self.quitbutton)
        self.layout.addLayout(self.def2xhboxtop)
        self.layout.addLayout(self.def2xhboxbot)

        # Finalize UI setup and open the window
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)
        self.setMenuBar(self.menubar)
        self.show()
        self.run()

        # Tower setup
        self.snipx = 0
        self.snipy = 0
        self.alchx = 0
        self.alchy = 0
        self.vilx = 0
        self.vily = 0
        self.nintopx = 0
        self.nintopy = 0
        self.ninbottomx = 0
        self.ninbottomy = 0
        self.alchtopx = 0
        self.alchtopy = 0
        self.alchbottomx = 0
        self.alchbottomy = 0


        # Reset Coordinates
        self.x = 0
        self.y = 0
        
        # Thread setup
        self.running = False

    # Separate methods to run in the buttons
    def deflation(self):
        self.coordinateHandler()
        width, height = pyautogui.size()
        x_fact = width / 1920
        y_fact = height / 1080

        while self.running:
            counter = 0
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/homemenu.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping... {counter + 1}")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/homemenu.png')),
                                                           confidence=0.9)
                    counter += 1
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(0.7)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Maps/infernal.png')), confidence=0.9)
            if (imageToFind is None):
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MapDifficulty/expert.png')), confidence=0.9)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.7)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Maps/infernal.png')), confidence=0.9)
                x, y, _, _ = imageToFind
            else:
                x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(0.6)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Difficulty/easy.png')), confidence=0.9)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(0.6)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Mode/deflation.png')), confidence=0.9)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            counter = 0
            time.sleep(0.6)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/existinggame.png')), confidence=0.9)
            if (imageToFind is not None):
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/existingok.png')), confidence=0.9)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/ingame.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping... {counter + 1}")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/ingame.png')), confidence=0.9)
                    counter += 1
            time.sleep(0.7)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/tooltipcheck.png')), confidence=0.9)
            if (imageToFind is not None):
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.25)
            pyautogui.click(self.nintopx, self.nintopy)
            time.sleep(0.25)
            keyboard.press_and_release('d')
            time.sleep(0.25)
            pyautogui.click(self.nintopx, self.nintopy)
            time.sleep(0.25)
            pyautogui.click(self.nintopx, self.nintopy)
            for i in range(4):
                time.sleep(0.25)
                keyboard.press_and_release(',')
            for i in range(2):
                time.sleep(0.25)
                keyboard.press_and_release('/')
            time.sleep(0.25)
            pyautogui.click(self.alchtopx, self.alchtopy)
            time.sleep(0.25)
            keyboard.press_and_release('f')
            time.sleep(0.25)
            pyautogui.click(self.alchtopx, self.alchtopy)
            time.sleep(0.25)
            pyautogui.click(self.alchtopx, self.alchtopy)
            for i in range(4):
                time.sleep(0.25)
                keyboard.press_and_release(',')
            for i in range(2):
                time.sleep(0.25)
                keyboard.press_and_release('.')
            time.sleep(0.25)
            pyautogui.click(self.alchbottomx, self.alchbottomy)
            time.sleep(0.25)
            keyboard.press_and_release('f')
            time.sleep(0.25)
            pyautogui.click(self.alchbottomx, self.alchbottomy)
            time.sleep(0.25)
            pyautogui.click(self.alchbottomx, self.alchbottomy)
            for i in range(4):
                time.sleep(0.25)
                keyboard.press_and_release(',')
            for i in range(2):
                time.sleep(0.25)
                keyboard.press_and_release('.')
            time.sleep(0.25)
            pyautogui.click(self.ninbottomx, self.ninbottomy)
            time.sleep(0.25)
            keyboard.press_and_release('d')
            time.sleep(0.25)
            pyautogui.click(self.ninbottomx, self.ninbottomy)
            time.sleep(0.25)
            pyautogui.click(self.ninbottomx, self.ninbottomy)
            for i in range(4):
                time.sleep(0.25)
                keyboard.press_and_release(',')
            for i in range(2):
                time.sleep(0.25)
                keyboard.press_and_release('/')
            time.sleep(0.25)
            keyboard.press_and_release('space')
            time.sleep(0.25)
            keyboard.press_and_release('space')
            keyboard.press_and_release('esc')
            counter = 0
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping... {counter + 1}")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame.png')), confidence=0.9)
                    counter += 1
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(0.6)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame2.png')), confidence=0.9)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(3)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/collectionevent.png')), confidence=0.9)
            if (imageToFind is not None):
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(1.5)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/instamonkey.png')), confidence=0.7)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.8)
                pyautogui.click(x, y)
                time.sleep(0.8)
                while imageToFind is not None:
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/instamonkey.png')), confidence=0.7)
                    x, y, _, _ = imageToFind
                    pyautogui.click(x, y)
                    time.sleep(0.8)
                    pyautogui.click(x, y)
                    time.sleep(0.8)
                time.sleep(0.8)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endcollection.png')), confidence=0.7)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.8)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/backhome.png')), confidence=0.9)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                print("Done with the loop!")

    def deflation2x(self):
        self.coordinateHandler()
        width, height = pyautogui.size()
        x_fact = width / 1920
        y_fact = height / 1080

        while self.running:
            counter = 0
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/homemenu.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping... {counter + 1}")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/homemenu.png')), confidence=0.9)
                    counter += 1
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(0.7)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Maps/infernal.png')), confidence=0.9)
            if (imageToFind is None):
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MapDifficulty/expert.png')), confidence=0.9)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.7)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Maps/infernal.png')), confidence=0.9)
                x, y, _, _ = imageToFind
            else:
                x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(0.6)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Difficulty/easy.png')), confidence=0.9)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(0.6)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/Mode/deflation.png')), confidence=0.9)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            counter = 0
            time.sleep(0.6)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/existinggame.png')), confidence=0.9)
            if (imageToFind is not None):
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/existingok.png')), confidence=0.9)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/ingame.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping... {counter + 1}")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/ingame.png')), confidence=0.9)
                    counter += 1
            time.sleep(0.7)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/tooltipcheck.png')), confidence=0.9)
            if(imageToFind is not None):
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.25)
            pyautogui.click(self.snipx, self.snipy)
            time.sleep(0.25)
            keyboard.press_and_release('z')
            time.sleep(0.25)
            pyautogui.click(self.snipx, self.snipy)
            time.sleep(0.25)
            pyautogui.click(self.snipx, self.snipy)
            for i in range(2):
                time.sleep(0.25)
                keyboard.press_and_release(',')
            for i in range(5):
                time.sleep(0.25)
                keyboard.press_and_release('/')
            time.sleep(0.25)
            pyautogui.click(self.alchx, self.alchy)
            time.sleep(0.25)
            keyboard.press_and_release('f')
            time.sleep(0.25)
            pyautogui.click(self.alchx, self.alchy)
            time.sleep(0.25)
            pyautogui.click(self.alchx, self.alchy)
            for i in range(4):
                time.sleep(0.25)
                keyboard.press_and_release(',')
            for i in range(2):
                time.sleep(0.25)
                keyboard.press_and_release('.')
            time.sleep(0.25)
            pyautogui.click(self.vilx, self.vily)
            time.sleep(0.25)
            keyboard.press_and_release('k')
            time.sleep(0.25)
            pyautogui.click(self.vilx, self.vily)
            time.sleep(0.25)
            pyautogui.click(self.vilx, self.vily)
            for i in range(2):
                time.sleep(0.25)
                keyboard.press_and_release(',')
            for i in range(3):
                time.sleep(0.25)
                keyboard.press_and_release('.')
            time.sleep(0.25)
            keyboard.press_and_release('space')
            time.sleep(0.25)
            keyboard.press_and_release('space')
            keyboard.press_and_release('esc')
            counter = 0
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame.png')), confidence=0.9)
            while imageToFind is None:
                if not self.running:
                    print("We're not running anymore, exit!")
                    return
                else:
                    print(f"We're still running, keep sleeping... {counter + 1}")
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame.png')), confidence=0.9)
                    counter += 1
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(0.6)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endgame2.png')), confidence=0.9)
            x, y, _, _ = imageToFind
            pyautogui.click(x, y)
            time.sleep(3.0)
            imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/collectionevent.png')), confidence=0.9)
            if(imageToFind is not None):
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(1.5)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/instamonkey.png')), confidence=0.7)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.8)
                pyautogui.click(x, y)
                time.sleep(0.8)
                while imageToFind is not None:
                    imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/instamonkey.png')), confidence=0.7)
                    x, y, _, _ = imageToFind
                    pyautogui.click(x, y)
                    time.sleep(0.8)
                    pyautogui.click(x, y)
                    time.sleep(0.8)
                time.sleep(0.8)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/endcollection.png')), confidence=0.7)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                time.sleep(0.8)
                imageToFind = pyscreeze.locateOnScreen((self.resolve_path('Resources/MenuNav/backhome.png')), confidence=0.9)
                x, y, _, _ = imageToFind
                pyautogui.click(x, y)
                print("Done with the loop!")


    def editdeflation(self):
        self.defsubwin = BloonsUISub("Deflation",["Top Ninja Pos", "Bottom Ninja Pos", "Top Alchemist Pos", "Bottom Alchemist Pos"])
        self.defsubwin.show()
        self.defsubwin.raise_()

    def editdeflation2x(self):
        self.def2xsubwin = BloonsUISub("Deflation 2x Cash", ["Sniper Pos", "Alchemist Pos", "Village Pos"])
        self.def2xsubwin.show()
        self.def2xsubwin.raise_()

    # Define button functionality for main window
    def deflationpress(self):
        self.running = True
        self.deflationlabel.show()
        self.quitbutton.show()
        self.mainlabel.hide()
        self.defbutton.hide()
        self.def2xbutton.hide()
        self.thread = threading.Thread(target=self.deflation, daemon=True)
        self.thread.start()

    def deflation2xpress(self):
        self.running = True
        self.deflation2xlabel.show()
        self.quitbutton.show()
        self.mainlabel.hide()
        self.defbutton.hide()
        self.def2xbutton.hide()
        self.thread = threading.Thread(target=self.deflation2x, daemon=True)
        self.thread.start()

    def quit(self):
        self.running = False
        self.deflation2xlabel.hide()
        self.deflationlabel.hide()
        self.quitbutton.hide()
        self.mainlabel.show()
        self.defbutton.show()
        self.def2xbutton.show()
        self.thread.join()

    # Writing and handling tower coordinates
    def coordinateHandler(self):
        with open('towerpos.json', 'r') as f:
            pos = json.load(f)
        self.snipx, self.snipy = pos['sniper_pos']
        self.alchx, self.alchy = pos['alchemist_pos']
        self.vilx, self.vily= pos['village_pos']
        self.nintopx, self.nintopy = pos['top_ninja_pos']
        self.ninbottomx, self.ninbottomy = pos['bottom_ninja_pos']
        self.alchtopx, self.alchtopy = pos['top_alchemist_pos']
        self.alchbottomx, self.alchbottomy = pos['bottom_alchemist_pos']
        
        

    # Finding file path for assets
    def resolve_path(self, path):
        if getattr(sys, "frozen", False):
            # If the 'frozen' flag is set, we are in bundled-app mode!
            resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
        else:
            # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
            resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))

        return resolved_path

    # Run program
    def run(self):
        try:
            with open("towerpos.json") as f:
                pass
        except FileNotFoundError:
            CoordinateHandler.main()
        sys.exit(self.BloonsUI.exec())

if __name__ == "__main__":
    BloonsUI = BloonsUIMain()
    BloonsUI.run()
