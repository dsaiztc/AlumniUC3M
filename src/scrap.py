#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time

import printer

# Log to UC3M with credentials and return the session (or None if it couldn't connect)
def loguc3m(user, password):
	print 'Login UC3M... ',
	# Initiate session to maintain state (cookie)
	session = requests.Session()

	# Add User-Agent to prevent blocking from server
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
	response = session.get('https://portal.uc3m.es/portal/page/portal/inicio_privada', headers=headers)

	# Parse html
	soup = BeautifulSoup(response.text, 'html.parser')

	# Get formulary data
	data = {'v': None,
			'site2pstoretoken': None,
			'locale': None,
			'simulacion': None}
	inputs = soup.find_all('input')
	for tag in inputs:
		if 'name' in tag.attrs.keys():
			if tag.attrs['name'] in data.keys():
				data[tag.attrs['name']] = tag.attrs['value']
	data['ssousername'] = user
	data['password'] = password

	# Request login by POST
	response = session.post('https://sso.uc3m.es/sso/auth', data = data, headers=headers)
	if response.status_code == requests.codes.ok:
		print 'DONE'
		print_urlstatus(response)
		return session
	else:
		print 'ERROR'
		print_urlstatus(response)
		return None

# Print status code and the first 30 characters of a URL
def print_urlstatus(response):
	print '\tStatus Code: {}'.format(response.status_code)
	if len(response.url) > 30:
		print '\tURL: {}...'.format(response.url[:30])
	else:
		print '\tURL: {}'.format(response.url)

# Access Alumni directory and return a list of grades
def access_directory(session):
	print 'Accessing directory... ',
	# Access alumni directory
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, sdch',
				'Accept-Language': 'es,en;q=0.8',
				'Connection': 'keep-alive'}
	alumni_web = 'https://servicios.fund.uc3m.es/aa/antiguosalumnos/DirectorioPage.aspx'
	response = session.get(alumni_web, headers=headers)
	if response.status_code == requests.codes.ok and alumni_web == response.url:
		print 'DONE'
		print_urlstatus(response)

		grades = []
		soup = BeautifulSoup(response.text, 'html.parser')
		html_grades = soup.find(id='ctl00_ContentPlaceHolder1_dropTitulacion')
		for grade in html_grades.find_all('option'):
			grades.append({'value': grade['value'], 'name': grade.text})
	
		return grades
	else:
		print 'ERROR'
		print_urlstatus(response)
		print '\t     != ' + alumni_web
		return None

# Access first page of the directory
# Return form'session data so that we could iterate over pages (from 1 to N)
def get_first_page(session, titulacion):

	alumni_web = 'https://servicios.fund.uc3m.es/aa/antiguosalumnos/DirectorioPage.aspx'

	# Access alumni directory and get form's data
	response = session.get(alumni_web)
	soup = BeautifulSoup(response.text, 'html.parser')
	viewstate = soup.find(id='__VIEWSTATE')['value']
	eventvalidation = soup.find(id='__EVENTVALIDATION')['value']
	data = {'__EVENTTARGET': '',
			'__EVENTARGUMENT': '',
			'__EVENTVALIDATION': eventvalidation,
			'__VIEWSTATE': viewstate,
			'ctl00$ContentPlaceHolder1$DropTipoBusqueda': '1',
			'ctl00$ContentPlaceHolder1$txtPalabrasClave': '',
			'ctl00$ContentPlaceHolder1$dropAreasInteres': '- cualquiera -',
			'ctl00$ContentPlaceHolder1$txtNombre': '',
			'ctl00$ContentPlaceHolder1$dropPreferencias': '- cualquiera -',
			'ctl00$ContentPlaceHolder1$txtLocalidad': '',
			'ctl00$ContentPlaceHolder1$txtProvincia': '',
			'ctl00$ContentPlaceHolder1$dropTitulacion': titulacion,
			'ctl00$ContentPlaceHolder1$txtInicio': '',
			'ctl00$ContentPlaceHolder1$txtFin': '',
			'ctl00$ContentPlaceHolder1$txtEmprendedores': '',
			'ctl00$ContentPlaceHolder1$botonBuscar': 'Buscar'}

	# Search for specific grade (titulation)
	response = session.post(alumni_web, data=data)
	soup = BeautifulSoup(response.text, 'html.parser')
	viewstate = soup.find(id='__VIEWSTATE')['value']
	eventvalidation = soup.find(id='__EVENTVALIDATION')['value']
	data = {'ctl00$ContentPlaceHolder1$ScriptManager1': 'ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$gridBusqueda',
			'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gridBusqueda',
			'__EVENTARGUMENT': 'Page$2',
			'__EVENTVALIDATION': eventvalidation,
			'__VIEWSTATE': viewstate,
			'ctl00$ContentPlaceHolder1$DropTipoBusqueda': '1',
			'ctl00$ContentPlaceHolder1$txtPalabrasClave': '',
			'ctl00$ContentPlaceHolder1$dropAreasInteres': '- cualquiera -',
			'ctl00$ContentPlaceHolder1$txtNombre': '',
			'ctl00$ContentPlaceHolder1$dropPreferencias': '- cualquiera -',
			'ctl00$ContentPlaceHolder1$txtLocalidad': '',
			'ctl00$ContentPlaceHolder1$txtProvincia': '',
			'ctl00$ContentPlaceHolder1$dropTitulacion': titulacion,
			'ctl00$ContentPlaceHolder1$txtInicio': '',
			'ctl00$ContentPlaceHolder1$txtFin': '',
			'ctl00$ContentPlaceHolder1$txtEmprendedores': ''}

	# Search for the second page for a specific grade (titulation) so that we could iterate over pages later (form 1 to N)
	response = session.post( alumni_web, data=data)
	soup = BeautifulSoup(response.text, 'html.parser')
	update_data(soup, data)

	return data

# Update form's data while iterating over pages of the same grade (titulacion)
def update_data(soup, data):
	try:
		data['__VIEWSTATE'] = soup.find(id='__VIEWSTATE')['value']
		data['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION')['value']
	except:
		pass

# Iterate over pages (1 to N) to get all the alumni
# Return a list of alumni
def interate_pages(session, data, limit = 5000):

	print '\tIterating over pages... '

	alumni = []
	for i in xrange(1, limit):
		alumni_page = []
		data['__EVENTARGUMENT'] = 'Page$' + str(i)
		response = session.post('https://servicios.fund.uc3m.es/aa/antiguosalumnos/DirectorioPage.aspx', data=data)
		printer.printer_in_line('\tPage: {} StatusCode: {}'.format(i, response.status_code))
		soup = BeautifulSoup(response.text, 'html.parser')
		update_data(soup, data)
		alumni_page = find_alumns_page(soup)
		if len(alumni_page) == 0:
			break
		else:
			alumni.extend(alumni_page)
		time.sleep(1)

	return alumni

# Get list of alumns within a specific page
def find_alumns_page(soup_page):
	alumns_page = []
	table = soup_page.find('table', id='ctl00_ContentPlaceHolder1_gridBusqueda')
	try:
		items = table.find_all('tr')
		for item in items:
			try:
				if (item['class'][0] == 'item' or item['class'][0] == 'altItem'):
					alumn = {}
					name_elements = item.find_all('a')
					for name_element in name_elements:
						if ('enlaceNombre' in name_element['id']):
							alumn['name'] = name_element.text
					degree_elements = item.find_all('span')
					for degree_element in degree_elements:
						if 'labelTitulacion' in degree_element['id']:
							all_string = degree_element.text.split('(')
							if len(all_string) == 2:
								# There is not tag
								alumn['degree'] = all_string[0].strip().strip(')')
								alumn['tag'] = '-'
								years = all_string[1].split('-')
								alumn['year_start'] = years[0].strip().strip(')')
								alumn['year_fin'] = years[1].strip().strip(')')
							elif len(all_string) == 3:
								# There is tag
								alumn['degree'] = all_string[0].strip().strip(')')
								alumn['tag'] = all_string[1].strip().strip(')')
								years = all_string[2].split('-')
								alumn['year_start'] = years[0].strip().strip(')')
								alumn['year_fin'] = years[1].strip().strip(')')
					alumns_page.append(alumn)
			except Exception, e:
				# The <tr> item hasn't got any class attribute
				#print 'Something was wrong: {}'.format(repr(e))
				continue
	except Exception, e:
		printer.printer_in_line('\tPage limit reached')
		pass
	return alumns_page