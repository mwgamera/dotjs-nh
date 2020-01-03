#!/usr/bin/python3
import os
import sys
import struct
import json

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    str = unicode

stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

def dotjs(host, ext='.js', path=None):
    if path is None:
        path = os.path.expanduser(os.path.join('~', ext))
    host = host.rstrip('.')
    files = []
    while True:
        files.append(host)
        try:
            _, host = host.split('.', 1)
        except ValueError:
            break
    files.append('default')
    data = []
    for fn in files[::-1]:
        try:
            if os.path.sep in fn:
                continue
            with open(os.path.join(path, fn+ext)) as f:
                data.append(f.read())
        except IOError:
            pass
    return data

while True:
    tag = stdin.read(4)
    if not tag:
        break
    length = struct.unpack('=L', tag)[0]
    req = json.loads(stdin.read(length).decode('UTF-8'))
    res = []
    try:
        req = urlparse(req).hostname
        if req:
            res = [
                dotjs(req, '.js'),
                dotjs(req, '.css'),
            ]
    except Exception as e:
        sys.stderr.write(str(e)+'\n')
    res = json.dumps(res).encode('UTF-8')
    stdout.write(struct.pack('=L', len(res)) + res)

