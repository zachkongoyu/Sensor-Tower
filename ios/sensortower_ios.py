import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import date
import time

def add():

	try:
		df = pd.read_csv('data pool/raw_ios.csv', index_col=0)
	except:
		df = pd.DataFrame()

	to_add = dict()
	month = input('Month: ')

	with open('names_urls.txt', 'r',  encoding='UTF-8') as f:

		names_urls = f.read().splitlines()

	names_urls = [ele for ele in names_urls if ele != '' and ele != "\ufeff"]

	if month in df.columns:
		command = input(f'{month} is already included in the file, do you want to replace it? (y/other keys to leave) ')
		
		if command != 'y':
			return None

		df.drop(month, axis=1, inplace=True)

	for i, name_url in enumerate(names_urls):

		if (i % 10 == 0 and i > 0):

			print('Taking a 10-second break to pretend as a human...')
			time.sleep(10)

		app_name = name_url.split(',')[0]
		url = name_url.split(',')[-1]

		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		
		id = int(url.split('/')[-2])

		print(i+1, response, id, app_name)

		target = [element for element in list(soup.body) if 'downloads_and_revenue' in element][0]
		target = '{' + target.replace(' ', '') + '}'

		kocomponent = 'kocomponent'
		name = 'name'
		params = 'params'
		null = float('NaN')
		true = True
		false = False

		target = eval(target)
		downloads = target['kocomponent']['params']['downloads_and_revenue']['downloads']

		try:
			if '<' in downloads:
				downloads = downloads.replace('<', '')

			if 'k' in downloads:
				downloads = int(downloads[:-1])*1000
			elif 'm' in downloads:
				downloads = int(downloads[:-1])*1000000
		except:
			pass

		revenue = target['kocomponent']['params']['downloads_and_revenue']['revenue']

		try:
			if '<' in revenue:
				revenue = revenue.replace('<', '')

			if 'k' in revenue:
				revenue = int(revenue[1:-1])*1000
			elif 'm' in revenue:
				revenue = int(revenue[1:-1])*1000000
		except:
			pass

		rating = target['kocomponent']['params']['current_rating']
		rating_count = target['kocomponent']['params']['current_rating_count']

		headers = {
			'authority': 'sensortower.com',
			'accept': 'application/json, text/javascript, */*; q=0.01',
			'x-csrf-token': 'T7ygaSsbtl+gvxrGZcvgsj0i8zix4uHJ/32e16Y/k1TT8UKG2fAQxkmItIt0dxGilNxS8ohI2Sc2ih68PVBBkQ==',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
			'x-requested-with': 'XMLHttpRequest',
			'sec-gpc': '1',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://sensortower.com/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
			'cookie': 'locale=en; session=c5e603284f395fb6b917669a20432f14; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jul+05+2021+11%3A02%3A31+GMT%2B0800+(Hong+Kong+Standard+Time)&version=6.16.0&hosts=&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=HK%3BHCW; OptanonAlertBoxClosed=2021-07-05T03:02:31.664Z; amplitude_id_6edb64137a31fa337b6f553dbccf2d8bsensortower.com=eyJkZXZpY2VJZCI6IjI3Yzk4MzJjLWU5ZDItNGQ3Yy05OGFlLWQ2YjhmMjg5MGFmMVIiLCJ1c2VySWQiOiJuZ295dWtvNzhAZ21haWwuY29tIiwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNjI1NDUzMzY4NzEyLCJsYXN0RXZlbnRUaW1lIjoxNjI1NDU0ODY0MzU2LCJldmVudElkIjo0OCwiaWRlbnRpZnlJZCI6MSwic2VxdWVuY2VOdW1iZXIiOjQ5fQ==',
		}

		params = (
			('app_id', id),
			('country', 'US'),
			('limit', '1'),
		)

		response = requests.get('https://sensortower.com/api/ios/visibility_scores', headers=headers, params=params)

		score = eval(response.content.decode('utf8'))[0]['total_score']

		to_add[app_name] = str([downloads, revenue, rating, rating_count, score])

		time.sleep(3)

	d = {month:to_add}
	to_add_df = pd.DataFrame(d)

	df = pd.concat([df, to_add_df], axis=1)

	df.to_csv('data pool/raw_ios.csv')

def e0(self):

	nan = float('NaN')

	try:
		return eval(self)[0]
	except:
		return float('NaN')

def e1(self):

	nan = float('NaN')

	try:
		return eval(self)[1]
	except:
		return float('NaN')

def e2(self):

	nan = float('NaN')

	try:
		return eval(self)[2]
	except:
		return float('NaN')

def e3(self):

	nan = float('NaN')

	try:
		return eval(self)[3]
	except:
		return float('NaN')

def e4(self):

	nan = float('NaN')

	try:
		return eval(self)[4]
	except:
		return float('NaN')

def extract():

	df = pd.read_csv('data pool/raw_ios.csv', index_col=0)

	df1 = pd.DataFrame()

	for col in df:
		df1[col] = df[col].apply(e0)

	df1.to_excel('lab/downloads.xlsx')

	df = pd.read_csv('data pool/raw_ios.csv', index_col=0)

	df1 = pd.DataFrame()

	for col in df:
		df1[col] = df[col].apply(e1)

	df1.to_excel('lab/revenue.xlsx')

	df1 = pd.DataFrame()

	for col in df:
		df1[col] = df[col].apply(e2)

	df1.to_excel('lab/rating.xlsx')

	df1 = pd.DataFrame()

	for col in df:
		df1[col] = df[col].apply(e3)

	df1.to_excel('lab/rating_count.xlsx')

	df1 = pd.DataFrame()

	for col in df:
		df1[col] = df[col].apply(e4)

	df1.to_excel('lab/visibility_score.xlsx')


if __name__ == '__main__':

	command = input("What can I help you? \'menu\' to check all the commands ")

	while command != 'exit':

		if command == 'add':
			add()

		elif command == 'extract':
			extract()

		elif command == 'menu':

			print("add -- add new app data to data pool")
			print('extract -- extract the excel file you want')
			print('exit -- leave the survice')

		command = input("What can I help you? \'menu\' to check all the commands ")