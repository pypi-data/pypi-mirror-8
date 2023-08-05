# Screenshot-related features of PyAutoGUI

"""
So, apparently Pillow support on Ubuntu 64-bit has several additional steps since it doesn't have JPEG/PNG support out of the box. Description here:

https://stackoverflow.com/questions/7648200/pip-install-pil-e-tickets-1-no-jpeg-png-support
http://ubuntuforums.org/showthread.php?t=1751455
"""

import datetime
import os
import subprocess
import sys
from PIL import Image
from PIL import ImageOps

RUNNING_PYTHON_2 = sys.version_info[0] == 2

try:
    whichProc = subprocess.Popen(['which', 'scrot'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    scrotExists = whichProc.wait() == 0
except:
    # if there is no "which" program to find scrot, then assume there is no scrot.
    scrotExists = False



def locateAll(needleImage, haystackImage, grayscale=False, limit=None):
    needleFileObj = None
    haystackFileObj = None
    if isinstance(needleImage, str):
        # 'image' is a filename, load the Image object
        needleFileObj = open(needleImage, 'rb')
        needleImage = Image.open(needleFileObj)
    if isinstance(haystackImage, str):
        # 'image' is a filename, load the Image object
        haystackFileObj = open(haystackImage, 'rb')
        haystackImage = Image.open(haystackFileObj)


    if grayscale:
        needleImage = ImageOps.grayscale(needleImage)
        haystackImage = ImageOps.grayscale(haystackImage)

    needleWidth, needleHeight = needleImage.size
    haystackWidth, haystackHeight = haystackImage.size

    needleImageData = tuple(needleImage.getdata()) # TODO - rename to needleImageData??
    haystackImageData = tuple(haystackImage.getdata())

    needleImageRows = [needleImageData[y * needleWidth:(y+1) * needleWidth] for y in range(needleHeight)] # LEFT OFF - check this
    needleImageFirstRow = needleImageRows[0]

    assert len(needleImageFirstRow) == needleWidth
    assert [len(row) for row in needleImageRows] == [needleWidth] * needleHeight

    numMatchesFound = 0

    for y in range(haystackHeight):
        for matchx in kmp(needleImageFirstRow, haystackImageData[y * haystackWidth:(y+1) * haystackWidth]):
            foundMatch = True
            for searchy in range(1, needleHeight):
                haystackStart = (searchy + y) * haystackWidth + matchx
                if needleImageData[searchy * needleWidth:(searchy+1) * needleWidth] != haystackImageData[haystackStart:haystackStart + needleWidth]:
                    foundMatch = False
                    break
            if foundMatch:
                # Match found, report the x, y, width, height of where the matching region is in haystack.
                numMatchesFound += 1
                yield (matchx, y, needleWidth, needleHeight)
                if limit is not None and numMatchesFound >= limit:
                    # Limit has been reached. Close file handles.
                    if needleFileObj is not None:
                        needleFileObj.close()
                    if haystackFileObj is not None:
                        haystackFileObj.close()


    # There was no limit or the limit wasn't reached, but close the file handles anyway.
    if needleFileObj is not None:
        needleFileObj.close()
    if haystackFileObj is not None:
        haystackFileObj.close()


def locate(needleImage, haystackImage, grayscale=False):
    # Note: The gymnastics in this function is because we want to make sure to exhaust the iterator so that the needle and haystack files are closed in locateAll.
    points = tuple(locateAll(needleImage, haystackImage, grayscale, 1))
    if len(points) > 0:
        return points[0]
    else:
        return None


def locateOnScreen(image, grayscale=False):
    screenshotIm = screenshot()
    retVal = locate(image, screenshotIm, grayscale)
    if 'fp' in dir(screenshotIm):
        screenshotIm.fp.close() # Screenshots on Windows won't have an fp since they came from ImageGrab, not a file.
    return retVal


def locateAllOnScreen(image, grayscale=False, limit=None):
    screenshotIm = screenshot()
    retVal = locateAll(image, screenshotIm, grayscale, limit)
    if 'fp' in dir(screenshotIm):
        screenshotIm.fp.close() # Screenshots on Windows won't have an fp since they came from ImageGrab, not a file.
    return retVal


def screenshot_win32(imageFilename=None):
    im = ImageGrab.grab()
    if imageFilename is not None:
        im.save(imageFilename)
    return im


def screenshot_osx(imageFilename=None):
    if imageFilename is None:
        tmpFilename = '.screenshot%s.png' % (datetime.datetime.now().strftime('%Y-%m%d_%H-%M-%S-%f'))
    else:
        tmpFilename = imageFilename
    subprocess.call(['screencapture', tmpFilename])
    im = Image.open(tmpFilename)
    if imageFilename is None:
        os.unlink(tmpFilename)
    return im


def screenshot_linux(imageFilename=None):
    if not scrotExists:
        raise NotImplementedError('"scrot" must be installed to use screenshot functions in Linux. Run: sudo apt-get install scrot')
    if imageFilename is None:
        tmpFilename = '.screenshot%s.png' % (datetime.datetime.now().strftime('%Y-%m%d_%H-%M-%S-%f'))
    else:
        tmpFilename = imageFilename
    if scrotExists:
        subprocess.call(['scrot', tmpFilename])
        im = Image.open(tmpFilename)
        if imageFilename is None:
            os.unlink(tmpFilename)
        return im
    else:
        raise Exception('The scrot program must be installed to take a screenshot with PyAutoGUI on Linux. Run: sudo apt-get install scrot')



def kmp(needle, haystack): # Knuth-Morris-Pratt search algorithm implementation (to be used by screen capture)
    # build table of shift amounts
    shifts = [1] * (len(needle) + 1)
    shift = 1
    for pos in range(len(needle)):
        while shift <= pos and needle[pos] != needle[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in haystack:
        while matchLen == len(needle) or \
              matchLen >= 0 and needle[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(needle):
            yield startPos


def center(coords):
    return (coords[0] + int(coords[2] / 2), coords[1] + int(coords[3] / 2))



# set the screenshot() function based on the platform running this module
if sys.platform.startswith('java'):
    raise NotImplementedError('Jython is not yet supported by PyAutoGUI.')
elif sys.platform == 'darwin':
    screenshot = screenshot_osx
elif sys.platform == 'win32':
    screenshot = screenshot_win32
    from PIL import ImageGrab
else:
    screenshot = screenshot_linux
