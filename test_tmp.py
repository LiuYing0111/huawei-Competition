#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 23:02:02 2019

@author: wanchao
"""

import datetime

'''
numOfCross = len(cross.idList)
adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxunicode
roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
for i in range(len(road.idList)):
    adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]
    roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
    if(road.isDuplexList[i] == 1):
        adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
        roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
for i in range(numOfCross):
    adjMatrix[i,i] = 0

starttime = datetime.datetime.now()
for i in range(50):
    #print(i)
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    endtime = datetime.datetime.now()
print((endtime - starttime))
'''

'''
starttime = datetime.datetime.now()

a=[sum(car.fromList==i) for i in range(101)]

endtime = datetime.datetime.now()
print((endtime - starttime))
'''

aa=np.array([[1,2],[3,4],[5,4],[3,7],[9,7]])
aaa=np.zeros([64,64])
for i,j in routeCrossList[0][63]:
    print(str(i)+'------'+str(j))
    aaa[i,j]=1