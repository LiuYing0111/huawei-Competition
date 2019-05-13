#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 23:25:07 2019

@author: wanchao
"""
import numpy as np
from collections import defaultdict
from heapq import heappop, heappush
from copy import copy
import sys

def floyd(l, n):
    '''
    l: l[i][j] = distace of i and j if <i, j> in E else sys.maxint
    k: sum of point
    '''
    d = copy(l[:])
    
    route = [([np.empty([0],dtype=int) for i0 in range(n)]) for i1 in range(n)]
    for i in range(n):
        for j in range(n):
            if d[i][j]:
                route[i][j] = np.r_[i + 1,j + 1]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    #route[i][j] = route[i][k] + " " + route[k][j][2:]
                    #route[i][j] = np.r_[route[i][k],route[k][j][1:]]
                    route[i][j] = np.append(route[i][k],route[k][j][1:])
    for i in range(n):
#最大支持的长度sys.maxsize
        d[i,i] = sys.maxsize
    return d, route
 
def dijkstra_raw(edges, from_node, to_node):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))
    q, seen = [(0,from_node,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
			seen.add(v1)
			path = (v1, path)
			if v1 == to_node:
				return cost,path
			for c, v2 in g.get(v1, ()):
				if v2 not in seen:
					heappush(q, (cost+c, v2, path))
	return float("inf"),[]
 
def dijkstra(edges, from_node, to_node):
	len_shortest_path = -1
	ret_path=[]
	length,path_queue = dijkstra_raw(edges, from_node, to_node)
	if len(path_queue)>0:
		len_shortest_path = length		## 1. Get the length firstly;
		## 2. Decompose the path_queue, to get the passing nodes in the shortest path.
		left = path_queue[0]
		ret_path.append(left)		## 2.1 Record the destination node firstly;
		right = path_queue[1]
		while len(right)>0:
			left = right[0]
			ret_path.append(left)	## 2.2 Record other nodes, till the source-node.
			right = right[1]
		ret_path.reverse()	## 3. Reverse the list finally, to make it be normal sequence.
	return len_shortest_path,ret_path