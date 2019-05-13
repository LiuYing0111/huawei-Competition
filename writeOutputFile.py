#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 02:35:15 2019

@author: wanchao
"""

def writeAnswerFile(answer_path, answer):
    
    fid = open(answer_path,'w')
    fid.writelines('#(carId,StartTime,RoadId...)'+'\n')
    for i in range(len(answer)):
        fid.writelines('(' + answer[i] + ')\n')
    fid.close()
    
    #print('write finish')