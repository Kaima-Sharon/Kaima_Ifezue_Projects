import os
import phylib
import sqlite3

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;

# add more here
BALL_DIAMETER  = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS  = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH  = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE  = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON  = phylib.PHYLIB_VEL_EPSILON;
DRAG  = phylib.PHYLIB_DRAG;
MAX_TIME  = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS  = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL = 0.01;
################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
                      "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg ( self ):
        sbStr = """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n"""%(self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

        return sbStr;

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class
    """

    def __init__( self, number, pos, vel, acc ):

        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y) and acceleration (x,y) as arguments
        """

        #creates a generic phylib object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_ROLLING_BALL, 
                                       number, pos, vel, acc, 0.0, 0.0);
            
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    def svg ( self ):
        rbStr = """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n"""%(self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

        return rbStr;

class Hole( phylib.phylib_object ):
    """
    Python Hole Class
    """

    def __init__( self, pos ):

        """
        Constructor function. Requires hole position (x,y)
        """

        #creates a generic phylib object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HOLE, 
                                        0, pos, None, None, 0.0, 0.0 );
                
        #this converts the phylib_object into a Hole class
        self.__class__ = Hole;

    def svg ( self ):
        holeStr = """<circle cx="%d" cy="%d" r="%d" fill="black" />\n"""%(self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS, )

        return holeStr;

class HCushion( phylib.phylib_object ):
    """
    Python HCushion Class
    """

    def __init__( self, y ):

        """
        Constructor function. Requires y coordinate of horinzontal cushion
        """

        #creates a generic phylib object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HCUSHION,
                                        0, None, None, None, 0.0, y);
        
        #this converts the phylib_object into a Hole class
        self.__class__ = HCushion;

    def svg ( self ):
        y = -25 if self.obj.hcushion.y == 0 else 2700
        HCushionStr = """<rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n"""%(self.obj.hcushion.y)

        return HCushionStr;

class VCushion( phylib.phylib_object ):
    """
    Python VCushion Class
    """

    def __init__( self, x ):

        """
        Constructor function. Requires x coordinate of vertical cushion
        """

        #creates a generic phylib object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_VCUSHION,
                                        0, None, None, None, x, 0.0);
        
        #this converts the phylib_object into a Hole class
        self.__class__ = VCushion;

    def svg ( self ):
        x = -25 if self.obj.vcushion.x == 0 else 1350
        VCushionStr = """<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n"""%(self.obj.vcushion.x)

        return VCushionStr;


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self, tableID=None, time=None ):
        """
        Table constructor method.
        """
        phylib.phylib_table.__init__( self );
        self.TABLEID = tableID
        self.TIME = time
        self.balls = []
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg ( self ):
        svgString = HEADER 

        for object in self:
            if object is not None:
                svgString += "%s"%object.svg()
        svgString += FOOTER

        return svgString

    def roll( self, t ):
            new = Table();
            for ball in self:
                if isinstance( ball, RollingBall ):
                    # create4 a new ball with the same number as the old ball
                    new_ball = RollingBall( ball.obj.rolling_ball.number,
                                            Coordinate(0,0),
                                            Coordinate(0,0),
                                            Coordinate(0,0) );
                    # compute where it rolls to
                    phylib.phylib_roll( new_ball, ball, t );

                    # add ball to table
                    new += new_ball;

                if isinstance( ball, StillBall ):
                    # create a new ball with the same number and pos as the old ball
                    new_ball = StillBall( ball.obj.still_ball.number,
                                          Coordinate( ball.obj.still_ball.pos.x,
                                                      ball.obj.still_ball.pos.y ) );
                    # add ball to table
                    new += new_ball;

            # return table
            return new;
    
    def cueBall(self):
        # Retrieve the cue ball from the table
        for ball in self.balls:
            if ball.number == 0:
                return ball

        # Return None if cue ball not found
        return None

class Database ():
    def __init__ (self, reset=False ) :
        dataBaseFName = "phylib.db"

        #if reset = True, delete database for fresh database creation
        if reset and os.path.exists(dataBaseFName):
            os.remove(dataBaseFName)
            print(f"Deleted existing 'dataBaseFName' for reset.")

        #create database connection and store it as a class attribute
        self.conn = sqlite3.connect(dataBaseFName)
        self.cursor = self.conn.cursor()

        # call createDB to create the necessary tables
        self.createDB()

    def createDB(self) :

        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Ball (
                    BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    BALLNO INTEGER NOT NULL,
                    XPOS FLOAT NOT NULL,
                    YPOS FLOAT NOT NULL,
                    XVEL FLOAT,
                    YVEL FLOAT,
                    FOREIGN KEY (BALLID) REFERENCES Ball
                );
            ''')
        
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS TTable (
                    TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    TIME FLOAT NOT NULL
                );
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS BallTable (
                    BALLID INTEGER NOT NULL, 
                    TABLEID INTEGER NOT NULL, 
                    FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                    FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
                );
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Shot (
                    SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    PLAYERID INTEGER NOT NULL,
                    GAMEID INTEGER NOT NULL,
                    FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                    FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                );
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS TableShot (
                    TABLEID INTEGER NOT NULL,
                    SHOTID INTEGER NOT NULL,
                    FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                    FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
                );
            ''')
        
            self.cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS Game (
                    GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    GAMENAME VARCHAR(64)
                );
            ''')

            self.cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS Player (
                    PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    GAMEID INTEGER NOT NULL,
                    PLAYERNAME VARCHAR(64) NOT NULL,
                    FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                );
            ''')

            # commit changes and close cursor
            self.conn.commit()
        finally:
            # close cursor and commit connection
            self.cursor.close()
            self.conn.commit()

    # def readTable( self, tableID ):
    #     cursor = self.conn.cursor()
    #     table = Table()
    #     Id = tableID + 1
    #     ball = []

    #     # Get balls from Ball table based on TABLEID
    #     cursor.execute('''
    #                    SELECT * FROM BALL INNER JOIN BALLTABLE 
    #                    WHERE (BALL.BALLID = BALLTABLE.BALLID 
    #                    AND BALLTABLE.TABLEID = ?);
    #     ''',(Id,));
    #     ball = cursor.fetchall()

    #     if ball == []:
    #         return None;
    #     else:
    #         # Get the time from TTABLE based on TABLEID
    #         cursor.execute('''
    #                    SELECT * FROM TTABLE 
    #                    WHERE (TTABLE.TABLEID = ?);
    #         ''',(Id,));
    #         table.time = (cursor.fetchall())[0][1];

    #         for i in range(0,len(ball)):
    #             # if its a stillBall, set the following columns
    #             if ball[i][4] == 0 and ball[i][5] == 0:
    #                 xpos = ball[i][2]
    #                 ypos = ball[i][3]
    #                 stillb = StillBall(ball[i][1], Coordinate(xpos, ypos));
    #                 table.iadd(stillb)
    #             else:
    #             # if its a RollingBall, set the following columns
    #                 xpos = ball[i][2]
    #                 ypos = ball[i][3]
    #                 xvel = ball[i][4]
    #                 yvel = ball[i][5]

    #                 vel = Coordinate(xvel, yvel)
    #                 speed = phylib.phylib_length(vel)

    #                 if speed != 0:
    #                     rollb = RollingBall(ball[i][1], Coordinate(xpos, ypos), vel, Coordinate(-DRAG * xvel / speed, -DRAG * yvel / speed))
    #                     table.iadd(rollb)

    #     self.conn.commit()
    #     cursor.close()

    #     return table


    def readTable(self, tableID):

        self.cursor = self.conn.cursor()

        try:

            with self.conn:

                tempID = tableID + 1

                self.cursor.execute ("""
                    SELECT Ball.BALLID, BALLNO, XPOS, YPOS, XVEL, YVEL
                    FROM Ball
                    JOIN BallTable WHERE (Ball.BallID = BallTable.BALLID
                    AND BallTable.TABLEID = ?);
                """, (tempID,))
                
                #Execute the query 
                #self.cursor.execute(query, (tempID,))

                # fetch all rows
                rows = self.cursor.fetchall()   

                if not rows:
                    return None    # If TABLEID does not exist in BallTable table, return None

                else:
                    # create a table object
                    table = Table()

                    for row in rows:
                        ball_id, ball_no, xpos, ypos, xvel, yvel = row
                        position = Coordinate(xpos, ypos)
                        velocity = Coordinate(xvel, yvel)

                        if xvel == 0.0 and yvel == 0.0:
                            ball = StillBall(ball_no, position)
                            xPos = xpos
                            yPos = ypos
                            table += ball
                        else:
                            xPos = xpos
                            yPos = ypos
                            xVel = xvel
                            yVel = yvel

                            # Calculate acceleration for RollingBall
                            acceleration = phylib.phylib_length(velocity)

                            if acceleration != 0:
                                ball = RollingBall(ball_no, position, velocity, Coordinate(-DRAG * xVel / acceleration, -DRAG * yVel / acceleration))

                                # Add ball to the table
                                table += ball

                    # Retrieve time attribute from TTable SQL table
                    query_time = "SELECT TIME FROM TTable WHERE TABLEID = ?"
                    self.cursor.execute(query_time, (tableID + 1,))
                    time = self.cursor.fetchone()[0]
                    table.TIME = time

                return table

        finally:
            self.cursor.close()
            self.conn.commit()

    def writeTable( self, table ):
        cursor = self.conn.cursor()
        #table = Table() took out

        #insert Time unto TTABLE
        cursor.execute('''
                       INSERT INTO TTABLE(TIME)
                       VALUES (%f);
        ''' %(table.time));
        tableID = cursor.lastrowid

        for ball in table :
            if ball is not None:
            #if the object on the table is a Rolling ball
                if type(ball) == RollingBall:
                    cursor.execute('''
                                INSERT INTO BALL(BALLNO, XPOS, YPOS, XVEL, YVEL)
                                VALUES (?, ?, ?, ?, ?);
                    ''',(ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y));
                    #print("test 1")
                #if the object on the table is a Still ball
                elif type(ball) == StillBall:
                    cursor.execute('''
                                INSERT INTO BALL(BALLNO, XPOS, YPOS, XVEL, YVEL)
                                VALUES (?, ?, ?, 0.0, 0.0);
                    ''',(ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y));
                    #print("test 2")
                ballID = cursor.lastrowid
                cursor.execute('''
                            INSERT INTO BALLTABLE(BALLID, TABLEID)
                            VALUES (%d,%d);
                ''' %(ballID, tableID));

        self.conn.commit()
        cursor.close()
        return tableID - 1;

    # def writeTable ( self, table):

    #     self.cursor = self.conn.cursor()

    #     self.cursor.execute('''
    #                 INSERT INTO TTABLE(TIME)
    #                 VALUES (%f);
    #     ''' %(table.time));
    #     table_id = self.cursor.lastrowid

    #     # Insert Ball records in the Ball table
    #     for ball in table:

    #         if type(ball) == RollingBall:
    #             self.cursor.execute('''
    #                 INSERT INTO BALL(BALLNO, XPOS, YPOS, XVEL, YVEL)
    #                 VALUES (?, ?, ?, ?, ?);
    #             ''',(ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y));
                
    #         #if the object on the table is a Still ball
    #         elif type(ball) == StillBall:
    #             self.cursor.execute('''
    #                         INSERT INTO BALL(BALLNO, XPOS, YPOS, XVEL, YVEL)
    #                         VALUES (?, ?, ?, 0.0, 0.0);
    #             ''',(ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y));
                
    #         # Retrieve the auto-generated BALLID
    #         ball_id = self.cursor.lastrowid

    #         self.cursor.execute('''
    #                         INSERT INTO BALLTABLE(BALLID, TABLEID)
    #                         VALUES (%d,%d);'''%(ball_id, table_id))

    #     self.conn.commit()
    #     self.cursor.close()

    #     return table_id - 1

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
        
    def setGame(self, gameName, player1Name, player2Name):

        self.cursor = self.conn.cursor()

        # Add a new row to the Game table
        query_game = "INSERT INTO Game (gameName) VALUES (?);"
        self.cursor.execute(query_game, (gameName,))
        gameID = self.cursor.lastrowid  # Retrieve the auto-generated gameID

        # Add new rows to the Player table
        query_player1 = "INSERT INTO Player (gameID, playerName) VALUES (?,?);"
        self.cursor.execute(query_player1, (gameID, player1Name,))
        player1ID = self.cursor.lastrowid  # Retrieve the auto-generated PLAYERID

        query_player2 = "INSERT INTO Player (gameID, playerName) VALUES (?,?);"
        self.cursor.execute(query_player2, (gameID, player2Name,))
        player2ID = self.cursor.lastrowid  # Retrieve the auto-generated PLAYERID

        self.conn.commit()
       
        return gameID
       
    def getGame(self, gameID):

        self.cursor = self.conn.cursor()

        # Retrieve game details using JOIN across Game and Player tables
        query = """
            SELECT G.gameID, G.gameName, P1.playerName AS player1Name, P2.playerName AS player2Name
            FROM Game G
            JOIN Player P1 ON G.player1ID = P1.PLAYERID
            JOIN Player P2 ON G.player2ID = P2.PLAYERID
            WHERE G.gameID = ?;
        """
        self.cursor.execute(query, (gameID,))
        result = self.cursor.fetchone()

        if result:
            return {
                'gameID': result[0],
                'gameName': result[1],
                'player1Name': result[2],
                'player2Name': result[3],
            }
        else:
            return None

    def getPlayerID(self, playerName):

        self.cursor = self.conn.cursor()

        # Retrieve playerID using playerName
        query = "SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?;"
        self.cursor.execute(query, (playerName,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            raise ValueError(f"Player with name {playerName} not found.")

    def getGameID(self, gameName):

        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT GAMEID FROM Game WHERE GAMENAME = ?;", (gameName,))
        gameID = self.cursor.fetchone()

        if gameID:
            return gameID[0]
        else:
            raise ValueError(f"Game with name {gameName} not found.")

    def newShot(self, gameName, playerName):

        self.cursor = self.conn.cursor()

        # Retrieve gameID and playerID using gameName and playerName
        gameID = self.getGameID(gameName)
        playerID = self.getPlayerID(playerName)

        # Add a new entry to the Shot table
        query = "INSERT INTO Shot (GAMEID, PLAYERID) VALUES (?, ?);"
        self.cursor.execute(query, (gameID, playerID))
        shotID = self.cursor.lastrowid  # Retrieve the auto-generated shotID

        # Commit changes to the database
        self.conn.commit()

        return shotID

class Game ():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):

        # if gameID != None
        # game2 = Game(None, "GameName", "PlayerName", "Player2Name", table_instance)

        # # Invalid calls 
        # gameInvalid = Game("Invalid", "Arguments")

        # if gameID != None:
        #     gameData = database.getGame(gameID)
        #     self.gameID = gameData['gameID']
        #     self.gameName = gameData['gameName']
        #     self.player1Name = gameData['player1Name']
        #     self.player2Name = gameData['player2Name']
        #     #self.table = database.readTable(self.gameID)
        # else:
        #     self.gameID = None
        #     self.gameName = gameName
        #     self.player1Name = player1Name
        #     self.player2Name = player2Name

        #     if gameName is not None and player1Name is not None and player2Name is not None:
        #         self.gameID = self.database.setGame(gameName, player1Name, player2Name)

        if gameID is not None and (gameName is None or player1Name is None or player2Name is None):
            gameID += 1
            self.getGame(gameID)

        elif gameID is None and (isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str)):
            dataB = Database(True)
            gameID = dataB.setGame(gameName, player1Name, player2Name)
            dataB.close()
        else:
            raise TypeError("Invalid combination of arguments provided to the constructor")

    

    def shoot( self, gameName, playerName, table, xvel, yvel ) :

        db = Database(False)
        # Add a new entry to the Shot table and retrieve shotID
        shotID = db.newShot(gameName, playerName)

        #if the cue ball is a stillBall
        for i in range(10, MAX_OBJECTS):
            if isinstance(table[i], StillBall) and table[i].obj.still_ball.number == 0:
                cue_ball = i
                xPos = table[cue_ball].obj.still_ball.pos.x;
                yPos = table[cue_ball].obj.still_ball.pos.y;
                break

        table[cue_ball].obj.type = phylib.PHYLIB_ROLLING_BALL
        table[cue_ball].__class__ = RollingBall

        # Set attributes of the cue ball
        table[cue_ball].obj.rolling_ball.pos.x = xPos
        table[cue_ball].obj.rolling_ball.pos.y = yPos
        table[cue_ball].obj.rolling_ball.vel.x = xvel
        table[cue_ball].obj.rolling_ball.vel.y = yvel

        # Set the number of the cue ball to 0
        table[cue_ball].obj.rolling_ball.number = 0

        # Initialize variables for segment loop
        start_time = table.time

        for obj in table:

            try:

                start_time = table.time
                temp_table = table

                # Call the segment method and get the length of the segment
                table = table.segment()

                # Loop over integers and create new frames
                time_passed = int((table.time - start_time) / FRAME_INTERVAL)

                for i in range (time_passed):

                    end_time = i * FRAME_INTERVAL

                    new_table = temp_table.roll(end_time)

                    # Call the roll method to create a new Table object for the next frame
                    new_table.time = start_time + time_passed

                    self.db.writeTable(new_table)

                    self.db.recordTableShot(shotID, new_table)

            except:
                break

            db.close()

    