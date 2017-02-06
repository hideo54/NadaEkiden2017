import json
import datetime
import sys
import hashlib, binascii
import nfc, nfc.ndef

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())

def connected(tag):
    now_str = str(datetime.datetime.now())
    data_raw = tag.ndef.message[0].data.lstrip('\x02en')
    data = json.loads(data_raw, object_hook=ascii_encode_dict)
    print data

    salt = ''
    with open('salt.txt') as f:
        salt = f.read().rstrip('\n')
    dk = hashlib.pbkdf2_hmac('sha256', data['id'], salt, 114514)
    true_key = binascii.hexlify(dk)
    print true_key

    if data['key'] == true_key:
        print now_str
    else:
        print 'Invalid'

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
