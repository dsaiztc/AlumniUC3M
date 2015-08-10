#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdout

def printer_in_line(text, newline = False):
	stdout.write('\r                                                  ')
	stdout.write('\r' + text)
	stdout.flush()
	if newline:
		stdout.write('\n')