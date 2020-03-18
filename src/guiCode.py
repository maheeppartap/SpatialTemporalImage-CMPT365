import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import png
import matplotlib
import PIL
from STIclass import STI
from tkinter import messagebox
from PIL import Image
from sklearn.preprocessing import normalize

global tink  # the parent declaration
global fileName
global sti


def begin():
    global tink

    tink = tk.Tk()  # the parent window
    tink.geometry("500x400")
    tink.title("test")
    # add widgets here
    chooserButton = tk.Button(tink, text="pick a file", width=25, command=fileselection)

    # this is for arrangement of widgets
    chooserButton.pack()
    tink.protocol("WM_DELETE_WINDOW", onClosing)
    w = tink.mainloop()


# file selector.
def fileselection():
    tink.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
    global fileName
    fileName = tink.filename
    videoBreakDown()
    # print(tink.filename)


def videoBreakDown():
    windowname = "CMPT 365 Project"
    vidCapture = cv2.VideoCapture(fileName)
    if not vidCapture.isOpened():
        print("Error opening the stream")

    successful, image = vidCapture.read()
    global sti
    width = vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    length = int(vidCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vidCapture.get(cv2.CAP_PROP_FPS)
    currFrame = 0
    print("video is: ", width, " ", height)
    sti = STI(width, length)
    cv2.namedWindow(windowname)
    cv2.startWindowThread()

    middleCol = int(width / 2)


    while currFrame < length-1:
        sti.addCol(currFrame, image[middleCol])
        #print("Sending colour: ", image[middleCol], "Done")
        successful, image = vidCapture.read()
        cv2.imshow(windowname, image)
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty(windowname, 0) < 0:
            break
        currFrame += 1
   # print(width)

    for i in range(int(length)):
        for j in range(int(width)):
            for k in range(3):
                #print(i," " ,j , " ", k)
                sti.sti[i][j][k] /= 255

    cv2.imshow("test", sti.sti)
    cv2.waitKey(25000)
    vidCapture.release()
    cv2.destroyAllWindows()  # just to be safe

def normme(m, width, height):
    pass

def onClosing():
    tink.destroy()
