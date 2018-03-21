from lib.microservices import Microservices
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("login", type=str, help="<phone number>@<domain>")
parser.add_argument('password', help='password')
args = parser.parse_args()

print "login = %s" % args.login
print "password = %s" % args.password
# URL is 10.3.1.5 for svlab, pro.esiapi.io for production
ms = Microservices(args.login, args.password, 'http://10.3.1.5/')
for cat in 'new', 'saved', 'deleted':
    print "%s %s" % (cat, ms.get_vm_count(cat))
