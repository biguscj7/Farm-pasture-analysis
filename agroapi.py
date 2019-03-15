import requests
import json
import pprint
import datetime
import logbook
import sys
import cProfile

profiler = cProfile.Profile()
profiler.disable()


class Polygon:
    """This class represents a list of polygons from the Agro API https://home.agromonitoring.com/"""

    def __init__(self, appid='8cde214c90d41e08e5d1c297a3551e10'):
        """Initialize with API ID only"""
        self.queryurl = 'http://api.agromonitoring.com/agro/1.0/polygons?appid='
        self._apiid = appid

    def printPoly(self):
        """Returns a list of polygons available with ID, size (hectares), and Name"""
        polyurl = self.queryurl + self._apiid
        # pprint.pprint(polyurl)

        r = requests.get(polyurl)  # add logging of response from server & consider adding exception handling
        app_log.trace(f'Server response {r.status_code}')
        j = json.loads(r.text)

        _shrtPoly = []

        for i in j:
            _shrtPoly.append(
                {'area': i['area'], 'name': i['name'], 'id': i['id']})  # add logging of number of returned polys
        app_log.trace(f'Total poly\'s returned - {len(_shrtPoly)}')
        return _shrtPoly


class SatImage:
    """This class handles the satellite image API
    from https://home.agromonitoring.com/"""

    def __init__(self, polyid, strttime, stptime,
                 appid='8cde214c90d41e08e5d1c297a3551e10',
                 sattype=None, cloudmax=None,
                 ):
        """Requires input of polygon, strttime/stptime (UNIX timestamp as string). Will accept sattype l8 or s2."""
        self._queryurl = f'http://api.agromonitoring.com/agro/1.0/image/search?start={strttime}&end={stptime}&polyid={polyid}&appid={appid}'
        if sattype:
            self._queryurl += f'&type={sattype}'
        if cloudmax:
            self._queryurl += f'&clouds_max={cloudmax}'

    def polysat(self, product):
        """Method accepts type product requested (str) and prints the product options"""
        r = requests.get(
            self._queryurl)  # another place to add logging as well as error handling, # log request variables (sattype/cloudmax)
        app_log.trace(f'Query url {self._queryurl}')
        j = json.loads(r.text)
        _urldict = []
        for i in j:
            _urldict.append({'dt': i['dt'], 'type': i['type'], 'cl': i['cl'], product: i[product]})
        pprint.pprint(_urldict)  # add logging for number of returned items


def dateinput():
    '''Use the fuction to solicit input and return datetime object'''
    date_str = input('Enter date in format MM-DD-YYYY\n')
    while True:
        try:
            app_log.trace(f'Date entered ' + date_str)
            return datetime.datetime.strptime(date_str, "%m-%d-%Y")
        except ValueError as x:
            app_log.error(x)
            print('Ensure you enter leading zeros for single digit month/date and use format MM-DD-YYYY\n')
            date_str = input()


def init_logging(filename: str = None):
    level = logbook.TRACE

    if filename:
        logbook.TimedRotatingFileHandler(filename, level=level).push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=level).push_application()

    msg = 'Logging initialized, level: {}, mode: {}'.format(
        level,
        "stdout mode" if not filename else 'file mode: ' + filename
    )
    logger = logbook.Logger('Startup')
    logger.notice(msg)


if __name__ == '__main__':
    profiler.enable()

    init_logging('logtest')
    app_log = logbook.Logger('App')

    p = Polygon()
    pprint.pprint(p.printPoly())

    print('Please enter the start date.')
    starturl = f'{dateinput().timestamp()}'
    print('Please enter the end date.')
    endurl = f'{dateinput().timestamp()}'

    polyid = f'5c34b76f16d58400097c9e82'
    g = SatImage(polyid, starturl, endurl, cloudmax='5', sattype='s2')
    g.polysat('data')

    #profiler.print_stats(sort='cumtime')
