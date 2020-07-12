#!/usr/bin/env python3

from scipy.io import wavfile
import os
import argparse


def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="path to wav file you want to segment", required=True)
    parser.add_argument("-s", "--seconds", help="length of segment you want to get", default=2.0, type=float)
    parser.add_argument("-w", "--window", help="window around the loudest part of the file you ware segmenting",
                        default=0.1, type=float)

    return parser.parse_args()


def main():
    args = command_line_args()
    sample_rate, data = wavfile.read(args.file)

    # i only really care about getting 1 channel, because a) they are mono samples and b) it makes the result smaller
    left_channel = data[:, 0]
    loudest_sample_location = left_channel.argmax()

    window_in_samples = args.seconds * sample_rate
    sample_start_location = int(loudest_sample_location - (args.window * window_in_samples))
    sample_end_location = int(sample_start_location + window_in_samples)

    if left_channel.size < sample_end_location:
        sample_end_location = left_channel.size
    else:
        sample_end_location = find_closest_quiet_sample(left_channel, sample_end_location)

    sample_start_location = find_closest_quiet_sample(left_channel, sample_start_location)
    wav_segment = left_channel[sample_start_location:sample_end_location]

    directory, file = os.path.split(args.file)
    new_file = "results/" + file
    wavfile.write(new_file, sample_rate, wav_segment)


# this is to avoid the sample doing some nasty clipping
def find_closest_quiet_sample(channel, location):
    while True:
        if abs(channel[location]) < 15:
            return location
        location = location + 1


if __name__ == '__main__':
    main()
