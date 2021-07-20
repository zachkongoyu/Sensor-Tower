import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import date
import time

def add():

	try:
		df = pd.read_csv('data pool/raw_android.csv', index_col=0)
	except:
	 	df = pd.DataFrame()

	to_add = dict()
	month = input('Month: ')

	if month in df.columns:
		command = input(f'{month} is already included in the file, do you want to replace it? (y/other keys to leave) ')
		
		if command != 'y':
			return None

		df.drop(month, axis=1, inplace=True)

	with open('names_urls.txt', 'r',  encoding='UTF-8') as f:

		names_urls = f.read().splitlines()

	names_urls = [ele for ele in names_urls if ele != '' and ele != "\ufeff"]


	for i, name_url in enumerate(names_urls):

		if (i % 10 == 0 and i > 0):

			print('Taking a 10-second break to pretend as a human...')
			time.sleep(10)

		app_name = name_url.split(',')[0]
		url = name_url.split(',')[-1]

		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')

		print(i+1, response, app_name)

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

		to_add[app_name] = str([downloads, revenue, rating, rating_count])

	d = {month:to_add}
	to_add_df = pd.DataFrame(d)

	df = pd.concat([df, to_add_df], axis=1)

	df.to_csv('data pool/raw_android.csv')

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

def extract():

	df = pd.read_csv('data pool/raw_android.csv', index_col=0)

	df1 = pd.DataFrame()

	for col in df:
		df1[col] = df[col].apply(e0)

	df1.to_excel('lab/downloads.xlsx')

	df = pd.read_csv('data pool/raw_android.csv', index_col=0)

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