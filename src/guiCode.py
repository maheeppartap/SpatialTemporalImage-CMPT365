import cv2
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.videoplayer import VideoPlayer

from src.STImg import STImg

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


def videoBreakDown():
    global fileName

    vidCapture = cv2.VideoCapture(fileName)
    global sti
    global sti_r
    # Check if camera opened successfully
    if (vidCapture.isOpened() == False):
        print("Error opening video  file")

    width = vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    length = int(vidCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vidCapture.get(cv2.CAP_PROP_FPS)
    currFrame = 0
    print("video is: ", width, " ", height)
    print("Number of frames: ", length)
    sti = STImg(height, length)
    sti_r = STImg(width, length)

    middleRow = int(height / 2)
    middlecol = int(width / 2)

    # Read until video is completed
    while (vidCapture.isOpened()):

        # Capture frame-by-frame
        ret, frame = vidCapture.read()
        if ret == True:
            sti.addCol(currFrame, frame[:, middlecol])
            sti_r.addRow(currFrame, frame[middleRow, :])
            currFrame += 1
            # Display the resulting frame
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    for i in range(int(height)):
        for j in range(int(length)):
            for k in range(3):
                # print(i," " ,j , " ", k)
                sti.sti[i][j][k] /= 255

    # todo: something is wrong with this this normalizing function, fix
    for t in range(int(height)):
        for l in range(int(length)):
            for m in range(3):
                sti_r.sti[t][l][m] /= 255

    # display()
    vidCapture.release()
    cv2.destroyAllWindows()  # just to be safe

    global videoBreakbtn
    videoBreakbtn.text = "Show transition"
    videoBreakbtn.disabled = False


def display(instance=0):
    global sti
    global checkBox1

    if checkBox1.active:
        try:
            cv2.imshow("test", sti.sti)
            cv2.waitKey(0)
        except:
            pass
    else:
        try:
            cv2.imshow("test", sti_r.sti)
            cv2.waitKey(0)
        except:
            pass
