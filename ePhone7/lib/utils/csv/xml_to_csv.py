import os
import re
import xml.etree.ElementTree as ET
import six

import mtaf.android_zpath
from ePhone7.config.configure import cfg

tagre = re.compile('([^\[]+)(.*)')


def printall(ofile, node, tag_index, pfx):
    if node.tag == 'node':
        tag = node.attrib['class']
    else:
        tag = node.tag
    tag = mtaf.android_zpath.get_zpath_tag(tag)
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
                    items.append(repr(_str))
            except UnicodeEncodeError as e:
                six.print_(e.message)
        else:
            items.append('')
    ofile.write('%s\n' % ','.join(items))
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
            printall(ofile, child, tag_indices[child_tag], new_prefix + '/')
        else:
            printall(ofile, child, 0, new_prefix + '/')


def xml_to_csv(xml_file_path, csv_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    prefix = ''
    with open(csv_file_path, 'w') as output_file:
        # header line helps vim display csv (with csv plugin) and used by python cvs.DictReader()
        output_file.write('zpath,resource-id,text,min_x,min_y,lim_x,lim_y\n')
        printall(output_file, root, 0, prefix)


def visit(arg, dirname, names):
    # print "dirname = %s" % dirname
    # for name in names:
    #     print "  name = %s" % name
    # csv_dir = cfg.site.CsvFolder + '/csv' + re.sub(cfg.XmlFolder + '/xml', '', dirname)
    # print '"%s"' % cfg.site.CsvFolder + '/csv' + re.sub(cfg.XmlFolder + '/xml', '', dirname)
    subdir = re.sub(cfg.site.XmlFolder, '', dirname)
    six.print_("    subdir = %s" % subdir)
    sp = subdir.split('/xml')
    if len(sp) == 1:
        csv_dir = cfg.site.CsvFolder
    else:
        csv_dir = cfg.site.CsvFolder + '/csv' + sp[1]
    try:
        os.makedirs(csv_dir)
    except OSError as e:
        # ignore 'File exists' error but re-raise any others
        if e.errno != 17:
            raise e
    for name in names:
        if name[-4:] == '.xml':
            _xml_file_path = os.path.join(dirname, name)
            _csv_file_path = "csv".join(_xml_file_path.rsplit('xml', 3))
            # six.print_("calling xml_to_csv(%s, %s)" % (_xml_file_path, _csv_file_path))
            xml_to_csv(_xml_file_path, _csv_file_path)


def xml_folder_to_csv():
    os.path.walk(cfg.site.XmlFolder, visit, '')

if __name__ == '__main__':
    xml_folder_to_csv()
    # os.path.walk('ePhone7/lib/utils/xml/xml_appium_gui/', visit, '')