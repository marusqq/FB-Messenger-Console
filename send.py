#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
"""Messenger Output"""

SHOW_ALL_THREADS = "!chats"
JOIN_CHAT = "!join"
QUIT_CHAT = "!leave"
CLEAR_SCREEN = "!clear"


from FBMessenger import FBMessenger

messenger = FBMessenger(listen=False)


def get_threads():
    return


def controller(text):

    text_split = text.split(" ")

    if text == SHOW_ALL_THREADS:
        for thread in messenger.client.threads:
            print(str(thread[0]) + ": " + thread[2])

    elif len(text_split) == 2 and text_split[0] == JOIN_CHAT:

        thread_join = False
        for thread in messenger.client.threads:
            if str(text_split[1]) == str(thread[0]):
                thread_join = True
                thread_join_name = thread[2]
                thread_join_id = thread[1]

        if thread_join:
            join_thread(thread_id=thread_join_id, real_thread_name=thread_join_name)
        else:
            print("No chat", text_split[1], "found")

        return

    elif text == CLEAR_SCREEN:
        # clear the screen
        messenger.client.onLoggedIn("dummy")


def join_thread(thread_id, real_thread_name):
    # print(thread_id, "joined")
    message = ""
    print("Connected to", real_thread_name)
    while True:

        message = input()
        if message == QUIT_CHAT:
            return
        messenger.client.sendMessage(message=message, thread_id=thread_id)


# start sending messages

# workflow:
#   lock onto thread id
#   change threads somehow
#   accept all messages and send them
chatroom = ""

messenger.client.load_threads()

while True:
    text = input()
    controller(text)
