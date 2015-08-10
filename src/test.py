#!/usr/bin/env python
# -*- coding: utf-8 -*-

from printer import *
from saving import *
from coding import *
from credentials import *

from transformdata import *

import pprint

def test_printer():
	print '\n*** test_printer ***\n'
	printer_in_line('Primera frase')
	sleep(1)
	printer_in_line('Segunda frase muuuuy larga')
	sleep(1)
	printer_in_line('Tercera frase')
	sleep(1)
	printer_in_line('Ultima frase', newline = True)
	sleep(1)
	printer_in_line('Otra frase')

def test_coding_from_unicode_to_ascii():
	my_dict = {
		'name': u'Ingeniería de Telecomunicación',
		'value': '1990'
	}
	my_dict_list = []
	my_dict_list.append(my_dict)
	pprint.pprint(my_dict_list)
	from_unicode_to_ascii(my_dict_list)
	pprint.pprint(my_dict_list)

def test_logging_login():
	login()

def test_combinecsv():
	path_base = '2015-07-29'
	combinecsv(path_base)

def test_create_alumnianonimus():
	path_base = '2015-07-29'
	create_alumnianonimus(path_base)

test_create_alumnianonimus()