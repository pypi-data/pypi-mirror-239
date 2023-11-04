#from plot import Figure, Group

import plot
from plot import Figure,Post,Group
import numpy as np
import pandas as pd
import sys


# Let us get the cumulative wins
plot.initApp(appName='chartart', webAppBaseUrl='http://localhost:6060', apiGatewayBaseUrl='https://chartart4-gw-4sjw1jja.uc.gateway.dev')
candyData = pd.read_csv('data/candy.csv')

print(candyData.to_dict(orient='split'))



group = Group(grp_id='lineType')
#for chartType in ['line', 'area', 'spline', 'stepLine', 'splineArea', 'stepArea', 'stackedLine', 'stackedArea', 'stackedArea100', 'stackedLine100']:
#    line = Figure(chart_id=chartType, title=chartType)
#    line.line(x=candyData['id'], y=candyData['sugarpercent'], labels='sugarpercent', c='#31948A', type=chartType)
#    line.line(x=candyData['id'], y=candyData['pricepercent'], labels='pricepercent', c='#51ADE2', type=chartType)
#    group.add(line)

table = Figure(chart_id='t1', title='t1')
table.table(df=candyData, colsTypes= ['number', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'number', 'number', 'heatmap'])
p = Post(postId = 'mapcapablity', postTitle= 'Map capablity')
p.addInMemory(table)
print(p.getInmemoryPostInfo())


