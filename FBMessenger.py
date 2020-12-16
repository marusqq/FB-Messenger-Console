#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
"""Messenger Class"""

# for error fixing
import re

# for playing alarm when message comes
from playsound import playsound

# utilities
import utilities as ut

# fb chat
import fbchat
from fbchat.models import *

# for chat colors
from colorama import Fore, Back, Style, init

init(autoreset=True)


# class SendClient(fbchat.Client):
# TODO send client


class ListenClient(fbchat.Client):
    def onLoggedIn(self, email):
        self.thread_information, self.author_information = self.load_info()
        ut.clear_screen()

    def on2FACode(self):
        return ut.generate_pyOTPcode()

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):

        self.download_queue = []
        self.void_message()

        # Message is instantly delivered, but not read hihihi
        self.markAsDelivered(thread_id, message_object.uid)
        # self.markAsRead(thread_id)

        # Playsound if someone sent me a message
        if author_id != self.uid:
            playsound(ut.current_dir() + "/data/message.wav")

        # Add time
        self.add_to_message(ut.get_time(), after_add_message=" ")

        # Get the real name of dict
        real_thread = self.get_thread_name(thread_id)
        self.add_to_message(real_thread, before_add_message="[", after_add_message="] ")

        # Add the author's name
        real_author = self.get_real_name(author_id)
        self.add_to_message(real_author, after_add_message=": ")

        # Read all the message_object now
        self.add_to_message(self.fix_message_object_data(message_object, thread_id))

        print(self.message)
        self.ask_for_downloads()

        return

    def onReactionAdded(
        self, mid, reaction, author_id, thread_id, thread_type, ts, msg, **kwargs
    ):
        """TODO add persons name"""
        real_author = self.get_real_name(author_id)
        real_thread = self.get_thread_name(thread_id)

        print(msg)

        print(
            "{} reacted to message {} with {} in {} ({})".format(
                author_id, mid, reaction.name, thread_id, thread_type.name
            )
        )

        return

    def onReactionRemoved(
        self, mid, reaction, author_id, thread_id, thread_type, ts, msg, **kwargs
    ):
        """TODO add persons name"""

        print(
            "{} removed reaction from {} message in {} ({})".format(
                author_id, mid, thread_id, thread_type
            )
        )

    def onMessageSeen(
        self, seen_by, thread_id, thread_type, seen_ts, ts, metadata, msg, **kwargs
    ):
        """override to remove printing functionality"""
        return

    def onMessageDelivered(
        self,
        msg_ids,
        delivered_for,
        thread_id,
        thread_type,
        ts,
        metadata,
        msg,
        **kwargs
    ):
        """override to remove printing functionality"""
        return

    def onMarkedSeen(self, threads, seen_ts, ts, metadata, msg):
        """override to remove printing functionality"""
        return

    ### Custom functions:
    def void_message(self):
        self.message = ""
        return

    def add_to_message(
        self, add_message, before_add_message=None, after_add_message=None
    ):

        if before_add_message:
            self.message += before_add_message

        self.message += add_message

        if after_add_message:
            self.message += after_add_message

        return

    def load_info(self):
        return ut.read_json(ut.current_dir() + "/data/thread_data.json"), ut.read_json(
            ut.current_dir() + "/data/author_data.json"
        )

    def get_real_name(self, _id):

        if _id == self.uid:
            return "Me"

        elif _id in self.author_information:
            return self.author_information[_id]

        else:
            return str(_id)

    def get_thread_name(self, _id):

        if _id in self.thread_information:
            return self.thread_information[_id]

        else:
            return str(_id)

    def fix_message_object_data(self, message_obj, thread_id):
        # Things we need to get out of message:
        #       - Text                                              +
        #       - Does it reply to anyone?                          +
        #       - Is there a photo/video attached?
        #               If so ask if want to download or maybe open
        #       - Is there a file attached?
        #               If so ask if want to download

        message = ""

        # first, check text
        if message_obj.text:
            message = message + message_obj.text + " "

        # then check attachments
        if message_obj.attachments:
            message = message + "<Attachments: "
            for attachment in message_obj.attachments:
                attachment_info = ""
                print(attachment)

                if type(attachment).__name__ == "ImageAttachment":
                    attachment_info = (
                        attachment_info
                        + "image["
                        + attachment.uid
                        + "."
                        + attachment.original_extension
                        + "]"
                    )

                    self.download_queue.append(attachment)

                # add informatio about every attachment
                message = message + attachment_info

            # close attachments
            message = message + ">"

        # check for replies
        if message_obj.replied_to:

            replied_message = message_obj.replied_to

            if replied_message:

                message = (
                    message
                    + "( Reply To - "
                    + self.get_real_name(replied_message.author)
                    + ": "
                    + replied_message.text
                    + ")"
                )

        return message

    def ask_for_downloads(self):

        if len(self.download_queue):
            for download in self.download_queue:
                if type(download).__name__ == "ImageAttachment":
                    action = input(
                        Fore.BLUE
                        + "Do you want to download / open / ignore image "
                        + download.uid
                        + "."
                        + download.original_extension
                        + "?"
                        + " (d/o/i* - * for default)\n"
                    )

                    if action.lower() == "d":
                        print(
                            Fore.BLUE
                            + "Downloading "
                            + download.uid
                            + "."
                            + download.original_extension
                        )

                        ut.download_image("test", "test")

                    elif action.lower() == "o":
                        print(
                            Fore.BLUE
                            + "Opening"
                            + download.uid
                            + "."
                            + download.original_extension
                        )

                        ut.open_image("test", "test")

                    elif action.lower() == "" or action.lower() == "i":
                        print(Fore.BLUE + "Ignoring")

        return


class SendClient(fbchat.Client):
    def onLoggedIn(self, email):
        ut.clear_screen()

    # Overridden functions
    def on2FACode(self):
        return ut.generate_pyOTPcode()

    def onReactionAdded(
        self, mid, reaction, author_id, thread_id, thread_type, ts, msg, **kwargs
    ):
        """override to remove printing functionality"""
        return

    def onReactionRemoved(
        self, mid, reaction, author_id, thread_id, thread_type, ts, msg, **kwargs
    ):
        """override to remove printing functionality"""
        return

    def onMessageSeen(
        self, seen_by, thread_id, thread_type, seen_ts, ts, metadata, msg, **kwargs
    ):
        """override to remove printing functionality"""
        return

    def onMessageDelivered(
        self,
        msg_ids,
        delivered_for,
        thread_id,
        thread_type,
        ts,
        metadata,
        msg,
        **kwargs
    ):
        """override to remove printing functionality"""
        return

    def onMarkedSeen(self, threads, seen_ts, ts, metadata, msg):
        """override to remove printing functionality"""
        return

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        """override to remove printing functionality"""
        return

    # Custom functions
    def get_threads(self):
        return

    def load_threads(self):
        unsorted_threads = ut.read_json(ut.current_dir() + "/data/thread_data.json")
        thread_count = 0
        self.threads = []

        for key, value in unsorted_threads.items():
            single_thread = []
            single_thread.append(thread_count)
            single_thread.append(key)
            single_thread.append(value)
            self.threads.append(single_thread)

            thread_count += 1

        # self.threads = sorted_threads


class FBMessenger:
    def __init__(self, listen=True):
        logins = ut.read_file(ut.current_dir() + "/keys/fb-details.key")
        login = logins[0]
        password = ut.decode64(ut.decode64(logins[1]))

        self.fix_api_errors()
        if listen:
            self.client = ListenClient(login, password, max_tries=3)
        else:
            self.client = SendClient(login, password, max_tries=3)

    def listen(self):
        self.client.listen()
        return

    def fix_api_errors(self):
        ### see https://github.com/fbchat-dev/fbchat/issues/615#issuecomment-710127001
        fbchat._util.USER_AGENTS = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        ]
        fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')
