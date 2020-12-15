#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
"""Messenger Class"""

# for error fixing
import re

# utilities
import utilities as ut

# fb chat
import fbchat
from fbchat.models import *


class CustomClient(fbchat.Client):
    def on2FACode(self):
        return ut.generate_pyOTPcode()

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        fbchat.log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        # If you're not the author, echo
        if author_id == self.uid:
            self.send(message_object, thread_id=thread_id, thread_type=thread_type)

class FBMessengerListener:
    def __init__(self):
        logins = ut.read_file(ut.current_dir() + '/fb-details.key')
        login = logins[0]
        password = ut.decode64(ut.decode64(logins[1]))
        
        self.fix_api_errors()
        self.client = CustomClient(login, password, max_tries = 3)

    def listen(self):
        self.client.listen()
        return

    def fix_api_errors(self):
        ### see https://github.com/fbchat-dev/fbchat/issues/615#issuecomment-710127001 
        fbchat._util.USER_AGENTS    = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
        fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')
    
class FBMessengerWriter:
    def __init__(self):
        logins = ut.read_file(ut.current_dir() + '/fb-details.key')
        login = logins[0]
        password = ut.decode64(ut.decode64(logins[1]))
        
        self.fix_api_errors()
        self.client = CustomClient(login, password, max_tries = 3)

    def fix_api_errors(self):
        ### see https://github.com/fbchat-dev/fbchat/issues/615#issuecomment-710127001 
        fbchat._util.USER_AGENTS    = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
        fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')