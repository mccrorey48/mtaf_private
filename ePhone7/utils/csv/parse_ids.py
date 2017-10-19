import re

re_id = re.compile('.*,([^,]*:id/[^,]*),[^,]*,(\d+),(\d+),(\d+),(\d+)')


def parse_ids(csv_fullpath):
    ids = {}
    with open(csv_fullpath) as f:
        lines = f.readlines()
        for line in lines:
            m = re_id.match(line)
            if m:
                if m.group(1) not in ids:
                    ids[m.group(1)] = [{"x1": int(m.group(2)), "y1": int(m.group(3)), "x2": int(m.group(4)),
                                        "y2": int(m.group(5))}]
                else:
                    ids[m.group(1)].append({"x1": int(m.group(2)), "y1": int(m.group(3)), "x2": int(m.group(4)),
                                        "y2": int(m.group(5))})
    return ids


if __name__ == "__main__":
    print "hello, world"
    ids = parse_ids('/home/mmccrorey/mtaf/ePhone7/utils/csv/csv_appium_gui/appium_gui.csv')
    print "# of ids: %s" % len(ids)
    for _id in sorted(ids):
        print "%60s %s" % (_id, ids[_id][0])
        for geom in ids[_id][1:]:
            print "%60s %s" % ("", geom)
