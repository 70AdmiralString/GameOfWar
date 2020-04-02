#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def vec_remove(point_list, point):
    '''
        Outputs point_list, except with all entries equal to point removed.
            
            point_list is a list of vectors
            point is a single vector
    '''
    indices = [i for i in range(len(point_list)) if point_list[i] != point]
    result = [point_list[i] for i in indices]
    return result
    
def vec_remove_list(point_list1, point_list2):
    '''
        Outputs point_list1, except with all entries which appear in point_list2 removed.
            
            point_list1 and point_list2 are both lists of vectors.
    '''
    for point in point_list2:
        point_list1 = vec_remove(point_list1, point)
    return point_list1

class Vector(object):
    def __init__(self, *args):
        """ 
            Create a vector, example: v = Vector(1,2) 
            The methods included here are intended to be sufficient operations for the class of integer vectors.
        """
        if len(args)==0: self.values = (0,0)
        else: self.values = args
        
    def norm_sq(self):
        """ 
            Returns the norm squared (length, magnitude) of the vector 
        """
        return sum( comp**2 for comp in self )
        
    def matrix_mult(self, matrix):
        """ 
            Multiply this vector by a matrix.  Assuming matrix is a list of lists.
        
            Example:
            mat = [[1,2,3],[-1,0,1],[3,4,5]]
            Vector(1,2,3).matrix_mult(mat) ->  (14, 2, 26)
         
        """
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError('Matrix must match vector dimensions') 
        
        # Grab a row from the matrix, make it a Vector, take the dot product, 
        # and store it as the first component
        product = tuple(Vector(*row)*self for row in matrix)
        
        return Vector(*product)
    
    def inner(self, other):
        """ 
            Returns the dot product (inner product) of self and other vector
        """
        return sum(a * b for a, b in zip(self, other))
    
    def __mul__(self, other):
        """ 
            Returns the dot product of self and other if multiplied
                by another Vector.  If multiplied by an int or float,
                multiplies each component by other.
        """
        if type(other) == type(self):
            return self.inner(other)
        elif type(other) == type(1) or type(other) == type(1.0):
            product = tuple( a * other for a in self )
            return Vector(*product)
    
    def __rmul__(self, other):
        """ 
            Called if 4*self for instance 
        """
        return self.__mul__(other)
            
    def __div__(self, other):
        if type(other) == type(1) or type(other) == type(1.0):
            divided = tuple( a / other for a in self )
            return Vector(*divided)
    
    def __add__(self, other):
        """ 
            Returns the vector addition of self and other 
        """
        added = tuple( a + b for a, b in zip(self, other) )
        return Vector(*added)
    
    def __sub__(self, other):
        """ 
            Returns the vector difference of self and other 
        """
        subbed = tuple( a - b for a, b in zip(self, other) )
        return Vector(*subbed)
    
    def __eq__(self, other):
        """
            Determines if this vector is identical to other
        """
        if type(other) != type(self):
            return False
        difference = self - other;
        return difference.norm_sq() == 0
    
    def __ne__(self, other):
        """
            The negation of equals
        """
        return not self.__eq__(other)
    
    def __iter__(self):
        return self.values.__iter__()
    
    def __len__(self):
        return len(self.values)
    
    def __getitem__(self, key):
        return self.values[key]
        
    def __repr__(self):
        return str(self.values)