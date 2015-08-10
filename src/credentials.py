#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getpass

def login():
	user = raw_input("User: ")
	password = getpass.getpass()

	return user, password