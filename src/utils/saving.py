# -*- coding: utf-8 -*-

import os
from datetime import datetime
import csv


DATE_FORMAT = '%Y-%m-%d'


# root_folder =  '../data/' + datetime.now().strftime(DATE_FORMAT) + '/'


# Save alumni in csv file for a grade within the '../data/YYYY-MM-DD/alumni/' folder
def save_alumni_to_csv(alumns, grade):
	filename = '../data/' + datetime.now().strftime(DATE_FORMAT) + '/' + 'alumni/' + grade + '.csv'
	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))
	with open(filename, 'wb') as wf:
		fieldnames = ['name', 'degree', 'tag', 'year_start', 'year_fin']
		writer = csv.DictWriter(wf, fieldnames=fieldnames)
		writer.writeheader()
		for alumn in alumns:
			writer.writerow(alumn)


# Save grade names and values in a csv within the '../data/YYYY-MM-DD/' folder
def save_grades_to_csv(grades, name):
	filename = '../data/' + datetime.now().strftime(DATE_FORMAT) + '/' + name
	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))
	with open(filename, 'wb') as wf:
		fieldnames = grades[0].keys()
		writer = csv.DictWriter(wf, fieldnames=fieldnames)
		writer.writeheader()
		for grade in grades:
			writer.writerow(grade)


# Check if a grade (titulacion) is already saved
def alumni_from_grade_is_already_saved(grade, updated_last_days):

	result = False

	saved_dates = []
	directory_paths = [x[0] for x in os.walk('../data/')]
	for directory_path in directory_paths:
		path_split = directory_path.split('/')
		if len(path_split) >= 3:
			date_str = path_split[2]
			filename = '../data/' + date_str + '/' + 'alumni/' + grade + '.csv'
			if os.path.exists(filename):
				date = datetime.strptime(date_str, DATE_FORMAT)
				saved_dates.append(date)

	if saved_dates:
		last_date = saved_dates[0]
		for saved_date in saved_dates:
			if saved_date < last_date:
				last_date = saved_date
		result = (datetime.utcnow() - last_date).days <= updated_last_days

	return result
