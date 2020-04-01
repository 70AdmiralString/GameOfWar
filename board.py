#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vector as v
import gamePiece as gp

class Tile():
    """
        Represents a single tile of the map.  Contains attributes for a string for a terrain type, 
        and a list of gamePieces if the tile is occupied.
    """
    
    def __init__(self, terrainType = '', occupants = None):
        """
            terrainType is a string, by default set to '' to represent an empty tile 
                (empty tiles are used only to fill up space in non-rectangular boards)
            occupants is a list of GamePiece objects, by default set to an empty list for an unoccupied tile
        """
        if occupants == None:
            occupants = [];
        
        self.terrainType = terrainType;
        self.occupants = occupants;
        
    def __repr__(self):
        return str(self.__dict__)
        
    def addPiece(self, gamePiece):
        """
            Adds gamePiece to the list of occupants of this tile.
        """
        self.occupants.append(gamePiece)
        
    def removePiece(self, gamePiece):
        """
            If gamePiece is one of the occupants of this tile, removes it.
        """
        if self.occupants.count(gamePiece):
            self.occupants.remove(gamePiece)
        else:
            print("Selected gamePiece not present in this tile")
            

class Board():  
    """
        Represents an entire map of a game.  Contains a list of lists of Tile objects.
    """
    
    def __init__(self, tileList, gamePieceList = None):
        """
            tileList is a list of tuples, each tuple containing a 
                Vector and a string, representing the location and terrain type of a tile, respectively.
                If the list of locations is not a rectangular grid, empty tiles (terrain '') will be
                    created to fill empty space.
            gamePieceList is a list of gamePieces,
                It should be ensured that each location of a piece in gamePieceList falls within tileList.
                By default, this list is set to be empty.
                
            The list of list of Tile objects created (self.tileList) will be indexed 
                so that a tile at location (x,y) can be found as
                self.tileList[y - self.minY][x - self.minX]
        """
        if gamePieceList == None:
            gamePieceList = [];
        
        self.minX = min([i[0][0] for i in tileList]);
        self.maxX = max([i[0][0] for i in tileList]);
        self.minY = min([i[0][1] for i in tileList]);
        self.maxY = max([i[0][1] for i in tileList]);
        
        self.width = self.maxX - self.minX + 1;
        self.height = self.maxY - self.minY + 1;
        
        # First, tiles from tileList are added
        self.tileList = [[0] * self.width for i in range(self.height)];
        for spot in tileList:
            location = spot[0];
            self.tileList[location[1]][location[0]] = Tile(spot[1]);
        
        # Now, we fill in any still-empty locations with empty tiles.
        for i in range(self.height):
            for j in range(self.width):
                if self.tileList[i][j] == 0:
                    self.tileList[i][j] = Tile();
        
        # Finally, gamePieces are added to tiles.
        for piece in gamePieceList:
            currentTile = self.getTile(piece.location);
            currentTile.addPiece(piece);
        
    def getTile(self, location):
        """
            Outputs the tile at Vector location given by location.
        """
        x = location[0];
        y = location[1];
        return self.tileList[y - self.minY][x - self.minX]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        