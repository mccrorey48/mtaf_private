from pyand import ADB
import os
import errno
from xml_to_csv import xml_to_csv
from PIL import Image


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


adb = ADB()
adb.run_cmd('shell screencap -p /sdcard/screencap.png')
adb.run_cmd('pull /sdcard/screencap.png')
adb.run_cmd('shell uiautomator dump')
adb.run_cmd('pull /sdcard/window_dump.xml')
screenshot_path = os.path.join('appium_gui', 'screenshot', 'appium_gui.png')
os.rename('screencap.png', screenshot_path)
im = Image.open(screenshot_path)
im = im.rotate(-90, expand=True)
im.save(screenshot_path)
xml_path = os.path.join('appium_gui', 'xml', 'appium_gui.xml')
csv_path = os.path.join('appium_gui', 'csv', 'appium_gui.csv')
os.rename('window_dump.xml', xml_path)
xml_to_csv(xml_path, csv_path)


