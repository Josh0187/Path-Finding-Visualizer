import pygame
from pygame import *
from queue import PriorityQueue
import time
from tkinter import *
from tkinter import Button, Tk

WIDTH = 805
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finder")
clock = pygame.time.Clock()
RED = (255, 0, 0)
GREY = (211,211,211)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = 255, 105, 180
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
ast = False
dijs = False

# creating menu
root = Tk()
root.title('Please Select a Path Finding Algorithm')
root.geometry("700x250")

def make_ast_true():
    global ast
    ast = True
    root.destroy()
   

def make_dijs_true():
    global dijs
    dijs = True
    root.destroy()
   

instructions = Label(root, text = "Path Finding Visualizer - INSTRUCTIONS",font=('Courier', 15, 'bold'),anchor = 'w').pack(fill = 'both')
instructions1 = Label(root, text = "1. Select a start and end position with your first two clicks",font=('Courier',10) ,anchor = 'w').pack(fill = 'both')
instructions2 = Label(root, text = "2. Draw walls by holding down left click. You can delete walls by right clicking", font=('Courier',10),anchor = 'w').pack(fill = 'both')
instructions3 = Label(root, text = "3. Press space to start Path Finding. To reset press r", font=('Courier',10), anchor = 'w').pack(fill = 'both')

astb = Button(root, text = "A*", width = 200, height = 4, command = make_ast_true)
astb.pack()
dijsb = Button(root, text = "Dijkstra's", width = 200, height = 4, command = make_dijs_true)
dijsb.pack()

#########################################
class node:
    def __init__(self, row, col, rad, total_rows):
        self.row = row 
        self.col = col 
        self.x = (row * rad)+10
        self.y = (col * rad)+10
        self.rad = rad 
        self.color = WHITE
        self.adjacent = []
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN
    
    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
    
    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN
    
    def make_wall(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self):
        self.color = PINK

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), 7)
    
    def update_adjacent(self,grid):
        self.adjacent = []
        #CHECK DOWN
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_wall():
            self.adjacent.append(grid[self.row+1][self.col])

        #CHECK UP
        if self.row > 0 and not grid[self.row-1][self.col].is_wall():
            self.adjacent.append(grid[self.row-1][self.col])

        #CHECK RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_wall():
            self.adjacent.append(grid[self.row][self.col+1])

        #CHECK LEFT
        if self.col > 0 and not grid[self.row][self.col-1].is_wall():
            self.adjacent.append(grid[self.row][self.col-1])
        
    def __lt__(self,other):
        return False


def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            NewNode = node(i,j,gap,rows)
            grid[i].append(NewNode)
    return grid


def which_node(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def drawEveryThing(win, grid):
	win.fill(GREY)

	for row in grid:
		for node in row:
			node.draw(win)
	pygame.display.update()

# Manhattan
def h(pos1,pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def make_shortest_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def dij(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    # same as push (pushing (fscore,count,node))
    open_set.put((0,count,start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    #keeps track of items in priority Queue
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #removes and returns from priority queue (min f score)
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # found path
        if current == end:
            make_shortest_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.adjacent:
            temp_g_score = g_score[current]+1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()
    return False


def astar(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    # same as push (pushing (fscore,count,node))
    open_set.put((0,count,start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    #keeps track of items in priority Queue
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #removes and returns from priority queue (min f score)
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # found path
        if current == end:
            make_shortest_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.adjacent:
            temp_g_score = g_score[current]+1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()
    return False


def main():
    ROWS = 50
    run = True
    start = None
    end = None
    grid = make_grid(ROWS, WIDTH)
    drawEveryThing(WIN, grid)
    root.mainloop()

    while(run):
        drawEveryThing(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = which_node(pos,ROWS,WIDTH)
                clicked_node = grid[row][col]
                if start == None:
                    clicked_node.make_start()
                    start = clicked_node
                elif end == None and clicked_node != start:
                    clicked_node.make_end()
                    end = clicked_node
                elif clicked_node != end and clicked_node != start:
                    clicked_node.make_wall()
            
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = which_node(pos,ROWS,WIDTH)
                clicked_node = grid[row][col]
                clicked_node.reset()
                if clicked_node == start:
                    start = None
                if clicked_node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_adjacent(grid)
                    if dijs == True:
                        dij(lambda: drawEveryThing(WIN,grid),grid,start,end)
                    else:
                        astar(lambda: drawEveryThing(WIN,grid),grid,start,end)
                
                # reset 
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)
                               
main()