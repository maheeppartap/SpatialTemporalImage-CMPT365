
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

def main():
    print(cv2.__version__)
    videoBreakDown()

def videoBreakDown():
    vidCapture = cv2.VideoCapture("../assets/test.mp4")
    if vidCapture.isOpened() == False:
        print("Error opening the stream")

    successful, image = vidCapture.read()
    framNum = 0

    while successful:
        cv2.imshow("de", image)
        successful, image = vidCapture.read()
        framNum += 1
        if cv2.waitKey(250) & 0xFF == ord('q'):
            break


if __name__== "__main__":
    main()



