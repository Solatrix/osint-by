import os
import sys
from multiprocessing.pool import ThreadPool as Pool
import requests
from datetime import date, datetime
import json
from urllib.parse import urljoin
from requests_html import HTMLSession

pool_size = 1

PARAMETERS = {
	"channels" : '--channels',
	"period" : '--period',
	"metric" :  '--metric',
	"start-date" : '--start-date',
	"end-date" : '--end-date'
}

METRICS = {
	"views" : "views_count",
	"posts" : "posts_count",
	"views_per_post" : "views_per_post",
	"members" : "members_count",
	"reposts" : "ic_count"
}

USER_INPUT = sys.argv[1:len(sys.argv)]

PERIODS = ['years', 'months', 'weeks', 'days']

CURRENT_DATE = date.today()
CURRENT_DATE_STR = CURRENT_DATE.strftime('%Y-%m-%d')

TARGET_IDS=[]
ENDPOINT_URI="https://tgstat.ru"
CHANNEL_DATA_URI=f"{ENDPOINT_URI}/channels/chart-data"
def initialize():
	global USER_INPUT
	global pool
	try:
		if validate_arguments():
			print("STARTING CHANNEL CRAWLING \n")
			print("RETRIEVING UNIQUE IDS \n")
			if len(FORMATTED_ARGS['channels']) > 1 and len(FORMATTED_ARGS['channels']) < 5:
				pool_size=len(FORMATTED_ARGS['channels'])
			else:
				pool_size=5
			pool = Pool(pool_size)
			global session
			session = HTMLSession()
			for channel in FORMATTED_ARGS['channels']:

				pool.apply_async(worker, (channel,))

			pool.close()
			pool.join()
	except Exception:
		print(f"Missing arguments : channels, period, metric, start-date")
		raise Exception
		sys.exit(1)
	if len(TARGET_IDS) > 0:
		print(f"")

def validate_arguments():
	global FORMATTED_ARGS

	FORMATTED_ARGS = {}
	PARAM_KEYS = PARAMETERS.keys()

	USER_ARGS = [x for x in USER_INPUT if x.split('=')[0] in PARAMETERS.values()]
	FORMATTED_ARGS = {x:y.split('=')[1].split(',') for x in PARAM_KEYS for y in USER_ARGS if x == y.split('=')[0].split('--')[1]}

	length_assertion =  len(FORMATTED_ARGS['channels']) > 0 and len(FORMATTED_ARGS['period']) > 0 and len(FORMATTED_ARGS['metric']) > 0

	for x in FORMATTED_ARGS['channels']:
		if "@" not in x:
			FORMATTED_ARGS['channels'][FORMATTED_ARGS['channels'].index(x)] = '@'+x

	FORMATTED_ARGS['period'] = FORMATTED_ARGS['period'][0]
	FORMATTED_ARGS['metric'] = FORMATTED_ARGS['metric'][0]
	if "start-date" in FORMATTED_ARGS and len(FORMATTED_ARGS['start-date'][0]) > 0:
		FORMATTED_ARGS['start-date'] = FORMATTED_ARGS['start-date'][0]
	else:
		FORMATTED_ARGS['start-date'] = CURRENT_DATE_STR

	period_assertion = FORMATTED_ARGS['period'] in PERIODS
	metric_assertion = FORMATTED_ARGS['metric'] in METRICS.values()
	date_assertion  = datetime.strptime(FORMATTED_ARGS['start-date'], '%Y-%m-%d')
	return length_assertion and metric_assertion and period_assertion


def worker(target_channel):

	def rest_api_worker(params):
		target = CHANNEL_DATA_URI
		headers = {
			'X-Requested-With': 'XMLHttpRequest'
		}
		params['Content-Type'] = 'application/x-www-form-urlencoded'
		req=session.post(target, data=params, headers=headers)
		print(req.json())


	def crawler(channel):
		print(f"HTTING CHANNEL {channel}")
		target_id = session.get(urljoin(ENDPOINT_URI, f"/channel/{channel}" ))
		if int(target_id.status_code) == 200: 
			try:
				TARGET_IDS.append(int(target_id.html.find('input[name=channel_id]')[0].attrs['value']))
				requested_id = int(target_id.html.find('input[name=channel_id]')[0].attrs['value'])
				if requested_id > 0:
					params = FORMATTED_ARGS
					params.pop("channels")
					params['id']=requested_id

					if 'end-date' in params:
						params['dateRangeMax'] = params['end-date']
						params.pop('end-date')
						params['dateRangeMin'] = params['start-date']
					elif 'start-date' in params and 'end-date' not in params:
						params['dateRangeMin'] = params['start-date']
						params['dateRangeMax'] = CURRENT_DATE_STR

					params.pop('start-date')
					rest_api_worker(params)
			except Exception:
				print('Error whilst retrieving channel id : '+channel)
		else:
			print(f"Request error {target_id.status_code}")
			print(f"Error : invalid response whilst retrieving channel : "+channel)
			print("Skipping")
	

	try:
		crawler(target_channel)
	except Exception:
		print(f"Error : worker could not proceed with request for channel {target_channel}")


# tgstat-crawler.py --channels=@pul_1,@nexta_tv,@zerkalo_io  --period=months --metric= --start-date=2020-01-01 --end-date=2022-01-01 

if __name__ == "__main__":
	initialize()