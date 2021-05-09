from datetime import datetime
from numpy import nan as Nan
import pandas as pd
import numpy as np
import pytz, requests


def posix_to_isoweek(target):

	ts = float(target)
	try:
		local_time = datetime.fromtimestamp(ts, pytz.timezone("Asia/Jakarta")) 
	except ValueError:
		local_time = datetime.fromtimestamp(ts/1000, pytz.timezone("Asia/Jakarta")) 
	year, week, _ = local_time.isocalendar()
	
	return str(year) + "-W" + str(week)


def get_data():

	url = 'https://stein.efishery.com/v1/storages/5e1edf521073e315924ceab4/list'

	header = {'Content-Type': 'application/json'}

	response = requests.get(url, headers=header)

	results = response.json()

	rets = []
	for d in results:
		dt = {}

		if d["uuid"] is not None:
			dt["uuid"] = d["uuid"]
		else:
			dt["uuid"] = "no_data"

		if d["komoditas"] is not None:
			dt["komoditas"] = d["komoditas"]
		else:
			dt["komoditas"] = "no_data"

		if d["area_provinsi"] is not None:
			dt["area_provinsi"] = d["area_provinsi"]
		else:
			dt["area_provinsi"] = "no_data"

		if d["area_kota"] is not None:
			dt["area_kota"] = d["area_kota"]
		else:
			dt["area_kota"] = "no_data"

		if d["size"] is not None:
			dt["size"] = d["size"]
		else:
			dt["size"] = "no_data"

		if d["price"] is not None:
			dt["price"] = d["price"]
		else:
			dt["price"] = "no_data"

		if d["tgl_parsed"] is not None:
			dt["tgl_parsed"] = d["tgl_parsed"]
		else:
			dt["tgl_parsed"] = "no_data"

		if d["timestamp"] is not None:
			dt["timestamp"] = d["timestamp"]
		else:
			dt["timestamp"] = "no_data"

		rets.append(dt)

	return rets


def extract():

	datas = get_data()
	df = pd.DataFrame(datas)
	df = df.drop_duplicates()

	df['Week'] = df['timestamp'].apply(lambda x: posix_to_isoweek(x) if x != "no_data" else "no_data")

	df['price'] = df['price'].apply(lambda x: float(x) if x.isdigit() else Nan)

	results = df[['Week','komoditas','price']].groupby(["Week","komoditas"]).agg(
		min_price=pd.NamedAgg(column="price", aggfunc='min'),
		max_price=pd.NamedAgg(column="price", aggfunc='max'),
		average_price=pd.NamedAgg(column="price", aggfunc=np.mean),
		).reset_index()

	results = results[results['Week']!="no_data"].reset_index(drop=True)

	results = results[results['komoditas']!="no_data"].reset_index(drop=True)

	results = results[results['min_price'].notna()].reset_index(drop=True)

	# print(results.to_csv(index=False))
	return results.to_csv(index=False)

# if __name__ == '__main__':
# 	extract()