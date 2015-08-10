#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import csv

# root_folder =  '../data/' + datetime.now().strftime('%Y-%m-%d') + '/'

# Save alumni in csv file for a grade within the '../data/YYYY-MM-DD/alumni/' folder
def alumni_to_csv(alumns, grade):
	filename = '../data/' + datetime.now().strftime('%Y-%m-%d') + '/' + 'alumni/' + grade + '.csv'
	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))
	with open(filename, 'wb') as wf:
		fieldnames = ['name', 'degree', 'tag', 'year_start', 'year_fin']
		writer = csv.DictWriter(wf, fieldnames=fieldnames)
		writer.writeheader()
		for alumn in alumns:
			writer.writerow(alumn)

# Save grade names and values in a csv within the '../data/YYYY-MM-DD/' folder
def grades_to_csv(grades, name):
	filename = '../data/' + datetime.now().strftime('%Y-%m-%d') + '/' + name + '.csv'
	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))
	with open(filename, 'wb') as wf:
		fieldnames = ['name', 'value']
		writer = csv.DictWriter(wf, fieldnames=fieldnames)
		writer.writeheader()
		for grade in grades:
			writer.writerow(grade)

# Check if a grade (titulacion) is already saved
def is_grade_already_saved(grade):
	filename = '../data/' + datetime.now().strftime('%Y-%m-%d') + '/' + 'alumni/' + grade + '.csv'
	return os.path.exists(filename)