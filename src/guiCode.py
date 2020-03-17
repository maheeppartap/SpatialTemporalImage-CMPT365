import tkinter as tk
from tkinter import filedialog
import cv2

global tink  # the parent declaration
global fileName


def begin():
    global tink
    tink = tk.Tk()  # the parent window
    tink.title("test")
    # add widgets here
    chooserButton = tk.Button(tink, text="pick a file", width=25, command=fileselection)


    # this is for arrangement of widgets
    chooserButton.pack()
    w = tink.mainloop()


# file selector.
def fileselection():
    tink.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
    global fileName
    fileName = tink.filename
    videoBreakDown()
    # print(tink.filename)


def videoBreakDown():
    vidCapture = cv2.VideoCapture(fileName)
    if vidCapture.isOpened() == False:
        print("Error opening the stream")

    successful, image = vidCapture.read()
    framNum = 0

    while successful:
        cv2.imshow("test", image)
        successful, image = vidCapture.read()
        framNum += 1
        if cv2.waitKey(250) & 0xFF == ord('q'):
            break
