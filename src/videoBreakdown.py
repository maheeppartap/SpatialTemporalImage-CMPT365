import cv2
import numpy as np


def breakdowntoSTI(filename: str, height: int, thresh: float):
    vidCapture = cv2.VideoCapture(filename)
    # Check if camera opened successfully
    if not vidCapture.isOpened():
        print("Error opening video  file")

    width = vidCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    full_height = vidCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # reduce the size
    width = int(width / (full_height / height))
    length = int(vidCapture.get(cv2.CAP_PROP_FRAME_COUNT))

    index = 0
    N = int(1 + np.log2(height))

    prevcolhists = np.full((width, N, N), width + 1, dtype=int)
    prevrowhists = np.full((height, N, N), height + 1, dtype=int)
    colhists = np.zeros((width, N, N), int)
    rowhists = np.zeros((height, N, N), int)
    colsti = np.empty((width, length), dtype=np.uint8)
    rowsti = np.empty((height, length), dtype=np.uint8)
    # Read until video is completed
    while vidCapture.isOpened():
        # Capture frame-by-frame
        ret, frame_full = vidCapture.read()

        if ret:
            # reduce resolution
            frame = cv2.resize(frame_full, (width, height))
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
                        pass
                    #   print(str(frame[i][j]))
                    #  print(str(r) + " " + str(g))
                    colhists[j][rN][gN] += 1
                    rowhists[i][rN][gN] += 1

            # create a column of our column sti
            for i in range(width):
                diff = hist_intersection(height, N, prevcolhists[i], colhists[i])
                colsti[i][index] = (diff > thresh) * 255

            for i in range(height):
                diff = hist_intersection(width, N, prevrowhists[i], rowhists[i])
                rowsti[i][index] = (diff > thresh) * 255

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
    cv2.imwrite("C.png", colsti)
    cv2.imwrite("R.png", rowsti)
    return colsti, rowsti


def hist_intersection(total, N, prevhist, hist):
    diff = 0
    for j in range(N):
        for k in range(N):
            diff += min(prevhist[j][k], hist[j][k])
            # reset for next loop since we are done with it
            prevhist[j][k] = hist[j][k]
            hist[j][k] = 0
    return diff / total


def ibm_hist_diff(total, N, prevhist, hist):
    pass



