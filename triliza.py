# -*- coding: cp1252 -*-
#Project: triliza.py
#Author: Niko Pinnis
#Copyright 2012-2017 Niko Pinnis
#Code released under the MIT Licence
#Python version 2.6.4

"""
A simple command line based tic-tac-toe game
Featuring 2 different game modes (interactive, cmd commands)
The game properties are given in this format: X Y W
where X is the rows, Y the columns and W the victory condition of the game
e.g 3 3 3 gives a standard 3x3 game.
available options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  Read game sitiation from FILE
  -n, --new             Start a new game
  -i, --interactive     Play game in interactive mode
  -s, --save            Saves the table after the game ends and
                        if the game is closed by the player it
                        can be loaded in the commandline mode
Any parameters given that are not on this table will raise an error.
"""

import sys, random, getopt
version = 'v 1.3 final'

#-------------------------------------------------------------------------------
#----------------------------New grid creator-----------------------------------
#-------------------------------------------------------------------------------

def maketable(rows, columns):
    """
    Creates a 2-dimensional list with the specified number
    of rows and columns.
    """
    if rows <= 0 or columns <= 0:
        print 'dimensions must be positive integers'
        sys.exit(0)
    table = list()
    for i in range(rows):
        row = list('-')
        for j in range(columns-1):
            row.append('-')
        table.append(row)
    return table

#-------------------------------------------------------------------------------
#----------------------------Current grid printer-------------------------------
#-------------------------------------------------------------------------------

def printtable(rows, columns, table):
    """
    Print a two dimensional list as a matrix, numbering its
    rows and columns. The amount of rows and columns must be given.
    """
    line = ' '
    for j in range(columns):
        line += ' %i' %(j)
    print line
    for i in range(rows):
        line = '%i' %(i)
        for j in range(columns):
            line = line + ' %s' %(table[i][j])
        print line

#-------------------------------------------------------------------------------
#-----------------------------Verify input--------------------------------------
#-------------------------------------------------------------------------------

def checkinput(coords):
    """
    Checks if the input is in the format X Y and returns True
    else returns False.
    X and Y must be numbers separated by one space only.
    """
    if coords.startswith(' ') or coords.endswith(' '):
        return False
    for i in range(0, len(coords)): #checks first part of input if numerical
        if coords[i].isdigit():
            continue
        else:
            if coords[i] == ' ':    #determines if the second part is numerical
                for j in range(len(coords)-1, i, -1):
                    if coords[j].isdigit():
                        continue
                    else:
                        return False
                return True
            else:
                return False
    return False


#-------------------------------------------------------------------------------
#-----------------------------read X coordinate---------------------------------
#-------------------------------------------------------------------------------

def read_x(coords):
    """
    Separates the X component from an input in the format X Y
    e.g 2 4 , 1 4 , 123 131
    Returns X coordinate as integer.
    """
    coord = ''
    for i in range(0, len(coords)):
        if coords[i] != ' ':
            coord += coords[i]
        elif coords[i] == ' ':
            try:
                x_coord = int(coord)   
                break
            except TypeError:               #should not happen if checkinput
                print 'error in input: X'   #works properly
    return x_coord


#-------------------------------------------------------------------------------
#-----------------------------read Y coordinate---------------------------------
#-------------------------------------------------------------------------------

def read_y(coords):
    """
    Separates the Y component from an input in the format X Y
    e.g 2 4 , 1 4 , 123 , 131
    Returns Y coordinate as integer.
    """
    coord = ''
    coords_rev = coords[::-1]   #reverse the input
    for i in range(0, len(coords_rev)):
        if coords[i] != ' ':
            coord += coords_rev[i] #take the y-coord in a reversed form
        elif coords[i] == ' ':
            y_coord = int(coord[::-1]) #reverse again for the y-coord
            break
    return y_coord


#-------------------------------------------------------------------------------
#-----------------------------Winner check--------------------------------------
#-------------------------------------------------------------------------------

def wincheck(table, to_win):
    """
    This function uses multiple for-loops to check if the victory
    conditon has been met by either player.
    The analysis is done separately for each axis in the grid
    (horiz, vert, diag). It returs a string containing
    the symblol of the winner (X or 0) or if there
    is no winner it return None.
    Requires 2-dimensional list to be prossesed and the victory condition.
    """
    x_size = len(grid)      #Gets the needed size of the table's dimensions 
    y_size = len(grid[0])
#---Horizontal------------------------------------------------------------------
    for i in range(0, x_size):
        line = ''
        for j in range(0, y_size):
            line += table[i][j]
        for z in range(0, len(line)):           #the loops go through all the 
            if line[z] == 'x':                  #elements in a straight line 
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'x':
                        group += line[k]        #group increases as long as the
                    else:                       #loop finds the same character
                        group = ''              #if something else comes next
                    if len(group) >= to_win:    #the group is nullified
                        result = 'x'
                        return result
            if line[z] == 'o':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'o':
                        group += line[k]
                    else:
                        group = ''              #the same method is used
                    if len(group) >= to_win:    #throughout the algorithm
                        result = 'o'
                        return result
#---Vertical--------------------------------------------------------------------
    for i in range(0, x_size):
        line = ''
        for j in range(0, y_size):
            line += table[j][i]
        for z in range(0, len(line)):
            if line[z] == 'x':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'x':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'x'
                        return result
            if line[z] == 'o':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'o':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'o'
                        return result
#---Diagonal left>right>down----------------------------------------------------
    for x in range(0, x_size):
        j = 0
        line = ''
        for i in range(x, x_size):
            line += table[i][j]
            j += 1
            if j == y_size:
                break
        for z in range(0, len(line)):
            if line[z] == 'x':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'x':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'x'
                        return result
            if line[z] == 'o':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'o':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'o'
                        return result
#---Diagonal left>right>up------------------------------------------------------
    for y in range(0, y_size):
        i = 0
        line = ''
        for j in range(y, y_size):
            line += table[i][j]
            i += 1
            if i == x_size:
                break
        for z in range(0, len(line)):
            if line[z] == 'x':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'x':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'x'
                        return result
            if line[z] == 'o':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'o':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'o'
                        return result
            else:
                continue
#---Diagonal right>left>down----------------------------------------------------
    for x in range(0, x_size):
        j = y_size
        line = ''
        for i in range(x, x_size):
            j -= 1
            line += table[i][j]
            if j == 0:
                break
        for z in range(0, len(line)):
            if line[z] == 'x':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'x':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'x'
                        return result
            if line[z] == 'o':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'o':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'o'
                        return result
#---Diagonal right>left>up------------------------------------------------------
    y_size -= 1
    for y in range(y_size, -1, -1):
        i = 0
        line = ''
        for j in range(y, -1, -1):
            line += table[i][j]
            i += 1
            if i == x_size:
                break
        for z in range(0, len(line)):
            if line[z] == 'x':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'x':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'x'
                        return result
            if line[z] == 'o':
                group = ''
                for k in range(z, len(line)):
                    if line[k] == 'o':
                        group += line[k]
                    else:
                        group = ''
                    if len(group) >= to_win:
                        result = 'o'
                        return result


    return None

#-------------------------------------------------------------------------------
#-----------------------------victory possibility check-------------------------
#-------------------------------------------------------------------------------

def emptyslot(table):
    """
    Checks if the board is playable
    returns True if yes or else returns False
    """
    rows = len(table)
    columns = len(table[0])
    for x in range(0, rows):
        for y in range(0, columns):
            if table[x][y] != '-':
                continue
            else:
                return True
    return False
    
#-------------------------------------------------------------------------------
#-----------------------------Saves current game--------------------------------
#-------------------------------------------------------------------------------

def savegame(use_file, turn, to_win, table):
    """
    Stores the status of the current game to a specified file.
    Requires the name of the file, the table and its dimensions and
    a string containing the symbol (X or 0) of the next player to play.
    """
    line = ' '
    rows = len(table)
    columns = len(table[0])
    output = open(use_file, 'w')
    output.write(turn + str(to_win) + '\n')
    for j in range(columns):
        line += ' %i' %(j)
    output.write(line + '\n')
    output.close()
    output = open(use_file, 'a')
    for i in range(rows):
        line = '%i' %(i)
        for j in range(columns):
            line = line + ' %s' %(table[i][j])
        output.write(line + '\n')
    output.close()

#-------------------------------------------------------------------------------
#------------------Loads the saved table of a previous game---------------------
#-------------------------------------------------------------------------------

def loadgame(use_file):
    """
    Reads the gamedata from a file and returns a 2-dimensional list
    The data must be saved with the savegame function.
    """
    table = list()
    try:
        handle = open(use_file, 'r')
    except IOError:
        print 'File %s not found' %(use_file)
        sys.exit(1)
    while True:
        line = handle.readline()
        row = list()
        for i in range(0, len(line)):
            if line[0] == ' ':
                break
            if line[i] == '-' or line[i] == 'x' or line[i] == 'o':
                row.append(line[i])
            else:
                continue
        if line != ' ' and line != '':    
            table.append(row)
        if line == '':
            break
    table.pop(0)                #the algorithm puts 2 empty elements in the
    table.pop(0)                #beginning they are dropped here
    handle.close()
    return table

        

#-------------------------------------------------------------------------------
#-----------------------------Load turn-----------------------------------------
#-------------------------------------------------------------------------------

def loadturn(use_file):
    """
    Loads the current turn from the specified file and returns a string
    If the data is not found gives a random result.
    The data must be saved with the savegame function.
    """
    turn = None
    try:
        handle = open(use_file, 'r')
    except IOError:
        print 'File not found'
        sys.exit(1)
    line = handle.readline()
    for i in range(len(line)):
        if line[i] == 'x' or line[i] == 'o':
            turn = line[i]
            break
    try:
        if turn == None:
            raise Exception
    except:
        print 'turn data not found'     #if turndata is not found gives random
        print 'randomizing...'
        turn = random.choice(['x', 'o'])
        return turn
    handle.close()
    return turn

        

#-------------------------------------------------------------------------------
#-----------------------------Load victory condition----------------------------
#-------------------------------------------------------------------------------

def loadvictory(use_file):
    """
    Loads the number of symbols in sequence needed for victory from a file
    Returns the amount as an integer.
    The data must be saved with the savegame function.
    """
    try:
        handle = open(use_file, 'r')
    except IOError:
        print 'File not found'
        sys.exit(1)
    line = handle.readline()
    value = ''
    for i in range(len(line)):      #the loop reads multiple digit numbers
        if line[i].isdigit():
            value = value + line[i]
        else:
            continue
    try:
        to_win = int(value)
    except TypeError:
        print 'Error in loading victory condition'
        sys.exit(1)
    return to_win
            

#-------------------------------------------------------------------------------
#-----------------------------Parameter analysis--------------------------------
#-------------------------------------------------------------------------------

def parameters(arguments):
    """
    Uses the getopt module to parse the given parameters and sets some
    global flags needed by the main program. Those are:
    use_file, new_game, interactive, x_size, y_size, to_win, save_result
    and specificly for the command line mode: select_x, select_y
    The accepted arguments are given above in a table.
    """
    global use_file, new_game, interactive #using globals shouldn't
    global x_size, y_size, to_win          #be a problem
    global select_x, select_y
    global save_result
    try:
        opts, args = getopt.getopt(arguments, "f:shni", ["help", "file=", "new", "interactive", "save"])
    except getopt.GetoptError:
        help('triliza')
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help('triliza')
            sys.exit(0)
        elif opt in ('-f', '--file'):
            use_file = arg
            print 'file in use: ', use_file
        elif opt in ('-n', '--new'):
            new_game = True
            print 'Starting a new game...'
        elif opt in ('-i', '--interactive'):
            interactive = True
            print 'Interactive mode active.'
        elif opt in ('-s', '--save'):
            save_result = True
            print 'The result will be saved in: %s' %(use_file)
    unused = "".join(args)        #beginning here we get the game settings
    if unused.isdigit() == False: #only numbers should be left in list: args
        print 'unknown characters in parameters'
        sys.exit(1)
    elif len(args) != 2 and len(args) != 3: 
        print 'Wrong parameters'
        sys.exit(1)
    else:
        if len(args) == 3:          #when creating a new game
            x_size = int(args[0])
            y_size = int(args[1])
            to_win = int(args[2])
        else:                       #when loading a saved game
            select_x = int(args[0])
            select_y = int(args[1])
            
#-------------------------------------------------------------------------------
#-----------------------------Global variables----------------------------------
#-------------------------------------------------------------------------------

#the flags used by the main program
interactive = False
new_game = False
winner = None
save_result = False
x_size = 0
y_size = 0
to_win = 0
select_x = 0
select_y = 0
use_file = 'file.txt'

#-------------------------------------------------------------------------------
#-----------------------------Interactive mode----------------------------------
#-------------------------------------------------------------------------------

parameters(sys.argv[1:])                    #begins by parsing the arguments

#-----------------------the intective mode begins here--------------------------
if interactive:
    x_turn = True
    print 'Welcome to Triliza'
    grid = maketable(x_size, y_size)        #makes the empty gameboard
    printtable(x_size, y_size, grid)        #and shows it
    print 'need: #%i' %(to_win)
    while winner == None:
        if winner != None:                  #checks if a winner was
            break                           #determined in a previous loop
        while x_turn:                       #x's turn is run here                    
            if emptyslot(grid) != True:     #checks if the game can continue
                print 'no more slots to play'
                sys.exit(0)
            try:
                coords = raw_input('x play\'s: ')
            except KeyboardInterrupt, EOFError:  #players may end the game
                print 'Game ended by user'       #any time by pressing ctrl + c
                if save_result:                  #or ctrl + shift + c
                    savegame(use_file, 'x', to_win, grid)
                sys.exit(0)
            coord_ver = checkinput(coords)
            if coord_ver == False:          #requests the coordinates again if
                print 'Wrong coodinates'    #they fail the test (by looping)
                print 'Give them in this format: X Y'
                continue
            select_x = read_x(coords)       
            select_y = read_y(coords)
            if select_x >= x_size or select_y >= y_size:
                print 'coordinates out of bounds'
                continue
            if grid[select_x][select_y] != '-':
                print '%i %i already played' %(select_x, select_y)
                continue
            try:
                grid[select_x][select_y] = 'x' #updates the gameboard
            except IndexError:
                print 'not on this table'      #useless?
                continue
            x_turn = False                     #toggles the other player's turn
            o_turn = True                      #for the next loop
            printtable(x_size, y_size, grid)
            print 'need: #%i' %(to_win)
            winner = wincheck(grid, to_win)
            if winner != None:
                break
        while o_turn:                          #this loop is the same with the                                         
            if emptyslot(grid) != True:        #above for the other player
                print 'no more slots to play'
                sys.exit(0)
            try:                               
                coords = raw_input('o play\'s: ')
            except KeyboardInterrupt, EOFError:
                print 'Game ended by user'
                if save_result:
                    savegame(use_file, 'o', to_win, grid)
                sys.exit(0)
            coord_ver = checkinput(coords)
            if coord_ver == False:
                print 'Wrong coodinates'
                print 'Give them in this format: X Y'
                continue
            select_x = read_x(coords)
            select_y = read_y(coords)
            if select_x >= x_size or select_y >= y_size:
                print 'coordinates out of bounds'
                continue
            if grid[select_x][select_y] != '-':
                print '%i %i already played' %(select_x, select_y)
                continue
            try:
                grid[select_x][select_y] = 'o' #useless?
            except IndexError:
                print 'not on this table'
                continue
            o_turn = False
            x_turn = True
            printtable(x_size, y_size, grid)
            print 'need: #%i' %(to_win)
            winner = wincheck(grid, to_win)
            if winner != None:
                break
    print '%s Wins!!!' %(winner)
    if save_result:
        savegame(use_file, winner, to_win, grid)   #saves the board 
    sys.exit(0)

#-------------------------------------------------------------------------------
#-----------------------------Command line mode----------------------------------
#-------------------------------------------------------------------------------

else:
    if new_game:                            #creates a new game and saves it
        grid = maketable(x_size, y_size)
        turn = random.choice(['x', 'o'])
        printtable(x_size, y_size, grid)
        print 'need: #%i' %(to_win)
        print 'it\'s %s\'s turn' %(turn)
        savegame(use_file, turn, to_win, grid)
    else:                                   
        grid = loadgame(use_file)           #loads a previously saved game
        x_size = len(grid)
        y_size = len(grid[0])
        turn = loadturn(use_file)
        to_win = loadvictory(use_file)
        try:
            if grid[select_x][select_y] != '-':     #checks if the input coords
                printtable(x_size, y_size, grid)    #point at an empty cell
                print 'need: #%i' %(to_win)
                print '%i %i already played' %(select_x, select_y)
                sys.exit(0)
            if turn == 'x':                         #updates board
                grid[select_x][select_y] = 'x'
                turn = 'o'
            else:
                grid[select_x][select_y] = 'o'
                turn = 'x'
        except IndexError:
            print 'coordinates out of bounds'
            sys.exit(1)
        printtable(x_size, y_size, grid)
        if emptyslot(grid) != True:         #checks if the game can continue
            print 'no more slots to play'
            sys.exit(0)
        print 'need: #%i' %(to_win)
        winner = wincheck(grid, to_win)
        if winner != None:                          #checks for winner
            print '%s Wins!!!' %(winner)
            if save_result:
                savegame(use_file, turn, to_win, grid)
            sys.exit(0)
        print 'it\'s %s\'s turn' %(turn)
        savegame(use_file, turn, to_win, grid)      #and saves the current game
sys.exit(0)

