#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Numpy replacement functions
    
        This module contains a number of functions intended to replace numpy functionality with 
            equivalent functionality based upon lists of tuples of integers.
'''

DATA_TYPE = int;

def tupleAdd(tuple1, tuple2):
    '''
        Adds two tuples element-wise, where each tuple is the same size.
    '''
    result = [0] * len(tuple1);
    for i in range(len(tuple1)):
        result[i] = tuple1[i] + tuple2[i];
    return tuple(result)

def tupleListAdd(tupleList, toBeAdded):
    '''
        Adds toBeAdded to each entry of tupleList element-wise.
        
        tupleList is a list of tuples all of the same length n
        toBeAdded is a tuple of length n
    '''
    result = list(map(lambda x : tupleAdd(x, toBeAdded), tupleList));
    return result

def tupleConstMult(tuple1, const):
    '''
        Multiplies tuple1 by a constant factor const.
    '''
    result = [0] * len(tuple1);
    for i in range(len(tuple1)):
        result[i] = const * tuple1[i];
    return tuple(result)
    

def tupleMult(tuple1, tuple2):
    '''
        Multiplies two tuples element-wise, where each tuple is the same size.
    '''
    result = [0] * len(tuple1);
    for i in range(len(tuple1)):
        result[i] = tuple1[i] * tuple2[i];
    return tuple(result)

def tupleListMult(tupleList, toBeAdded):
    '''
        Multiplies toBeAdded by each entry of tupleList element-wise.
        
        tupleList is a list of tuples all of the same length n
        toBeAdded is a tuple of length n
    '''
    result = list(map(lambda x : tupleMult(x, toBeAdded), tupleList));
    return result

# From here on, our lists are assumed to consist of tuples of type DATA_TYPE of length 2;
def distanceSq(point1, point2):
    '''
        Outputs an integer corresonding to the squared Euclidean distance between point1 and point2.
    '''
    difference = tupleAdd(point1,tupleConstMult(point2, -1));   
    result = sum(tupleMult(difference, difference));
    return result

def distanceSqList(pointList, specificPoint):
    '''
        Outputs a list of integers corresponding to the squared Euclidean distances from 
            each point in pointList to the specified point.
    '''
    result = list(map(lambda x : distanceSq(x, specificPoint), pointList));
    return result
    
def remove(pointList, point):
    '''
        Outputs pointList, except with all entries equal to point removed.
        
            pointList is a list of tuples
            point is a single tuple
    '''
    indices = [i for i in range(len(pointList)) if pointList[i] != point];
    result = [pointList[i] for i in indices];
    return result

def removeList(pointList1, pointList2):
    '''
        Outputs pointList1, except with all entries which appear in pointList2 removed.
        
            pointList1 and pointList2 are both lists of tuples.
    '''
    for point in pointList2:
        pointList1 = remove(pointList1, point);
    return pointList1























































