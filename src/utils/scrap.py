# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
import random

import logging
#logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('\033[93m%(asctime)s\033[0m:\033[94m%(name)s\033[0m:\033[92m%(levelname)s\033[0m:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
alumni_url = 'https://servicios.fund.uc3m.es/aa/antiguosalumnos/DirectorioPage.aspx'


def login_into_uc3m(session, user, password):

	login_url = 'https://portal.uc3m.es/portal/page/portal/inicio_privada'
	logger.info('Accessing to {}'.format(login_url))
	response = session.get(login_url, headers=headers)
	if response.history:
		logger.debug('Request redirected')
		for resp in response.history:
			logger.debug('{} {}'.format(resp.status_code, resp.url))
	logger.info('{} {}'.format(response.status_code, response.url))

	soup = BeautifulSoup(response.text, 'html.parser')

	payload = {}
	input_tags = soup.find_all('input')
	for input_tag in input_tags:
		name = input_tag.attrs.get('name')
		value = input_tag.attrs.get('value')
		if name:
			payload[name] = value
	payload['ssousername'] = user
	payload['password'] = password
	login_post_headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en,es;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Content-Length': '550',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
	}
	login_post_url = 'https://sso.uc3m.es/sso/auth'
	logger.info('Submitting credentials to {}'.format(login_post_url))
	response = session.post(login_post_url, data=payload, headers=login_post_headers)
	if response.history:
		logger.debug('Request redirected')
		for resp in response.history:
			logger.debug('{} {}'.format(resp.status_code, resp.url))
	logger.info('{} {}'.format(response.status_code, response.url))


def get_list_of_grades_from_directory(session):
	"""Navigates into the Alumni directory webpage and retrieves a list of the different grades available

	Args:
		session: Persistent session with logged-user cookie

	Returns:
		list: List of dictionaries with the following structure:
			{
				'name': [Name of the grade],
				'code': [Unique code that identifies the degree]
			}
	"""
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch, br',
		'Accept-Language': 'en,es;q=0.8',
		'Connection': 'keep-alive',
		'Host': 'servicios.fund.uc3m.es',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	}
	logger.info('Trying to access {}'.format(alumni_url))
	response = session.get(alumni_url, headers=headers, verify=False)
	if response.history:
		logger.debug('Request redirected')
		for resp in response.history:
			logger.debug('{} {}'.format(resp.status_code, resp.url))
	logger.info('{} {}'.format(response.status_code, response.url))

	grades = []
	soup = BeautifulSoup(response.text, 'html.parser')
	html_grades = soup.find(id='ctl00_ContentPlaceHolder1_dropTitulacion')
	for grade in html_grades.find_all('option'):
		if grade['value'] != '- cualquiera -':
			grades.append({'code': grade['value'], 'name': grade.text})

	return grades


def prepare_grade_for_iteration(session, grade_code):
	"""Search for a specific grade page and navigate to page 2

	Every navigation needs a __EVENTVALIDATION and __EVENTARGUMENT comming from thre previous navigation. In order to
	iterate over all the pages (form 1 to N) we need to 'initialize' those variables.

	To do so, we search for the first page and then navigate to the second page. This would allow us start iterating
	from the first page and on.

	Returns:
		payload: Necessary payload for the following requests
	"""

	response = session.get(alumni_url)

	soup = BeautifulSoup(response.text, 'html.parser')
	eventvalidation = soup.find(id='__EVENTVALIDATION')['value'] if soup.find(id='__EVENTVALIDATION') else ''
	viewstate = soup.find(id='__VIEWSTATE')['value'] if soup.find(id='__VIEWSTATE') else ''

	basic_payload = {
		'__EVENTTARGET': '',
		'__EVENTARGUMENT': '',
		'ctl00$ContentPlaceHolder1$DropTipoBusqueda': '1',
		'ctl00$ContentPlaceHolder1$txtPalabrasClave': '',
		'ctl00$ContentPlaceHolder1$dropAreasInteres': '- cualquiera -',
		'ctl00$ContentPlaceHolder1$txtNombre': '',
		'ctl00$ContentPlaceHolder1$dropPreferencias': '- cualquiera -',
		'ctl00$ContentPlaceHolder1$txtLocalidad': '',
		'ctl00$ContentPlaceHolder1$txtProvincia': '',
		'ctl00$ContentPlaceHolder1$dropTitulacion': grade_code,
		'ctl00$ContentPlaceHolder1$txtInicio': '',
		'ctl00$ContentPlaceHolder1$txtFin': '',
		'ctl00$ContentPlaceHolder1$txtEmprendedores': '',
	}
	extend_payload = {
		'__EVENTVALIDATION': eventvalidation,
		'__VIEWSTATE': viewstate,
		'ctl00$ContentPlaceHolder1$botonBuscar': 'Buscar'
	}
	payload = dict(basic_payload, **extend_payload)

	response = session.post(alumni_url, data=payload)

	soup = BeautifulSoup(response.text, 'html.parser')
	eventvalidation = soup.find(id='__EVENTVALIDATION')['value'] if soup.find(id='__EVENTVALIDATION') else ''
	viewstate = soup.find(id='__VIEWSTATE')['value'] if soup.find(id='__VIEWSTATE') else ''

	extend_payload = {
		'ctl00$ContentPlaceHolder1$ScriptManager1': 'ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$gridBusqueda',
		'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gridBusqueda',
		'__EVENTARGUMENT': 'Page$2',
		'__EVENTVALIDATION': eventvalidation,
		'__VIEWSTATE': viewstate
	}
	payload = dict(basic_payload, **extend_payload)

	response = session.post(alumni_url, data=payload)

	soup = BeautifulSoup(response.text, 'html.parser')
	eventvalidation = soup.find(id='__EVENTVALIDATION')['value'] if soup.find(id='__EVENTVALIDATION') else ''
	viewstate = soup.find(id='__VIEWSTATE')['value'] if soup.find(id='__VIEWSTATE') else ''

	extend_payload = {
		'__EVENTVALIDATION': eventvalidation,
		'__VIEWSTATE': viewstate
	}
	payload = dict(basic_payload, **extend_payload)

	return payload


def iterate_pages_and_get_alumni_list(session, payload, page_limit=5000):

	alumni_list = []

	payload = dict(payload)

	for i in xrange(1, page_limit):
		alumni_list_in_page = []

		payload['__EVENTARGUMENT'] = 'Page${}'.format(i)

		response = session.post(alumni_url, data=payload)

		soup = BeautifulSoup(response.text, 'html.parser')
		eventvalidation = soup.find(id='__EVENTVALIDATION')['value'] if soup.find(id='__EVENTVALIDATION') else ''
		viewstate = soup.find(id='__VIEWSTATE')['value'] if soup.find(id='__VIEWSTATE') else ''

		payload.update(__EVENTVALIDATION=eventvalidation, __VIEWSTATE=viewstate)

		alumni_list_in_page = get_alumni_list_in_page(soup)
		if alumni_list_in_page:
			logger.info('{} alumni in page {}'.format(len(alumni_list_in_page), i + 1))
			alumni_list.extend(alumni_list_in_page)
		else:
			break

		time.sleep(random.uniform(0, 1.5))

	return alumni_list


def get_alumni_list_in_page(soup):

	alumni_list_in_page = []

	table = soup.find('table', id='ctl00_ContentPlaceHolder1_gridBusqueda')
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
					alumni_list_in_page.append(alumn)
			except Exception, e:
				# The <tr> item hasn't got any class attribute
				#print 'Something was wrong: {}'.format(repr(e))
				continue
	except Exception, e:
		logger.info('Page limit reached')

	return alumni_list_in_page
