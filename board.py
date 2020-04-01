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
            
    def __str__(self):
        # This will output two grids.  The first will display types of Tile objects.  
        # The second will display units and their types where they appear.
        
        # Determine how big to make grid spacing
        tileSpacing = max([max([len(tile.terrainType) for tile in row]) for row in self.tileList]);
        unitSpacing = max([max([sum([len(piece.pieceType) for piece in tile.occupants]) for tile in row]) for row in self.tileList]);

        result1 = '';
        result2 = '';
        for row in self.tileList:
            tilerow = '';
            unitrow = '';
            for tile in row:
                spaceNeeded = len(tile.terrainType);
                leftSpace = (tileSpacing - spaceNeeded)//2;
                rightSpace = tileSpacing - spaceNeeded - leftSpace;
                tilerow += '|' + leftSpace * ' ' + tile.terrainType + rightSpace * ' ' + '|';
                
                spaceNeeded = sum([len(piece.pieceType) for piece in tile.occupants]);
                leftSpace = (unitSpacing - spaceNeeded)//2;
                rightSpace = unitSpacing - spaceNeeded - leftSpace;
                unitrow += '|' + leftSpace * ' ';
                for piece in tile.occupants:
                    unitrow += piece.pieceType;
                unitrow += rightSpace * ' ' + '|';           
            tilerow += '\n';
            unitrow += '\n';
            result1 = tilerow + result1;
            result2 = unitrow + result2;  
        result1 = 'Terrain Grid:\n' + result1;
        result2 = 'Unit Grid:\n' + result2;
        return result1 + result2;
        
    def getTile(self, location):
        """
            Outputs the tile at Vector location given by location.
        """
        x = location[0];
        y = location[1];
        return self.tileList[y - self.minY][x - self.minX]
        
    def getTilesByType(self, terrainType):
        """
            Outputs a list of all tile locations on the board of the type specified.
            
                terrainType is a string, representing a particular Tile terrain type.
        """
        result = [];
        for i in range(self.minY, self.maxY):
            for j in range(self.minX, self.maxX):
                location = v.Vector(i,j);
                currentTile = self.getTile(location);
                if currentTile.terrainType == terrainType:
                    result.append(location);
        return result
    
    def getPiecesByType(self, unitType):
        """
            Outputs a list of all gamePieces on the board of the type specified.
            
                unit is a string, representing a particular GamePiece type.
        """
        result = [];
        for i in range(self.minY, self.maxY):
            for j in range(self.minX, self.maxX):
                location = v.Vector(i,j);
                currentTile = self.getTile(location);
                for unit in currentTile.occupants:
                    if unit.pieceType == unitType:
                        result.append(unit);
        return result
    
    def getPiecesByTeam(self, team):
        """
            Outputs a list of all gamePieces on the board on the team specified.
            
                team is a string
        """
        result = [];
        for i in range(self.minY, self.maxY):
            for j in range(self.minX, self.maxX):
                location = v.Vector(i,j);
                currentTile = self.getTile(location);
                for unit in currentTile.occupants:
                    if unit.team == team:
                        result.append(unit);
        return result
 
    def determineImpassable(self, impassableTypes):
        """
            Outputs a list of all tiles on the board corresponding to all of the impassable types of tiles.
            Different definitions of impassable are required for different types of actions in the game.
            
                impassableTypes is a list of strings, each corresponding to a terrain type of a Tile.
        """
        result = [];
        for terrain in impassableTypes:
            result.append(self.getTilesByType(terrain));
        return result
 
    def addPiece(self, gamePiece):
        """
            Add the selected piece to the board.
            
                gamePiece is a GamePiece object.  
                    Notably, it contains the desired location as an attribute.
        """    
        tile = self.getTile(gamePiece.location);
        for unit in tile.occupants:
            if unit.occupiesSquare:
                raise Exception("This square is already full.")
        tile.addPiece(gamePiece)
 
    def removePiece(self, gamePiece):
        """
            Removes the selected piece from the board.
            
                gamePiece is a GamePiece object.  
                    Notably, it contains its current location as an attribute.
        """
        tile = self.getTile(gamePiece.location);
        tile.removePiece(gamePiece)
    
    def movePiece(self, gamePiece, newLocation, impassableSquares):
        """
            Moves the selected gamePiece from its current location to the specified new location.
            
                gamePiece is a GamePiece object.  
                    Notably, it contains its current location as an attribute.
                newLocation is a Vector representing the new location of gamePiece.
                impassableSquares is a list of Vector locations representing which tiles pieces may not cross.
            
            This will throw an exception if the move is not valid, given the impassable terrain 
                and based on whether or not the unit has already moved.
        """
        self.removePiece(gamePiece);
        try:
            gamePiece.move(newLocation, impassableSquares);
        except Exception as error:
            print(error)
        self.addPiece(gamePiece)
        
# Some sample variables for testing purposes
tileList1 = [(v.Vector(0,0),'A'),(v.Vector(0,1), 'B'),(v.Vector(1,1),'C')]
gamePieceList1 = [gp.Infantry(1,1,'b'), gp.Cavalry(0,1,'b'),gp.Arsenal(0,0,'w'), gp.SwiftArtillery(0,0,'w')]
board1 = Board(tileList1,gamePieceList1);
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        