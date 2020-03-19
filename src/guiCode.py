import tkinter as tk
from tkinter import filedialog

import cv2

from STIclass import STI
import numpy as np

global tink  # the parent declaration
global fileName
global sti
global videoPlayer
global frameBG

def begin():
    global tink
    global videoPlayer
    global frameBG

    tink = tk.Tk()  # the parent window

    appRes = [500, 500] #for a 500x500 res


    tink.title("test")
    tink.geometry("%dx%d" % (appRes[0],appRes[1]))
    bgName = tk.PhotoImage(file="../assets/bg.png")
    frameBG = tk.Frame(tink, bg="white")
    frameBG.place(relx=0,rely=0,relwidth=1,relheight=1)
    backgroundIMG=tk.Label(frameBG, image=bgName)
    backgroundIMG.place(relx=0,rely=0,relwidth=1,relheight=1)

    # add widgets here
    chooserButton = tk.Button(frameBG, text="Pick a file", width=25, command=fileselection, relief="ridge")
    videoPlayer = tk.Label(frameBG,bg="black")
    # this is for arrangement of widgets

    chooserButton.place(relx=0.4,rely=0.75,relwidth=0.2,relheight=0.07)
    videoPlayer.place(relx=0.15,rely=0.2,relwidth=0.7,relheight=0.5)
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
    global sti
    global videoPlayer
    global frameBG
    windowname = "CMPT 365 Project"
    vidCapture = cv2.VideoCapture(fileName)
    if not vidCapture.isOpened():
        print("Error opening the stream")

    successful, image = vidCapture.read()

    width = vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    length = int(vidCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vidCapture.get(cv2.CAP_PROP_FPS)
    currFrame = 0
    print("video is: ", width, " ", height)
    print("Number of frames: ", length)
    sti = STI(width, length)
    cv2.namedWindow(windowname)
    cv2.startWindowThread()

    middleCol = int(width / 2)

#########################################working here 18 march
    while currFrame < length-1:
        sti.addCol(currFrame, image[middleCol])
        image_ = tk.PhotoImage(vidCapture.read()[1].all())#vidCapture.read()
        x = image_
        videoPlayer=tk.Label(frameBG,image=x)
        videoPlayer.image = x
        videoPlayer.place(relx=0.15, rely=0.2, relwidth=0.7, relheight=0.5)
        #cv2.imshow(windowname, image_)
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty(windowname, 0) < 0:
            break
        currFrame += 1
   # print(width)

    for i in range(int(width)):
        for j in range(int(length)):
            for k in range(3):
                #print(i," " ,j , " ", k)
                sti.sti[i][j][k] /= 255

    cv2.imshow("test",sti.sti)
    cv2.waitKey(25000)
    vidCapture.release()
    cv2.destroyAllWindows()  # just to be safe
    onClosing()

def onClosing():
    tink.destroy()
