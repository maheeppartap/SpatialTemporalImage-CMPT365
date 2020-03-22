import cv2
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.videoplayer import VideoPlayer

from STIclass import STI

global tink  # the parent declaration
global fileName
global sti
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
import os
from kivy.uix.boxlayout import BoxLayout




# todo: make a decent filechooser




mainCanvasbg = """

mainCanvas:

    orientation: 'vertical'

    canvas: 

        Rectangle:

            size: self.size

            pos: self.pos
            
            source: '../assets/bg.png'
"""

fileChoosing = """

<FileChooser>:

    label:  label
    
    orientation:    'vertical'
    
    BoxLayout:
    
        FileChooserListView:
            canvas.before:
                Color:
                    rgb:    .4, .5, .5
                Rectangle:
                    pos:    self.pos
                    size:   self.size
            on_selection:   root.select(*args)
    Label:
        id: label
        size_hint_y:    .1
        canvas.before:
            Color:
                rgb:    .5, .5, .4
            Rectangle:
                pos: self.pos
                size:   self.size
"""

Builder.load_string("""
<MyWidget>:
    id: my_widget
    Button
        text: "open"
        on_release: my_widget.open(filechooser.path, filechooser.selection)
    FileChooserIconView:
        id: filechooser
        on_selection: my_widget.selected(filechooser.selection)
""")


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
class mainGUI(App):

    def build(self):
        global fileName
        fileName= ""
        parent = Builder.load_string(mainCanvasbg)
        # self.fileChooser = fileChooser = FileChooserListView(size_hint_y=None, path='../assets/')

        player = VideoPlayer(source=fileName, state='play',
                             options={'allow_stretch': True})
        player.state = 'pause'
        parent.add_widget(player)
        parent.add_widget(MyWidget())
        # parent.add_widget(self.fileChooser)

        return parent
        # return Label(text="hello")


def begin():
    global fileName
    fileName = "../assets/test.mp4"


def videoBreakDown():
    global fileName
    fileName = "../assets/test.mp4"
    vidCapture = cv2.VideoCapture(fileName)
    global sti

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
    sti = STI(width, length)

    middlecol = int(width / 2)

    # Read until video is completed
    while (vidCapture.isOpened()):

        # Capture frame-by-frame
        ret, frame = vidCapture.read()
        if ret == True:
            sti.addCol(currFrame, frame[middlecol])
            currFrame += 1
            # Display the resulting frame
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    for i in range(int(width)):
        for j in range(int(length)):
            for k in range(3):
                # print(i," " ,j , " ", k)
                sti.sti[i][j][k] /= 255

    cv2.imshow("test", sti.sti)
    cv2.waitKey(25000)
    vidCapture.release()
    cv2.destroyAllWindows()  # just to be safe
