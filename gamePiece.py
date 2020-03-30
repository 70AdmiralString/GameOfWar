import numpy as np

DIRECTIONS = np.array([[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]); #Every valid straight line direction as a vector. Plus the zero-vector.

class GamePiece:
    ''' 
        This class represents a single piece on the game board.  
        It possesses general methods and attributes which any piece will need.
    '''
    
    def __init__(self, xLocation, yLocation):
        self.location = np.array([xLocation,yLocation])
        self.inCommunication = True;
        
        self.pieceType = '';
        self.icon = [];
        
        self.moveRange = 0;

        
        self.attackRange = 0;
        self.attackPower = 0;
        self.supportPower = 0;
        
        self.threatenedValue = 0;
        self.supportedValue = 0; 
          
    def movementRange(self): 
        '''
            A function which returns a list of all possible location coordinates that can be reached by this piece. 
            Does not account for terrain, communication lines, or other pieces. 
        '''
        
        width = 2 * self.moveRange + 1;
        result = np.zeros([width**2, 2]);
        for i in range(width**2):
            result[i] = [i//width - self.moveRange, i%width - self.moveRange];
        return (self.location + result)
            
    def adjacentSquares(self):
        return (self.location + DIRECTIONS)
    
    def attackSupportRange(self):
        '''
            A function which returns a list of all possible location coordinates that can be attacked/supported by this piece. 
            Does not account for terrain. 
        '''
        result = np.zeros([1 + 8 * self.attackRange, 2]);
        for i in range(8 * self.attackRange):
            result[i + 1] = (1 + i//8) * DIRECTIONS[i%8];
        return (self.location + result)
        
    def move(self, newXLoc, newYLoc):
        self.location = np.array([newXLoc,newYLoc])
        

class Infantry(GamePiece):
    '''
        This class represents a single unit of infantry on the board.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.pieceType = 'I';
        self.icon = [];
        
        self.moveRange = 1;
        
        self.attackRange = 2;
        self.attackPower = 4;
        self.supportPower = 6;
        
        self.threatenedValue = 0;
        self.supportedValue = 0; 
        
        
class Cavalry(GamePiece):
    '''
        This class represents a single unit of cavalry on the board.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.pieceType = 'H';
        self.icon = [];
        
        self.moveRange = 2;
        
        self.attackRange = 2;
        self.attackPower = 4;
        self.supportPower = 5;
        
        self.threatenedValue = 0;
        self.supportedValue = 0; 
        
    #TODO: Cavalry charges/melee attack power
  
    
class Artillery(GamePiece):
    '''
        This class represents a single unit of artillery.
        It is further divided into foot artillery and swift artillery based on speed.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.pieceType = '';
        self.icon = [];
        
        self.moveRange = 0;
        
        self.attackRange = 3;
        self.attackPower = 5;
        self.supportPower = 8;
        
        self.threatenedValue = 0;
        self.supportedValue = 0; 
     
        
class FootArtillery(Artillery):
    '''
        This class represents a single unit of foot artillery on the board.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation,yLocation)
        
        self.pieceType = 'A';
        self.icon = [];
        
        self.moveRange = 1;
 
        
class SwiftArtillery(Artillery):
    '''
        This class represents a single unit of swift artillery on the board.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.pieceType = 'A_H';
        self.icon = [];
        
        self.moveRange = 2;       

        
class Relay(GamePiece):
    '''
        This class represents a single relay unit on the board.
        It is further divided into foot relays and swift relays based on speed.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.pieceType = '';
        self.icon = [];
        
        self.moveRange = 0;
        
        self.attackRange = 2;
        self.attackPower = 0;
        self.supportPower = 1;
        
        self.threatenedValue = 0;
        self.supportedValue = 0;         
        
    #TODO: Communication Line Relay Mechanism
    
    
class FootRelay(Relay):
    '''
        This class represents a single swift relay unit on the board.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.pieceType = 'C';
        self.icon = [];
        
        self.moveRange = 1;
        

class SwiftRelay(Relay):
    '''
        This class represents a single swift relay unit on the board.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.pieceType = 'C_H';
        self.icon = [];
        
        self.moveRange = 2;
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        