import pprint, datetime, requests, json

# TODO - Get start/stop dates
starttime = datetime.datetime(2018,4,1,0,0,0,0)
endtime = datetime.datetime(2018,8,31,23,59,59)

# TODO - Build url string
starturl = f'{int(starttime.timestamp())}'
endurl = f'{int(endtime.timestamp())}'
polyid = f'5c3eff0716d58400097c9eee'
apiid = f'8cde214c90d41e08e5d1c297a3551e10'
sattype = f'&type=s2'
cloudmax = f'&clouds_max=5'
baseurl = f'http://api.agromonitoring.com/agro/1.0/image/search?start={starturl}&end={endurl}&polyid={polyid}&appid={apiid}'

# not currently including satellite type in query
queryurl = baseurl+cloudmax+sattype
#pprint.pprint(queryurl)

# TODO - Receive and parse url response
r = requests.get(queryurl)
j = json.loads(r.text)  
pprint.pprint(j)

for i in j:
    filedate = datetime.datetime.fromtimestamp(i['dt'])
    datestring = filedate.strftime('%d-%b-%y')
    f = requests.get(i['data']['evi'], allow_redirects=True)
    open(f'{datestring}-EVI.tif', 'wb').write(f.content)
    f = requests.get(i['image']['evi'], allow_redirects=True)
    open(f'{datestring}-EVI.png', 'wb').write(f.content)