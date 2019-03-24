# Monkey-Rabbit Games
# Candy Seller
# You need money to buy a car so you make a candy-selling shop.

# 16th October 2016: You dream about a monster. When you wake up, it all felt so real... You prepare for another candy-selling day. You spot something green in the shop window and are sure you had seen it before... The letter 'Q' pops into your head.

import random, sys, time, math, pygame

sys.path.append( '../GameEngine' )

from pygame.locals import *
from geometry import *
import viewport, game, game_map, game_dynamics
from game_objects import *
from game_constants import *




# Constants.

WINWIDTH = 800  # Width of the program's window, in pixels.
WINHEIGHT = 600 # Height in pixels.

BACKGROUND_COLOUR = (211, 211, 211)
SHOP_FLOOR_COLOUR = (240, 180, 211)

MOVERATE = Vector( 17, 10 ) # How fast the player moves in the x and y direction.
BOUNCERATE = 6       # How fast the player bounces (large is slower).
BOUNCEHEIGHT = 10    # How high the player bounces.
MANSIZE = 30         # How big the man is.
SHOPSIZE = 280       # How big the shops are.
MONEYSIZE = 20       # How big the money is.
ARROWSIZE = 160      # How big the arrows are.
BUSHSIZE = 200       # How big the bushes are.
MONSTERSIZE = 800    # How big the jumpscare monster is.




class CandySeller( game.Game ):
    def __init__( self, viewPort ):
        # Set up generic game one time set up.
        super().__init__( 'Candy Seller', 'gameiconc', viewPort )

        # Game one time setup.
        # self.setDrawOrder( 'BackGround', 'Shop', 'Arrow', 'Bush', 'Coin', 'Player', 'Monster', 'Score' )
        self.setCursor()
        viewPort.loadMusic( 'Money Ping.ogg' )
        viewPort.setCameraMovementStyle( game_dynamics.KeyMovementStyle( moveRate=Vector( 20, 12 ) ) )


    def loadImages( self ):
        images = self.images

        images.load( 'man', 'LR' )
        images.load( 'bush' )
        images.load( 'ingredients store' )
        images.load( 'jumpscare monster' )
        images.load( 'money' )
        images.load( 'shop', range( 1, 4 ) )
        images.load( 'arrow', range( 1, 4 ) )


    # Per game initialisation.
    def init( self ):
        self.winMode = False           # If the player has won.
        self.invulnerableMode = False  # If the player is invulnerable.
        self.invulnerableStartTime = 0 # Time the player became invulnerable.
        self.gameOverMode = False      # If the player has lost.
        self.gameOverStartTime = 0     # Time the player lost.
        self.moneyScore = 0
        self.player = None

        game.Game.init( self )


    def initMap( self ):
        viewPort = self.viewPort
        gameMap = self.gameMap
        images = self.images

        gameMap.setImageStore( images )

        gameMap.createScene( 'shops', backGroundColour=BACKGROUND_COLOUR )

        # Create scene objects.

        # Start off with some shops on the screen.
        self.createShops( gameMap )

        # Start off with some bushes on the screen.
        gameMap.addObject( Bush( Point( -200, 400 ), images.bush, size=BUSHSIZE ) )
        gameMap.addObject( Bush( Point( 928, 400 ), images.bush, size=BUSHSIZE ) )

        # Start off with some arrows on the screen.
        self.createArrows( gameMap )

        # Start off with some money on the screen.
        self.createCoins( gameMap, 4 )

        insideShop1 = SoftBackGround( ORIGIN, images.ingredients_store, size=WINWIDTH )
        insideShop1Rect = insideShop1.getRect()
        insideShop1Bounds = game_dynamics.RectangleBoundary( insideShop1Rect, grow=-10 )
        gameMap.createScene( 'insideShop1', backGroundColour=SHOP_FLOOR_COLOUR, boundaryStyle=insideShop1Bounds )
        gameMap.changeScene( 'insideShop1' )
        gameMap.addObject( insideShop1 )
        self.createCoins( gameMap, 4 )

        gameMap.changeScene( 'shops' )

        gameMap.addOverlay( Score( Point( viewPort.width - 180, 20 ), self.moneyScore ) )

        self.player = self.createPlayer()
        gameMap.addObject( self.player )


    def createPlayer( self ):
        viewPort = self.viewPort
        images = self.images
        # How big the player starts off.
        playerStartPos = Point( viewPort.halfWidth, viewPort.halfHeight )

        # Sets up the movement style of the player.
        # playerBounds = game_dynamics.RectangleBoundary( Rectangle( Point( 0, 220 ), Point( 900, 550 ) ) )
        playerBounds = game_dynamics.CollisionBoundary()
        moveStyle = game_dynamics.KeyMovementStyle( boundaryStyle=playerBounds )
        moveStyle.setMoveRate( MOVERATE )
        moveStyle.setBounceRates( BOUNCERATE, BOUNCEHEIGHT )

        return Player( playerStartPos, moveStyle, size=MANSIZE, ratio=1.0, imageL=images.manL, imageR=images.manR )


    def createShops( self, gameMap ):
        for shopNum in range( 1, 4 ):
            shopPos = Point( 140 + ( shopNum - 1 ) * 320, 140 )
            shop = Shop( shopPos, self.images.shops[shopNum], size=SHOPSIZE, name='Shop{}'.format( shopNum ) )
            gameMap.addObject( shop )


    def createArrows( self, gameMap ):
        for arrowNum in range( 1, 4 ):
            arrowPos = Point( ( arrowNum - 1 ) * 320 + 30, 640 )
            arrow = Arrow( arrowPos, self.images.arrows[arrowNum], size=ARROWSIZE )
            gameMap.addObject( arrow )


    def createCoins( self, gameMap, num ):
        for ii in range( num ):
            pos = Point( random.randint( 0, WINWIDTH ), random.randint( 400, 500 ) )
            coin = Coin( pos, self.images.money, size=MONEYSIZE )
            gameMap.addObject( coin )


    def createMonster( self ):
        return Monster( Point( 0, 0 ), self.gameMap.images.jumpscare_monster, size=MONSTERSIZE, ratio=1.0 )


    # Could move cursor description into a file and read from there.
    def setCursor( self ):
        thickarrow_strings = (               # Sized 24x24.
            "XXXXXXXXXXX             ",
            " X.......X              ",
            "  X.....X               ",
            "   X...X                ",
            "  X.....X               ",
            " X.......X              ",
            "X.........X             ",
            "X.........X             ",
            "X.........X             ",
            " X.......X              ",
            "  X.....X               ",
            "   X...X                ",
            "  X.....X               ",
            " X.......X              ",
            "XXXXXXXXXXX             ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ")
        datatuple, masktuple = pygame.cursors.compile( thickarrow_strings,
                                      black='X', white='.', xor='o' )
        pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )


    def setSceneShop1( self ):
        gameMap = self.gameMap

        if gameMap.changeScene( 'insideShop1' ):
            viewPort = self.viewPort
            player = self.player
            player.moveToScene( 'insideShop1' )
            viewPort.resetCamera()
            player.pushPos( Point( viewPort.halfWidth, viewPort.halfHeight ), offsetOldPos=Point( 0, 20 ) )


    def setSceneShops( self ):
        gameMap = self.gameMap

        if gameMap.changeScene( 'shops' ):
            player = self.player
            player.popPos()
            player.moveToScene( 'shops' )


    def processEvent( self, event ):
        game.Game.processEvent( self, event )

        viewPort = self.viewPort
        gameMap = self.gameMap
        player = self.player

        if event.type == KEYDOWN:
            if event.key == K_r and self.winMode:
                self.running = False
            elif event.key is K_q:
                # Releases the jumpscare if you press 'q'.
                viewPort.playSound( "Jumpscare V2" )
                monster = self.createMonster()
                gameMap.addSprite( monster )
        elif event.type == KEYUP:
            if event.key is K_q:
                gameMap.deleteAllObjectsOfType( 'Monster' )
            elif event.key is K_i:
                self.setSceneShop1()
            elif event.key is K_o:
                self.setSceneShops()
        elif event.type == MOUSEBUTTONUP:
            # This can now be handled with a CLICK_COLLISION_EVENT.
            if None is self.clackPos:
                arrow = gameMap.objectsOfType( go.Arrow )[0]
                wClickPos = viewPort.getWorldCoordinate( self.clickPos )

                # Does the click point collide with a colour that is not the background colour.
                if viewPort.collisionOfPoint( self.clickPos, arrow ):
                    viewPort.playSound( 'Money Ping' )
        elif event.type == COLLISION_EVENT:
            if event.obj1.isInteractionTypePair( event.obj2, 'Player', 'Shop=Shop1' ):
                collisionData = event.collisionData
                collisionPoint = event.point
                x = collisionPoint.x
                y = collisionPoint.y
                rect = event.obj2.getRect()
                width = rect.right - rect.left
                thirdWidth = width / 3
                left = rect.left + thirdWidth
                right = rect.right - thirdWidth
                middle = rect.centery

                # print( 'left %s right %s point %s' % ( left, right, collisionPoint ) )

                if y > middle and x > left and x < right:
                    self.setSceneShop1()


    def updateState( self ):
        game.Game.updateState( self )

        if self.gameOverMode:
            return

        viewPort = self.viewPort
        gameMap = self.gameMap
        player = self.player

        # If the man has walked a certain distance then make a new coin.
        if player.steps >= 400:
            self.createCoins( gameMap, 1 )
            player.steps = 0

        # Check if the player has collided with any money.
        money = gameMap.objectsOfType( go.Coin )

        for ii in range( len( money ) - 1, -1, -1 ):
            coin = money[ii]

            if player.collidesWithRect( coin ):
                # A player/money collision has occurred.
                coin.delete()
                self.moneyScore += 1
                viewPort.playMusic()

        # Update the money score.
        gameMap.score.updateScore( self.moneyScore )

        # Wins the game if you get 100 money.
        if self.moneyScore >= 100:
            self.winMode = True


    # Update the positions of all the map objects according to the camera and new positions.
    def updateMap( self ):
        # Update the generic map stuff.
        game.Game.updateMap( self )

        viewPort = self.viewPort
        gameMap = self.gameMap
        player = self.player

        # Update the player man.
        player.update( viewPort.camera, gameOverMode=self.gameOverMode, invulnerableMode=self.invulnerableMode )


    def run( self ):
        print( "You own a business that's in London. You live in Poole." )
        print( "Poole is too far away from London to walk, and you do not have a car." )
        print( "You have to make money somehow. I know, you can create a candy shop!" )
        #time.sleep(10)

        game.Game.run( self )




def main():
    viewPort = viewport.ViewPort( WINWIDTH, WINHEIGHT, topLeft=Point( 400, 80 ) )
    game = CandySeller( viewPort )

    while True:
        game.run()
        # Re-initialised the game state.
        game.reset()


if __name__ == '__main__':
    main()

