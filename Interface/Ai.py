

from typing                 import List, Set, Tuple
from Interface.gameBox      import GameBox
from Interface.util         import Utility
import random               as RANDOM


class AStarPathFinding():
    MAX_TRY_NODE = (Utility.GAME_BOX_GRID[0] * Utility.GAME_BOX_GRID[1] )
    
    class Node():
        """A node class for A* Pathfinding"""

        def __init__(self, parent=None, position=None):
            self.parent     = parent
            self.position   = position

            self.g = 0
            self.h = 0
            self.f = 0

        def __eq__(self, other):
            return self.position == other.position

        def __hash__(self):               #<-- added a hash method
            return hash(self.position)

        def getPosition( self ):
            return self.position

    def __init__(self) -> None:
        pass

    def _findNearEnd( self, maze: List[List[GameBox]], targetPos:Tuple[int, int]  ):
        flagList:List[List[bool]]       = [[False for x in range(Utility.GAME_BOX_GRID[1])] for y in range(Utility.GAME_BOX_GRID[0])]
        walkStack:List[(int, int)]      = []  
        walkStack.append( targetPos )
        currentPos = walkStack[0]

        resultPos = None
        while( len( walkStack ) > 0 ):
            
            currentPos = walkStack[0]
            walkStack.pop( 0 )
            flagList[ currentPos[0] ][ currentPos[1] ]  = True

            for direct in RANDOM.sample( Utility.MOVE_DIRECTION, 4 ): # Adjacent squares

                newPos = (currentPos[0] + direct[0], currentPos[1] + direct[1])
                # Make sure within range
                if newPos[0] > (Utility.GAME_BOX_GRID[0] - 1) or newPos[0] < 0 or newPos[1] > (Utility.GAME_BOX_GRID[1] - 1) or newPos[1] < 0:
                    continue

                if( flagList[ newPos[0] ][ newPos[1] ] == False ):
                    if( maze[ newPos[0] ][ newPos[1] ].isObstruction() == False ):
                        if( resultPos == None ):
                            resultPos = newPos
                    elif( maze[ newPos[0] ][ newPos[1] ].isEnemyOn() == True ):
                        walkStack.append( newPos )

        return resultPos, flagList
            


    def find(self, maze: List[List[GameBox]], startPos:Tuple[int, int], endPos:Tuple[int, int] ) -> None:
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        openList:List[AStarPathFinding.Node]    = []
        closeList:Set[AStarPathFinding.Node]    = set()

        # Add the start node
        startNode               = AStarPathFinding.Node(None, startPos )
        newEndPos, flagList     = self._findNearEnd( maze=maze, targetPos=endPos )
        endNode                 = AStarPathFinding.Node(None,  newEndPos )

        # 假如是自己
        if( flagList[ startPos[0] ][ startPos[1] ] == True ):
            return None


        openList.append( startNode )
        
        tryCount = 0

        # 計算到找到路近
        while len( openList ) > 0:

            # 搜尋過久，跳出
            tryCount += 1
            if( tryCount > AStarPathFinding.MAX_TRY_NODE ):
                return None

            # 取得現在節點
            currentNode = openList[0]
            currentIndex = 0

            for index, item in enumerate( openList ):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIndex = index

            # 移除已經算過的 Node，並且加入至封閉
            openList.pop( currentIndex )
            closeList.add( currentNode )

            # 找到目標位置
            if currentNode == endNode:
                path = []
                current = currentNode
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path


            # Generate children
            children:List[AStarPathFinding.Node]  = []
            for newPosition in Utility.MOVE_DIRECTION: # Adjacent squares

                # Get node position
                nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])

                # Make sure within range
                if nodePosition[0] > (Utility.GAME_BOX_GRID[0] - 1) or nodePosition[0] < 0 or nodePosition[1] > (Utility.GAME_BOX_GRID[1] - 1) or nodePosition[1] < 0:
                    continue

                # Make sure walkable terrain
                walkNode = maze[ nodePosition[0] ][ nodePosition[1] ]
                if walkNode.isObstruction() == True :
                    continue


                # Create new node
                newNode = AStarPathFinding.Node(currentNode, nodePosition)

                # Append
                children.append( newNode )

            # Loop through children
            for child in children:

                # Child is on the closed list
                if child in closeList:
                    continue

                # Create the f, g, and h values
                child.g = currentNode.g + 1
                child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for openNode in openList:
                    if child == openNode and child.g > openNode.g:
                        continue

                # Add the child to the open list
                openList.append( child )

        pass