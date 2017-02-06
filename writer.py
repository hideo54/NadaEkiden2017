import json
import sys
import hashlib, binascii
import nfc, nfc.ndef

def connected(tag):
    num = str(sys.argv[1])
    salt = ''
    with open('salt.txt') as f:
        salt = f.read().rstrip('\n')
    dk = hashlib.pbkdf2_hmac('sha256', num, salt, 114514)
    key = binascii.hexlify(dk)
    data = { 'id': num, 'key': key }
    record = nfc.ndef.TextRecord(str(json.dumps(data)))
    tag.ndef.message = nfc.ndef.Message(record)
    print tag.ndef.message.pretty()

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})