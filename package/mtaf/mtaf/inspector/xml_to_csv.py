import re
import xml.etree.ElementTree as ET
import csv

import mtaf.lib.android_zpath

tagre = re.compile('([^\[]+)(.*)')


def printall(writer, node, tag_index, pfx):
    if node.tag == 'node':
        tag = node.attrib['class']
    else:
        tag = node.tag
    tag = mtaf.lib.android_zpath.get_zpath_tag(tag)
    if tag_index == 0:
        new_prefix = pfx + tag
    else:
        new_prefix = '%s%s[%s]' % (pfx, tag, tag_index)
    items = [new_prefix]
    for key in ['resource-id', 'text', 'bounds']:
        if key in node.attrib and node.attrib[key] != "":
            try:
                _str = node.attrib[key].encode('utf-8')
                if key == 'bounds':
                    m = re.match('\[(\d+),(\d+)\]\[(\d+),(\d+)\]', _str)
                    if m:
                        items += m.groups()
                    else:
                        items += ['', '', '', '']
                else:
                    items.append(repr(_str))
            except UnicodeEncodeError as e:
                print e.message
        else:
            items.append('')
    writer.writerow(items)
    tag_total = {}
    for child in node:
        child_tag = child.attrib['class']
        if child_tag in tag_total:
            tag_total[child_tag] += 1
        else:
            tag_total[child_tag] = 1
    tag_indices = {}
    for key in tag_total:
        tag_indices[key] = 0
    for child in node:
        if child.tag == 'node':
            child_tag = child.attrib['class']
        else:
            child_tag = child.tag
        if tag_total[child_tag] > 1:
            tag_indices[child_tag] += 1
            printall(writer, child, tag_indices[child_tag], new_prefix + '/')
        else:
            printall(writer, child, 0, new_prefix + '/')


def xml_to_csv(xml_file_path, csv_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    prefix = ''
    with open(csv_file_path, 'w') as output_file:
        # header line helps vim display csv (with csv plugin) and used by python cvs.DictReader()
        writer = csv.writer(output_file, quotechar="'")
        writer.writerow(['zpath', 'resource-id', 'text', 'min_x', 'min_y', 'lim_x', 'lim_y'])
        printall(writer, root, 0, prefix)


# run this file from mtaf top level (repo) directory
if __name__ == "__main__":
    import csv
    xml_file = 'inspector_app/xml/inspector.xml'
    csv_file = 'inspector_app/csv/inspector.csv'
    xml_to_csv(xml_file, csv_file)
    with open(csv_file) as f:
        reader = csv.DictReader(f, quotechar="'")
        for i, row in enumerate(reader):
            print "row %d" % i
            for key in row:
                print "  %s: %s" % (key, row[key])