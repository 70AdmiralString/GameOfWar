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

    _cheat_sheat = {'I':'Infantry', 'H':'Cavalry', 'C':'Relay', 'A':'FootArtillery', 'A_H':'SwiftRelay', 'C':'FootRelay', 'C_H':'SwiftRelay'}

    def __init__(self, xLocation, yLocation):
        # Attributes which track the state of the piece.
        self.location = int32Array([xLocation,yLocation])

        self.inCommunication = True;
        self.hasMoved = False;
        self.canMove = True;
            #occupiesSquare is True if a piece fills the square it is being placed in, so 
            #   that no other pieces may occupy it.
        self.occupiesSquare = True;
            #canUseForts is True if a piece is capable of receiving a defensive bonus 
            #   from terrain and false otherwise.
        self.canUseForts = True;
        
        # Attributes of the piece based on the type of piece.
        self.pieceType = '';
        self.icon = [];
        
        self.moveRange = 0;

        self.attackRange = 0;
        self.attackPower = 0;
        self.supportPower = 0;

    '''Functions to help with representation of objects'''

    def __repr__(self):
        "Should return a string representation of the class or instance with as much information as possible, preferably something that can be passed to eval/quick_init to recreate the object. Return value must be a string." 
        "Only returns the attributes that different from the default ones. If you want to see all values, then use self.__dict__"

        #Decide which class to compare our piece to

        if (self.pieceType in list(GamePiece._cheat_sheat)):
            test_piece = eval(GamePiece._cheat_sheat[self.pieceType])(0,0)
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
        "Only gives essential information"

        essential_info = ['pieceType', 'location'] # A list of all the essential bits of information that we want to appear when printing

        dic = {}
        for i in range(0,len(essential_info)):
            dic[essential_info[i]] = getattr(self, essential_info[i])

        dic['location'] = tuple(dic['location']) #tuples are easier to read
        return "Game Piece " + str( dic)

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

        if (pieceType in list(GamePiece._cheat_sheat)):
            piece = eval(GamePiece._cheat_sheat[pieceType])(dic['location'][0],dic['location'][1])
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

            If this doesn't use any instance attributes why does it use self? Why is it an instance method and not a static method

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
        
    def updateLocation(self, newLocation):
        '''
            Updates the location of the piece while changing no other attributes.
            
                newLocation is an integer array consisting of two elements, the x and y positions of the new location.
        '''
        self.location = newLocation;
        
    def move(self, newLocation, impassableSquares):
        '''
            Updates the location of the piece to the location specified, if newLocation is a square within
                the movement range of the piece not its current location and the piece has not yet moved.  
                Updates the hasMoved attribute to True;
                
            newLocation is an integer array consisting of two elements, the x and y positions of the new location.
            impassableSquares : Integer array of all tile locations which may not be traversed by a piece.
        '''
        options = self.movementRange(impassableSquares)
        
        nearest = min(np.sum((options - newLocation)**2, axis = 1));
        distanceFromSelf = np.sum((self.location - newLocation)**2);
        if self.canMove:
            if self.hasMoved:
                print("This piece has already moved, movement not carried out.")
            else:
                if nearest == 0 and distanceFromSelf != 0:
                    self.updateLocation(newLocation);
                    self.hasMoved = True;
                else:
                    print("Not a valid move, movement not carried out.")
        else:
            print("This piece is not movable, movement not carried out.")
                
    def refreshMovement(self):
        '''
            Resets the value of self.hasMoved to False, so that pieces may move again.
        '''
        self.hasMoved = False;
        

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

        
        
class Cavalry(GamePiece):
    '''
        This class represents a single unit of cavalry on the board.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        self.canUseForts = False;
        
        self.pieceType = 'H';
        self.icon = [];
        
        self.moveRange = 2;
        
        self.attackRange = 2;
        self.attackPower = 4;
        self.chargePower = 7;
        self.supportPower = 5;
        
    def _cavalryLines(self, friendlyCavalryPositions):
        '''
            Outputs a list of 8 integer arrays, corresponding to each direction emanating outwards from self.location.
                Each array consists of points starting at self.location and moving in a specific direction one unit at a time,
                such that each listed point corresponds to a square containing a cavalry.
                Every array contains self.location, so has a minimum length of 1.
                The 8 integer arrays are ordered (using cardinal directions as a reference) as follows:
                    [NW, N, NE, W, E, SW, S, SE]
                    
                friendlyCavalryPositions : Integer array of all positions currently occupied by friendly cavalry.
                This includes the location of this unit itself.
        '''
        result = [];
        for i in range(len(DIRECTIONS)):
            lineDist = 1;
            while True:
                examinedTile = self.location + lineDist * DIRECTIONS[i];
                
                cavalryDistances = np.sum((friendlyCavalryPositions - examinedTile)**2, axis = 1);
                if min(cavalryDistances) != 0:
                    break;
                
                lineDist += 1;
            currentLine = int32Zeros([lineDist,2]);
            for j in range(lineDist):
                currentLine[j] = self.location + j * DIRECTIONS[i];
            result.append(currentLine);
        return result;
    
    def chargeRange(self, impassableSquares, friendlyCavalryPositions):
        '''
            Returns an integer array consisting of all points which may be targeted
                by this unit in a cavalry charge.
            
            impassableSquares : Integer array of all positions which may not be traversed by a unit.
            friendlyCavalryPositions : Integer array of all positions currently occupied by friendly cavalry.
                This includes the location of this unit itself.
        '''
        cavalryLines = self._cavalryLines(friendlyCavalryPositions);
        lengthList = [len(i) for i in cavalryLines];
        #   There is one more anomalous situation we wish to remove, that where a line of cavalry
        #       ends on impassable terrain.  If this is the case, we will simply remove the last entry.
        if len(impassableSquares) != 0:
            for i in range(len(DIRECTIONS)):
                lineEndTile = self.location + lengthList[i] * DIRECTIONS[i];
                impassableDist = min(np.sum((impassableSquares - lineEndTile)**2, axis = 1));
                if impassableDist == 0:
                    lengthList[i] += -1;
        
        length = 1 + sum(lengthList);
        
        result = int32Zeros([length,2]);
        result[0] = self.location;
        
        index = 0;
        currentDirIndex = 0;
        for i in range(1,length):
            while True:
                if index >= lengthList[currentDirIndex]:
                    currentDirIndex += 1;
                    index = 0;
                else:
                    break;
            result[i] = cavalryLines[currentDirIndex][index] + DIRECTIONS[currentDirIndex];
            index += 1;            
        return result;
    
    def nonChargeAttackRange(self, impassableSquares, friendlyCavalryPositions):
        '''
            Returns an integer array consisting of all points which may be targeted
                by this unit in a normal attack, but not by a cavalry charge.
            
            impassableSquares : Integer array of all positions which may not be traversed by a unit.
            friendlyCavalryPositions : Integer array of all positions currently occupied by friendly cavalry.
                This includes the location of this unit itself.
        '''
        chargeSquares = self.chargeRange(impassableSquares, friendlyCavalryPositions);
        attackSquares = self.attackSupportRange(impassableSquares);
        
        toBeKept = len(attackSquares) * [True];
        for i in range(len(attackSquares)):
            distance = min(np.sum((chargeSquares - attackSquares[i])**2, axis = 1));
            if distance == 0:
                toBeKept[i] = False;
        
        result = attackSquares[toBeKept];
        return result
        
    
class Artillery(GamePiece):
    '''
        This class represents a single unit of artillery.
        It is further divided into foot artillery and swift artillery based on speed.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.moveRange = 0;
        
        self.attackRange = 3;
        self.attackPower = 5;
        self.supportPower = 8;
     
        
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
        self.canUseForts = False;        
        
        self.pieceType = 'A_H';
        self.icon = [];
        
        self.moveRange = 2;       

        
class Relay(GamePiece):
    '''
        This class represents a single relay unit on the board.
        It is further divided into foot relays, swift relays, and arsenals based on speed.
        It is represented as a GamePiece with particular specified attributes.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.moveRange = 0;
        
        self.attackRange = 2;
        self.attackPower = 0;
        self.supportPower = 1;       
        
    def communicationRange(self, impassableSquares):
        '''
            Returns all squares within communication range of the relay.
            Returns a list of 8 numpy integer arrays, each consisting of all tiles in a 
                specific direction from self.location, ordered by distance from that point, 
                stopping when an obstacle is reached or the maximum distance desired is reached.
            The 8 integer arrays are ordered (using cardinal directions as a reference) as follows:
                [NW, N, NE, W, E, SW, S, SE]
            
                impassableSquares : Integer array of all tile locations which may not be traversed by a
                    friendly communication line.  Likely includes impassable terrain and enemy units.
        '''
        result = self.straightLinePts(impassableSquares);
        
        return result;
    
    
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
        self.canUseForts = False;
        
        self.pieceType = 'C_H';
        self.icon = [];
        
        self.moveRange = 2;
        

class Arsenal(Relay):
    '''
        Represents one of the arsenals which generate the initial lines of communication.
        Generally placed at the start of the game and then is unable to move.  
        Another piece may be stacked on top of it.
        An enemy unit being stacked on this location will destroy the arsenal.
    '''
    def __init__(self, xLocation, yLocation):
        super().__init__(xLocation, yLocation)
        
        self.occupiesSquare = False;
        self.canMove = False;
        self.canUseForts = False;
        
        self.pieceType = 'B';
        self.icon = [];
        
        self.moveRange = 0;
        self.attackRange = 0;
        self.attackPower = 0;
        self.supportPower = 0;    
        
        
        
        
#Just so I can run some tests quickly
a = GamePiece(10,10)
b = GamePiece(9,8)
b.moveRange = 4
c =  GamePiece.quick_init("{'location': (9, 7), 'pieceType': 'Fake Piece', 'moveRange': 9}")
d = GamePiece.quick_init({'location': (-5, 0), 'pieceType': '100'})
e = GamePiece.quick_init({'location': (30, 0), 'pieceType': 'C_H',  'extraValue':"easter egg"})
f = Infantry.quick_init("{'location': (9, 7), 'pieceType': 'I', 'moveRange': -9}")
       
        

        
        
