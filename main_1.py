            #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:07:37 2019

@author: wanchao
"""
import sys
sys.path.append('src')
from readInputFile import readCarFile,readRoadFile,readCrossFile
from processFun1 import process_10_1 as process
from writeOutputFile import writeAnswerFile
import datetime


'''
car_path = '../../../../1-map-training-4/car.txt'
road_path = '../../../../1-map-training-4/road.txt'
cross_path = '../../../../1-map-training-4/cross.txt'
answer_path = '../../../../1-map-training-4/answer.txt'
'''


car_path = '../config/1-map-exam-1/car.txt'
road_path = '../config/1-map-exam-1/road.txt'
cross_path = '../config/1-map-exam-1/cross.txt'
answer_path = '../config/1-map-exam-1/answer.txt'


'''
car_path = '../config/car.txt'
road_path = '../config/road.txt'
cross_path = '../config/cross.txt'
answer_path = '../config/answer.txt'
'''

# to read input file
car = readCarFile(car_path)
road = readRoadFile(road_path)
cross =  readCrossFile(cross_path)

#cross number re order
#因为cross路口的编号，不是依次顺序过去的，可能是100,230,500，所以这里对其重新排了一下变成1,2,3
#然后road和car里面记录的cross路口编号，也要相应重排一下

for i in range(len(road.idList)):
    road.fromList[i] = cross.idList.tolist().index(road.fromList[i]) + 1
    road.toList[i] = cross.idList.tolist().index(road.toList[i]) + 1
for i in range(len(car.idList)):
    car.fromList[i] = cross.idList.tolist().index(car.fromList[i]) + 1
    car.toList[i] = cross.idList.tolist().index(car.toList[i]) + 1

# process
starttime = datetime.datetime.now()
answer = process(car, road, cross)
#,routeCrossMatCode,routeCrossList,roadMatrixIndex
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)

# to write output file
writeAnswerFile(answer_path, answer)