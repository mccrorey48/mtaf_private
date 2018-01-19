from time import sleep
from ePhone7.utils.get_softphone import get_softphone

if __name__ == '__main__':
    sp = get_softphone('DRS tester00', "DrsTestUsers")
    sleep(5)
    sp.unregister()
    sleep(1)
