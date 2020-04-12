import argparse
import os
from time import time

import cv2

from src.videoEnhancer import enhance
from src.videoBreakdown import breakdowntoSTI
from src.transitionDetector import detect_transitions
from src.transitions import ColWipe, HorWipe, Cut


def main():
    overall_start = time()
    args = parse_args()
    transitions = [ColWipe(0, 30, 0, 1), Cut(90)]
    enhance(args.filename, transitions, args.output)
    return

    row_path = append_to_filename(args.filename, "rowsti", "png")
    col_path = append_to_filename(args.filename, "colsti", "png")

    # if we can find the sti's and aren't asked to recreate them just grab them
    if os.path.exists(row_path) and os.path.exists(col_path) and not args.regenerate:
        if args.verbose:
            print("Previous rowsti, and colsti detected. Retrieving them instead of recreating them.")
        rowsti = cv2.imread(row_path)
        colsti = cv2.imread(col_path)
    else:
        if args.verbose:
            print("Beginning video breakdown to Spatial-Temporal images.")
            print("Breaking down video: " + args.filename)
            print("Resizing video to height=" + str(args.filename))
            print("Using histogram intersection threshold of: " + str(args.threshold))
            if args.ibm:
                print("Using ibm colour histogram difference method")
            else:
                print("Using histogram intersection method")
            print("This may take a while please be patient...")
        start = time()
        colsti, rowsti = breakdowntoSTI(args.filename, args.size, args.threshold, args.ibm)
        diff = time() - start
        if args.verbose:
            print("Completed in " + str(diff) + " seconds.")
        if args.write:
            cv2.imwrite(row_path, rowsti)
            cv2.imwrite(col_path, colsti)
            if args.verbose:
                print("Writing row STI to: " + row_path)
                print("Writing col STI to: " + col_path)

    if args.verbose:
        print("Beginning transition detection.")
    start = time()
    transitions = detect_transitions(colsti, rowsti)
    diff = time() - start
    if args.verbose:
        print("Completed in " + str(diff) + " seconds.")
        print(str(len(transitions)) + " transitions detected.")
    if len(transitions) == 0:
        print("No transitions were detected!")
        print("This may mean that your video has no transitions, or that we did not detect them. Either way there is "
              "nothing to enhance.")
    else:
        if args.verbose:
            print("Beginning video enhancement.")
        start = time()
        enhance(args.filename, transitions, args.output)
        diff = time() - start
        if args.verbose:
            print("Completed in " + str(diff) + " seconds.")

    if args.verbose:
        diff = time() - overall_start
        print("Program completed in " + str(diff) + " seconds.")



def parse_args():
    parser = argparse.ArgumentParser(description='Enhance Transitions in Video.')
    parser.add_argument("filename", help="Path to file that you would like to analyze") # main filename
    parser.add_argument("-v", "--verbose", action="store_true", help="Be verbose when executing")
    parser.add_argument("-o", "--output", type=str, help="file to output to") # output file
    parser.add_argument("-rg", "--regenerate", action="store_true", help="regenerate sti's even if they are found in "
                                                                          "the path")
    parser.add_argument("-w", "--write", action="store_true", help="Write STIs to improve speed for re-enhancing "
                                                                   "video with different options")
    parser.add_argument("-s", "--size", type=int, choices=[32, 64, 128, 256, 512], default=64, help="height video "
                                                                                                    "should be "
                                                                                                    "resized to ("
                                                                                                    "smaller = "
                                                                                                    "faster), "
                                                                                                    "higher may "
                                                                                                    "provide better "
                                                                                                    "quality")
    parser.add_argument("-t", "--threshold", type=float, default=0.7, help="threshold for which the intersection "
                                                                           "between consecutive colour histograms is "
                                                                           "considered abnormally low")
    parser.add_argument("-i", "--ibm", action="store_true", help="use ibm histogram difference method instead of "
                                                                 "histogram intersection method")
    parser.add_argument("-p", "--prominence", type=int, choices=range(1, 11), help="a number between 1 and 10 "
                                                                                  "representing how prominently "
                                                                                  "enhanced the output video should "
                                                                                  "be")
    args = parser.parse_args()
    args.filename = full_name(args.filename)
    # assign default threshold when bad one is provided
    if args.threshold < 0.4 or args.threshold > 0.9:
        print("[threshold] must be between 0.4 and 0.9, continuing with threshold = 0.7")
        args.threshold = 0.7

    # assign default output
    if args.output is None:
        args.output = append_to_filename(args.filename, "enhanced", "mp4")
    return args


def full_name(filename) -> str:
    if not os.path.isfile(filename):
        raise ValueError(filename + " doesn't exist!")
    else:
        return os.path.abspath(filename)


# note: requires file format to be
def append_to_filename(filename: str, appendix: str, ext: str) -> str:
    split = filename.split(".")
    return split[0] + "_" + appendix + "." + ext


if __name__ == "__main__":
    main()