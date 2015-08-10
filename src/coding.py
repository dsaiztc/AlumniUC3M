#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unidecode import unidecode
import warnings

# Catch warnings as errors 
# http://stackoverflow.com/questions/5644836/in-python-how-does-one-catch-warnings-as-if-they-were-exceptions
warnings.filterwarnings("error")

# Create a copy of a dictionary with unicode characters translated to ascii
def from_unicode_to_ascii(my_dict_list):
	for elem in my_dict_list:
		for key in elem:
			try:
				elem[key] = unidecode(elem[key])
			except RuntimeWarning:
				pass