import argparse
import os
from ePhone7.utils.configure import cfg
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'local', 'ds'], help="specify site tag")

args = parser.parse_args()
cfg.set_site(args.site_tag)

from lib.android.actions import Actions
import lib.common.logging_esi as logging_esi
log = logging_esi.get_logger('esi.screenshot')
logging_esi.console_handler.setLevel(logging_esi.TRACE)


if __name__ == '__main__':
    Actions.get_screenshot_as_png('screenshot', cfg.screenshot_folder)
    image_filename = os.path.join(cfg.screenshot_folder, 'screenshot.png')
    image_filename2 = os.path.join(cfg.screenshot_folder, 'screenshot2.png')
    im = Image.open(image_filename)
    print im.getbbox()
    if im.getbbox()[2] == 1024:
        print "rotating"
        im = im.rotate(-90, expand=True)
        im.save(image_filename2)
    print im.getbbox()
