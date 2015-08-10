#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv

import pprint

path_base = '../data/'

# Combine CSV files for individual grades (titulaciones) in a CSV file within the '../data/YYYY-MM-DD/' for path_date='YYYY-MM-DD'
def combinecsv(path_date):

	path_alumni = path_base + '/' + path_date + '/' + 'alumni/'
	csv_alumni_list = os.listdir(path_alumni)

	with open(path_base + '/' + path_date + '/' + 'alumni.csv', 'wb') as csv_file_w:
		writer = csv.DictWriter(csv_file_w, fieldnames = ['name', 'degree', 'tag', 'year_start', 'year_fin'])
		writer.writeheader()
		for csv_alumni in csv_alumni_list:
			with open(path_alumni + csv_alumni) as csv_file_r:
				reader = csv.DictReader(csv_file_r)
				for row in reader:
					writer.writerow(row)
			
# Create CSV file without names for path_date='YYYY-MM-DD'
def create_alumnianonymous(path_date):

	with open(path_base + '/' + path_date + '/' + 'alumni_anonymous.csv', 'wb') as csv_file_w:
		writer = csv.DictWriter(csv_file_w, fieldnames = ['degree', 'tag', 'year_start', 'year_fin'])
		writer.writeheader()
		with open(path_base + '/' + path_date + '/' + 'alumni.csv') as csv_file_r:
				reader = csv.DictReader(csv_file_r)
				for row in reader:
					row.pop('name', None)
					writer.writerow(row)

def clean(path_date):
	with open(path_base + '/' + path_date + '/' + 'alumni_anonymous_clean.csv', 'wb') as csv_file_w:
		writer = csv.DictWriter(csv_file_w, fieldnames = ['degree', 'tag', 'year_start', 'year_fin'])
		writer.writeheader()
		with open(path_base + '/' + path_date + '/' + 'alumni_anonymous.csv') as csv_file_r:
				reader = csv.DictReader(csv_file_r)
				for row in reader:
					if row['degree'] == '' or not 'Ingenieria' in row['degree']:
						continue
					if row['year_start'] == '0':
						continue
					if row['year_fin'] == '1':
						continue
					if row['year_start'] > row['year_fin']:
						continue
					writer.writerow(row)

path_date = '2015-07-29'
combinecsv(path_date)
create_alumnianonymous(path_date)
clean(path_date)