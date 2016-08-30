import json
import os
from csv import DictReader

import Image
from svauto.user_exception import UserException as Ux

from ePhone7.utils.configure import cfg
from ePhone7.utils.view_info import view_info


def get_tab_maxcolors(version):
    colors = {}
    with open(os.path.join(cfg.colors_folder, 'colors.txt'), 'w') as outfile:
        for view in sorted(view_info):
            info = view_info[view]
            if len(info['tabs']) == 0:
                continue
            classname = info['view_classname']
            colors[classname] = {'crop_points': {}}
            csv_filename = '%s_%s.csv' % (view, version)
            csv_subfolder = 'csv_%s' % version
            outfile.write("view: %s,  csv_filename: %s\n" % (view, csv_filename))
            csv_fullpath = os.path.join(cfg.csv_folder, csv_subfolder, csv_filename)
            # for each view, this outer loop finds a line in the view's
            # csv file for each tab id and calculates image location data
            for tab_name in sorted(info['tabs']):
                with open(csv_fullpath) as csv:
                    reader = DictReader(csv)
                    locator_name = info['tabs'][tab_name]['locator_name']
                    view_instance = info['view_instance']
                    locator = cfg.get_locator(locator_name, view_instance)
                    if locator['by'] == 'id':
                        for row in reader:
                            if row['resource-id'] == locator['value']:
                                break
                        else:
                            raise Ux('row not found in %s with resource-id %s' % (csv_filename, locator['value']))
                    elif locator['by'] == 'zpath':
                        for row in reader:
                            zpath_tail = locator['value'][1:]
                            tail_offset = -1 * len(zpath_tail)
                            if row['zpath'][tail_offset:] == zpath_tail:
                                break
                        else:
                            raise Ux('row not found with zpath matching %s' % locator['value'])
                    else:
                        raise Ux('Unexpected locator type')
                    (min_x, min_y, lim_x, lim_y) = [int(val) for val in [row['min_x'], row['min_y'], row['lim_x'], row['lim_y']]]
                    (x1, y1, x2, y2) = (min_y, 599 - (lim_x - 1), lim_y - 1, 599 - min_x)
                    crop_points = (x2 - 25, y1 + 20, x2 - 20, y2 - 20)
                    tab_info = info['tabs'][tab_name]
                    tab_info['crop_points'] = crop_points
                    colors[classname]['crop_points'][tab_info['locator_name']] = crop_points

            # - now we have all of the tab location data for this view
            # - for each tab in the view, open the image file for
            #   this view with that tab selected
            # - collect color info for the all tabs in that image
            for outer_name in sorted(info['tabs']):
                outfile.write('  selected tab: %s\n' % outer_name)
                im = Image.open(os.path.join(cfg.screenshot_folder, "%s_%s_%s.png" % (view, outer_name, version)))
                for inner_name in sorted(info['tabs']):
                    crop_points = tuple(info['tabs'][inner_name]['crop_points'])
                    cropped = im.crop(crop_points)
                    (x1, y1, x2, y2) = crop_points
                    im_copy = im.copy()
                    color_band = Image.new('RGBA', (x2 - x1, y2 - y1), 'yellow')
                    im_copy.paste(color_band, crop_points, 0)
                    im_copy.save(os.path.join(cfg.screenshot_folder, "%s_%s_%s_%s.png" % (view, outer_name, version, inner_name)))
                    # stripe.show()
                    # for c in sorted(cropped.getcolors(100000), reverse=True, key=lambda x: x[0])[:2]:
                    c = max(cropped.getcolors(100000), key=lambda x: x[0])
                    c_tuple = (c[1][0], c[1][1], c[1][2], c[0])
                    outfile.write("    %10s @(%3d, %3d, %3d, %3d): (%3d, %3d, %3d) (%3d) " % ((inner_name,) + crop_points + c_tuple))
                    if outer_name == inner_name:
                        # this is the selected tab, which should have a unique color
                        colors[classname]['active_color'] = list(c_tuple)
                        outfile.write("*\n")
                    else:
                        # this is one of the unselected tabs, which should all share a color different from
                        # the selected tab
                        if 'inactive_color' not in colors[classname]:
                            colors[classname]['inactive_color'] = list(c_tuple)
                        else:
                            if list(c_tuple)[:-1] != colors[classname]['inactive_color'][:-1]:
                                raise Ux('inactive colors do not match')
                        outfile.write("\n")
                        # outfile.write("%02X%02X%02X: %d\n" % (c[1][0], c[1][1], c[1][2], c[0]))

    with open(os.path.join(cfg.config_folder, 'colors_generated.json'), 'w') as f:
        f.write(json.dumps(colors, sort_keys=True, indent=2, separators=(',', ': ')))

if __name__ == '__main__':
    get_tab_maxcolors('0_15_4')