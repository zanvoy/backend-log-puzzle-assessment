#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import argparse
import urllib

def last_eight(item):
    return item[-8:]

def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    url_header = 'http://code.google.com'
    url_list = []
    pattern = re.compile(r'\S*puzzle\S*\.jpg')
    with open(filename) as f:
        data = f.read()
    matches = re.findall(pattern,data)
    for match in matches:
        url_list.append(url_header+match)
    set_list = set(url_list)
    url_list = []
    for item in set_list:
        url_list.append(item)   
    url_list = sorted(url_list, key=last_eight)
    return url_list


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists('./'+dest_dir):
        os.mkdir(dest_dir)
    count = 0
    with open('./'+dest_dir+'/index.html','a') as f:
        f.write('<html><body>')
        for url in img_urls:
            urllib.urlretrieve(url, './'+dest_dir+'/img'+str(count))
            f.write('<img src="img'+str(count)+'">')
            count += 1
        f.write('</html></body>')
def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
