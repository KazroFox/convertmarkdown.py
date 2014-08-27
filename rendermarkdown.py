#!/usr/bin/env python3

"""rendermarkdown.py: Script to render all markdown files in a directory"""

import os
import sys
import argparse

# parser and cli arguments
parser = argparse.ArgumentParser(description="render all markdown files in a\
        given directory to HTML using pandoc")
parser.add_argument("-e", "--extensions",
        help="list of extensions that are interpreted as markdown",
        default=[".md", ".mdown", ".mkd", ".markdown"], action="append_const",
        const="str")
parser.add_argument("-l", "--location", help="directory of files to render",
        metavar="PATH", required=True)
parser.add_argument("-p", "--pandoc", help="location of pandoc binary",
        default="pandoc", metavar="PATH")
parser.add_argument("-r", "--recursive",
        help="also render files in all subdirectories", action="store_true")
parser.add_argument("-s", "--stylesheet", help="location of css file.",
        metavar="URL/PATH")
parser.add_argument("-v", "--verbosity", action="count",
        help="increase command verbosity")

args = parser.parse_args()

# pandoc formatting arguments
pandocFormatArgs = "-r markdown_github -w html5 -s --toc -c http://eku.tau.bz/notes/css/main.css"

# list of accepted markdown files
validExts = [".md", ".mdown", ".mkd", ".markdown"]

for root, dirs, files in os.walk(args.location):
    for f in files:
        filename, ext = os.path.splitext(os.path.join(root, f))
        if ext in validExts:
            os.system("pandoc " + pandocFormatArgs + " " + "-o" + " " + os.path.join(root, filename)+".html" + " " + os.path.join(root, f))

print("done")
