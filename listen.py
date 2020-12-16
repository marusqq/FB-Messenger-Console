#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
"""Messenger Input"""

from FBMessenger import FBMessenger

messenger = FBMessenger(listen=True)

# just listen and print out what we get
messenger.listen()
