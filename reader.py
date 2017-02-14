import json
import datetime
import sys, time
import hashlib, binascii
import nfc, nfc.ndef
import atexit

SUCCESS = '\033[32mSUCCESS\033[0m'
WARNING = '\033[35mWARNING\033[0m'
CRITICAL = '\033[37m\033[41mCRITICAL\033[0m'

def output(code, id, date, message=None):
    if code == 0:
        print '%s[%s] %s' % (SUCCESS, id, date)
    elif code == 1:
        print '%s[%s] %s (Falsification detected)' % (WARNING, id, date)
    else:
        print '%s %s' % (CRITICAL, message)

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())

def connected(tag):
    try:
        now_str = str(datetime.datetime.now())
        data_raw = tag.ndef.message[0].data.lstrip('\x02en')
        data = json.loads(data_raw, object_hook=ascii_encode_dict)

        salt = ''
        with open('salt.txt') as f:
            salt = f.read().rstrip('\n')
        dk = hashlib.pbkdf2_hmac('sha256', data['id'], salt, 810)
        true_key = binascii.hexlify(dk)

        if data['key'] == true_key:
            output(0, data['id'], now_str)
        else:
            output(1, data['id'], now_str)
    except KeyboardInterrupt:
        clf.close()
        print 'Bye'
        sys.exit()
    except:
        output(2, 0, '', 'Unknown error occurred')
        sys.exit()

print 'Initializing...'

try:
    clf = nfc.ContactlessFrontend('usb')
    atexit.register(lambda: clf.close())
except IOError:
    output(2, 0, '', 'Device busy or not connected')
    sys.exit()
except:
    output(2, 0, '', 'Unknown error occurred')
    sys.exit()

print 'Initialized.'

exception = False

while True:
    try:
        clf.connect(rdwr={'on-connect': connected})
        time.sleep(0.5)
    except KeyboardInterrupt:
        clf.close()
        print 'Bye'
        sys.exit()
