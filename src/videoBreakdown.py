import math

import cv2
import numpy as np


def breakdowntoSTI(filename: str, height=64, thresh=0.75):
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

    A = compute_A(N)

    # todo: convert these to 1 dimentional histograms
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
                    rN = int(min(r * N, N-1))
                    gN = int(min(g * N, N-1))
                    colhists[j][rN][gN] += 1
                    rowhists[i][rN][gN] += 1

            # create a column of our column sti
            for i in range(width):
                # intersect = hist_inter(height, prevcolhists[i], colhists[i])
                intersect = 1 - ibm_hist_diff(A, height, prevcolhists[i], colhists[i])
                colsti[i][index] = (intersect > thresh) * 255

            for i in range(height):
                # intersection = hist_inter(width, prevrowhists[i], rowhists[i])
                intersect = 1 - ibm_hist_diff(A, width, prevrowhists[i], rowhists[i])
                rowsti[i][index] = (intersect > thresh) * 255

            # reset for next loop
            prevcolhists = np.copy(colhists)
            colhists.fill(0)
            prevrowhists = np.copy(rowhists)
            rowhists.fill(0)

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


def compute_A(N: int):
    sqrt2 = np.sqrt(2)
    N2 = N*N
    A = np.empty((N2, N2))
    for i in range(N2):
        r_i = (int(i / N) + 0.5) / N
        g_i = (int(i % N) + 0.5) / N
        for j in range(N2):
            r_j = (int(j / N) + 0.5) / N
            g_j = (int(j % N) + 0.5) / N
            euc = np.sqrt((r_i - r_j) * (r_i - r_j) + (g_i - g_j) * (g_i - g_j))
            A[i][j] = 1 - euc / sqrt2
    return A


def ibm_hist_diff(A: np.ndarray, total: int, prevhist: np.ndarray, hist: np.ndarray) -> int:
    z = (prevhist - hist)/total
    z = z.reshape(-1, 1)
    D2 = np.matmul(z.T, A)
    D2 = np.matmul(D2, z)
    return np.sqrt(D2[0][0])


def hist_inter(total, prevhist, hist):
    return np.sum(np.minimum(prevhist, hist))/total

