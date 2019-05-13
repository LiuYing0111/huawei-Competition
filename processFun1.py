#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 02:41:14 2019

@author: wanchao
"""
import sys
import numpy as np
import math
from funList_wc import floyd, dijkstra


#我们的方法process_10_1

def process_1(car, road, cross):
    #method 1
    
    #create graph matrix
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
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    for i in range(numOfCar):
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        if i>650:
            planTimeList[i] = car.planTimeList[i] + math.floor((i-650) / 11)
        else:
            planTimeList[i] = car.planTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
    
    #print('process finish')
    return answer

'''
def process_2(car, road, cross):
    #method 2
    
    #create graph matrix
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
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    k = 0
    for i in (-car.speedList).argsort():
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        if k > 650:
            planTimeList[i] = car.planTimeList[i] + math.floor((k-650) / 11)
        else:
            planTimeList[i] = car.planTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        k = k + 1
    
    #print('process finish')
    return answer
'''

def process_3(car, road, cross):
    #sum Of the routes
    numOfCross = len(cross.idList)
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    
    for i in range(20):
        answer, sumRoutesMat,roadMatrix = process_3_1(car, road, cross, sumRoutesMat, i)
        sumRoutesMat = sumRoutesMat
    
    return answer, sumRoutesMat,roadMatrix

def process_3_1(car, road, cross, sumRoutesMat, ii):
    #method 3
    
    #create graph matrix
    numOfCross = len(cross.idList)
    #lambda0 = 0.1
    adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxunicode*1000
    roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
    for i in range(len(road.idList)):
        adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]
        roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
        if(road.isDuplexList[i] == 1):
            adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
            roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
    for i in range(numOfCross):
        adjMatrix[i,i] = 0
    
    #if sum(sum(sumRoutesMat==0))!=64**2:
    if ii > 0:
        #adjMatrix[adjMatrix<sys.maxunicode] = sumRoutesMat[adjMatrix<sys.maxunicode]
        adjMatrix[roadMatrix>0] = sumRoutesMat[roadMatrix>0] + 1
        #adjMatrix[adjMatrix != 0] += 1000
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    for i in range(numOfCar):
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        #print([[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)])
        #print(roadIdList)
        if (i-800)>0:
            planTimeList[i] = car.planTimeList[i] + math.floor((i-800) / 11)
        else:
            planTimeList[i] = car.planTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        
        for i in range(len(routeMin[i0][j0])-1):
            sumRoutesMat[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] += 1
    
    
    
    #print('process finish')
    return answer, sumRoutesMat,roadMatrix

def process_4(car, road, cross):
    #method 1
    
    #create graph matrix
    numOfCross = len(cross.idList)
    adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxsize
    roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
    for i in range(len(road.idList)):
        adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]
        roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
        if(road.isDuplexList[i] == 1):
            adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
            roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
    for i in range(numOfCross):
        adjMatrix[i,i] = 0
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    
    #edges
    edges = []
    for i in range(numOfCross):
        for j in range(numOfCross):
            if i!=j and adjMatrix[i][j]!=sys.maxsize:
                edges.append((i,j,adjMatrix[i,j]))
                
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    Shortest_path = [-1]
                
    for i in range(numOfCar):
        if (i%100) == 0:
            print(str(i))
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        
        for i in range(numOfCross):
            for j in range(numOfCross):
                if i!=j and adjMatrix[i][j]!=sys.maxsize:
                    edges.append((i,j,adjMatrix[i,j]+sumRoutesMat[i,j]))
        for n in range(len(Shortest_path) - 1):
            adjMatrix_0 = adjMatrix[Shortest_path[n], Shortest_path[n+1]]
            edges[edges.index((Shortest_path[n], Shortest_path[n+1], adjMatrix_0))] = ((Shortest_path[n], Shortest_path[n+1], adjMatrix_0 + 0.1 * sumRoutesMat[Shortest_path[n], Shortest_path[n+1]]))
        
        length,Shortest_path = dijkstra(edges, i0, j0)
        
        roadIdList = [roadMatrix[Shortest_path[i],Shortest_path[i+1]] for i in range(len(Shortest_path)-1)]
        #roadIdList =Shortest_path
        if i>650:
            planTimeList[i] = car.planTimeList[i] + math.floor((i-650) / 11)
        else:
            planTimeList[i] = car.planTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        
        for i in range(len(routeMin[i0][j0])-1):
            sumRoutesMat[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] += 1
    
    #print('process finish')
    return answer

def process_5(car, road, cross):
    #method 5
    
    #create graph matrix
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
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    
    for i in range(numOfCar):
        if i%20 ==0:
            #print(i)
            distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 0.1, numOfCross)
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        if i>650:
            planTimeList[i] = car.planTimeList[i] + math.floor((i-650) / 21)
        else:
            planTimeList[i] = car.planTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        
        for j in range(len(routeMin[i0][j0])-1):
            sumRoutesMat[routeMin[i0][j0][j]-1,routeMin[i0][j0][j+1]-1] += 1
    
    #print('process finish')
    #, sumRoutesMat, roadMatrix
    return answer

def process_6(car, road, cross):
    #method 6
    
    #create graph matrix
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
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    
    range0 = np.arange(len(car.fromList))
    car_idList_1 = car.fromList > car.toList
    
    k = 0
    for i in range0[car_idList_1]:
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        if k>1200:
            planTimeList[i] = car.planTimeList[i] + math.floor((k-1200) / 12)
        else:
            planTimeList[i] = car.planTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        k = k + 1
        
    for i in range0[~car_idList_1]:
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        planTimeList[i] = car.planTimeList[i] + math.floor((k-1500) / 12)
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        k = k + 1
    
    #print('process finish')
    return answer

def process_7(car, road, cross):
    #method 7
    
    #create graph matrix
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
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    for i in range(numOfCar):
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        if i>650:
            planTimeList[i] = car.planTimeList[i] + math.floor((i-650) / 11)
        else:
            planTimeList[i] = car.planTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
    
    #print('process finish')
    return answer

def process_8(car, road, cross):
    #method 8
    
    #create graph matrix
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
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)

    index0 = np.arange(numOfCar)
    k = 0
    for i in range(numOfCross):
        index_i = index0[car.fromList==i+1]
        for j in index_i[car.toList[car.fromList==i+1].argsort()]:
            #print(j)
            i0 = car.fromList[j] - 1
            j0 = car.toList[j] - 1
            print(str(i0)+'------'+str(j0))
            #if k%20 == 0:
                #distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 0.1, numOfCross)
            roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
            if (k - 500)>0:
                planTimeList[j] = car.planTimeList[j] + math.floor((k-500) / 9)
            else:
                planTimeList[j] = car.planTimeList[j]
            answer[j] = str(car.idList[j]) + ', ' + str(planTimeList[j]) + ', ' + str(roadIdList)[1 : -1]
            k += 1
            for i in range(len(routeMin[i0][j0])-1):
                sumRoutesMat[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] += 1
    
    return answer

def process_9(car, road, cross):
    #method 8
    
    #create graph matrix
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
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)

    index0 = np.arange(numOfCar)
    k = 0
    for i in range(numOfCross): 
        if i%2 == 1:
            i = 64 - i
        #print(i)
        index_i = index0[car.fromList==i+1]
        for j in index_i[car.toList[car.fromList==i+1].argsort()]:
            #print(j)
            i0 = car.fromList[j] - 1
            j0 = car.toList[j] - 1
            #print(str(i0)+'------'+str(j0))
            if k%20 == 0:
                distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 0.1, numOfCross)
            roadIdList = [roadMatrix[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
            if (k - 700)>0:
                planTimeList[j] = car.planTimeList[j] + math.floor((k-700) / 21)
            else:
                planTimeList[j] = car.planTimeList[j]
            answer[j] = str(car.idList[j]) + ', ' + str(planTimeList[j]) + ', ' + str(roadIdList)[1 : -1]
            k += 1
            for i in range(len(routeMin[i0][j0])-1):
                sumRoutesMat[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] += 1
    
    return answer

def process_10(car, road, cross):
    #method 10
    
    print('-------------------1')
    
    #create graph matrix
    numOfCross = len(cross.idList)
    #numOfRoad = len(road.idList)
    adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxunicode
    roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixIndex = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixSpeed = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixChannel = np.zeros([numOfCross, numOfCross],dtype = int)
    for i in range(len(road.idList)):
        adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]
        roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
        roadMatrixIndex[road.fromList[i]-1, road.toList[i]-1] = i
        roadMatrixSpeed[road.fromList[i]-1, road.toList[i]-1] = road.speedList[i]
        roadMatrixChannel[road.fromList[i]-1, road.toList[i]-1] = road.channelList[i]
        if(road.isDuplexList[i] == 1):
            adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
            roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
            roadMatrixIndex[road.toList[i]-1, road.fromList[i]-1] = i
            roadMatrixSpeed[road.toList[i]-1, road.fromList[i]-1] = road.speedList[i]
            roadMatrixChannel[road.toList[i]-1, road.fromList[i]-1] = road.channelList[i]
    for i in range(numOfCross):
        adjMatrix[i,i] = 0
    print('-------------------2')
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    print('-------------------3')
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    
    #compute the time of the routes
    #sumCrossMat =  np.zeros([numOfCross,numOfCross])
    #sumCrossList = [[car.fromList[i],car.toList[i]] for i in range(len(car.idList))]
    #for i in range(len(sumCrossList)):
        #sumCrossMat[sumCrossList[i][0] - 1,sumCrossList[i][1] - 1] += 1
    #[([np.empty([0],dtype=int)] * numOfCross) for i in range(numOfCross)]
    #routeCrossMatCode = [[np.zeros([numOfCross,numOfCross],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossList = [[np.empty([0],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossListCode = [[np.zeros([1,numOfRoad],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    
    #for i in range(numOfCross):
        #for j in range(numOfCross):
            #if sumCrossMat[i][j] > 0:
                #routeCrossList[i][j] = [[routeMin[i][j][i0]-1,routeMin[i][j][i0+1]-1] for i0 in range(len(routeMin[i][j])-1)]
                #routeCrossListCode[i][j] = [roadMatrixIndex[i0,j0] for i0,j0 in routeCrossList[i][j]]
                #for i0,j0 in routeCrossList[i][j]:
                    #routeCrossMatCode[i][j][i0,j0] = 1
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    print('-------------------4')
    costTimeList = np.zeros(1, dtype = int)
    endTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    timeOfNow = 0
    carInRoutesIndex = np.arange(numOfCar)
    print('-------------------5')
    carRouteCrossMatCode = [[np.zeros([numOfCross, numOfCross],dtype=int)] for i0 in range(len(car.idList))]
    print('-------------------6')
    for i in range(numOfCar):
        if i%600 ==0:
            print(i)
            #distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 300, numOfCross)
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        routeCrossListCode_0 = [roadMatrixIndex[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        roadIdList = [road.idList[i] for i in routeCrossListCode_0]
        for j1 in range(len(routeMin[i0][j0])-1):
            carRouteCrossMatCode[i][0][routeMin[i0][j0][j1]-1,routeMin[i0][j0][j1+1]-1] += 1
        if i>1000:
            timeOfNow = math.floor((i-1000) / 28)
        else:
            timeOfNow = car.planTimeList[i]
        planTimeList[i] = max(timeOfNow,car.planTimeList[i])
        costTime_tmp = [road.lengthList[i] for i in routeCrossListCode_0]
        costTime_tmp2 = [road.speedList[i] for i in routeCrossListCode_0]
        costTime_tmp3 = np.vstack((costTime_tmp2,car.speedList[i] * np.ones([1,len(routeCrossListCode_0)]))).min(0)
        costTimeList = sum(costTime_tmp / costTime_tmp3)
        endTimeList[i] =  planTimeList[i] + costTimeList
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        carInRoutes = carInRoutesIndex[endTimeList >= timeOfNow]
        #print('i:'+str(i)+'--------'+'timeOfNow:'+str(timeOfNow))
        #print(sum(endTimeList >= timeOfNow))
        sumRoutesMat = sumRoutesMat * 0
        for j2 in carInRoutes:
            sumRoutesMat += carRouteCrossMatCode[j2][0]
        sumRoutesMat[roadMatrix > 0] = sumRoutesMat[roadMatrix > 0] / roadMatrixChannel[roadMatrix > 0]

    return answer

def process_10_1(car, road, cross):
    #method 10
    
    print('-------------------1')
    
    #create graph matrix
    numOfCross = len(cross.idList)
    #numOfRoad = len(road.idList)
    adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxunicode
    roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixIndex = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixSpeed = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixChannel = np.zeros([numOfCross, numOfCross],dtype = int)
    for i in range(len(road.idList)):
        adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]#road的长度
        roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
        roadMatrixIndex[road.fromList[i]-1, road.toList[i]-1] = i
        roadMatrixSpeed[road.fromList[i]-1, road.toList[i]-1] = road.speedList[i]
        roadMatrixChannel[road.fromList[i]-1, road.toList[i]-1] = road.channelList[i]
        if(road.isDuplexList[i] == 1):
            adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
            roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
            roadMatrixIndex[road.toList[i]-1, road.fromList[i]-1] = i
            roadMatrixSpeed[road.toList[i]-1, road.fromList[i]-1] = road.speedList[i]
            roadMatrixChannel[road.toList[i]-1, road.fromList[i]-1] = road.channelList[i]
    for i in range(numOfCross):
        adjMatrix[i,i] = 0
    print('-------------------2')
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    print('-------------------3')
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    
    #compute the time of the routes
    #sumCrossMat =  np.zeros([numOfCross,numOfCross])
    #sumCrossList = [[car.fromList[i],car.toList[i]] for i in range(len(car.idList))]
    #for i in range(len(sumCrossList)):
        #sumCrossMat[sumCrossList[i][0] - 1,sumCrossList[i][1] - 1] += 1
    #[([np.empty([0],dtype=int)] * numOfCross) for i in range(numOfCross)]
    #routeCrossMatCode = [[np.zeros([numOfCross,numOfCross],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossList = [[np.empty([0],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossListCode = [[np.zeros([1,numOfRoad],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    
    #for i in range(numOfCross):
        #for j in range(numOfCross):
            #if sumCrossMat[i][j] > 0:
                #routeCrossList[i][j] = [[routeMin[i][j][i0]-1,routeMin[i][j][i0+1]-1] for i0 in range(len(routeMin[i][j])-1)]
                #routeCrossListCode[i][j] = [roadMatrixIndex[i0,j0] for i0,j0 in routeCrossList[i][j]]
                #for i0,j0 in routeCrossList[i][j]:
                    #routeCrossMatCode[i][j][i0,j0] = 1
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    print('-------------------4')
    costTimeList = np.zeros(1, dtype = int)
    endTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    timeOfNow = 0
    print('-------------------5')
    carRouteCrossMatCode = [[np.zeros([numOfCross, numOfCross],dtype=int)] for i0 in range(len(car.idList))]
    print('-------------------6')
    
    carInRoutesIndex = []#-------------------------------------------------------------------------------#
    carOutRoutesIndex = np.arange(numOfCar).tolist()#----------------------------------------------------#
    for i in range(numOfCar):
        if i%20 ==0:
            print(i)
            distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 300, numOfCross)
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        routeCrossListCode_0 = [roadMatrixIndex[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        roadIdList = [road.idList[i] for i in routeCrossListCode_0]
        for j1 in range(len(routeMin[i0][j0])-1):
            carRouteCrossMatCode[i][0][routeMin[i0][j0][j1]-1,routeMin[i0][j0][j1+1]-1] += 1
        if i>1000:
            timeOfNow = math.floor((i-1000) / 28)
        else:
            timeOfNow = car.planTimeList[i]
        planTimeList[i] = max(timeOfNow,car.planTimeList[i])
        costTime_tmp = [road.lengthList[i] for i in routeCrossListCode_0]
        costTime_tmp2 = [road.speedList[i] for i in routeCrossListCode_0]
        costTime_tmp3 = np.vstack((costTime_tmp2,car.speedList[i] * np.ones([1,len(routeCrossListCode_0)]))).min(0)
        costTimeList = sum(costTime_tmp / costTime_tmp3)#长度/速度=每条道路花的时间
        endTimeList[i] =  planTimeList[i] + costTimeList
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        #carInRoutes = carOutRoutesIndex[endTimeList >= timeOfNow]
        
        #-------------------------------------------------------------------------------#
        for i in carInRoutesIndex:
            if endTimeList[i] < timeOfNow:
                sumRoutesMat -= carRouteCrossMatCode[i][0]
                carInRoutesIndex.remove(i)
        for i in carOutRoutesIndex:
            if endTimeList[i] >= timeOfNow:
                sumRoutesMat += carRouteCrossMatCode[i][0]
                carOutRoutesIndex.remove(i)
                carInRoutesIndex.append(i)
        #-------------------------------------------------------------------------------#
                
                
                
        #print('i:'+str(i)+'--------'+'timeOfNow:'+str(timeOfNow))
        #print(sum(endTimeList >= timeOfNow))
        #sumRoutesMat = sumRoutesMat * 0
        #for j2 in carInRoutes:
            #sumRoutesMat += carRouteCrossMatCode[j2][0]
        #车道数对拥堵程度的影响
        sumRoutesMat[roadMatrix > 0] = sumRoutesMat[roadMatrix > 0] / roadMatrixChannel[roadMatrix > 0]

    return answer

def process_11(car, road, cross):
    #method 11
    
    #create graph matrix
    numOfCross = len(cross.idList)
    #numOfRoad = len(road.idList)
    adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxunicode
    roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixIndex = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixSpeed = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixChannel = np.zeros([numOfCross, numOfCross],dtype = int)
    for i in range(len(road.idList)):
        adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]
        roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
        roadMatrixIndex[road.fromList[i]-1, road.toList[i]-1] = i
        roadMatrixSpeed[road.fromList[i]-1, road.toList[i]-1] = road.speedList[i]
        roadMatrixChannel[road.fromList[i]-1, road.toList[i]-1] = road.channelList[i]
        if(road.isDuplexList[i] == 1):
            adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
            roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
            roadMatrixIndex[road.toList[i]-1, road.fromList[i]-1] = i
            roadMatrixSpeed[road.toList[i]-1, road.fromList[i]-1] = road.speedList[i]
            roadMatrixChannel[road.toList[i]-1, road.fromList[i]-1] = road.channelList[i]
    for i in range(numOfCross):
        adjMatrix[i,i] = 0
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    
    #compute the time of the routes
    sumCrossMat =  np.zeros([numOfCross,numOfCross])
    sumCrossList = [[car.fromList[i],car.toList[i]] for i in range(len(car.idList))]
    routeCrossCarIndex = [[[] for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossCarIndex[sumCrossList[i][0] - 1][sumCrossList[i][1] - 1]
    for i in range(len(sumCrossList)):
        sumCrossMat[sumCrossList[i][0] - 1,sumCrossList[i][1] - 1] += 1
        routeCrossCarIndex[sumCrossList[i][0] - 1][sumCrossList[i][1] - 1].append(i)
        
    #[([np.empty([0],dtype=int)] * numOfCross) for i in range(numOfCross)]
    routeCrossMatCode = [[np.zeros([numOfCross,numOfCross],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    routeCrossList = [[np.empty([0],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossListCode = [[np.zeros([1,numOfRoad],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    sumCrossListIndex = []
    for i in range(numOfCross):
        for j in range(numOfCross):
            if sumCrossMat[i][j] > 0:
                sumCrossListIndex.append([i,j])
                routeCrossList[i][j] = [[routeMin[i][j][i0]-1,routeMin[i][j][i0+1]-1] for i0 in range(len(routeMin[i][j])-1)]
                #routeCrossListCode[i][j] = [roadMatrixIndex[i0,j0] for i0,j0 in routeCrossList[i][j]]
                for i0,j0 in routeCrossList[i][j]:
                    routeCrossMatCode[i][j][i0,j0] = 1
    
    #for i,j in sumCrossListIndex:
        #print(routeCrossCarIndex[i][j])
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    costTimeList = np.zeros(numOfCar, dtype = int)
    endTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    timeOfNow = 0
    carInRoutes = []
    carInRoutesIndex = np.arange(numOfCar)
    carRouteCrossMatCode = [[np.zeros([numOfCross, numOfCross],dtype=int)] for i0 in range(len(car.idList))]
    #carIndexWillStartList = list(np.arange(numOfCar))
    carsNumSumRoutesList = np.zeros([len(sumCrossListIndex),1])
    carOrderIndex = np.zeros([numOfCar,1],dtype=int)
    for iterStep in range(numOfCar):
        if iterStep%100 ==0:
            print(iterStep)
        #choose the car to start in timeOfNow
        
        for i3 in range(len(sumCrossListIndex)):
            #print(sum(sum((sumRoutesMat * routeCrossMatCode[car.fromList[j3]-1][car.toList[j3]-1])>0)))
            #a=sum(sum((sumRoutesMat * routeCrossMatCode[car.fromList[j3]-1][car.toList[j3]-1])>0))
            carsNumSumRoutesList[i3] = sum(sum((sumRoutesMat * routeCrossMatCode[sumCrossListIndex[i3][0]][sumCrossListIndex[i3][1]])))
        
        index_tmp = carsNumSumRoutesList.argmin()
        '''
        print(index_tmp)
        print(len(sumCrossListIndex))
        print(carsNumSumRoutesList)
        print([sumCrossListIndex[index_tmp][0],sumCrossListIndex[index_tmp][1]])
        print(routeCrossCarIndex[sumCrossListIndex[index_tmp][0]][sumCrossListIndex[index_tmp][1]])
        '''
        i = routeCrossCarIndex[sumCrossListIndex[index_tmp][0]][sumCrossListIndex[index_tmp][1]].pop()
        #print(str(iterStep)+'------'+str(i))
        if len(routeCrossCarIndex[sumCrossListIndex[index_tmp][0]][sumCrossListIndex[index_tmp][1]]) == 0:
            del sumCrossListIndex[index_tmp]
            carsNumSumRoutesList = np.delete(carsNumSumRoutesList, index_tmp,axis=0)
        carOrderIndex[iterStep] = i
        #print(carsNumSumRoutesList.min(),carsNumSumRoutesList.max())
        carsNumSumRoutesList = carsNumSumRoutesList * 0
        
        #carIndexWillStartList = np.delete(carIndexWillStartList,carsNumSumRoutesList.argmin(),axis=0)
        #print(max(carsNumSumRoutesList))
        
        #if i%100 ==0:
            #print(i)
            #distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 300, numOfCross)
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        routeCrossListCode_0 = [roadMatrixIndex[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        roadIdList = [road.idList[i] for i in routeCrossListCode_0]
        for j1 in range(len(routeMin[i0][j0])-1):
            carRouteCrossMatCode[i][0][routeMin[i0][j0][j1]-1,routeMin[i0][j0][j1+1]-1] += 1
        if iterStep>1000:
            timeOfNow = math.floor((iterStep-1000) / 32)
        else:
            timeOfNow = car.planTimeList[i]
        planTimeList[i] = max(timeOfNow,car.planTimeList[i])
        costTime_tmp = [road.lengthList[i] for i in routeCrossListCode_0]
        costTime_tmp2 = [road.speedList[i] for i in routeCrossListCode_0]
        costTime_tmp3 = np.vstack((costTime_tmp2,car.speedList[i] * np.ones([1,len(routeCrossListCode_0)]))).min(0)
        costTimeList[i] = sum(costTime_tmp / costTime_tmp3)
        endTimeList[i] =  planTimeList[i] + costTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        carInRoutes = carInRoutesIndex[endTimeList >= timeOfNow]
        #print('i:'+str(i)+'--------'+'timeOfNow:'+str(timeOfNow))
        #print(sum(endTimeList >= timeOfNow))
        sumRoutesMat = sumRoutesMat * 0
        for j2 in carInRoutes:
            sumRoutesMat += carRouteCrossMatCode[j2][0]
        #sumRoutesMat[roadMatrix > 0] = sumRoutesMat[roadMatrix > 0] / roadMatrixChannel[roadMatrix > 0]
        #print(sumRoutesMat)
        
    #write the carOrderIndex
    
    fid = open('carOrderIndex.txt','w')
    for i4 in carOrderIndex:
        fid.writelines(str(i4)[1:-1] + '\n')
    fid.close()
    
    
    #print('process finish')
    return answer

def process_12(car, road, cross):
    #method 12
    
    #read the carOrderIndex
    carOrderIndex = []
    fid = open('src/carOrderIndex_2.txt','r')
    for line in fid.readlines():
        line = line.replace('\n','')
        #print(line)
        carOrderIndex.append(int(line))
    #carOrderIndex = np.array(carOrderIndex)
    #print(str(carOrderIndex[0]))
    fid.close()
    
    #create graph matrix
    numOfCross = len(cross.idList)
    #numOfRoad = len(road.idList)
    adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxunicode
    roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixIndex = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixSpeed = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixChannel = np.zeros([numOfCross, numOfCross],dtype = int)
    for i in range(len(road.idList)):
        adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]
        roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
        roadMatrixIndex[road.fromList[i]-1, road.toList[i]-1] = i
        roadMatrixSpeed[road.fromList[i]-1, road.toList[i]-1] = road.speedList[i]
        roadMatrixChannel[road.fromList[i]-1, road.toList[i]-1] = road.channelList[i]
        if(road.isDuplexList[i] == 1):
            adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
            roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
            roadMatrixIndex[road.toList[i]-1, road.fromList[i]-1] = i
            roadMatrixSpeed[road.toList[i]-1, road.fromList[i]-1] = road.speedList[i]
            roadMatrixChannel[road.toList[i]-1, road.fromList[i]-1] = road.channelList[i]
    for i in range(numOfCross):
        adjMatrix[i,i] = 0
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    
    #compute the time of the routes
    sumCrossMat =  np.zeros([numOfCross,numOfCross])
    sumCrossList = [[car.fromList[i],car.toList[i]] for i in range(len(car.idList))]
    routeCrossCarIndex = [[[] for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossCarIndex[sumCrossList[i][0] - 1][sumCrossList[i][1] - 1]
    for i in range(len(sumCrossList)):
        sumCrossMat[sumCrossList[i][0] - 1,sumCrossList[i][1] - 1] += 1
        routeCrossCarIndex[sumCrossList[i][0] - 1][sumCrossList[i][1] - 1].append(i)
        
    #[([np.empty([0],dtype=int)] * numOfCross) for i in range(numOfCross)]
    routeCrossMatCode = [[np.zeros([numOfCross,numOfCross],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    routeCrossList = [[np.empty([0],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossListCode = [[np.zeros([1,numOfRoad],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    sumCrossListIndex = []
    for i in range(numOfCross):
        for j in range(numOfCross):
            if sumCrossMat[i][j] > 0:
                sumCrossListIndex.append([i,j])
                routeCrossList[i][j] = [[routeMin[i][j][i0]-1,routeMin[i][j][i0+1]-1] for i0 in range(len(routeMin[i][j])-1)]
                #routeCrossListCode[i][j] = [roadMatrixIndex[i0,j0] for i0,j0 in routeCrossList[i][j]]
                for i0,j0 in routeCrossList[i][j]:
                    routeCrossMatCode[i][j][i0,j0] = 1
    
    #for i,j in sumCrossListIndex:
        #print(routeCrossCarIndex[i][j])
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    costTimeList = np.zeros(numOfCar, dtype = int)
    endTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    timeOfNow = 0
    carInRoutes = []
    carInRoutesIndex = np.arange(numOfCar)
    carRouteCrossMatCode = [[np.zeros([numOfCross, numOfCross],dtype=int)] for i0 in range(len(car.idList))]
    #carIndexWillStartList = list(np.arange(numOfCar))
    #carsNumSumRoutesList = np.zeros([len(sumCrossListIndex),1])
    for iterStep in range(numOfCar):
        if iterStep%1000 ==0:
            print(iterStep)
        #choose the car to start in timeOfNow
        i = carOrderIndex[iterStep]
        #i = iterStep
        #print(carOrderIndex[0])
        #print(str(iterStep)+'------'+str(i))
        
        #if i%100 ==0:
            #print(i)
            #distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 300, numOfCross)
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        routeCrossListCode_0 = [roadMatrixIndex[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        roadIdList = [road.idList[i] for i in routeCrossListCode_0]
        for j1 in range(len(routeMin[i0][j0])-1):
            carRouteCrossMatCode[i][0][routeMin[i0][j0][j1]-1,routeMin[i0][j0][j1+1]-1] += 1
        if iterStep>400:
            timeOfNow = math.floor((iterStep-400) / 7)
        else:
            timeOfNow = car.planTimeList[i]
        planTimeList[i] = max(timeOfNow,car.planTimeList[i])
        costTime_tmp = [road.lengthList[i] for i in routeCrossListCode_0]
        costTime_tmp2 = [road.speedList[i] for i in routeCrossListCode_0]
        costTime_tmp3 = np.vstack((costTime_tmp2,car.speedList[i] * np.ones([1,len(routeCrossListCode_0)]))).min(0)
        costTimeList[i] = sum(costTime_tmp / costTime_tmp3)
        endTimeList[i] =  planTimeList[i] + costTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        carInRoutes = carInRoutesIndex[endTimeList >= timeOfNow]
        #print('i:'+str(i)+'--------'+'timeOfNow:'+str(timeOfNow))
        #print(sum(endTimeList >= timeOfNow))
        sumRoutesMat = sumRoutesMat * 0
        for j2 in carInRoutes:
            sumRoutesMat += carRouteCrossMatCode[j2][0]
        sumRoutesMat[roadMatrix > 0] = sumRoutesMat[roadMatrix > 0] / roadMatrixChannel[roadMatrix > 0]
        #print(sumRoutesMat)
    
    #print('process finish')
    #,routeCrossMatCode,routeCrossList,roadMatrixIndex,routeCrossCarIndex
    return answer

def process_13(car, road, cross):
    #method 13
    
    #create graph matrix
    numOfCross = len(cross.idList)
    #numOfRoad = len(road.idList)
    adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxunicode
    roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixIndex = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixSpeed = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixChannel = np.zeros([numOfCross, numOfCross],dtype = int)
    for i in range(len(road.idList)):
        adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]
        roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
        roadMatrixIndex[road.fromList[i]-1, road.toList[i]-1] = i
        roadMatrixSpeed[road.fromList[i]-1, road.toList[i]-1] = road.speedList[i]
        roadMatrixChannel[road.fromList[i]-1, road.toList[i]-1] = road.channelList[i]
        if(road.isDuplexList[i] == 1):
            adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
            roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
            roadMatrixIndex[road.toList[i]-1, road.fromList[i]-1] = i
            roadMatrixSpeed[road.toList[i]-1, road.fromList[i]-1] = road.speedList[i]
            roadMatrixChannel[road.toList[i]-1, road.fromList[i]-1] = road.channelList[i]
    for i in range(numOfCross):
        adjMatrix[i,i] = 0
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    
    #compute the time of the routes
    sumCrossMat =  np.zeros([numOfCross,numOfCross])
    sumCrossList = [[car.fromList[i],car.toList[i]] for i in range(len(car.idList))]
    routeCrossCarIndex = [[[] for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossCarIndex[sumCrossList[i][0] - 1][sumCrossList[i][1] - 1]
    for i in range(len(sumCrossList)):
        sumCrossMat[sumCrossList[i][0] - 1,sumCrossList[i][1] - 1] += 1
        routeCrossCarIndex[sumCrossList[i][0] - 1][sumCrossList[i][1] - 1].append(i)
        
    #[([np.empty([0],dtype=int)] * numOfCross) for i in range(numOfCross)]
    routeCrossMatCode = [[np.zeros([numOfCross,numOfCross],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    routeCrossList = [[np.empty([0],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossListCode = [[np.zeros([1,numOfRoad],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    sumCrossListIndex = []
    for i in range(numOfCross):
        for j in range(numOfCross):
            if sumCrossMat[i][j] > 0:
                sumCrossListIndex.append([i,j])
                routeCrossList[i][j] = [[routeMin[i][j][i0]-1,routeMin[i][j][i0+1]-1] for i0 in range(len(routeMin[i][j])-1)]
                #routeCrossListCode[i][j] = [roadMatrixIndex[i0,j0] for i0,j0 in routeCrossList[i][j]]
                for i0,j0 in routeCrossList[i][j]:
                    routeCrossMatCode[i][j][i0,j0] = 1
    
    #for i,j in sumCrossListIndex:
        #print(routeCrossCarIndex[i][j])
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    costTimeList = np.zeros(numOfCar, dtype = int)
    endTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    timeOfNow = 0
    carInRoutes = []
    carInRoutesIndex = np.arange(numOfCar)
    carRouteCrossMatCode = [[np.zeros([numOfCross, numOfCross],dtype=int)] for i0 in range(len(car.idList))]
    #carIndexWillStartList = list(np.arange(numOfCar))
    carsNumSumRoutesList = np.zeros([len(sumCrossListIndex),1])
    carOrderIndex = np.zeros([numOfCar,1],dtype=int)
    for iterStep in range(numOfCar):
        if iterStep%100 ==0:
            print(iterStep)
        #choose the car to start in timeOfNow
        
        for i3 in range(len(sumCrossListIndex)):
            #print(sum(sum((sumRoutesMat * routeCrossMatCode[car.fromList[j3]-1][car.toList[j3]-1])>0)))
            #a=sum(sum((sumRoutesMat * routeCrossMatCode[car.fromList[j3]-1][car.toList[j3]-1])>0))
            carsNumSumRoutesList[i3] = sum(sum((sumRoutesMat * routeCrossMatCode[sumCrossListIndex[i3][0]][sumCrossListIndex[i3][1]])))
        
        index_tmp = carsNumSumRoutesList.argmin()
        '''
        print(index_tmp)
        print(len(sumCrossListIndex))
        print(carsNumSumRoutesList)
        print([sumCrossListIndex[index_tmp][0],sumCrossListIndex[index_tmp][1]])
        print(routeCrossCarIndex[sumCrossListIndex[index_tmp][0]][sumCrossListIndex[index_tmp][1]])
        '''
        i = routeCrossCarIndex[sumCrossListIndex[index_tmp][0]][sumCrossListIndex[index_tmp][1]].pop()
        #print(str(iterStep)+'------'+str(i))
        if len(routeCrossCarIndex[sumCrossListIndex[index_tmp][0]][sumCrossListIndex[index_tmp][1]]) == 0:
            del sumCrossListIndex[index_tmp]
            carsNumSumRoutesList = np.delete(carsNumSumRoutesList, index_tmp,axis=0)
        carOrderIndex[iterStep] = i
        #print(carsNumSumRoutesList.min(),carsNumSumRoutesList.max())
        carsNumSumRoutesList = carsNumSumRoutesList * 0
        
        #carIndexWillStartList = np.delete(carIndexWillStartList,carsNumSumRoutesList.argmin(),axis=0)
        #print(max(carsNumSumRoutesList))
        
        #if i%100 ==0:
            #print(i)
            #distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 300, numOfCross)
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        routeCrossListCode_0 = [roadMatrixIndex[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        roadIdList = [road.idList[i] for i in routeCrossListCode_0]
        for j1 in range(len(routeMin[i0][j0])-1):
            carRouteCrossMatCode[i][0][routeMin[i0][j0][j1]-1,routeMin[i0][j0][j1+1]-1] += 1
        if iterStep>1000:
            timeOfNow = math.floor((iterStep-1000) / 32)
        else:
            timeOfNow = car.planTimeList[i]
        planTimeList[i] = max(timeOfNow,car.planTimeList[i])
        costTime_tmp = [road.lengthList[i] for i in routeCrossListCode_0]
        costTime_tmp2 = [road.speedList[i] for i in routeCrossListCode_0]
        costTime_tmp3 = np.vstack((costTime_tmp2,car.speedList[i] * np.ones([1,len(routeCrossListCode_0)]))).min(0)
        costTimeList[i] = sum(costTime_tmp / costTime_tmp3)
        endTimeList[i] =  planTimeList[i] + costTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        carInRoutes = carInRoutesIndex[endTimeList >= timeOfNow]
        #print('i:'+str(i)+'--------'+'timeOfNow:'+str(timeOfNow))
        #print(sum(endTimeList >= timeOfNow))
        sumRoutesMat = sumRoutesMat * 0
        for j2 in carInRoutes:
            sumRoutesMat += carRouteCrossMatCode[j2][0]
        sumRoutesMat[roadMatrix > 0] = sumRoutesMat[roadMatrix > 0] - roadMatrixChannel[roadMatrix > 0]
        sumRoutesMat[sumRoutesMat < 0] = 0
        #print(sumRoutesMat)
        
    #write the carOrderIndex
    
    fid = open('carOrderIndex.txt','w')
    for i4 in carOrderIndex:
        fid.writelines(str(i4)[1:-1] + '\n')
    fid.close()
    
    
    #print('process finish')
    return answer

def process_14(car, road, cross):
    #method 14
    
    #create graph matrix
    numOfCross = len(cross.idList)
    #numOfRoad = len(road.idList)
    adjMatrix = np.zeros([numOfCross, numOfCross]) + sys.maxunicode
    carFromToMatrixBool = np.zeros([numOfCross, numOfCross]) + sys.maxsize
    roadMatrix = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixIndex = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixSpeed = np.zeros([numOfCross, numOfCross],dtype = int)
    roadMatrixChannel = np.zeros([numOfCross, numOfCross],dtype = int)
    for i in range(len(road.idList)):
        adjMatrix[road.fromList[i]-1, road.toList[i]-1] = road.lengthList[i]
        roadMatrix[road.fromList[i]-1, road.toList[i]-1] = road.idList[i]
        roadMatrixIndex[road.fromList[i]-1, road.toList[i]-1] = i
        roadMatrixSpeed[road.fromList[i]-1, road.toList[i]-1] = road.speedList[i]
        roadMatrixChannel[road.fromList[i]-1, road.toList[i]-1] = road.channelList[i]
        if(road.isDuplexList[i] == 1):
            adjMatrix[road.toList[i]-1, road.fromList[i]-1] = road.lengthList[i]
            roadMatrix[road.toList[i]-1, road.fromList[i]-1] = road.idList[i]
            roadMatrixIndex[road.toList[i]-1, road.fromList[i]-1] = i
            roadMatrixSpeed[road.toList[i]-1, road.fromList[i]-1] = road.speedList[i]
            roadMatrixChannel[road.toList[i]-1, road.fromList[i]-1] = road.channelList[i]
    for i in range(numOfCross):
        adjMatrix[i,i] = 0
        
    #compute the min distance by floyd
    distanceMin, routeMin = floyd(adjMatrix, numOfCross)
    
    #sum Of the routes
    sumRoutesMat = np.zeros([numOfCross, numOfCross],dtype = int)
    
    #compute the time of the routes
    sumCrossMat =  np.zeros([numOfCross,numOfCross])
    sumCrossList = [[car.fromList[i],car.toList[i]] for i in range(len(car.idList))]
    routeCrossCarIndex = [[[] for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossCarIndex[sumCrossList[i][0] - 1][sumCrossList[i][1] - 1]
    for i in range(len(sumCrossList)):
        sumCrossMat[sumCrossList[i][0] - 1,sumCrossList[i][1] - 1] += 1
        carFromToMatrixBool[sumCrossList[i][0] - 1,sumCrossList[i][1] - 1] = 1
        routeCrossCarIndex[sumCrossList[i][0] - 1][sumCrossList[i][1] - 1].append(i)
        
    #[([np.empty([0],dtype=int)] * numOfCross) for i in range(numOfCross)]
    routeCrossMatCode = [[np.zeros([numOfCross,numOfCross],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    routeCrossList = [[np.empty([0],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    #routeCrossListCode = [[np.zeros([1,numOfRoad],dtype=int) for i0 in range(numOfCross)] for i1 in range(numOfCross)]
    sumCrossListIndex = []
    for i in range(numOfCross):
        for j in range(numOfCross):
            if sumCrossMat[i][j] > 0:
                sumCrossListIndex.append([i,j])
                routeCrossList[i][j] = [[routeMin[i][j][i0]-1,routeMin[i][j][i0+1]-1] for i0 in range(len(routeMin[i][j])-1)]
                #routeCrossListCode[i][j] = [roadMatrixIndex[i0,j0] for i0,j0 in routeCrossList[i][j]]
                for i0,j0 in routeCrossList[i][j]:
                    routeCrossMatCode[i][j][i0,j0] = 1
    
    #for i,j in sumCrossListIndex:
        #print(routeCrossCarIndex[i][j])
    
    #answer
    numOfCar = len(car.idList)
    planTimeList = np.zeros(numOfCar, dtype = int)
    costTimeList = np.zeros(numOfCar, dtype = int)
    endTimeList = np.zeros(numOfCar, dtype = int)
    answer = [[''] for i in range(numOfCar)]
    timeOfNow = 0
    carInRoutes = []
    carInRoutesIndex = np.arange(numOfCar)
    carRouteCrossMatCode = [[np.zeros([numOfCross, numOfCross],dtype=int)] for i0 in range(len(car.idList))]
    #carIndexWillStartList = list(np.arange(numOfCar))
    #carsNumSumRoutesList = np.zeros([len(sumCrossListIndex),1])
    #carOrderIndex = np.zeros([numOfCar,1],dtype=int)
    for iterStep in range(numOfCar):
        #i = iterStep
        if iterStep%100 ==0:
            print(iterStep)
        #choose the car to start in timeOfNow
        #i = iterStep
        '''
        for i3 in range(len(sumCrossListIndex)):
            #print(sum(sum((sumRoutesMat * routeCrossMatCode[car.fromList[j3]-1][car.toList[j3]-1])>0)))
            #a=sum(sum((sumRoutesMat * routeCrossMatCode[car.fromList[j3]-1][car.toList[j3]-1])>0))
            carsNumSumRoutesList[i3] = sum(sum((sumRoutesMat * routeCrossMatCode[sumCrossListIndex[i3][0]][sumCrossListIndex[i3][1]])))
        
        index_tmp = carsNumSumRoutesList.argmin()
        i = routeCrossCarIndex[sumCrossListIndex[index_tmp][0]][sumCrossListIndex[index_tmp][1]].pop()
        #print(str(iterStep)+'------'+str(i))
        if len(routeCrossCarIndex[sumCrossListIndex[index_tmp][0]][sumCrossListIndex[index_tmp][1]]) == 0:
            del sumCrossListIndex[index_tmp]
            carsNumSumRoutesList = np.delete(carsNumSumRoutesList, index_tmp,axis=0)
        carOrderIndex[iterStep] = i
        #print(carsNumSumRoutesList.min(),carsNumSumRoutesList.max())
        carsNumSumRoutesList = carsNumSumRoutesList * 0
        '''
        #carIndexWillStartList = np.delete(carIndexWillStartList,carsNumSumRoutesList.argmin(),axis=0)
        #print(max(carsNumSumRoutesList))
        
        if iterStep%100 ==0:
            #print(iterStep)
            distanceMin, routeMin = floyd(adjMatrix + sumRoutesMat * 300, numOfCross)
        distanceMin = distanceMin * carFromToMatrixBool
        index_tmp2 = np.unravel_index(distanceMin.argmin(), distanceMin.shape)
        #print(distanceMin)
        
        #print(distanceMin.min())
        #print(index_tmp2)
        #print(routeCrossCarIndex[index_tmp2[0]][index_tmp2[1]])
        i = routeCrossCarIndex[index_tmp2[0]][index_tmp2[1]].pop()
        if len(routeCrossCarIndex[index_tmp2[0]][index_tmp2[1]]) == 0:
            carFromToMatrixBool[index_tmp2] = sys.maxsize
        
        i0 = car.fromList[i] - 1
        j0 = car.toList[i] - 1
        routeCrossListCode_0 = [roadMatrixIndex[routeMin[i0][j0][i]-1,routeMin[i0][j0][i+1]-1] for i in range(len(routeMin[i0][j0])-1)]
        roadIdList = [road.idList[i] for i in routeCrossListCode_0]
        for j1 in range(len(routeMin[i0][j0])-1):
            carRouteCrossMatCode[i][0][routeMin[i0][j0][j1]-1,routeMin[i0][j0][j1+1]-1] += 1
        if iterStep>1000:
            timeOfNow = math.floor((iterStep-1000) / 28)
        else:
            timeOfNow = car.planTimeList[i]
        planTimeList[i] = max(timeOfNow,car.planTimeList[i])
        costTime_tmp = [road.lengthList[i] for i in routeCrossListCode_0]
        costTime_tmp2 = [road.speedList[i] for i in routeCrossListCode_0]
        costTime_tmp3 = np.vstack((costTime_tmp2,car.speedList[i] * np.ones([1,len(routeCrossListCode_0)]))).min(0)
        costTimeList[i] = sum(costTime_tmp / costTime_tmp3)
        endTimeList[i] =  planTimeList[i] + costTimeList[i]
        answer[i] = str(car.idList[i]) + ', ' + str(planTimeList[i]) + ', ' + str(roadIdList)[1 : -1]
        carInRoutes = carInRoutesIndex[endTimeList >= timeOfNow]
        #print('i:'+str(i)+'--------'+'timeOfNow:'+str(timeOfNow))
        #print(len(carInRoutes))
        sumRoutesMat = sumRoutesMat * 0
        for j2 in carInRoutes:
            sumRoutesMat += carRouteCrossMatCode[j2][0]
        #sumRoutesMat[roadMatrix > 0] = sumRoutesMat[roadMatrix > 0] / roadMatrixChannel[roadMatrix > 0]
        #print(sumRoutesMat)
        
    #write the carOrderIndex
    '''
    fid = open('carOrderIndex.txt','w')
    for i4 in carOrderIndex:
        fid.writelines(str(i4)[1:-1] + '\n')
    fid.close()
    '''
    
    #print('process finish')
    return answer