from scipy.io import wavfile
import argparse
import pytest


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="path to wav file you want to segment")
parser.add_argument("-m", "--milliseconds", help="length of segment you want to get", default=1000, type=int)
parser.add_argument("-w", "--window", help="window around the loudest part of the file you ware segmenting", default=0.1, type=float)
args = parser.parse_args()
print(args)

fs, data = wavfile.read(args.file)

