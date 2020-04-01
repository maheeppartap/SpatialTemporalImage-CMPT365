import cv2
import numpy as np
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.videoplayer import VideoPlayer

from src.STImg import STImg
from src.TransitionDetector import TransitionDetector

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
    vbthread = threading.Thread(target=videoBreakDown)
    vbthread.start()


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


global sti_r


########################
def test(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1
    theta = np.pi / 180
    threshold = 43
    min_line_length = 50
    max_line_gap = 20
    line_image = np.copy(img) * 0

    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    if type(lines) is np.ndarray:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
        cv2.imshow("test", lines_edges)
    else:
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
        cv2.imshow("test", lines_edges)

    cv2.waitKey(0)


#########################

def videoBreakDown():
    global fileName
    global colsti
    global rowsti
    vidCapture = cv2.VideoCapture(fileName)
    # Check if camera opened successfully
    if not vidCapture.isOpened():
        print("Error opening video  file")

    width = int(vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(vidCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vidCapture.get(cv2.CAP_PROP_FPS)
    index = 0
    N = int(1 + np.log2(height))

    prevcolhists = np.full((width, N, N), width + 1, dtype=int)
    prevrowhists = np.full((height, N, N), height + 1, dtype=int)
    colhists = np.zeros((width, N, N), int)
    rowhists = np.zeros((height, N, N), int)
    colsti = np.empty((width, length), dtype=float)
    rowsti = np.empty((height, length), dtype=float)
    thresh = 0.5
    # Read until video is completed
    while vidCapture.isOpened():

        # Capture frame-by-frame
        ret, frame = vidCapture.read()
        if ret:
            # create a histogram for every row and column in the given frame
            for i in range(height):
                for j in range(width):
                    # convert to chromaticity
                    total = np.sum(frame[i][j])
                    if total == 0:
                        r = 0
                        g = 0
                    else:
                        r = frame[i][j][0] / total
                        g = frame[i][j][1] / total
                    # quantize chromaticity
                    rN = int(np.floor(r * (N - 1)))
                    gN = int(np.floor(g * (N - 1)))
                    if rN == 7 or gN == 7:
                        print(str(frame[i][j]))
                        print(str(r) + " " + str(g))
                    colhists[j][rN][gN] += 1
                    rowhists[i][rN][gN] += 1

            # create a column of our column sti
            for i in range(width):
                diff = 0
                for j in range(N):
                    for k in range(N):
                        diff += min(prevcolhists[i][j][k], colhists[i][j][k])
                        # reset for next loop since we are done with it
                        prevcolhists[i][j][k] = colhists[i][j][k]
                        colhists[i][j][k] = 0
                diff /= height
                colsti[i][index] = diff > thresh

            for i in range(height):
                diff = 0
                for j in range(N):
                    for k in range(N):
                        diff += min(prevrowhists[i][j][k], rowhists[i][j][k])
                        # reset for next loop since we are done with it
                        prevrowhists[i][j][k] = rowhists[i][j][k]
                        rowhists[i][j][k] = 0
                diff /= width
                rowsti[i][index] = diff > thresh

            index += 1
            # Display the resulting frame
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else:
            break

    # display()
    vidCapture.release()
    cv2.destroyAllWindows()  # just to be safe

    global videoBreakbtn
    videoBreakbtn.text = "Show transition"
    videoBreakbtn.disabled = False


def display(instance=0):
    global rowsti
    global colsti
    global checkBox1

    if checkBox1.active:
        try:
            cv2.imshow("test", colsti)
            cv2.waitKey(0)
        except:
            pass
    else:
        try:
            cv2.imshow("test", rowsti)
            cv2.waitKey(0)
        except:
            pass

