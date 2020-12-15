#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
"""utilities"""

# for passwords
import base64

# for two factor
import pyotp

# for current dir
import os 

# encode in 64
def encode64(string_to_encode):
    in_bytes = string_to_encode.encode('ascii')
    base64_bytes = base64.b64encode(in_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

# decode in 64
def decode64(string_to_decode):
    base64_bytes = string_to_decode.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message

# read [dir_to_read] file [lines_to_read] lines
def read_file(dir_to_read, lines_to_read=2):

    data = []
    _file = open(dir_to_read, 'r')
    for _ in range(lines_to_read):
        line = _file.readline().strip('\n')
        data.append(line)
    
    if lines_to_read == 1:
        return "".join(data)
    else:
        return data

def current_dir():
    return os.getcwd()

def generate_pyOTPcode():
    
    #get base32secret
    secret = read_file(
        current_dir() + '/two-factor-auth.key',
        lines_to_read=1
    )

    totp = pyotp.TOTP(decode64(secret))        
    code = totp.now()

    while not totp.verify(code):
        code = totp.now()

    return code 

