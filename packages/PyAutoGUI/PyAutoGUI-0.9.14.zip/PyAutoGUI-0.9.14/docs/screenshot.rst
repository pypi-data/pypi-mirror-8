.. default-role:: code

===========
Screenshots
===========

PyAutoGUI can take screenshots, save them to files, and locate subimages inside other images. This is useful if you have a small image of, say, a button that needs to be clicked and want to locate it on the screen.

Screenshot functionality requires the Pillow module. OS X uses the `screencapture` command, which comes with the operating system. Linux uses the `scrot` command, which can be installed by running `sudo apt-get install scrot`.

Ubuntu Installation
===================

Unfortunately, Ubuntu seems to have several deficiencies with installing Pillow. PNG and JPEG support are not included with Pillow out of the box on Ubuntu. The following links have more information

The screenshot() Function
=========================

Calling `screenshot()` will return an Image object (see the Pillow or PIL module documentation for details). Passing a string of a filename will save the screenshot to a file as well as return it as an Image object.

.. code:: python

    >>> import pyautogui
    >>> im1 = pyautogui.screenshot()
    >>> im2 = pyautogui.screenshot('my_screenshot.png')

On a 1920 x 1080 screen, the `screenshot()` function takes roughly 100 milliseconds - it's not fast but it's not slow.


The Locate Functions
====================

You can visually locate something on the screen if you have an image file of it. For example, say the calculator app was running on your computer and looked like this:

.. image:: calculator.png

You can't call the `moveTo()` and `click()` functions if you don't know the exact screen coordinates of where the calculator buttons are. The calculator can appear in a slightly different place each time it is launched, causing you to re-find the coordinates each time. However, if you have an image of the button, such as the image of the 7 button:

.. image:: calc7key.png

. . . you can call the `locateOnScreen('calc7key.png')` function to get the screen coordinates.

There are several "locate" functions:

    locateOnScreen(image) - Returns (x, y) coordinate of first found instance of the image on the screen. 'image' can be a string of an image filename or a PIL Image object. Returns None if not found on the screen.

    locateAllOnScreen(image) - Returns an iterator the returns (x, y) coordinates.

    locate(needle_image, haystack_image) - Returns (x, y) coordinate of first found instance of the needle_image on the haystack_image. Arguments can be a string of an image filename or a PIL Image object. Returns None if not found on the screen.

    locateAll(needle_image, haystack_image) - Returns an iterator the returns (x, y) coordinates.
