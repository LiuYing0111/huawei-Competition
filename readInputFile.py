#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 15:12:21 2019

@author: wanchao
"""
import numpy as np

class Car:
    idList = []
    fromList = []
    toList = []
    speedList = []
    planTimeList = []

class Road:
    idList = []
    lengthList = []
    speedList = []
    channelList = []
    fromList = []
    toList = []
    isDuplexList = []

class Cross:
    idList = []
    roadId = []

#数据处理
def readFile(path):
    dataList = []
    fid = open(path,'r')
    for line in fid.readlines()[1:]:
        line = line.replace('(','')
        line = line.replace(')','')
        line = line.replace('\n','')
        #print(line)
        data = [int(i) for i in line.split(', ')]
        dataList.append(data)
    dataList = np.array(dataList)
    fid.close()
    return dataList

def readCarFile(car_path):
    dataList = readFile(car_path)
    car = Car()
    car.idList = dataList[:,0]
    car.fromList = dataList[:,1]
    car.toList = dataList[:,2]
    car.speedList = dataList[:,3]
    car.planTimeList = dataList[:,4]
    return car

def readRoadFile(road_path):
    dataList = readFile(road_path)
    road = Road()
    road.idList = dataList[:,0]
    road.lengthList = dataList[:,1]
    road.speedList = dataList[:,2]
    road.channelList = dataList[:,3]
    road.fromList = dataList[:,4]
    road.toList = dataList[:,5]
    road.isDuplexList = dataList[:,6]
    return road

def readCrossFile(cross_path):
    dataList = readFile(cross_path)
    cross = Cross()
    cross.idList = dataList[:,0]
    cross.roadId = dataList[:,1:]
    return cross