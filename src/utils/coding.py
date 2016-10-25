# -*- coding: utf-8 -*-

from unidecode import unidecode


# Create a copy of a dictionary with unicode characters translated to ascii
def convert_dict_list_to_ascii(dict_list):
	converted_dict_list = []
	for elem in dict_list:
		new_dict = {}
		for key in elem:
			try:
				new_dict[key] = unidecode(elem[key])
			except:
				continue
		converted_dict_list.append(new_dict)
	return converted_dict_list
