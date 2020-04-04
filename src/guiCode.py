import cv2
import numpy as np
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.videoplayer import VideoPlayer
import math
from src.videoAnalysis import VideoAnalysis

global tink  # the parent declaration
global fileName
global sti
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
import os
from kivy.uix.boxlayout import BoxLayout
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import threading
from kivy.uix.checkbox import CheckBox

# todo: make a decent filechooser
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

class mainGUI(App):

    def build(self):
        global fileName
        global player
        global currentFile
        global videoBreakbtn
        global sti
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


def videoBreakDown_thread(instance=1):
    global va
    va = VideoAnalysis(fileName)
    vbthread = threading.Thread(target=va.analyse, args=(analysisDone,))
    vbthread.start()


def analysisDone(va):
    global videoBreakbtn
    global rowsti
    global colsti
    rowsti = va.rowsti
    colsti = va.colsti
    videoBreakbtn.text = "Show transition"
    videoBreakbtn.disabled = False


def FileChooserCallback(instance):
    Tk().withdraw()
    global fileName
    global videoBreakbtn
    videoBreakbtn.text = "Loading..."
    fileName = askopenfilename()
    updateVideoPlayer(fileName)
    updateLabel(fileName)
    videoBreakDown_thread()


def updateLabel(fname):
    global currentFile
    currentFile.text = fname


def updateVideoPlayer(fname):
    global player
    global fileName
    fileName = fname
    player.source = fname
    player.disabled = False


global detectedSTItransition


# def analyze_sti(img):
#     global detectedSTItransition
#     detectedSTItransition = np.zeros(2, dtype="float")
#     cv2.imwrite("temp.png", img)
#     img = cv2.imread("temp.png")
#     gray = img.copy()
#
#     kernel_size = 5
#     blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
#     low_threshold = 50
#     high_threshold = 100
#     edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
#
#     rho = 1
#     theta = np.pi / 180
#     threshold = 20  # seems like a sweet spot
#     min_line_length = 50
#     max_line_gap = 2
#     line_image = np.copy(img) * 0
#
#     lines_ = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
#                              min_line_length, max_line_gap)
#
#     lines = np.copy(lines_)
#
#     k = 0
#     slope = np.zeros(len(lines))
#     length = np.zeros(len(lines))
#     if type(lines) is np.ndarray:
#         for line in lines:
#             for x1, y1, x2, y2 in line:
#                 slope[k] = float((y2 - y1) / (x2 - x1))
#                 length[k] = math.hypot(x1 - x2, y1 - y2)
#                 k += 1
#
#     length.sort(kind='quicksort')
#
#     # checking for similar slope to reduce copies.
#     wiggleRoom = 0.1
#     for m in range(0, len(lines) - 1):
#         if slope[m] - slope[m + 1] > wiggleRoom:
#             lines = np.delete(lines, (m, 0), axis=0)
#
#     detectedSTItransition[0] = lines[len(lines) - 1][0][0]
#     detectedSTItransition[1] = lines[len(lines) - 1][0][2]
#     print(detectedSTItransition)
#     if type(lines) is np.ndarray:
#         for line in lines:
#             for x1, y1, x2, y2 in line:
#                 cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
#
#         # print(lines)
#
#         lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
#         cv2.imshow("detected transition", lines_edges)
#     else:
#         lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
#         cv2.imshow("detected transition", lines_edges)
#
#     os.remove("temp.png")
#
#     typeOfTransition(slope[len(slope)-1])
#
#     cv2.waitKey(0)
#
# def typeOfTransition(x=0):
#     if x is 0:
#         return
#     type = ""
#     theta = math.atan(x)
#     print(theta)
#     tol = 0.0001
#     if (theta ) > 0:
#         if checkBox1.active:
#             type = "lr"
#         else:
#             type = "ud"
#     else:
#         if(theta ) < 0:
#             if checkBox1.active:
#                 type = "rl"
#             else:
#                 type = "du"
#     print("type is: ", type)


#########################


def display(instance=0):
    global rowsti
    global colsti
    global checkBox1

    if checkBox1.active:
        try:
            cv2.imshow("test", colsti / 255)
            va.analyze_sti(True)
            cv2.waitKey(0)
        except:
            pass
    else:
        try:
            cv2.imshow("test", rowsti / 255)
            va.analyze_sti(False)
            cv2.waitKey(0)
        except:
            pass
