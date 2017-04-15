# Monkey-Rabbit Games
# Game Dynamics

from pygame.locals import *
from geometry import *


# Constants.

DEFAULT_MOVERATE = 10

DEFAULT_KEYSMAP = {
    'left'  : ( K_LEFT, K_a ),
    'right' : ( K_RIGHT, K_d ),
    'up'    : ( K_UP, K_w, ),
    'down'  : ( K_DOWN, K_s )
}




class Directions:
    DIRECTIONS = {
        'left'  : 'horizontal',
        'right' : 'horizontal',
        'up'    : 'vertical',
        'down'  : 'vertical'
    }

    AXES = {
        'horizontal'    : ( 'left', 'right' ),
        'vertical'      : ( 'up', 'down' )
    }


    def __init__( self ):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.horizonal = False
        self.vertical = False


    def __getattr__( self, key ):
        # if key == 'horizontal':
        #     value = self.__dict__['left'] or self.__dict__['right']
        # elif key == 'vertical':
        #     value = self.__dict__['up'] or self.__dict__['down']
        if key == 'any':
            value = self.horizontal or self.vertical
        else:
            value = self.__dict__[key]

        return value


    def __setattr__( self, key, value ):
        if key in Directions.DIRECTIONS.keys():
            self.__dict__[key] = value
            axis = Directions.DIRECTIONS[key]

            if value:
                axisValue = key
            else:
                axisValue = False

                for direction in Directions.AXES[axis]:
                    if self.__dict__.has_key( direction ) and self.__dict__[direction]:
                        axisValue = direction

            self.__dict__[axis] = axisValue
        else:
            self.__dict__[key] = value


    def __getitem__( self, key ):
        return self.__getattr__( key )


    def __setitem__( self, key, value ):
        return self.__setattr__( key, value )




# Interface of all movement Styles.
class MovementStyle:
    def __init__( self ):
        self.moveObject = None


    def setMoveObject( self, moveObject ):
        self.moveObject = moveObject


    def moving( self ):
        return False


    # Get the new position based on the movement style.
    def move( self, pos ):
        return pos




class KeyMovementStyle( MovementStyle ):
    def __init__( self, moveRate = DEFAULT_MOVERATE, bounceRate = 0, bounceHeight = 0 ):
        self.moveBounds = None
        self.moveRate = moveRate
        self.bounceRate = bounceRate
        self.bounceHeight = bounceHeight
        self.directions = Directions()
        self.bounce = 0
        self.dirToKeysMap = DEFAULT_KEYSMAP
        self.createKeyToDirMap()


    def createKeyToDirMap( self ):
        dirToKeysMap = self.dirToKeysMap
        self.keyToDirMap = keyToDirMap = {}

        for direction in self.dirToKeysMap.keys():
            keys = dirToKeysMap[direction]

            for key in keys:
                keyToDirMap[key] = direction

        dirToKeysMap['horizontal'] = dirToKeysMap['left'] + dirToKeysMap['right']
        dirToKeysMap['vertical'] = dirToKeysMap['up'] + dirToKeysMap['down']
        dirToKeysMap['all'] = dirToKeysMap['horizontal'] + dirToKeysMap['vertical']


    def setMoveRate( self, moveRate ):
        self.moveRate = moveRate


    def setBounceRates( self, bounceRate, bounceHeight ):
        self.bounceRate = bounceRate
        self.bounceHeight = bounceHeight


    def setMovement( self, key ):
        if key in self.dirToKeysMap['all']:
            direction = self.keyToDirMap[key]
            self.directions[direction] = True


    def stopMovement( self, key = None ):
        if not key:
            self.directions = {}
        elif key in self.dirToKeysMap['all']:
            direction = self.keyToDirMap[key]
            self.directions[direction] = False


    def moving( self, direction = 'any' ):
        return self.directions[direction]


    # Get the new position based on the movement style.
    def move( self, pos ):
        newPos = Point( pos )

        if self.moving():
            horizontalMovement = self.moving( 'horizontal' )
            verticalMovement = self.moving( 'vertical' )

            if horizontalMovement:
                if 'left' == horizontalMovement:
                    newPos.x -= self.moveRate
                else:
                    newPos.x += self.moveRate

            if verticalMovement:
                if 'up' == verticalMovement:
                    newPos.y -= self.moveRate
                else:
                    newPos.y += self.moveRate

            if horizontalMovement or self.bounce != 0:
                self.bounce += 1

            if self.bounce > self.bounceRate:
                # Reset bounce amount.
                self.bounce = 0

        return newPos




class BoundedKeyMovementStyle( KeyMovementStyle ):
    def __init__( self, moveBounds, **kwArgs ):
        KeyMovementStyle.__init__( self, **kwArgs )
        self.moveBounds = moveBounds


    def setMoveBounds( self, bounds ):
        self.moveBounds = bounds


    # Get the new position based on the movement style.
    def move( self, pos ):
        newPos = KeyMovementStyle.move( self, pos )

        if newPos != pos:
            # Restrict the player's movement to the specified boundary.
            newPos = self.moveBounds.boundPoint( newPos )

        return newPos




class CollisionKeyMovementStyle( KeyMovementStyle ):
    def __init__( self, viewPort, **kwArgs ):
        KeyMovementStyle.__init__( self, **kwArgs )
        self.viewPort = viewPort


    def setViewPort( self, viewPort ):
        self.viewPort = viewPort


    # Get the new position based on the movement style.
    def move( self, pos ):
        newPos = KeyMovementStyle.move( self, pos )

        if newPos == pos:
            return pos

        moveObject = self.moveObject
        offset = newPos - pos

        if not moveObject.collidesWithColour( self.viewPort, offset ) \
           or moveObject.collidesWithColour( self.viewPort ):
            newPos = pos

        return newPos