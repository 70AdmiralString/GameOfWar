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

    '''Functions to help with representation of objects'''

    def __repr__(self):
        "Should return a string representation of the class or instance with as much information as possible, preferably something that can be passed to eval/quick_init to recreate the object. Return value must be a string." 
        "Only returns the attributes that different from the default ones. If you want to see all values, then use self.__dict__"

        #Decide which class to compare our piece to
        pieceType = self.pieceType
        if (pieceType == 'I'):
            test_piece = Infantry(0,0)
        elif (pieceType == 'H'):
            test_piece = Cavalry(0,0)
        elif (pieceType == 'A'):
            test_piece = FootArtillery(0,0)
        elif (pieceType == 'A_H'):
            test_piece = SwiftArtillery(0,0)
        elif (pieceType == 'C'):
            test_piece = FootRelay(0,0)
        elif (pieceType == 'C_H'):
            test_piece = SwiftRelay(0,0)
        else:
            test_piece = GamePiece(0,0)

        test_dic = test_piece.__dict__
        key_list = list(test_dic)
        key_list.remove('location') # always want location displayed
        key_list.remove('pieceType') # always want piece type displayed

        dic = self.__dict__.copy()
        dic['location'] = tuple(dic['location']) # Can't have location being displayed as an array or else it causes problems for the quick_init function

        for i in range(0,len(key_list)):

            if (dic[key_list[i]] == test_dic[key_list[i]]):
                del dic[key_list[i]]

        return str(dic)

    def __str__(self):
        "A user friendly text representation of the instance. Allows the 'print' to work without giving too much information."
        "Only gives the peiceType and the Location information"

        dic = {'pieceType': self.pieceType, 'location':tuple(self.location)}
        return str(dic)

    def quick_init(dicORstr):
        "Takes in the output of __repr__ either as a string or as a dictionary. Returns a new member of the class with this information"
        if (type(dicORstr) == str):
            dic = eval(dicORstr)
        else:
            dic = dicORstr

        key_list = list(dic)
        key_list.remove('location')

        #Decide where the piece belongs
        pieceType = dic['pieceType']
        if (pieceType == 'I'):
            piece = Infantry(dic['location'][0],dic['location'][1])
        elif (pieceType == 'H'):
            piece = Cavalry(dic['location'][0],dic['location'][1])
        elif (pieceType == 'A'):
            piece = FootArtillery(dic['location'][0],dic['location'][1])
        elif (pieceType == 'A_H'):
            piece = SwiftArtillery(dic['location'][0],dic['location'][1])
        elif (pieceType == 'C'):
            pieceType = FootRelay(dic['location'][0],dic['location'][1])
        elif (pieceType == 'C_H'):
            piece = SwiftRelay(dic['location'][0],dic['location'][1])
        else:
            piece = GamePiece(dic['location'][0],dic['location'][1])

        #Put all the different attributes where they belong
        for i in range(0,len(key_list)):

            # using piece.key_list[i] didn't work
            setattr(piece,key_list[i],dic[key_list[i]]) 
        return piece
       
    
          
    '''Actual class methods'''

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
        
        
        
        
        
        
#Just so I can run some tests quickly
a = GamePiece(10,10)
b = GamePiece(9,8)
b.moveRange = 4
c =  GamePiece.quick_init("{'location': (9, 7), 'pieceType': 'Fake Piece', 'moveRange': 9}")
d = GamePiece.quick_init({'location': (-5, 0), 'pieceType': '100',  'threatenedValue':1})
e = GamePiece.quick_init({'location': (30, 0), 'pieceType': 'C_H',  'extraValue':"easter egg"})
f = Infantry.quick_init("{'location': (9, 7), 'pieceType': 'I', 'moveRange': -9}")
       
        

        
        