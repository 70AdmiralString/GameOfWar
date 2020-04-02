#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vector as v
import gamePiece as gp

class Tile():
    """
        Represents a single tile of the map.  Contains attributes for a string for a terrain type, 
        and a list of Pieces if the tile is occupied.
    """
    
    def __init__(self, terrain_type = '', occupants = None):
        """
            terrain_type is a string, by default set to '' to represent an empty tile 
                (empty tiles are used only to fill up space in non-rectangular boards)
            occupants is a list of Piece objects, by default set to an empty list for an unoccupied tile
        """
        if occupants == None:
            occupants = [];
        
        self.terrain_type = terrain_type;
        self.occupants = occupants;
        
    def __repr__(self):
        return str(self.__dict__)
        
    def add_piece(self, game_piece):
        """
            Adds game_piece to the list of occupants of this tile.
        """
        self.occupants.append(game_piece)
        
    def remove_piece(self, game_piece):
        """
            If game_piece is one of the occupants of this tile, removes it.
        """
        if self.occupants.count(game_piece):
            self.occupants.remove(game_piece)
        else:
            print("Selected game_piece not present in this tile")
            

class Board():  
    """
        Represents an entire map of a game.  Contains a list of lists of Tile objects.
    """
    
    def __init__(self, tile_list, game_piece_list = None):
        """
            tile_list is a list of tuples, each tuple containing a 
                Vector and a string, representing the location and terrain type of a tile, respectively.
                If the list of locations is not a rectangular grid, empty tiles (terrain '') will be
                    created to fill empty space.
            game_piece_list is a list of Pieces,
                It should be ensured that each location of a piece in game_piece_list falls within tile_list.
                By default, this list is set to be empty.
                
            The list of list of Tile objects created (self.tile_list) will be indexed 
                so that a tile at location (x,y) can be found as
                self.tile_list[y - self.minY][x - self.minX]
        """
        if game_piece_list == None:
            game_piece_list = [];
        
        self.minX = min([i[0][0] for i in tile_list]);
        self.maxX = max([i[0][0] for i in tile_list]);
        self.minY = min([i[0][1] for i in tile_list]);
        self.maxY = max([i[0][1] for i in tile_list]);
        
        self.width = self.maxX - self.minX + 1;
        self.height = self.maxY - self.minY + 1;
        
        # First, tiles from tile_list are added
        self.tile_list = [[0] * self.width for i in range(self.height)];
        for spot in tile_list:
            location = spot[0];
            self.tile_list[location[1]][location[0]] = Tile(spot[1]);
        
        # Now, we fill in any still-empty locations with empty tiles.
        for i in range(self.height):
            for j in range(self.width):
                if self.tile_list[i][j] == 0:
                    self.tile_list[i][j] = Tile();
        
        # Finally, Pieces are added to tiles.
        for piece in game_piece_list:
            current_tile = self.get_tile(piece.location);
            current_tile.add_piece(piece);
            
    def __str__(self):
        # This will output two grids.  The first will display types of Tile objects.  
        # The second will display units and their types where they appear.
        
        # Determine how big to make grid spacing
        tile_spacing = max([max([len(tile.terrain_type) for tile in row]) for row in self.tile_list]);
        unit_spacing = max([max([-1 + sum([len(piece.piece_type) + 1 for piece in tile.occupants]) 
                                for tile in row]) for row in self.tile_list]);

        result1 = '';
        result2 = '';
        for row in self.tile_list:
            tilerow = '';
            unitrow = '';
            for tile in row:
                space_needed = len(tile.terrain_type);
                left_space = (tile_spacing - space_needed)//2;
                right_space = tile_spacing - space_needed - left_space;
                tilerow += '|' + left_space * ' ' + tile.terrain_type + right_space * ' ' + '|';
                
                space_needed = -1 + sum([len(piece.piece_type) + 1 for piece in tile.occupants]);
                left_space = (unit_spacing - space_needed)//2;
                right_space = unit_spacing - space_needed - left_space;
                unitrow += '|' + left_space * ' ';
                for piece in tile.occupants:
                    unitrow += piece.piece_type + ' ';
                unitrow = unitrow[:-1]
                unitrow += right_space * ' ' + '|';           
            tilerow += '\n';
            unitrow += '\n';
            result1 = tilerow + result1;
            result2 = unitrow + result2;  
        result1 = 'Terrain Grid:\n' + result1;
        result2 = 'Unit Grid:\n' + result2;
        return result1 + '\n' + result2;
        
    def get_tile(self, location):
        """
            Outputs the tile at Vector location given by location.
        """
        x = location[0];
        y = location[1];
        return self.tile_list[y - self.minY][x - self.minX]
        
    def get_tiles_by_attribute(self, *kwargs):
        """
            Outputs a list of all tile locations on the board of the type specified.
            
                kwargs makes up several Tile attributes and values for which we wish to select.
                    A common example is terrain_type
        """
        if type(kwargs) == dict:
            attributes = list(vars(Tile()).keys());
            for key, value in kwargs.items():
                if key not in attributes:
                    raise Exception('Tile objects do not have the attribute %s' %key + '.')
            
        result = [];
        for i in range(self.minY, self.maxY + 1):
            for j in range(self.minX, self.maxX + 1):
                location = v.Vector(i,j);
                current_tile = self.get_tile(location);
                is_good_tile = True;
                if type(kwargs) == dict:
                    for key, value in kwargs.items():
                        if not current_tile.key == value:
                            is_good_tile = False;
                if is_good_tile:
                    result.append(location);
        return result
    
    def get_pieces_by_attribute(self, *kwargs):
        """
            Outputs a list of all game_pieces on the board of the type specified.
            
                kwargs makes up several Piece attributes for which we wish to select.
                    Common examples are piece_type and team
        """
        if type(kwargs) == dict:
            attributes = list(vars(gp.Piece(0,0)).keys());
            for key, value in kwargs.items():
                if key not in attributes:
                    raise Exception('Piece objects do not have the attribute %s' %key + '.')
                
        result = [];
        for i in range(self.minY, self.maxY + 1):
            for j in range(self.minX, self.maxX + 1):
                location = v.Vector(i,j);
                current_tile = self.get_tile(location);
                for unit in current_tile.occupants:
                    is_good_unit = True;
                    if type(kwargs) == dict:
                        for key, value in kwargs.items():
                            if not unit.key == value:
                                is_good_unit = False;
                    if is_good_unit:
                        result.append(unit);
        return result
 
    def determine_impassable(self, impassable_types):
        """
            Outputs a list of all tiles on the board corresponding to all of the impassable types of tiles.
            Different definitions of impassable are required for different types of actions in the game.
            
                impassable_types is a list of strings, each corresponding to a terrain type of a Tile.
        """
        result = [];
        for terrain in impassable_types:
            result.append(self.get_tiles_by_attribute(terrain));
        return result
 
    def add_piece(self, game_piece):
        """
            Add the selected piece to the board.
            
                game_piece is a Piece object.  
                    Notably, it contains the desired location as an attribute.
        """    
        tile = self.get_tile(game_piece.location);
        for unit in tile.occupants:
            if unit.occupies_square:
                raise Exception("This square is already full.")
        tile.add_piece(game_piece)
 
    def remove_piece(self, game_piece):
        """
            Removes the selected piece from the board.
            
                game_piece is a Piece object.  
                    Notably, it contains its current location as an attribute.
        """
        tile = self.get_tile(game_piece.location);
        tile.remove_piece(game_piece)
    
    def move_piece(self, game_piece, new_location, impassable_squares):
        """
            Moves the selected game_piece from its current location to the specified new location.
            
                game_piece is a Piece object.  
                    Notably, it contains its current location as an attribute.
                new_location is a Vector representing the new location of game_piece.
                impassable_squares is a list of Vector locations representing which tiles pieces may not cross.
            
            This will throw an exception if the move is not valid, given the impassable terrain 
                and based on whether or not the unit has already moved.
        """
        self.remove_piece(game_piece);
        try:
            game_piece.move(new_location, impassable_squares);
        except Exception as error:
            print(error)
        self.add_piece(game_piece)
        
    def refresh_pieces(self, *kwargs):
        """
            Takes all pieces with specified attributes and alters their movement status
                so piece.has_moved = False, enabling them to move again
                
                kwargs makes up several Piece attributes for which we wish to select.
        """
        pieces = self.get_pieces_by_attribute(kwargs);
        print(pieces)
        for piece in pieces:
            piece.refresh_movement();
        
# Some sample variables for testing purposes
tile_list1 = [(v.Vector(0,0),'A'),(v.Vector(0,1), 'B'),(v.Vector(1,1),'C')]
game_piece_list1 = [gp.Infantry(1,1,'b'), gp.Cavalry(0,1,'b'),gp.Arsenal(0,0,'w'), gp.SwiftArtillery(0,0,'w')]
board1 = Board(tile_list1,game_piece_list1);
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        