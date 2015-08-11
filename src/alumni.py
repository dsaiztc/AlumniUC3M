#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import credentials
import saving
import coding
import printer

import scrap

# Screen scraping of the Alumni database: all grades (titulaciones)
def all():
	user, password = credentials.login()
	session = scrap.loguc3m(user, password)

	if session is None:
		return

	grades = scrap.access_directory(session=session)

	if grades is None:
		return

	coding.from_unicode_to_ascii(grades)
	saving.grades_to_csv(grades, 'degree_names')

	iterate_over_grades(grades, session)

# Screen scraping of the Alumni database: Engineering grades (titulaciones)
def engineering():

	user, password = credentials.login()
	session = scrap.loguc3m(user, password)

	if session is None:
		return

	grades = scrap.access_directory(session=session)

	if grades is None:
		return

	coding.from_unicode_to_ascii(grades)

	eng_grades = []
	for grade in grades:
		if 'Ingenieria' in grade['name']:
			eng_grades.append(grade)

	saving.grades_to_csv(eng_grades, 'degree_names_engineering')

	iterate_over_grades(eng_grades, session)

# Iterate over a list of grades
# grades is a list of dictionaries, each one of them corresponding to a grade with the following form:
# 	{ 'name': 'grade_name', 'value': 'grade_value' }
# For each grade a CSV file will be created with the alumni data within the '../data/YYYY-MM-DD/alumni/' folder
def iterate_over_grades(grades, session):
	num_grades = str(len(grades))
	i = 0
	for grade in grades:
		i += 1
		alumns = []
		print 'Degree ({}): {}'.format(str(i) + '/' + num_grades, grade['name'])
		if saving.is_grade_already_saved(grade['value']):
			printer.printer_in_line('\tGrade already saved', newline = True)
			continue
		time.sleep(1)
		data = scrap.get_first_page(session=session, titulacion=grade['value'])
		alumns.extend(scrap.interate_pages(session=session, data=data))
		if len(alumns) == 0:
			printer.printer_in_line('\tEmpty directory', newline = True)
			continue
		printer.printer_in_line('\tTotal alumns: {}'.format(len(alumns)), newline = True)

		coding.from_unicode_to_ascii(alumns)
		saving.alumni_to_csv(alumns, grade['value'])