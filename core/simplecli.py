#!/usr/bin/env python

import argparse
import time


def download(args):
    time.sleep(3)
    print("Downloading...")

def main():
    parser = argparse.ArgumentParser(description='Download a file.')
    parser.add_argument('filename', metavar='filename', type=str, help='name of the file to download')
    args = parser.parse_args()

    download(args)

if __name__ == '__main__':
    main()
