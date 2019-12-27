#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--key")
parser.add_argument("--msg")

args = parser.parse_args()
key = args.key
msg = args.msg
ret = ""

for c in msg:
    ret += chr(ord(key)^ord(c))

print(ret)

if 'b' in ret or 'i' in ret or 'c' in ret or '/' in ret or ' ' in ret or 'f' in ret or 'n' in ret or 's' in ret:
    print("BADCHARS!")

