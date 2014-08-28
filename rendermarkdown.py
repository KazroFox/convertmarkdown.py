#!/usr/bin/env python3

"""rendermarkdown.py: Script to render all markdown files in a directory"""

import os
import sys
import argparse

def appendRenderList(l, f, extensions):
    if os.path.splitext(f)[1] in extensions:
        return l + [f]
    return l

def renderFile(inputPath, outputPath, pandoc, pandocFormatArgs):
    if args.verbosity >= 1:
        print(inputPath, "->", outputPath)
    if args.verbosity >= 2:
        print("\nCommand", pandoc + " " + pandocFormatArgs + " -o \"" +\
                outputPath + "\" \"" + inputPath +"\"")
        os.system(pandoc + " " + pandocFormatArgs + " -o \"" + outputPath +
                "\" \"" + inputPath + "\"")

def renderFolder(inputDir, outputDir, recursive, extensions, pandoc,
        formatArgs):

    renderList = []
    topDirs = []
    for f in os.listdir(inputDir):
        if os.path.isfile(os.path.join(inputDir, f)):
            renderList = appendRenderList(renderList,
                    os.path.join(inputDir, f), extensions)
        elif os.path.isdir(os.path.join(inputDir, f)):
            topDirs.append(os.path.join(inputDir, f))
            if not os.path.exists(os.path.join(outputDir, f)):
                os.mkdir(os.path.join(outputDir, f))

    if recursive:
        for d in topDirs:
            for root, dirs, files in os.walk(d):
                for d in dirs:
                    dirPath = os.path.join(root, d)
                    relPath = os.path.relpath(dirPath, start=inputDir)
                    newDir = os.path.join(outputDir, relPath)
                    if not os.path.exists(newDir):
                        os.mkdir(newDir)

                for f in files:
                    renderList = appendRenderList(renderList,
                            os.path.join(root, f), extensions)

    for f in renderList:
        outF = os.path.splitext(f)[0] + ".html"
        relPath = os.path.relpath(outF, start=inputDir)
        outputPath = os.path.join(outputDir, relPath)
        renderFile(f, outputPath, pandoc, formatArgs)

# parser and cli arguments
parser = argparse.ArgumentParser(description="render all markdown files in a\
        given directory to HTML using pandoc")
parser.add_argument("-4", "--html4", help="use HTML4 not HTML5 in output",
        action="store_const", const="html4", default="html5", dest="html")
parser.add_argument("-e", "--extensions",
        help="list of extensions that are interpreted as markdown. default =\
                .md, .mdown, .mkd, .markdown", action="append", type=str)
parser.add_argument("-m", "--markdown", help="flavor of markdown to use. \
        default = github",
        choices=["markdown", "github", "mmd", "phpextra", "strict"],
        default="github", type=str)
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
        help="more verbose output. option can be supplied several times for \
                more verbosity.", default=0)
parser.add_argument("path", help="directory of files to render",
        metavar="PATH")
args = parser.parse_args()

#Set default output path to the same input path
args.output = args.output or args.path
args.extensions = args.extensions or [".md", ".mdown", ".mkd", ".markdown"]

# pandoc formatting arguments
formatArgs = "-r "
if args.markdown == "markdown":
    formatArgs += "markdown"
else:
    formatArgs += "markdown_" + args.markdown
formatArgs      += " -w " + args.html
formatArgs      += " -s"
if args.toc:
    formatArgs  += " --toc"
if args.stylesheet:
    formatArgs  += " -c " + args.stylesheet

# Debug
if args.verbosity >= 2:
    print("extensions = ", args.extensions)
    print("command = " + args.pandoc + " " + formatArgs + " -o " + args.path)

renderFolder(
        args.path,
        args.output,
        args.recursive,
        args.extensions,
        args.pandoc,
        formatArgs
)
