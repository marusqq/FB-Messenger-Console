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

# for json reading
import json

# for screen cleaning
import sys

# for time
import datetime

# for file downloading
import urllib.request

# possible colors from colorama
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

# encode in 64
def encode64(string_to_encode):
    in_bytes = string_to_encode.encode("ascii")
    base64_bytes = base64.b64encode(in_bytes)
    base64_message = base64_bytes.decode("ascii")
    return base64_message


# decode in 64
def decode64(string_to_decode):
    base64_bytes = string_to_decode.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode("ascii")
    return message


# read [dir_to_read] file [lines_to_read] lines
def read_file(dir_to_read, lines_to_read=2):

    data = []
    _file = open(dir_to_read, "r")
    for _ in range(lines_to_read):
        line = _file.readline().strip("\n")
        data.append(line)

    if lines_to_read == 1:
        return "".join(data)
    else:
        return data


def current_dir():
    return os.getcwd()


def generate_pyOTPcode():
    # get base32secret
    secret = read_file(current_dir() + "/keys/two-factor-auth.key", lines_to_read=1)

    totp = pyotp.TOTP(decode64(secret))
    code = totp.now()

    while not totp.verify(code):
        code = totp.now()

    return code


def read_json(dir_to_json):
    with open(dir_to_json) as f:
        data = json.load(f)
    return data


def clear_screen():
    sys.stderr.write("\x1b[2J\x1b[H")


def get_time():
    now = datetime.datetime.now()
    hours_str = str(now.hour)
    minutes_str = str(now.minute)
    seconds_str = str(now.second)

    if len(hours_str) == 1:
        hours_str = "0" + hours_str

    if len(minutes_str) == 1:
        minutes_str = "0" + minutes_str

    if len(seconds_str) == 1:
        seconds_str = "0" + seconds_str

    time = hours_str + ":" + minutes_str + ":" + seconds_str
    return time


def download_file(url, filename):
    save_location = current_dir + "/downloads/" + filename
    urllib.request.urlretrieve(url, save_location)
    return save_location


def download_image(url, filename):
    return


def open_image(url, filename):
    return
