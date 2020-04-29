#!/usr/bin/env python
import argparse
import base64
import sys

PREFIX = "http://gtb.baidu.com/HttpService/get?p="
PATTERN = "type=image/jpeg&n=vis&t=adimg&c=tb:ig&r="

def gen_url_from_csid(csid):
    url = base64.b64encode( PATTERN + csid)
    return PREFIX + url

def get_csid_from_url(url):
    if url[0:len(PREFIX)] != PREFIX:
        print "Error: invalid url fromat: prefix incorrect"
    encoded = url[len(PREFIX):]
    decoded = base64.b64decode(encoded)
    if PATTERN not in decoded:
        print "Error: invalid url format: encoded part not correct"
    return decoded[len(PATTERN):]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='convert between gtb image url and csid.')
    parser.add_argument('--csid', type=str, help='the image csid')
    parser.add_argument('--url', type=str, help='the imageu url')
    args = parser.parse_args()
    if args.csid:
        url = gen_url_from_csid(args.csid)
        print url
    if args.url:
        csid = get_csid_from_url(args.url)
        print csid
    if len(sys.argv) <= 1:
        print "no arguments provided. try: %s --help" % sys.argv[0]
