import pprint, datetime, requests, json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# TODO - Get start/stop dates
starttime = datetime.datetime(2018,3,1,0,0,0,0)
endtime = datetime.datetime(2018,9,30,23,59,59)

# TODO - Build url string
starturl = f'{int(starttime.timestamp())}'
endurl = f'{int(endtime.timestamp())}'
polyid = f'5c34b76f16d58400097c9e82'
apiid = f'8cde214c90d41e08e5d1c297a3551e10'
sattype = f'&type=s2'
cloudmax = f'&clouds_max=5'
baseurl = f'http://api.agromonitoring.com/agro/1.0/image/search?start={starturl}&end={endurl}&polyid={polyid}&appid={apiid}'

# not currently including satellite type in query
queryurl = baseurl+cloudmax
pprint.pprint(queryurl)

# TODO - Receive and parse url response
r = requests.get(queryurl)
j = json.loads(r.text)  
#pprint.pprint(j)

# TODO - Execute data pull for each desired EVI data point
lowcloud = []

for i in j:
    dicttemp = json.loads((requests.get(i['stats']['evi'])).text)
    lowcloud.append({'cl':i['cl'],'dt':i['dt'],'evi':dict(dicttemp)})
        
#pprint.pprint(lowcloud)

def merge_lists(left_sublist,right_sublist):
	i,j = 0,0
	result = []
	#iterate through both left and right sublist
	while i<len(left_sublist) and j<len(right_sublist):
		#if left value is lower than right then append it to the result
		if left_sublist[i]['dt'] <= right_sublist[j]['dt']:
			result.append(left_sublist[i])
			i += 1
		else:
			#if right value is lower than left then append it to the result
			result.append(right_sublist[j])
			j += 1
	#concatenate the rest of the left and right sublists
	result += left_sublist[i:]
	result += right_sublist[j:]
	#return the result
	return result

def merge_sort(input_list):
	#if list contains only 1 element return it
	if len(input_list) <= 1:
		return input_list
	else:
		#split the lists into two sublists and recursively split sublists
		midpoint = int(len(input_list)/2)
		left_sublist = merge_sort(input_list[:midpoint])
		right_sublist = merge_sort(input_list[midpoint:])
		#return the merged list using the merge_list function above
		return merge_lists(left_sublist,right_sublist)

sortlowcloud = merge_sort(lowcloud)
pprint.pprint(sortlowcloud)

# TODO - Plot EVI data against datetime strings for the given date range
meanlist=[]
medianlist = []
cllist = []
timelist = []

for r in sortlowcloud:
	meanlist.append(r['evi']['mean'])
	medianlist.append(r['evi']['median'])
	cllist.append((r['cl'])/100)
	timelist.append(datetime.datetime.fromtimestamp(r['dt']))

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