import numpy as np

def int32Array(inputList):
    return np.array(inputList, dtype = np.int32)

def int32Zeros(shapeList):
    return np.zeros(shapeList, dtype = np.int32)

DIRECTIONS = int32Array([[1,-1],[1,0],[1,1],[0,-1],[0,1],[-1,-1],[-1,0],[-1,1]]); 
#Every valid straight line direction as a vector.

class GamePiece:
    ''' 
        This class represents a single piece on the game board.  
        It possesses general methods and attributes which any piece will need.
    '''

    def __init__(self, xLocation, yLocation):
        self.location = int32Array([xLocation,yLocation])
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

                          
    def adjacentSquares(self, center):
        '''
            Returns an integer array of all tiles adjacent to the specified center.
        '''
        return (center + DIRECTIONS)
    
    def _movementRangeCandidates(self): 
        '''
            Returns an integer array of all possible candidate location coordinates that can be reached by this piece. 
            Does not account for terrain, communication lines, or other pieces. 
        '''
        width = 2 * self.moveRange + 1;
        result = int32Zeros([width**2, 2]);
        for i in range(width**2):
            result[i] = [i//width - self.moveRange, i%width - self.moveRange];
        return (self.location + result)
    
    def movementRange(self, impassableSquares):
        '''
            Returns an integer array of all possible location coordinates reachable by this piece in one turn.
            
                impassableSquares : Integer array of all tile locations which may not be traversed by a piece.
        '''
        candidates = self._movementRangeCandidates();
        
        # Removing self.location from the candidate array, as it is automatically included later.
        locationIndex = np.shape(candidates)[0]//2;
        candidates = np.delete(candidates, locationIndex, axis = 0);
        
        # Removing candidate points which are impassable.
        if impassableSquares != []:
            indices = [];
            for j in range(np.shape(candidates)[0]):
                intersection = False;
                if min(np.sum((impassableSquares - candidates[j])**2, axis = 1)) == 0:
                    intersection = True;
                if not intersection:
                    indices.append(j)
            candidates = candidates[indices];
        
        # Determining which remaining candidate points are reachable in the specified number of moves 
        # by doing 1 move at a time
        result = int32Array([self.location]);
        currentLayer = int32Array([self.location]);
        for i in range(self.moveRange):
            goodIndices = [];
            badIndices = [];
            for j in range(np.shape(candidates)[0]):
                if min(np.sum((currentLayer - candidates[j])**2, axis = 1)) <= 2:
                    goodIndices.append(j);
                else:
                    badIndices.append(j);
            currentLayer = candidates[goodIndices];
            result = np.concatenate((result,currentLayer),axis = 0);
            candidates = candidates[badIndices];        
        return result
    
    def straightLinePts(self, impassableSquares, maxDist = -1):
        '''
            Returns a list of 8 numpy integer arrays, each consisting of all tiles in a 
                specific direction from self.location, ordered by distance from that point, 
                stopping when an obstacle is reached or the maximum distance desired is reached.
            The 8 integer arrays are ordered (using cardinal directions as a reference) as follows:
                [NW, N, NE, W, E, SW, S, SE]
            
                impassableSquares : Integer array of all tile locations which may not be traversed by a piece.
                maxDist is an integer representing the maximum distance along which any direction should be travelled.
                    A unit with attack range 2, for example, will only examine points in straight lines 2 units away.
                    If unlimited range (travel indefinitely until an obstacle) is desired, then set
                        maxDist = -1
                        This value is taken as a default if no value is given.
        '''
        if impassableSquares == [] and maxDist == -1:
            print("Infinite range vision with no obstacles attempted - output set to []\n")
            return [];
        else:
            result = [];
            for i in range(np.shape(DIRECTIONS)[0]):
                currentDir = DIRECTIONS[i];
                distanceAllowed = 0;
                
                breakCond = True;
                while breakCond:
                    distanceAllowed += 1;
                    
                    if impassableSquares != []:
                        currentTile = self.location + distanceAllowed * currentDir;
                        nearestImpassableDist = min(np.sum((impassableSquares - currentTile)**2, axis = 1));
                        if nearestImpassableDist == 0:
                            breakCond = False;
                    if distanceAllowed > maxDist:
                        breakCond = False;
                
                if distanceAllowed == 1:
                    currentArray = int32Array([]);
                else:
                    currentArray = int32Zeros([distanceAllowed - 1,2]);
                for j in range(1, distanceAllowed):
                    currentArray[j-1] = self.location + j * currentDir;
                result.append(currentArray);
                
            return result;
    
    def attackSupportRange(self, impassableSquares):
        '''
            A function which returns an integer array of all possible location 
            coordinates that can be attacked/supported by this piece.
            
                impassableSquares : Integer array of all tile locations which may not be traversed by a piece.
        '''
        almostResult = self.straightLinePts(impassableSquares, self.attackRange);
        
        lengthList = [len(i) for i in almostResult];
        length = 1 + sum(lengthList);
        
        result = int32Zeros([length,2]);
        result[0] = self.location;
        
        currentArrayIndex = 0;
        index = 0;
        for i in range(1,length):
            while True:
                if index == lengthList[currentArrayIndex]:
                    currentArrayIndex += 1;
                    index = 0;
                else:
                    break;
            
            result[i] = almostResult[currentArrayIndex][index];
            index += 1;
        
        return result
        
    def move(self, newXLoc, newYLoc):
        self.location = int32Array([newXLoc,newYLoc])
        

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
       
        

        
        