import threading

import cv2
from kivy.uix.button import Button
from kivy.uix.videoplayer import VideoPlayer
from src.videoAnalysis import VideoAnalysis
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
import os
from kivy.uix.boxlayout import BoxLayout
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from kivy.uix.checkbox import CheckBox

# todo: Clean the code


mainCanvasbg = """

mainCanvas:

    orientation: 'vertical'

    canvas: 

        Rectangle:

            size: self.size

            pos: self.pos
            
            source: '../assets/bg.png'
"""


class MyWidget(BoxLayout):
    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print(f.read())

    def selected(self, filename):
        global fileName
        fileName = filename
        print("selected: %s" % filename[0])


class mainCanvas(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


#   add stuff here
global player
global currentFile
global videoBreakbtn
global checkBox1
global checkBox2
global activeSTIstring
global va
global tink  # the parent declaration
global fileName
global rowsti
global colsti

class mainGUI(App):

    def build(self):
        global fileName
        global player
        global currentFile
        global videoBreakbtn
        global checkBox1
        global checkBox2

        # fileName= "../assets/test2.mp4"
        fileName = ""
        parent = Builder.load_string(mainCanvasbg)

        player = VideoPlayer(state='pause',
                             options={'allow_stretch': True}, disabled=True)
        parent.add_widget(player)

        fileChooser = Button(text="Choose a file", font_size=14, size=(2, 2), size_hint=(.2, .2),
                             pos_hint={"x": 0.4, "y": 0.9})
        fileChooser.bind(on_press=FileChooserCallback)
        currentFile = Label(text="No file selected" + fileName, font_size=14, size=(2, 2), size_hint=(.2, .2),
                            pos_hint={"x": 0.4})

        videoBreakbtn = Button(text="show transition", font_size=14, size=(2, 2), size_hint=(.2, .2),
                               pos_hint={"x": 0.4})
        videoBreakbtn.bind(on_press=display)
        videoBreakbtn.disabled = True

        colLablel = Label(text="Column STI", size_hint=(.05, .05), pos_hint={"x": 0.1})
        rowLablel = Label(text="row STI", size_hint=(.05, .05), pos_hint={"x": 0.1})
        checkBox1 = CheckBox(active=True, size_hint=(.05, .05), pos_hint={"x": 0.1})
        checkBox1.bind(active=activeSTI)
        checkBox2 = CheckBox(active=False, size_hint=(.05, .05), pos_hint={"x": 0.1})
        checkBox2.bind(active=activeSTI)

        parent.add_widget(fileChooser)
        parent.add_widget(colLablel)
        parent.add_widget(checkBox1)
        parent.add_widget(videoBreakbtn)
        parent.add_widget(rowLablel)
        parent.add_widget(checkBox2)
        parent.add_widget(currentFile)
        # parent.add_widget(self.fileChooser)

        return parent
        # return Label(text="hello")


def activeSTI(instance, isActive):
    global activeSTIstring
    global checkBox1
    global checkBox2
    if isActive:
        activeSTIstring = instance
        if instance is checkBox1:
            checkBox2.active = False
        else:
            checkBox1.active = False
    else:
        if instance is checkBox1:
            checkBox2.active = True
        else:
            checkBox1.active = True


def FileChooserCallback(instance):
    Tk().withdraw()
    global fileName
    global videoBreakbtn
    videoBreakbtn.text = "Loading..."
    fileName = askopenfilename()
    updateVideoPlayer(fileName)
    updateLabel(fileName)
    analyze_video()


def analyze_video():
    global va
    va = VideoAnalysis(fileName)
    va_process = threading.Thread(target=va.analyse, args=(breakdown_complete_callback,))
    va_process.start()


def breakdown_complete_callback(va):
    global videoBreakbtn
    global rowsti
    global colsti
    rowsti = va.rowsti
    colsti = va.colsti
    videoBreakbtn.text = "Show transition"
    videoBreakbtn.disabled = False


def updateLabel(fname):
    global currentFile
    currentFile.text = fname


def updateVideoPlayer(fname):
    global player
    global fileName
    fileName = fname
    player.source = fname
    player.disabled = False


def display(instance):
    global rowsti
    global colsti
    global checkBox1

    if checkBox1.active:
        try:
            cv2.imshow("test", colsti / 255)
            cv2.waitKey(0)
        except:
            pass
    else:
        try:
            cv2.imshow("test", rowsti / 255)
            cv2.waitKey(0)
        except:
            pass
