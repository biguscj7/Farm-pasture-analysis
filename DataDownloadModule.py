'''
This is intended to be a module to add to a class for getting NVDI/EVI data 
from the AgriAPI site.
'''

import pprint, datetime, requests, json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# TODO - implement aware datetimes using UTC
starttime = datetime.datetime(2018,1,1,0,0,0,0)
endtime = datetime.datetime(2018,12,31,23,59,59)

# TODO - use requests module to put strings together for request url
baseurl = 'http://api.agromonitoring.com/agro/1.0/ndvi/history?'
starturl = f'&start={int(starttime.timestamp())}'
endurl = f'&end={int(endtime.timestamp())}'
polyid = f'&polyid=5c34b76f16d58400097c9e82'
apiid = f'&appid=8cde214c90d41e08e5d1c297a3551e10'
sattype = f'&type=s2'
cloudmax = f'&clouds_max=10'
# not currently including satellite type in query
queryurl = baseurl+starturl+endurl+polyid+apiid+cloudmax+sattype
pprint.pprint(queryurl)
r = requests.get(queryurl)
j = json.loads(r.text)  
#pprint.pprint(j)

meanlist=[]
medianlist = []
cllist = []
timelist = []

for r in j:
	meanlist.append(r['data']['mean'])
	medianlist.append(r['data']['median'])
	cllist.append((r['cl'])/100)
	timelist.append(datetime.datetime.fromtimestamp(r['dt']))

#pprint.pprint(timelist)

def plot_data(first_time, first_value, second_value, third_value):
	# Set instance of plot at 6 x 9 inches
	fig, ax1 = plt.subplots(figsize=(12,6))
	ax1.set_ylim(0, 1)
	color = 'tab:red'
	ax1.set_xlabel('Date')
	ax1.xaxis_date()
	ax1.tick_params(axis='x', rotation=45)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b-%y'))
	ax1.fmt_xdata = mdates.DateFormatter('%b %d')
	ax1.set_ylabel('NVDI', color=color)
	ax1.tick_params(axis='y', labelcolor=color)
	fig.tight_layout()
	plt.plot(first_time, first_value)
	plt.plot(first_time, second_value)
	plt.plot(first_time, third_value)
	plt.show()

plot_data(timelist, meanlist, medianlist, cllist)