#!/usr/bin/env python3

"""rendermarkdown.py: Script to render all markdown files in a directory"""

import os
import sys
import argparse

def renderFile(inputPath, outputPath, pandoc, pandocFormatArgs):
    os.system(pandoc + " " pandocFormatArgs + " -o " + outputPath + " " +
            inputPath)

def renderFolder(inputDir, outputDir, recursive, extensions, pandoc,
        pandocFormatArgs):


    if recursive:
        for root, dirs, files in os.walk(inputDir):
            for f in files:
                filename, ext = os.path.splitext(os.path.join(root, f))
                relfilename = os.path.relpath(filename+ext,
                        start=inputDir)
                if ext in extensions:
                    renderFile(filename + ext,
                            outputDir + relfilename + ".html", pandoc,
                            pandocFormatArgs)

# parser and cli arguments
parser = argparse.ArgumentParser(description="render all markdown files in a\
        given directory to HTML using pandoc")
parser.add_argument("-e", "--extensions",
        help="list of extensions that are interpreted as markdown",
        default=[".md", ".mdown", ".mkd", ".markdown"], action="append_const",
        const="str")
parser.add_argument("-l", "--location", help="directory of files to render",
        metavar="PATH", required=True)
parser.add_argument("-o", "--output",
        help="specify alternate output directory. keeps structure intact",
        metavar="PATH")
parser.add_argument("-p", "--pandoc", help="location of pandoc binary",
        default="pandoc", metavar="PATH")
parser.add_argument("-r", "--recursive",
        help="also render files in all subdirectories", action="store_true")
parser.add_argument("-s", "--stylesheet", help="location of css file.",
        metavar="URL/PATH")
parser.add_argument("-t", "--toc", help="add table of contents to each file",
        action="store_true")
parser.add_argument("-v", "--verbosity", action="count",
        help="increase command verbosity")

args = parser.parse_args()

# pandoc formatting arguments
pandocFormatArgs = "-r markdown_github -w html5 -s --toc -c http://eku.tau.bz/notes/css/main.css"

for root, dirs, files in os.walk(args.location):
    for f in files:



print("done")
