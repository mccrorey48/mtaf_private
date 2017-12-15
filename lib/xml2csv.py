import re
import xml.etree.ElementTree as ET

import lib.android_zpath

tagre = re.compile('([^\[]+)(.*)')


def printall(output_lines, node, tag_index, pfx):
    if node.tag == 'node':
        tag = node.attrib['class']
    else:
        tag = node.tag
    tag = lib.android_zpath.get_zpath_tag(tag)
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
                        items.append(','.join(m.groups()))
                    else:
                        items.append(',,,')
                else:
                    items.append(_str)
            except UnicodeEncodeError as e:
                print e.message
        else:
            items.append('')
    output_lines.append('%s\n' % ','.join(items))
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
            printall(output_lines, child, tag_indices[child_tag], new_prefix + '/')
        else:
            printall(output_lines, child, 0, new_prefix + '/')


def xml2csv(xml_string):
    root = ET.fromstring(xml_string)
    prefix = ''
    # header line helps vim display csv (with csv plugin) and used by python cvs.DictReader()
    output_lines = ['zpath,resource-id,text,min_x,min_y,lim_x,lim_y\n']
    printall(output_lines, root, 0, prefix)
    return ''.join(output_lines)
