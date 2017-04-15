# Monkey-Rabbit Games
# Game Engine

import random, sys, time, math, pygame, copy
from geometry import *
from pygame.locals import *


# Constants.

DEFAULT_FPS = 30 # frames per second to update the screen




class Game:
    def __init__( self, name, icon, viewPort ):
        # Set up the game state variables.
        self.viewPort = viewPort
        self.clickDragLimit = 10
        self.clickPos = None
        self.dragPos = None
        self.fpsClock = pygame.time.Clock()
        self.drawOrder = None
        self.cameraUpdates = None
        self.debugDraw = False

        pygame.display.set_caption( name )
        pygame.display.set_icon( pygame.image.load( icon ) )

        self.init()


    def init( self ):
        self.running = True


    def reset( self ):
        self.init()


    def terminate( self ):
        pygame.quit()
        sys.exit()


    def setDrawOrder( self, *args ):
        self.drawOrder = args


    def setCameraUpdates( self, *cameraUpdates ):
        self.cameraUpdates = cameraUpdates


    def addCameraUpdates( self, *cameraUpdates ):
        self.cameraUpdates.extend( cameraUpdates )


    def addDebugText( self, text, pos, colour ):
        self.gameMap.addObject( DebugText( self.viewPort.basicFont, text, pos, colour ) )
        # DebugText( '%s' % (pos), ( pos.x + 80, pos.y + 40 ), RED )
        # DebugText( '%s' % (rect), ( pos.x + 120, pos.y + 80 ), RED )


    def processEvents( self ):
        # Event handling loop.
        for event in pygame.event.get():
            self.processEvent( event )


    # Generic game event processing.
    def processEvent( self, event ):
        if event.type == QUIT:
            self.terminate()
            self.running = False
        elif KEYUP == event.type:
            if K_ESCAPE == event.key:
                self.terminate()
            elif K_p == event.key:
                self.debugDraw = not self.debugDraw
        elif MOUSEBUTTONDOWN == event.type:
            # Remember position.
            self.clickPos = Point( event.pos )
        elif MOUSEBUTTONUP == event.type:
            # If clickPos nearby event.pos.
            dragPos = Point( event.pos )

            if self.viewPort.positionNear( dragPos, self.clickPos, self.clickDragLimit ):
                self.dragPos = None
            else:
                self.dragPos = dragPos


    # Update the state of the game.
    def updateState( self ):
        pass


    # Update the positions of all the map objects according to the camera and new positions.
    def updateMap( self ):
        viewPort = self.viewPort
        gameMap = self.gameMap

        # Update the objects offset by the camera.
        gameMap.update( viewPort.camera, self.cameraUpdates )


    # Update the game state, map and player.
    def update( self ):
        self.updateState()
        self.updateMap()
        self.fpsClock.tick( DEFAULT_FPS )


    def draw( self ):
        viewPort = self.viewPort
        gameMap = self.gameMap

        # Draw the background.
        viewPort.drawBackGround( gameMap.backGroundColour )

        # Draw all the map objects.
        gameMap.draw( viewPort, self.drawOrder, debugDraw=self.debugDraw )

        viewPort.draw()


    def run( self ):
        # Main game loop.
        while self.running:
            self.draw()
            self.processEvents()
            self.update()