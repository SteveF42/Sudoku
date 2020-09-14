import pygame
import copy
import time
from random import shuffle
from node import Node

WIDTH = 650
ROWS = 9
COUNTER = 0
RESOLUTION =(WIDTH//ROWS)*ROWS
WINDOW = pygame.display.set_mode((RESOLUTION,RESOLUTION))
pygame.display.set_caption("Sudoku Solver")

BLACK=(0,0,0)

def display_value(grid,window):
    for row in grid:
        for node in row:
            node.draw(window) 

def draw(grid,window):
    gap = WIDTH//ROWS
    display_value(grid,window)

    for row in range(ROWS):
        pygame.draw.line(WINDOW,BLACK,(0,row*gap),(WIDTH,row*gap), 3 if row % 3 == 0 and row != 0 else 1)
        for col in range(ROWS):
            pygame.draw.line(WINDOW,BLACK,(col*gap,0),(col*gap,WIDTH), 3 if col % 3 == 0 and col != 0 else 1)

    pygame.display.update()


def make_grid():
    gap = WIDTH//ROWS
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node = Node(i,j,gap)
            grid[i].append(node)

    WINDOW.fill((255,255,255))
    pygame.display.update()
    return grid

def get_clicked(mouse_pos,width,rows):
    gap = width//rows
    x,y = mouse_pos
    row = x//gap
    col = y//gap
    return row,col

def solve_helper(grid):
    global COUNTER  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pos = get_free_pos(grid)
    if not pos:
        COUNTER += 1
        return False
    col, row = pos

    node = grid[row][col]
    node.make_solving()
    for i in range(1,10):
        if validate(grid,row,col,i):
            node.set_value(i)
            if solve_helper(grid):
                return True
            node.set_value(0)
    return False

    
def make_puzzle(grid,draw):
    global COUNTER
    non_empty_squares = get_non_empty_squares(grid)
    non_empty_sqares_count = len(non_empty_squares)
    rounds = 5
    while rounds > 0 and non_empty_sqares_count > 17:
        draw()
        node = non_empty_squares.pop()
        node.make_solving()
        non_empty_sqares_count -= 1
        previous_value = node.get_value()
        row,col = node.get_pos()
        node.set_value(0)
        COUNTER = 0
        grid_copy = copy.deepcopy(grid)
        solve_helper(grid_copy)
        if COUNTER != 1:
            node.set_value(previous_value)
            node.make_orange()
            rounds -= 1
            non_empty_sqares_count += 1
    return

def get_non_empty_squares(grid):
    non_empty_sqares = []
    for i in range(9):
        for j in range(9):
            if grid[i][j].get_value() != 0:
                non_empty_sqares.append(grid[i][j])
    shuffle(non_empty_sqares)
    return non_empty_sqares
            

def generate_solution(grid,draw):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    number_list = [1,2,3,4,5,6,7,8,9]
    draw()

    pos = get_free_pos(grid)
    if not pos:
        return True

    col, row = pos

    shuffle(number_list)
    for number in number_list:
        if validate(grid,row,col,number):
            grid[row][col].set_value(number)
            grid[row][col].make_solved()
            if generate_solution(grid,draw):
                return True
            grid[row][col].make_solving()
            grid[row][col].set_value(0)

    return False

def solve(grid,draw = None):
    global COUNTER  
    if draw:
        draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pos = get_free_pos(grid)
    if not pos:
        return True
    col, row = pos

    node = grid[row][col]
    node.make_solving()
    for i in range(1,10):
        if validate(grid,row,col,i):
            node.set_value(i)
            node.make_solved()
            if solve(grid,draw):
                return True
            node.set_value(0)
            node.make_solving()
    return False

      
def validate(grid, row, col,value):
    #check col
    for i in range(9):
        if grid[row][i].get_value() == value and i != col:
            return False

    #check row
    for i in range(9):
        if grid[i][col].get_value() == value and i != row:
            return False

    #check the little 3x3 box
    sub_row = (row // 3) * 3
    sub_col = (col // 3) * 3
    for i in range(sub_row,sub_row+3):
        for j in range(sub_col,sub_col+3):
            if grid[i][j].get_value() == value and (i,j) != (row,col):
                return False
            
    return True


def get_free_pos(grid):
    for row in range(9):
        for col in range(9):
            node = grid[col][row]
            value = node.get_value()
            if value == 0:
                return (row, col)
    return None

def clear_grid(grid,draw):
    for row in grid:
        draw()
        time.sleep(0.1)
        for node in row:
            node.make_open()

def game_setup(window):
    grid = make_grid()
    generate_solution(grid,lambda: draw(grid,window))
    make_puzzle(grid,lambda: draw(grid,window))
    clear_grid(grid,lambda: draw(grid,window))
    return grid

def main(rows,width):
    grid = game_setup(WINDOW)

    run = True

    current_node = None
    while(run):
        draw(grid,WINDOW)
        key_states = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]: #left click
                mouse_pos = pygame.mouse.get_pos()
                row,col = get_clicked(mouse_pos,width,rows)
                node = grid[row][col]
                node.make_selected()
                if current_node and current_node != node: current_node.make_open()
                current_node = node
            
            if event.type == pygame.KEYDOWN:
                key = event.key - 48 #idk wtf this is ASCII???? but this makes the number start at zero since I only want 0-9
                if key in range(0,10):
                    if current_node:
                        current_node.set_value(key)
                if event.key == pygame.K_SPACE:
                    solve(grid,lambda: draw(grid,WINDOW))
                if event.key == pygame.K_c:
                    grid = game_setup(WINDOW)



if __name__ == '__main__':
    main(ROWS,WIDTH)