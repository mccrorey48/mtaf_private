import csv
import re
from lib.user_exception import UserException as Ux


re_id = re.compile('.*,([^,]*:id/[^,]*),[^,]*,(\d+),(\d+),(\d+),(\d+)')


def parse_zpaths(csv_fullpath):
    zpaths = {}
    short_zpaths = {}
    with open(csv_fullpath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['zpath'] in zpaths:
                raise Ux("Expected zpaths to be unique, found duplicate: %s" % row['zpath'])
            try:
                zpaths[row['zpath']] = [{"x1": int(row['min_x']), "y1": int(row['min_y']), "x2": int(row['lim_x']),
                                         "y2": int(row['lim_y'])}]
            except ValueError:
                pass
            except TypeError:
                print "TypeError processing %s" % repr(row)

    for zpath in zpaths:
        zterms = zpath.split('/')
        # - for each full zpath, calculate the minimum "tail" that will uniquely locate the element
        # - do this by incrementing the number of zpath terms in the tail until no other full zpaths match
        # - for this purpose, remove '[1]' enumerators from the zpath strings being evaluated because,
        #   when doing a "find by zpath" via webdriver/appium, #1 in a group of zpaths (designated by '[1]')
        #   will conflict with a similar tail that lacks the '[1]' because it is not part of an enumerated group)
        for count in range(len(zterms)):
            nterms = count + 1
            tail = '/'.join(zpath.split('/')[-1 * nterms:])
            matched = False
            for _zpath in zpaths:
                _tail = '/'.join(_zpath.split('/')[-1 * nterms:])
                if ''.join(_tail.split('[1]')) == ''.join(tail.split('[1]')):
                    # if _tail == tail:
                    if matched:
                        break
                    else:
                        matched = True
            else:
                # if all zpaths were checked for tail match and exactly one was found, use that tail,
                # otherwise this else clause is not run and the count loop continues
                if not matched:
                    raise Ux("no tails matched, at least one should!")
                short_zpaths['//' + tail] = zpaths[zpath]
                break
        else:
            short_zpaths[zpath] = zpaths[zpath]
    return short_zpaths


def parse_ids(csv_fullpath):
    ids = {}
    with open(csv_fullpath) as f:
        reader = csv.DictReader(f, quotechar="'")
        for row in reader:
            _id = row['resource-id']
            if _id != '':
                x1 = int(row['min_x'])
                y1 = int(row['min_y'])
                x2 = int(row['lim_x'])
                y2 = int(row['lim_y'])
                if _id in ids:
                    ids[_id].append({"x1": x1, "y1": y1, "x2": x2, "y2": y2})
                else:
                    ids[_id] = [{"x1": x1, "y1": y1, "x2": x2, "y2": y2}]
    return ids


if __name__ == "__main__":
    default_csv = '/home/mmccrorey/mtaf/ePhone7/utils/csv/csv_appium_gui/appium_gui.csv'
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  parses csv file generated by xml_to_csv.py and prints element' +
                                                 '  position and id info\n')
    parser.add_argument("-z", "--zpath", dest='zpath', action='store_true')
    parser.add_argument("-q", "--quiet", dest='quiet', action='store_true')
    args = parser.parse_args()
    if args.zpath:
        locs = parse_zpaths(default_csv)
    else:
        locs = parse_ids(default_csv)
    if not args.quiet:
        loc_keys = locs.keys()
        max_len = len(max(loc_keys, key=lambda x: len(x)))
        fmt = "%%-%ds %%s" % max_len
        for loc in sorted(locs):
            print fmt % (loc, locs[loc][0])
            for geom in locs[loc][1:]:
                print fmt % ("", geom)
