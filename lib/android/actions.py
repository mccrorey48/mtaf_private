import os
from time import sleep, time, strftime, localtime
from PIL import Image

import lib.common.logging_esi as logging
from ePhone7.utils.configure import cfg
from lib.android.remote import remote
from lib.selenium.selenium_actions import SeleniumActions
from lib.common.user_exception import UserException as Ux, UserFailException as Fx
from lib.common.wrappers import Trace

log = logging.get_logger('esi.action')
test_screenshot_folder = cfg.test_screenshot_folder
keycodes = {'KEYCODE_%d' % k: k + 7 for k in range(10)}


class Actions(SeleniumActions):

    def __init__(self, view=None):
        if view is None:
            raise Ux('Actions instantiation must include view parameter')
        self.view = view
        super(Actions, self).__init__(remote)
        self.failureException = Fx

    @Trace(log)
    def send_keycode(self, keycode):
        remote.driver.keyevent(keycodes[keycode])

    @staticmethod
    @Trace(log)
    def hide_keyboard():
        remote.driver.hide_keyboard()

    @staticmethod
    @Trace(log)
    def scroll(origin_el, destination_el):
        remote.driver.scroll(origin_el, destination_el)

    @staticmethod
    @Trace(log)
    def swipe(origin_x, origin_y, destination_x, destination_y, duration):
        remote.driver.swipe(origin_x, origin_y, destination_x, destination_y, duration)

    @staticmethod
    @Trace(log)
    def tap(x, y, duration=200):
        remote.driver.tap([(x, y)], duration)

    @staticmethod
    @Trace(log)
    def get_screenshot_as_png(filebase, screenshot_folder):
        sleep(5)
        fullpath = os.path.join(screenshot_folder, filebase + '.png')
        log.debug("saving screenshot to %s" % fullpath)
        remote.driver.get_screenshot_as_file(fullpath)
        im = Image.open(fullpath)
        if im.getbbox()[2] == 1024:
            log.debug("rotating screenshot -90 degrees")
            im = im.rotate(-90, expand=True)
            log.debug("saving rotated screenshot to %s" % fullpath)
            im.save(fullpath)

    @staticmethod
    def color_match(c1, c2, tolerance = 5):
        for i in range(3):
            if c2[i] > c1[i] + tolerance or c2[i] < c1[i] - tolerance:
                return False
        return True

    @Trace(log)
    def get_tab_color(self, filebase, tab_name):
        # now = time()
        # timestamp = strftime('%H:%M:%S', localtime(now)) + '.%s' % int((now-int(now)) * 1000)
        # suffix = "%s_%s_%s.png" % (filebase, tab_name, timestamp)
        image_filename = os.path.join(cfg.test_screenshot_folder, filebase + '.png')
        log.debug('getting tab color from file %s' % image_filename)
        im = Image.open(image_filename)
        view_classname = self.view.__class__.__name__
        active_color = cfg.colors[view_classname]['active_color'][:-1]
        inactive_color = cfg.colors[view_classname]['inactive_color'][:-1]
        # print "active_color: " + repr(active_color)
        # print "inactive_color: " + repr(inactive_color)
        crop_points = tuple(cfg.colors[view_classname]['crop_points'][tab_name])
        log.debug("crop_points: %s" % repr(crop_points))
        cropped = im.crop(crop_points)
        # cropped.save(os.path.join(cfg.test_screenshot_folder, 'cropped_%s' % suffix))
        (n, (r, g, b, depth)) = max(cropped.getcolors(1000), key=lambda x: x[0])
        tab_color = [r, g, b]
        # color_band = Image.new('RGBA', (crop_points[2] - crop_points[0], crop_points[3] - crop_points[1]), 'yellow')
        # im.paste(color_band, crop_points, 0)
        # im.save(os.path.join(cfg.test_screenshot_folder, filebase + '_after_%s.png' % suffix))
        if self.color_match(tab_color, active_color):
            log.debug('tab_color is "active": %s' % repr(tab_color))
            return 'active_color'
        elif self.color_match(tab_color, inactive_color):
            log.debug('tab_color is "inactive": %s' % repr(tab_color))
            return 'inactive_color'
        else:
            exc_format = 'invalid color %s found for tab %s in view %s, active = %s, inactive = %s'
            raise Ux(exc_format % (repr(tab_color), tab_name, view_classname, repr(active_color), repr(inactive_color)))

    @staticmethod
    @Trace(log)
    def get_element_color(filebase, elem, cropped_suffix=''):
        im = Image.open(os.path.join(cfg.test_screenshot_folder, filebase + '.png'))
        # calculate image crop points from element location['x'], location['y'], size['height'] and size['width']
        location = elem.location
        size = elem.size
        min_x = location['x']
        min_y = location['y']
        lim_x = min_x + size['width']
        lim_y = min_y + size['height']
        # print "min_x = %s, min_y = %s, lim_x = %s, lim_y = %s" % (min_x, min_y, lim_x, lim_y)
        # (x1, y1, x2, y2) = (min_y, 600-lim_x, lim_y, 600-min_x)
        (x1, y1, x2, y2) = (min_x, min_y, lim_x, lim_y)
        crop_points = [int(i) for i in (x1, y1, x2, y2)]
        # print "crop_points: " + repr(crop_points)
        cropped = im.crop(crop_points)
        cropped.save(os.path.join(cfg.test_screenshot_folder, 'cropped%s.png' % cropped_suffix))
        colors = cropped.getcolors(1000)
        color_band = Image.new('RGBA', (crop_points[2] - crop_points[0], crop_points[3] - crop_points[1]), 'yellow')
        im.paste(color_band, crop_points, 0)
        im.save(os.path.join(cfg.test_screenshot_folder, filebase + '_after.png'))
        current_color = list(sorted(colors, reverse=True, key=lambda x: x[0])[1][1])[:-1]
        return current_color


    @staticmethod
    @Trace(log)
    def pixel_from_xml_xy(pix, x, y):
        try:
            # print "(%d,%d) => [%d, %d]" % (x, y, y, 599-x)
            return [int(val) for val in pix[y, 599 - x]]
        except Exception as e:
            raise Ux("pixel_from_xml_xy(pix, %d, %d), pix[%d, %d] %s" % (x, y, y, 599 - x, e.message))

    @Trace(log)
    def get_pixel_histograms(self, pix, min_x, min_y, lim_x, lim_y):
        # translate screen layout (xml) x and y to pix (png file) x and y
        hists = {}
        pixels_per_color = {}
        for y in range(min_y, lim_y):
            yhist = {}
            for x in range(min_x, lim_x):
                pixel = self.pixel_from_xml_xy(pix, x, y)
                color = '%02X%02X%02X' % (pixel[0], pixel[1], pixel[2])
                if color in pixels_per_color:
                    pixels_per_color[color] += 1
                else:
                    pixels_per_color[color] = 1
                if color in yhist:
                    yhist[color] += 1
                else:
                    yhist[color] = 1
            hists[y] = yhist
        for key in pixels_per_color.keys():
            if pixels_per_color[key] < 10:
                del pixels_per_color[key]
        return hists

    @Trace(log)
    def assert_element_maxcolor(self, pix, elem_name, color_name, should_be_true):
        pass
    #     maxcolor = self.get_element_maxcolor(pix, elem_name)
    #     log.debug('verifying element %s has background color "%s"' % (elem_name, color_name))
    #     if should_be_true:
    #         self.assertEqual(maxcolor, color_name, 'maxcolor "%s" is not "%s"' % (maxcolor, color_name))
    #     else:
    #         self.assertNotEqual(maxcolor, color_name, 'maxcolor "%s" should not be "%s"' % (maxcolor, color_name))

    # def assert_contact_names_ok(self, names, contacts_group):
    #     self.assertListEqual(names, cfg.site['Accounts']['R2d2User'][contacts_group],
    #                          'contact names %s not equal to group "%s" names %s' %
    #                          (repr(names), contacts_group, repr(cfg.site['Accounts']['R2d2User'][contacts_group])))
    @staticmethod
    @Trace(log)
    def tap_element(el, duration=200):
        center = (el.location['x'] + (el.size['width'] / 2), el.location['y'] + (el.size['height'] / 2))
        remote.driver.tap([center], duration)

    # key is a locator name
    # "key" is the element whose locator is specified as a sub-element to
    # a parent key; in this case a specific parent element has been identified
    # from a list of candidates that match the parent key, and this element
    # is passed in as the "parent" argument
    # find all elements that match a locator named "key", put them in a list,
    # filter the list if filter_fn is not None
    #
    # filter_fn must take a list of elements and returns a filtered list of elements


