#import tupleList
from vector import *

DIRECTIONS = [Vector(1,-1),Vector(1,0),Vector(1,1),Vector(0,-1),Vector(0,1),Vector(-1,-1),Vector(-1,0),Vector(-1,1)]; 
#Every valid straight line direction as a vector.

class Piece:
    ''' 
        This class represents a single piece on the game board.  
        It possesses general methods and attributes which any piece will need.
    '''

    #changing these effects how things are displayed in the UI
    display_sheet = {'I':'Infantry', 'H':'Cavalry', 'A':'Foot Artillery', 'A_H':'Mounted Artillery', 'C':'Foot Relay', 'C_H':'Mounted Relay'}

    #changing this effects which keys users need to enter
    key_sheet = {'I':'I', 'H':'C', 'A':'FA', 'A_H':'MA', 'C':'FR', 'C_H':'MR', '':''}

    #changing these breaks the print and repr functions which use the eval function. These strings need to match the names of the subclasses. DO NOT CHANGE THIS
    _cheat_sheet = {'I':'Infantry', 'H':'Cavalry', 'A':'FootArtillery', 'A_H':'SwiftArtillery', 'C':'FootRelay', 'C_H':'SwiftRelay', 'B':'Arsenal'}


    def __init__(self, x_location, y_location, team = None):
        # Attributes which track the state of the piece.
        self.location = Vector(x_location, y_location)

        self.in_communication = True;
        self.has_moved = False;
        self.can_move = True;
            #occupies_square is True if a piece fills the square it is being placed in, so 
            #   that no other pieces may occupy it.
        self.occupies_square = True;
            #can_use_forts is True if a piece is capable of receiving a defensive bonus 
            #   from terrain and false otherwise.
        self.can_use_forts = True;
        
        # Attributes of the piece based on the type of piece.
        self.piece_type = '';
        
        self.move_range = 0;

        self.attack_range = 0;
        self.attack_power = 0;
        self.support_power = 0;

        self.team = team;
            #Each piece will have a side/team (white or black). There may be more than 2 sides. This will certainly be used in the future. It's used int the GameSettings class. 

    '''Functions to help with representation of objects'''

    def __repr__(self):
        "Should return a string representation of the class or instance with as much information as possible, preferably something that can be passed to eval/quick_init to recreate the object. Return value must be a string." 
        "Only returns the attributes that different from the default ones. If you want to see all values, then use self.__dict__"

        #Decide which class to compare our piece to

        if (self.piece_type in list(Piece._cheat_sheet)):
            test_piece = eval(Piece._cheat_sheet[self.piece_type])(0,0)
        else:
            test_piece = Piece(0,0)

        test_dic = test_piece.__dict__
        key_list = list(test_dic)
        key_list.remove('location') # always want location displayed
        key_list.remove('piece_type') # always want piece type displayed

        dic = self.__dict__.copy()
        dic['location'] = tuple(dic['location']) # Can't have location being displayed as an array or else it causes problems for the quick_init function

        for i in range(0,len(key_list)):

            if (dic[key_list[i]] == test_dic[key_list[i]]):
                del dic[key_list[i]]

        return str(dic)

    def __str__(self):
        "A user friendly text representation of the instance. Allows the 'print' to work without giving too much information."
        "Only gives essential information"

        essential_info = ['piece_type', 'location'] # A list of all the essential bits of information that we want to appear when printing

        dic = {}
        for i in range(0,len(essential_info)):
            dic[essential_info[i]] = getattr(self, essential_info[i])

        dic['location'] = tuple(dic['location']) #tuples are easier to read
        return "Game Piece " + str( dic)
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False;
        return self.location == other.location

    def quick_init(dicORstr):
        "Takes in the output of __repr__ either as a string or as a dictionary. Returns a new member of the class with this information"
        if (type(dicORstr) == str):
            dic = eval(dicORstr)
        else:
            dic = dicORstr

        key_list = list(dic)
        key_list.remove('location')

        #Decide where the piece belongs
        piece_type = dic['piece_type']

        if (piece_type in list(Piece._cheat_sheet)):
            piece = eval(Piece._cheat_sheet[piece_type])(dic['location'][0],dic['location'][1])
        else:
            piece = Piece(dic['location'][0],dic['location'][1])

        #Put all the different attributes where they belong
        for i in range(0,len(key_list)):

            # using piece.key_list[i] didn't work
            setattr(piece,key_list[i],dic[key_list[i]]) 
        return piece
       
    def update_display_name(self):
        "adds location to the display_name"

        if (self.piece_type == ''):
            raise AttributeError('This piece does not have a valid type')

        dis = Piece.display_sheet[self.piece_type]
        p = ' at '
        lay = str(self.location)
        
        self.display_name = dis + p + lay 

    def _get_type_key(self):
        self.type_key = Piece.key_sheet[self.piece_type]

          
    '''Actual class methods'''

                          
    def adjacent_squares(center):
        '''
            Returns an list of vectors of all tiles adjacent to the specified center.
        '''
        return [i + center for i in DIRECTIONS]
    
    def local_formation(self, piece_locations):
        """
            Returns a list of vectors with each vector representing a square containing a piece in piece_locations,
                representing the connected component of pieces containing this piece,
                with adjacency defined using the 8 adjacent squares to each square.
            
                piece_locations is a list of vectors, representing all pieces being considered.
        """
        formation = [self.location];
        for square in formation:
            candidates = Piece.adjacent_squares(square);
            for j in candidates:
                if piece_locations.count(j) and not formation.count(j):
                    formation.append(j);
        return formation           
    
    def _movement_range_candidates(self): 
        '''
            Returns an list of vectors of all possible candidate location coordinates that can be reached by this piece. 
            Does not account for terrain, communication lines, or other pieces. 
        '''
        width = 2 * self.move_range + 1;
        result = [Vector(0,0)] * (width**2);
        for i in range(width**2):
            result[i] = Vector(i//width - self.move_range, i%width - self.move_range);
        return [j + self.location for j in result]
    
    def movement_range(self, impassable_squares):
        '''
            Returns a list of vectors of all possible location coordinates reachable by this piece in one turn.
            
                impassable_squares : list of vectors of all tile locations which may not be traversed by a piece.
        '''
        candidates = self._movement_range_candidates();
        
        # Removing self.location from the candidate array, as it is automatically included later.
        candidates = vec_remove(candidates, self.location);
        
        # Removing candidate points which are impassable.
        candidates = vec_remove_list(candidates, impassable_squares);
        
        # Determining which remaining candidate points are reachable in the specified number of moves 
        # by doing 1 move at a time
        result = [self.location];    
        current_layer = [self.location];
        for i in range(self.move_range):
            good_indices = [];
            bad_indices = [];
            for j in range(len(candidates)):
                distances = [(k - candidates[j]).normSq() for k in current_layer];
                if min(distances) <= 2:
                    good_indices.append(j);
                else:
                    bad_indices.append(j);
            current_layer = [candidates[i] for i in good_indices];
            result = result + current_layer;
            candidates = [candidates[i] for i in bad_indices];   
        return result
    
    def straight_line_pts(self, impassable_squares, max_dist = -1):
        '''
            Returns a list of 8 lists of vectors of integers, each consisting of all tiles in a 
                specific direction from self.location, ordered by distance from that point, 
                stopping when an obstacle is reached or the maximum distance desired is reached.
            The 8 lists of vectors are ordered (using cardinal directions as a reference) as follows:
                [NW, N, NE, W, E, SW, S, SE]
            
                impassable_squares : Lists of vectors of all tile locations which may not be traversed by a piece.
                max_dist is an integer representing the maximum distance along which any direction should be travelled.
                    A unit with attack range 2, for example, will only examine points in straight lines 2 units away.
                    If unlimited range (travel indefinitely until an obstacle) is desired, then set
                        max_dist = -1
                        This value is taken as a default if no value is given.
        '''
        if impassable_squares == [] and max_dist == -1:
            raise Exception("Infinite range vision with no obstacles attempted.")
            return [];
        else:
            result = [];
            for i in range(len(DIRECTIONS)):
                current_dir = DIRECTIONS[i];
                distance_allowed = 0;
                
                break_cond = True;
                while break_cond:
                    distance_allowed += 1;
                    if impassable_squares != []:
                        current_tile = distance_allowed * current_dir + self.location;
                        if impassable_squares.count(current_tile):
                            break_cond = False;
                    if distance_allowed > max_dist:
                        break_cond = False;
                
                if distance_allowed == 1:
                    current_array = [];
                else:
                    current_array = [Vector(0,0)] * (distance_allowed - 1);
                for j in range(1, distance_allowed):
                    current_array[j-1] = j * current_dir + self.location;
                result.append(current_array);
                
            return result;
    
    def attack_support_range(self, impassable_squares):
        '''
            A function which returns a list of vectors of all possible location 
            coordinates that can be attacked/supported by this piece.
            
                impassable_squares : List of vectors of all tile locations which may not be traversed by a piece.
        '''
        almost_result = self.straight_line_pts(impassable_squares, self.attack_range);
        
        length_list = [len(i) for i in almost_result];
        length = 1 + sum(length_list);
        
        result = [Vector(0,0)] * length;
        result[0] = self.location;
        
        current_array_index = 0;
        index = 0;
        for i in range(1,length):
            while True:
                if index == length_list[current_array_index]:
                    current_array_index += 1;
                    index = 0;
                else:
                    break;
            
            result[i] = almost_result[current_array_index][index];
            index += 1;
        
        return result
        
    def update_location(self, new_location):
        '''
            Updates the location of the piece while changing no other attributes.
            
                new_location is a vector consisting of two elements, 
                    the x and y positions of the new location.
        '''
        self.location = new_location;
        
    def move(self, new_location, impassable_squares):
        '''
            Updates the location of the piece to the location specified, if new_location is a square within
                the movement range of the piece not its current location and the piece has not yet moved.  
                Updates the has_moved attribute to True;
                
            new_location is a list of vectors consisting of two elements, the x and y positions of the new location.
            impassable_squares : List of vectors of all tile locations which may not be traversed by a piece.
        '''
        options = self.movement_range(impassable_squares)
        if self.can_move:
            if self.has_moved:
                raise Exception("This piece has already moved.")
            else:
                if options.count(new_location) and (self.location != new_location):
                    self.update_location(new_location);
                    self.has_moved = True;
                else:
                    raise Exception("Not a valid move.")
        else:
            raise Exception("This piece is not movable.")
                
    def refresh_movement(self):
        '''
            Resets the value of self.has_moved to False, so that pieces may move again.
        '''
        self.has_moved = False;
        

class Infantry(Piece):
    '''
        This class represents a single unit of infantry on the board.
        It is represented as a Piece with particular specified attributes.
    '''

    def __init__(self, x_location, y_location, team = None):

        super().__init__(x_location, y_location, team)
        
        self.piece_type = 'I';

        
        self.move_range = 1;
        
        self.attack_range = 2;
        self.attack_power = 4;
        self.support_power = 6;
        self._get_type_key()


class Cavalry(Piece):
    '''
        This class represents a single unit of cavalry on the board.
        It is represented as a Piece with particular specified attributes.
    '''
    def __init__(self, x_location, y_location, team = None):
        super().__init__(x_location, y_location, team)
        self.can_use_forts = False;
        
        self.piece_type = 'H';
        
        self.move_range = 2;
        
        self.attack_range = 2;
        self.attack_power = 4;
        self.chargePower = 7;
        self.support_power = 5;
        self._get_type_key()

        
    def _cavalry_lines(self, friendly_cavalry_positions):
        '''
            Outputs a list of 8 lists of vectors, corresponding to each direction emanating outwards from self.location.
                Each list of vectors consists of points starting at self.location and moving in a specific direction 
                one unit at a time, such that each listed point corresponds to a square containing a cavalry.
                Every list contains self.location, so all have a minimum length of 1.
                The 8 lists of vectors are ordered (using cardinal directions as a reference) as follows:
                    [NW, N, NE, W, E, SW, S, SE]
                    
                friendly_cavalry_positions : List of vectors of all positions currently occupied by friendly cavalry.
                This includes the location of this unit itself.
        '''
        result = [];
        for i in range(len(DIRECTIONS)):
            line_dist = 1;
            while True:
                examined_tile = line_dist * DIRECTIONS[i] + self.location;
                if not friendly_cavalry_positions.count(examined_tile):
                    break; 
                line_dist += 1;
                
            current_line = [Vector(0,0)] * line_dist;
            for j in range(line_dist):
                current_line[j] = j * DIRECTIONS[i] + self.location;
            result.append(current_line);
        return result;
    
    def charge_range(self, impassable_squares, friendly_cavalry_positions):
        '''
            Returns a list of vectors consisting of all points which may be targeted
                by this unit in a cavalry charge.
            
            impassable_squares : List of vectors of all positions which may not be traversed by a unit.
            friendly_cavalry_positions : List of vectors of all positions currently occupied by friendly cavalry.
                This includes the location of this unit itself.
        '''
        cavalry_lines = self._cavalry_lines(friendly_cavalry_positions);
        length_list = [len(i) for i in cavalry_lines];
        #   There is one more anomalous situation we wish to remove, that where a line of cavalry
        #       ends on impassable terrain.  If this is the case, we will simply remove the last entry.
        if len(impassable_squares) != 0:
            for i in range(len(DIRECTIONS)):
                line_end_tile = length_list[i] * DIRECTIONS[i] + self.location;
                if impassable_squares.count(line_end_tile):
                    length_list[i] += -1;
        
        length = 1 + sum(length_list);      
        result = [Vector(0,0)] * length;
        result[0] = self.location;
        
        index = 0;
        current_dir_index = 0;
        for i in range(1,length):
            while True:
                if index >= length_list[current_dir_index]:
                    current_dir_index += 1;
                    index = 0;
                else:
                    break;
            result[i] = cavalry_lines[current_dir_index][index] + DIRECTIONS[current_dir_index];
            index += 1;            
        return result;
    
    def non_charge_attack_range(self, impassable_squares, friendly_cavalry_positions):
        '''
            Returns a list of vectors consisting of all points which may be targeted
                by this unit in a normal attack, but not by a cavalry charge.
            
            impassable_squares : List of vectors of all positions which may not be traversed by a unit.
            friendly_cavalry_positions : List of vectors of all positions currently occupied by friendly cavalry.
                This includes the location of this unit itself.
        '''
        charge_squares = self.charge_range(impassable_squares, friendly_cavalry_positions);
        attack_squares = self.attack_support_range(impassable_squares);
        
        result = vec_remove_list(attack_squares, charge_squares);
        return result
        
    
class Artillery(Piece):
    '''
        This class represents a single unit of artillery.
        It is further divided into foot artillery and swift artillery based on speed.
        It is represented as a Piece with particular specified attributes.
    '''
    def __init__(self, x_location, y_location, team = None):
        super().__init__(x_location, y_location, team)
        
        self.move_range = 0;
        
        self.attack_range = 3;
        self.attack_power = 5;
        self.support_power = 8;
     
class FootArtillery(Artillery):
    '''
        This class represents a single unit of foot artillery on the board.
        It is represented as a Piece with particular specified attributes.
    '''
    def __init__(self, x_location, y_location, team = None):
        super().__init__(x_location,y_location, team)
        
        self.piece_type = 'A';
        
        self.move_range = 1;
        self._get_type_key()
 
        
class SwiftArtillery(Artillery):
    '''
        This class represents a single unit of swift artillery on the board.
        It is represented as a Piece with particular specified attributes.
    '''
    def __init__(self, x_location, y_location, team = None):
        super().__init__(x_location, y_location, team)
        self.can_use_forts = False;        
        
        self.piece_type = 'A_H';
        
        self.move_range = 2;       
        self._get_type_key()

        
class Relay(Piece):
    '''
        This class represents a single relay unit on the board.
        It is further divided into foot relays, swift relays, and arsenals based on speed.
        It is represented as a Piece with particular specified attributes.
    '''
    def __init__(self, x_location, y_location, team = None):
        super().__init__(x_location, y_location, team)
        
        self.move_range = 0;
        
        self.attack_range = 2;
        self.attack_power = 0;
        self.support_power = 1;       

    def communication_range(self, impassable_squares):
        '''
            Returns all squares within direct communication range of the relay.
            Returns a list of 8 lists of vectors, each consisting of all tiles in a 
                specific direction from self.location, ordered by distance from that point, 
                stopping when an obstacle is reached or the maximum distance desired is reached.
            The 8 lists of vectors are ordered (using cardinal directions as a reference) as follows:
                [NW, N, NE, W, E, SW, S, SE]
            
                impassable_squares : List of vectors of all tile locations which may not be traversed by a
                    friendly communication line.  Likely includes impassable terrain and enemy units.
        '''
        result = self.straight_line_pts(impassable_squares);
        
        return result;
    
    
class FootRelay(Relay):
    '''
        This class represents a single swift relay unit on the board.
        It is represented as a Piece with particular specified attributes.
    '''
    def __init__(self, x_location, y_location, team = None):
        super().__init__(x_location, y_location, team)
        
        self.piece_type = 'C';
        
        self.move_range = 1;
        self._get_type_key()
        

class SwiftRelay(Relay):
    '''
        This class represents a single swift relay unit on the board.
        It is represented as a Piece with particular specified attributes.
    '''
    def __init__(self, x_location, y_location, team = None):
        super().__init__(x_location, y_location, team)
        self.can_use_forts = False;
        
        self.piece_type = 'C_H';
        
        self.move_range = 2;
        self._get_type_key()
        

class Arsenal(Relay):
    '''
        Represents one of the arsenals which generate the initial lines of communication.
        Generally placed at the start of the game and then is unable to move.  
        Another piece may be stacked on top of it.
        An enemy unit being stacked on this location will destroy the arsenal.
    '''
    def __init__(self, x_location, y_location, team = None):
        super().__init__(x_location, y_location, team)
        
        self.occupies_square = False;
        self.can_move = False;
        self.can_use_forts = False;
        
        self.piece_type = 'B';
        
        self.move_range = 0;
        self.attack_range = 0;
        self.attack_power = 0;
        self.support_power = 0;    
        
        
        
        
#Just so I can run some tests quickly
a = Piece(10,10)
b = Piece(9,8)
b.move_range = 4
c =  Piece.quick_init("{'location': (9, 7), 'piece_type': 'Fake Piece', 'move_range': 9}")
d = Piece.quick_init({'location': (-5, 0), 'piece_type': '100'})
e = Piece.quick_init({'location': (30, 0), 'piece_type': 'C_H',  'extraValue':"easter egg"})
f = Infantry.quick_init("{'location': (9, 7), 'piece_type': 'I', 'move_range': -9}")
  
g = Infantry(5,4)
h = SwiftRelay(-10,4)     
        

        
        
