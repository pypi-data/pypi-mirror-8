import unittest
import sys
import os
import time
import threading
from PIL import Image
sys.path.insert(0, os.path.abspath('..'))
import pyautogui

runningOnPython2 = sys.version_info[0] == 2

if runningOnPython2:
    INPUT_FUNC = raw_input
else:
    INPUT_FUNC = input

# TODO - note that currently most of the click-related functionality is not tested.

class TestGeneral(unittest.TestCase):
    def test_accessibleNames(self):
        # Check that all the functions are defined.

        # mouse-related API
        pyautogui.moveTo
        pyautogui.moveRel
        pyautogui.dragTo
        pyautogui.dragRel
        pyautogui.mouseDown
        pyautogui.mouseUp
        pyautogui.click
        pyautogui.rightClick
        pyautogui.doubleClick
        pyautogui.tripleClick

        # keyboard-related API
        pyautogui.typewrite
        pyautogui.hotkey
        pyautogui.keyDown
        pyautogui.keyUp
        pyautogui.press

        # The functions implemented in the platform-specific modules should also show up in the pyautogui namespace:
        pyautogui.position
        pyautogui.size
        pyautogui.scroll
        pyautogui.hscroll
        pyautogui.vscroll

    def test_size(self):
        width, height = pyautogui.size()

        self.assertTrue(isinstance(width, int), 'Type of width is %s' % (type(width)))
        self.assertTrue(isinstance(height, int), 'Type of height is %s' % (type(height)))
        self.assertTrue(width > 0, 'Width is set to %s' % (width))
        self.assertTrue(height > 0, 'Height is set to %s' % (height))

    def test_position(self):
        mousex, mousey = pyautogui.position()

        if runningOnPython2 and sys.platform != 'darwin':
            # Python 2 on OS X returns int.
            self.assertTrue(isinstance(mousex, long), 'Type of mousex is %s' % (type(mousex)))
            self.assertTrue(isinstance(mousey, long), 'Type of mousey is %s' % (type(mousey)))
        else:
            self.assertTrue(isinstance(mousex, int), 'Type of mousex is %s' % (type(mousex)))
            self.assertTrue(isinstance(mousey, int), 'Type of mousey is %s' % (type(mousey)))

        # Test passing x and y arguments to position().
        pyautogui.moveTo(mousex + 1, mousey + 1)
        x, y = pyautogui.position(mousex, None)
        self.assertEqual(x, mousex)
        self.assertNotEqual(y, mousey)

        x, y = pyautogui.position(None, mousey)
        self.assertNotEqual(x, mousex)
        self.assertEqual(y, mousey)

    def test_onScreen(self):
        width, height = pyautogui.size()
        halfWidth = int(width / 2)
        halfHeight = int(height / 2)

        self.assertTrue(pyautogui.onScreen(0, 0))
        self.assertTrue(pyautogui.onScreen([0, 0]))

        self.assertTrue(pyautogui.onScreen(halfWidth, 0))
        self.assertTrue(pyautogui.onScreen([halfWidth, 0]))
        self.assertTrue(pyautogui.onScreen(0, halfHeight))
        self.assertTrue(pyautogui.onScreen([0, halfHeight]))
        self.assertTrue(pyautogui.onScreen(halfWidth, halfHeight))
        self.assertTrue(pyautogui.onScreen([halfWidth, halfHeight]))

        self.assertFalse(pyautogui.onScreen(-1, 0))
        self.assertFalse(pyautogui.onScreen([-1, 0]))
        self.assertFalse(pyautogui.onScreen(-1, -1))
        self.assertFalse(pyautogui.onScreen([-1, -1]))
        self.assertFalse(pyautogui.onScreen(0, -1))
        self.assertFalse(pyautogui.onScreen([0, -1]))

        self.assertFalse(pyautogui.onScreen(width, 0))
        self.assertFalse(pyautogui.onScreen([width, 0]))
        self.assertFalse(pyautogui.onScreen(0, height))
        self.assertFalse(pyautogui.onScreen([0, height]))
        self.assertFalse(pyautogui.onScreen(width, height))
        self.assertFalse(pyautogui.onScreen([width, height]))


class TestMouse(unittest.TestCase):
    def test_moveTo(self):
        # NOTE - The user moving the mouse during this test will cause it to fail.

        # moving the mouse
        pyautogui.moveTo(1, 1)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (1, 1), 'mousepos set to %s' % (mousepos,))

        # no coordinate specified (should be a NO-OP)
        pyautogui.moveTo(None, None)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (1, 1), 'mousepos set to %s' % (mousepos,))

        # moving the mouse to a new location
        pyautogui.moveTo(2, 2)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (2, 2), 'mousepos set to %s' % (mousepos,))

        # moving the mouse over time (1/5 second)
        pyautogui.moveTo(1, 1, 0.2)
        mousepos = pyautogui.position()

        self.assertTrue(mousepos == (1, 1), 'mousepos set to %s' % (mousepos,))

        # moving the mouse with only x specified
        pyautogui.moveTo(5, None)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (5, 1), 'mousepos set to %s' % (mousepos,))

        # ...and only y specified
        pyautogui.moveTo(None, 5)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (5, 5), 'mousepos set to %s' % (mousepos,))


    def test_moveRel(self):
        # NOTE - The user moving the mouse during this test will cause it to fail.

        # start at 1,1
        pyautogui.moveTo(1, 1)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (1, 1), 'mousepos set to %s' % (mousepos,))

        # move down and right
        pyautogui.moveRel(4, 4)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (5, 5), 'mousepos set to %s' % (mousepos,))

        # move up and left
        pyautogui.moveRel(-4, -4)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (1, 1), 'mousepos set to %s' % (mousepos,))

        # move right
        pyautogui.moveRel(4, None)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (5, 1), 'mousepos set to %s' % (mousepos,))

        # move down
        pyautogui.moveRel(None, 4)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (5, 5), 'mousepos set to %s' % (mousepos,))

        # move left
        pyautogui.moveRel(-4, None)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (1, 5), 'mousepos set to %s' % (mousepos,))

        # move up
        pyautogui.moveRel(None, -4)
        mousepos = pyautogui.position()
        self.assertTrue(mousepos == (1, 1), 'mousepos set to %s' % (mousepos,))


    def test_scroll(self):
        # TODO - currently this just checks that scrolling doesn't result in an error.
        pyautogui.scroll(1)
        pyautogui.scroll(-1)
        pyautogui.hscroll(1)
        pyautogui.hscroll(-1)
        pyautogui.vscroll(1)
        pyautogui.vscroll(-1)


class TypewriteThread(threading.Thread):
    def __init__(self, msg, interval=0.0):
        super(TypewriteThread, self).__init__()
        self.msg = msg
        self.interval = interval

    def run(self):
        time.sleep(0.25) # NOTE: BE SURE TO ACCOUNT FOR THIS QUARTER SECOND FOR TIMING TESTS!
        pyautogui.typewrite(self.msg, self.interval)


class PressThread(threading.Thread):
    def __init__(self, keysArg):
        super(PressThread, self).__init__()
        self.keysArg = keysArg

    def run(self):
        time.sleep(0.25) # NOTE: BE SURE TO ACCOUNT FOR THIS QUARTER SECOND FOR TIMING TESTS!
        pyautogui.press(self.keysArg)


class TestKeyboard(unittest.TestCase):
    # NOTE: The terminal window running this script must be in focus during the keyboard tests.
    # You cannot run this as a scheduled task or remotely.
    def test_typewrite(self):
        # 'Hello world!\n' test
        t = TypewriteThread('Hello world!\n')
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, 'Hello world!')

        # 'Hello world!\n' as a list argument
        t = TypewriteThread(list('Hello world!\n'))
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, 'Hello world!')

        # All printable ASCII characters test
        allKeys = []
        for c in range(32, 127):
            allKeys.append(chr(c))
        allKeys = ''.join(allKeys)

        t = TypewriteThread(allKeys + '\n')
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, allKeys)

    def checkForValidCharacters(self, msg):
        for c in msg:
            self.assertTrue(pyautogui.isValidKey(c), '"%c" is not a valid key on platform %s' % (c, sys.platform))


    def test_typewrite_slow(self):

        # Test out the interval parameter to make sure it adds pauses.
        t = TypewriteThread('Hello world!\n', 0.1)
        startTime = time.time()
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, 'Hello world!')
        elapsed = time.time() - startTime
        self.assertTrue(1.0 < elapsed <  2.0, 'Took %s seconds, expected 1.0 < x 2.0 seconds.' % (elapsed))


    def test_typewrite_editable(self):
        # Backspace test
        t = TypewriteThread(['a', 'b', 'c', '\b', 'backspace', 'x', 'y', 'z', '\n'])
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, 'axyz')

        # TODO - Currently the arrow keys don't seem to work entirely correctly on OS X.
        if sys.platform != 'darwin':
            # Arrow key test
            t = TypewriteThread(['a', 'b', 'c', 'left', 'left', 'right', 'x', '\n'])
            t.start()
            response = INPUT_FUNC()
            self.assertEqual(response, 'abxc')

        # Del key test
        t = TypewriteThread(['a', 'b', 'c', 'left', 'left','left', 'del', 'delete', '\n'])
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, 'c')

        # Home and end key test
        t = TypewriteThread(['a', 'b', 'c', 'home', 'x','end', 'z', '\n'])
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, 'xabcz')


    def test_pause(self):
        oldValue = pyautogui.PAUSE

        startTime = time.time()
        pyautogui.PAUSE = 0.35 # there should be a 0.35 second pause after each call
        pyautogui.moveTo(0, 0)
        pyautogui.moveRel(0,1)
        pyautogui.moveTo(0, 0)

        elapsed = time.time() - startTime
        self.assertTrue(1.0 < elapsed <  1.1, 'Took %s seconds, expected 1.0 < 1.1 seconds.' % (elapsed))

        pyautogui.PAUSE = oldValue # restore the old PAUSE value

    def test_press(self):
        # '' test
        t = PressThread('enter')
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, '')

        # 'a' test, also test sending list of 1- and multi-length strings
        t = PressThread(['a', 'enter'])
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, 'a')

        # 'ba' test, also test sending list of 1- and multi-length strings
        t = PressThread(['a', 'left', 'b', 'enter'])
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, 'ba')

    def test_typewrite_space(self):
        # Backspace test
        t = TypewriteThread(['space', ' ', '\n']) # test both 'space' and ' '
        t.start()
        response = INPUT_FUNC()
        self.assertEqual(response, '  ')

class TestScreenshot(unittest.TestCase):
    # TODO - lots of warnings about unclosed file handles for these tests.
    def test_locate_filename(self):
        self.assertEqual((94, 94, 4, 4), tuple(pyautogui.locate('slash.png', 'haystack1.png')))
        self.assertEqual((93, 93, 4, 4), tuple(pyautogui.locate('slash.png', 'haystack2.png')))

        self.assertEqual((94, 94, 4, 4), tuple(pyautogui.locate('slash.png', 'haystack1.png', grayscale=True)))
        self.assertEqual((93, 93, 4, 4), tuple(pyautogui.locate('slash.png', 'haystack2.png', grayscale=True)))

        self.assertEqual(None, pyautogui.locate('slash.png', 'colornoise.png'))
        self.assertEqual(None, pyautogui.locate('slash.png', 'colornoise.png', grayscale=True))

    def test_locate_im(self):
        slashFp = open('slash.png' ,'rb')
        haystack1Fp = open('haystack1.png' ,'rb')
        haystack2Fp = open('haystack2.png' ,'rb')
        colorNoiseFp = open('colornoise.png' ,'rb')
        slashIm = Image.open(slashFp)
        haystack1Im = Image.open(haystack1Fp)
        haystack2Im = Image.open(haystack2Fp)
        colorNoiseIm = Image.open(colorNoiseFp)

        self.assertEqual((94, 94, 4, 4), tuple(pyautogui.locate(slashIm, haystack1Im)))
        self.assertEqual((93, 93, 4, 4), tuple(pyautogui.locate(slashIm, haystack2Im)))

        self.assertEqual((94, 94, 4, 4), tuple(pyautogui.locate(slashIm, haystack1Im, grayscale=True)))
        self.assertEqual((93, 93, 4, 4), tuple(pyautogui.locate(slashIm, haystack2Im, grayscale=True)))

        self.assertEqual(None, pyautogui.locate(slashIm, colorNoiseIm))
        self.assertEqual(None, pyautogui.locate(slashIm, colorNoiseIm, grayscale=True))

        slashFp.close()
        haystack1Fp.close()
        haystack2Fp.close()
        colorNoiseFp.close()

    def test_locateAll_filename(self):
        self.assertEqual(((94, 94, 4, 4),), tuple(pyautogui.locateAll('slash.png', 'haystack1.png')))
        self.assertEqual(((93, 93, 4, 4), (94, 94, 4, 4), (95, 95, 4, 4)), tuple(pyautogui.locateAll('slash.png', 'haystack2.png')))

        self.assertEqual(((94, 94, 4, 4),), tuple(pyautogui.locateAll('slash.png', 'haystack1.png', grayscale=True)))
        self.assertEqual(((93, 93, 4, 4), (94, 94, 4, 4), (95, 95, 4, 4)), tuple(pyautogui.locateAll('slash.png', 'haystack2.png', grayscale=True)))

        self.assertEqual((), tuple(pyautogui.locateAll('slash.png', 'colornoise.png')))
        self.assertEqual((), tuple(pyautogui.locateAll('slash.png', 'colornoise.png', grayscale=True)))

    def test_locateAll_im(self):
        slashFp = open('slash.png' ,'rb')
        haystack1Fp = open('haystack1.png' ,'rb')
        haystack2Fp = open('haystack2.png' ,'rb')
        colorNoiseFp = open('colornoise.png' ,'rb')
        slashIm = Image.open(slashFp)
        haystack1Im = Image.open(haystack1Fp)
        haystack2Im = Image.open(haystack2Fp)
        colorNoiseIm = Image.open(colorNoiseFp)

        self.assertEqual(((94, 94, 4, 4),), tuple(pyautogui.locateAll(slashIm, haystack1Im)))
        self.assertEqual(((93, 93, 4, 4), (94, 94, 4, 4), (95, 95, 4, 4)), tuple(pyautogui.locateAll(slashIm, haystack2Im)))

        self.assertEqual(((94, 94, 4, 4),), tuple(pyautogui.locateAll(slashIm, haystack1Im, grayscale=True)))
        self.assertEqual(((93, 93, 4, 4), (94, 94, 4, 4), (95, 95, 4, 4)), tuple(pyautogui.locateAll(slashIm, haystack2Im, grayscale=True)))

        self.assertEqual((), tuple(pyautogui.locateAll(slashIm, colorNoiseIm)))
        self.assertEqual((), tuple(pyautogui.locateAll(slashIm, colorNoiseIm, grayscale=True)))

        slashFp.close()
        haystack1Fp.close()
        haystack2Fp.close()
        colorNoiseFp.close()

    def test_center(self):
        self.assertEqual((10, 10), pyautogui.center((0, 0, 20, 20)))
        self.assertEqual((10, 10), pyautogui.center((5, 5, 10, 10)))

        self.assertEqual((100, 100), pyautogui.center((0, 0, 200, 200)))
        self.assertEqual((100, 100), pyautogui.center((50, 50, 100, 100)))


if __name__ == '__main__':
    unittest.main()
