'''
this takes the content of the clipboard and removes the 'elevation' from it
returns a list formatted as a string for pasting into the polygon geojson
'''

from richxerox import copy, paste

grids = paste()

gridsplit = grids.split(' ')

gridlist = []

for x in gridsplit:
    gridlist.append(x.split(','))

for y in gridlist:
    del y[-1]

#print(gridlist)

basicstr = f'['

for z in gridlist:
    basicstr += f'[{z[0]},{z[1]}],'

basicstr = basicstr[:-1]
basicstr += f']'

print(basicstr)

copy(basicstr)

'''
basic = f'{"type":"Feature","properties":{},"geometry":{"type":"Polygon",
"coordinates":[['
    [-121.267275,37.693058],
    [-121.259725,37.648219],
    [-121.182508,37.663304],
    [-121.196407,37.705825],
    [-121.267275,37.693058]]]}}'
'''