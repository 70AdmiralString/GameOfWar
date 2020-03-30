import numpy as np

directions = np.array([[1,1],[1,0],[1,-1],[0,1],[0,0],[0,-1],[-1,1],[-1,0],[-1,-1]]); #Every valid straight line direction as a vector. Plus the zero-vector.

class gamePiece:
    ''' 
        This class represents a single piece on the game board.  
        It possesses general methods and attributes which any piece will need.
    '''
    
    def __init__(self, xLocation, yLocation):
        self.location = np.array([xLocation,yLocation])
        
        self.pieceType = '';
        self.icon = [];
        
        self.moveRange = 0;
        
        self.attackRange = 0;
        self.attackPower = 0;
        self.supportPower = 0;
        
        self.threatenedValue = 0;
        self.supportedValue = 0; 
          
    def movementRange(self): 
        '''A function which returns a list of all possible location coordinates that can be reached by this piece. Does not account for terrain, supply lines, or other pieces. '''
        
        width = 2 * self.moveRange + 1;
        result = np.zeros([width**2, 2]);
        for i in range(width**2):
            result[i] = [i//width - self.moveRange, i%width - self.moveRange];
        return (self.location + result)
            
    def adjacentSquares(self):
        return (self.location + directions)
    
    def attackSupportRange(self):
        result = np.zeros([1 + 8 * self.attackRange, 2]);
        for i in range(8 * self.attackRange):
            result[i + 1] = (1 + i//8) * directions[i%8];
        return (self.location + result)
        
    def move(self, newXLoc, newYLoc):
        self.location = np.array([newXLoc,newYLoc])
        
    