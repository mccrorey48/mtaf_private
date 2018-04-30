from pkg_resources import Requirement, resource_filename
import six
import os
import sys

six.print_("[resource_filename method] %s" % resource_filename(Requirement.parse("mtaf"), "wav"))
six.print_("[sys.prefix method       ] %s" % os.path.join(sys.prefix, 'mtaf', 'wav'))

