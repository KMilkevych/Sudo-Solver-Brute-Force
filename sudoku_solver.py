import pygame
from pygame.locals import *
import math
import sys
import os

class Board:
    '''A Board class representing an instance of the Sudoku Board.
    Has a field that contains all numbers currently written to board (0 = empty cell).
    Also contains method for different checks and operations on the board.'''

    def __init__(self, dim = (9, 9), file=None):
        if file:
            #load from file
            a = None
        else:
            self.board = [[0 for x in range(0, 9)] for y in range(0, 9)]
    
    def drawboard(self, window, numbers):
        '''Draws the board to given window, using the rendered numbers passed as parameter'''
        global dim, size
        for y in range(0, 9):
            for x in range(0, 9):
                number = self.board[y][x]
                if number != 0:
                    window.blit(numbers[number], (x*size + numbers[number].get_width()/2, y*size))

    def printboard(self):
        '''Prints the board to stdout'''
        for y in range(0, 9):
            for x in range(0, 9):
                print(self.board[y][x], end=" ")
            print()
    
    def get_available(self, cell, other_boards = []):
        '''Returns a list of available (legal) inputs for current cell'''
        available_numbers = {x: True for x in range(1, 10)}
        
        #check both other boards, and own board for each row, column and "cell" of 3x3 fields
        boards = [self] + other_boards
        for board in boards:
            for x in range(0, 9):#check row
                val = board.board[cell[1]][x]
                if val != 0:
                    available_numbers[val] = False
            
            for y in range(0, 9):#check column
                val = board.board[y][cell[0]]
                if val != 0:
                    available_numbers[val] = False
            
            #check the cell of 3x3 fields
            offsetx = cell[0]//3
            offsety = cell[1]//3
            for y in range(0, 3):
                for x in range(0, 3):
                    val = board.board[y + offsety*3][x + offsetx*3]
                    if val != 0:
                        available_numbers[val] = False

        available = []
        for key, value in available_numbers.items():
            if value == True:
                available.append(key)
        
        #print(available)
        return available
    
    def isallfilled(self):
        '''Checks if whole board is filled'''
        for y in range(0, 9):
            for x in range(0, 9):
                if board[y][x] == 0:
                    return False
        
        return True


def getnumbers(bold=False):
    '''Generates a dictionary of rendered numbers, to easily draw onto screen'''
    numbers = {}

    font = pygame.font.SysFont("Times New Roman", 48, bold=bold)
    color = (0, 0, 0)
    for n in range(1, 10):
        #render the text surface
        txt_surf = font.render(str(n), True, color)

        #create a transparent surface
        alpha_image = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
        alpha_image.fill((255, 255, 255, 255))

        #blit alpha surface onto text surace
        txt_surf.blit(alpha_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        numbers[n] = txt_surf
    
    return numbers

def drawgrid(window):
    '''Draws a grid on the screen, using the global dim and size variables'''
    global dim, size
    for x in range(1, 10):
        w = 1
        if x % 3 == 0:
            w = 4
        pygame.draw.line(window, (0, 0, 0), (x*size, 0), (x*size, dim[1]), w)
    
    for y in range(1, 10):
        w = 1
        if y % 3 == 0:
            w = 4
        pygame.draw.line(window, (0, 0, 0), (0, y*size), (dim[0], y*size), w)

def solveboard(board, filled_board, cellnum):
    '''Solve board using brute force approach'''
    if cellnum > 80:
        return True
    x = cellnum % 9
    y = cellnum // 9
    
    if filled_board.board[y][x] == 0:
        # Attempt each available number in current cell
        for available_number in board.get_available((x, y), [filled_board]):
            board.board[y][x] = available_number

            result = solveboard(board, filled_board, cellnum + 1)
            if result == True:
                return result
        board.board[y][x] = 0
        
        return False
    else:
        # If currently expected cell is not available, jump to next cell
        result = solveboard(board, filled_board, cellnum + 1)
        if result == True:
            return result
        else:
            return False
    
def g_solveboard(window, board, filled_board, cellnum):
    '''Solve board graphically (slower) using brute force approach'''
    global numbers, numbers_bold

    # Compute row and column of current working cell. If cell out of bounds, then board has been filled and solved.
    if cellnum > 80:
        return True
    x = cellnum % 9
    y = cellnum // 9

    if filled_board.board[y][x] == 0:
        for available_number in board.get_available((x, y), [filled_board]):

            board.board[y][x] = available_number

            window.fill((255, 255, 255))
            board.drawboard(window, numbers)
            filled_board.drawboard(window, numbers_bold)
            drawgrid(window)
            pygame.display.update()

            result = g_solveboard(window, board, filled_board, cellnum + 1)
            if result == True:
                return result
        board.board[y][x] = 0

        # Draw the board after an attempt to fill in a number
        window.fill((255, 255, 255))
        board.drawboard(window, numbers)
        filled_board.drawboard(window, numbers_bold)
        drawgrid(window)
        pygame.display.update()
        
        return False
    else:
        result = g_solveboard(window, board, filled_board, cellnum + 1)
        if result == True:
            return result
        else:
            return False

def board_filling(window):
    '''Run the board filling phase, where user can input own numbers onto board.'''
    global dim, size, numbers, numbers_bold

    #first generate a "table" that will contain the board
    #a sudoku table is 9x9 "fields"
    board = Board(dim=(9,9), file=None)

    running = True
    clock = pygame.time.Clock()
    mouse_pos = pygame.mouse.get_pos()
    current_cell = (0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
                
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] >= 0 < dim[0] and mouse_pos[1] >= 0 < dim[1]:
                    current_cell = (mouse_pos[0]//size, mouse_pos[1]//size)
                
            if event.type == pygame.KEYDOWN:                
                #filling out board
                keys = [pygame.K_SPACE, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
                for k in range(0, len(keys)):
                    if event.key == keys[k]:
                        board.board[current_cell[1]][current_cell[0]] = k
                        break
                
                if event.key == pygame.K_RETURN:
                    #end board filling phase
                    running = False
                    continue         
                
        #Drawing part
        window.fill((255, 255, 255))

        #highlight hover cell
        pygame.draw.rect(window, (230, 230, 230), ((current_cell[0]*size, current_cell[1]*size), (size, size)))

        #draw the numberss
        board.drawboard(window, numbers_bold)

        #draw the grid
        drawgrid(window)
        
        pygame.display.update()
        clock.tick(30)

    return board

def board_solving(window, filled_board):
    '''Run the board solving phase, where user-filled board is solved either graphically (default, slower) or non-graphically (faster).'''
    global dim, size, numbers, numbers_bold

    solved_board = Board(dim=(9, 9))

    #res = solveboard(solved_board, filled_board, 0)
    res = g_solveboard(window, solved_board, filled_board, 0)
    print(res)
    solved_board.printboard()

    # Define different background colors, depending on if the board has been solved, or doesn't have a solution.
    if res:
        bg_color = (100, 255, 100)
    else:
        bg_color = (255, 100, 100)

    #start launching board, non-standard running loop as part of algorithm
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #end board solving_phase
                    running = False
                    continue         
                
        #Drawing part
        window.fill(bg_color)

        #draw the boards (filled_board = user filled board, solved_board = rest of the numbers in the board)
        filled_board.drawboard(window, numbers_bold)
        solved_board.drawboard(window, numbers)

        #draw the grid
        drawgrid(window)
        
        pygame.display.update()
        clock.tick(60)
    

    return solved_board

def board_checking(board):

    # Define counter object to check for illegal placements
    blocks = [[False for j in range(0, 9)] for i in range(0, 9)]
    rows = [[False for j in range(0, 9)] for i in range(0, 9)]
    columns = [[False for j in range(0, 9)] for i in range(0, 9)]

    for y in range(0, 9):
        for x in range(0, 9):
            # If user filled board has a filled cell
            cell_value = board.board[y][x]
            block_num = (y//3)*3 + x//3
            if cell_value != 0:
                if rows[y][cell_value] == False:
                    rows[y][cell_value] = True
                else:
                    return (False, (x, y))
                
                if columns[x][cell_value] == False:
                    columns[x][cell_value] = True
                else:
                    return (False, (x, y))
                
                if blocks[block_num][cell_value] == False:
                    blocks[block_num][cell_value] = True
                else:
                    return (False, (x, y))

    return (True, (0, 0))


#Initializes pygame window
pygame.init()
size = 60
dim = (9*size, 9*size)

window = pygame.display.set_mode(dim)
pygame.display.set_caption("Sudoku solver")

#create a linked list of transparent images of numbers
numbers = getnumbers(bold=False)
numbers_bold = getnumbers(bold=True)

#get a filled board by user input
filled_board = board_filling(window)

#check if user filled board is legal
check = board_checking(filled_board)
if not check[0]:
    print(False)
    print("Conflict on cell: ", end="")
    print(check[1])
    filled_board.printboard()
    sys.exit()
else:
    #solve the board using backtracking algorithm
    solved_board = board_solving(window, filled_board)

sys.exit()