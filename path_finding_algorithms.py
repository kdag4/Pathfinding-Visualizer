import pygame, sys
from pygame.locals import *
import heapq
import tkinter as tk
from tkinter import font
import time
import math
import os
import random

#dimensions
display_width = 900
display_height = 900
additional_display_width = 200 #space for buttons/sliders

#all colors used
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (125,255,255)
PURPLE = (148,0,211)
YELLOW = (255,255,0)
BLACK = (0,0,0)

#set up display
display = pygame.display.set_mode((display_width+additional_display_width,display_height))
display.fill(WHITE)
pygame.init()


row = 10 #initial rows
column = 10 #initial columns
w = display_width / column #initial width of square
h = display_height / row #initial height of square
speed = 0.01 #initial_speed
button_list = [] #list for all buttons made
slider_list = [] #List for all sliders made
mode = "Start" #game with begin with the option to move the start node

class square: #class square creates all squares in the grid
    def __init__(self,i,j,total_row,total_column):
        self.row = i #row in grid
        self.column = j #column in grid
        self.width = display_width / total_column #width of square
        self.height = display_height / total_row #height of square
        self.dist = sys.maxsize #distance from start is initially set to max for all nodes
        self.prev = None #tracks previous square of algorithm
        self.color = None #tracks current color of square
        self.set = None #for Kruskal Maze Generation; each square begins in a distinct set
        self.draws()
    def color_change(self,color): #changes color of square
        self.rect = pygame.draw.rect(display,color,(self.column*self.width,self.row*self.height,self.width,self.height))
        self.color = color
    def draws(self): #draws square's borders; white within borders
        self.rect = pygame.draw.rect(display,BLACK,(self.column*self.width,self.row*self.height,self.width,self.height),2)

def text_objects(text,font,color): #set up surface to display text
    textSurface = font.render(text,True,color)
    return textSurface, textSurface.get_rect()

class Button: #class button creates buttons
    def __init__(self,msg,x,y):
        self.msg = msg #the text label for the button
        self.x = x #x-coordinate
        self.y = y #y-coordinate
        if self.msg is "How To Use":
            self.w = int(additional_display_width) #width of button
            print(self.x,self.y)
        else:
            self.w = int(additional_display_width/2) #width of button
        self.h = int(additional_display_width/4) #height of button
        self.hover(pygame.mouse.get_pos())
    def hover(self,mouse): #display button
        if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y: #highlight in Green if mouse hovers above button
            pygame.draw.rect(display,GREEN,(self.x,self.y,self.w,self.h),5)
        else: #border in black otherwise
            pygame.draw.rect(display,BLACK,(self.x,self.y,self.w,self.h),5)
        #set up text display, adjusting font size if length of msg is too long
        if self.msg is "Breadth_First":
            textSurf, textRect = text_objects(self.msg, pygame.font.SysFont("timesnewroman",16),BLACK)
        elif self.msg is "Prim_Jarnik":
            textSurf, textRect = text_objects(self.msg, pygame.font.SysFont("timesnewroman",18),BLACK)
        elif self.msg is "Depth_First":
            textSurf, textRect = text_objects(self.msg, pygame.font.SysFont("timesnewroman",19),BLACK)
        else:
            textSurf, textRect = text_objects(self.msg, pygame.font.SysFont("timesnewroman",21),BLACK)
        textRect.center = (self.x+(self.w/2),self.y+(self.h/2))
        display.blit(textSurf,textRect) #display text
    def set_mode(self, mouse): #sets the mode to be the button msg
        if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y:
            return self.msg
        return None #returns None if mouse is not hovering above button

class Slider: #class slider creates custom sliders
    def __init__(self, name, val, min, max, x, y):
        self.name = name #msg on slider
        self.val = val #current value of slider
        self.min = min #minimum value of slider
        self.max = max #maximum value of slider
        self.x = int(x) #x coordinate
        self.y = int(y) #y coordinate
        self.w = int(additional_display_width/2) #width of slider
        self.h = int(additional_display_width/4) #height of slider
        self.build_slider()
    def build_slider(self):
        if self.name is "Speed":
            percent_of_range = (self.max - self.val)/(self.max - self.min)
        else:
            percent_of_range = (self.val - self.min)/(self.max - self.min)
        pygame.draw.rect(display, BLACK, (self.x,self.y,self.w,self.h),5)
        pygame.draw.rect(display, BLACK, (self.x,int(self.y+(self.h/2)-int(self.h/40)),self.w,int(self.h/20)),1)
        pygame.draw.circle(display, BLACK, (int(self.x+(self.w*percent_of_range)),int(self.y+(self.h/2))), int(self.h/10))
        textSurf, textRect = text_objects(self.name, pygame.font.SysFont("timesnewroman",20),BLACK)
        textRect.center = (self.x+(self.w/2),self.y+(self.h/5))
        display.blit(textSurf,textRect)
    def move_slider(self, move_val):
        if self.name is "Speed":
            temp_percent_of_range = (self.max - self.val)/(self.max - self.min)
        else:
            temp_percent_of_range = (self.val - self.min)/(self.max - self.min)
        pygame.draw.circle(display, LIGHT_BLUE, (int(self.x+(self.w*temp_percent_of_range)),int(self.y+(self.h/2))), int(self.h/10))
        self.val += move_val
        if self.val < self.min:
            self.val = self.min
        elif self.val > self.max:
            self.val = self.max
        if self.name is "Speed":
            percent_of_range = (self.max - self.val)/(self.max - self.min)
        else:
            percent_of_range = (self.val - self.min)/(self.max - self.min)
        pygame.draw.rect(display, BLACK, (self.x,self.y,self.w,self.h),5)
        pygame.draw.rect(display, BLACK, (self.x,int(self.y+(self.h/2)-int(self.h/40)),self.w,int(self.h/20)),1)
        pygame.draw.circle(display, BLACK, (int(self.x+(self.w*percent_of_range)),int(self.y+(self.h/2))), int(self.h/10))
        return self.val
    def detect(self,mouse):
        if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y:
            return self.name
        return None

#buttons
button_x = display_width
button_x2 = display_width+(additional_display_width/2)
display.fill(LIGHT_BLUE,(button_x,0,button_x + additional_display_width,display_height))
tutorial_button = Button("How To Use",button_x,(display_height/2) - 5*(additional_display_width/4))
start_button = Button("Start", button_x, display_height/2 - (additional_display_width/4))
end_button = Button("End", button_x2, display_height/2 - (additional_display_width/4))
wall_button = Button("Wall", button_x, display_height/2)
weight_button = Button("Weight", button_x2, (display_height/2))
dijkstra_button = Button("Dijkstra", button_x, (display_height/2) + 2*(additional_display_width/4))
A_Star_button = Button("A_Star", button_x2, (display_height/2) + 2*(additional_display_width/4))
depth_first_button = Button("Depth_First", button_x, (display_height/2) + 3*(additional_display_width/4))
breadth_first_button = Button("Breadth_First", button_x2, (display_height/2) + 3*(additional_display_width/4))
best_first_button = Button("Best_First", button_x, (display_height/2) + 4*(additional_display_width/4))
run_all_button = Button("Run_All", button_x2, (display_height/2) + 4*(additional_display_width/4))
kruskal_button = Button("Kruskal",button_x,(display_height/2) + 6*(additional_display_width/4))
prim_jarnik_button = Button("Prim_Jarnik",button_x2,(display_height/2) + 6*(additional_display_width/4))
clear_button = Button("clear",button_x2,(display_height/2) + 8*(additional_display_width/4))
analytics_button = Button("Analytics",button_x,(display_height/2) + 8*(additional_display_width/4))
button_list.extend([start_button,end_button,wall_button,weight_button,dijkstra_button,A_Star_button,
        best_first_button,depth_first_button,breadth_first_button,clear_button,run_all_button,
        kruskal_button,prim_jarnik_button,tutorial_button,analytics_button])

#sliders
size_slider = Slider("Size", 10,2,50,display_width,(display_height/2) - 3*(additional_display_width/4))
speed_slider = Slider("Speed", 0.05,0.0001,0.1,display_width + (additional_display_width/2),(display_height/2) - 3*(additional_display_width/4))
slider_list.append(size_slider)
slider_list.append(speed_slider)

def set_up_grid(row,column):
    grid = [] #instantiate 2d array
    for i in range(row): #nested for loop creates and stores a grid
        grid.append([])
        for j in range(column):
            grid[i].append(None)
            grid[i][j] = square(i,j,row,column)
            if len(button_list) is 0:
                pygame.display.update()
                time.sleep(0.003)
    grid[0][0].color_change(RED)
    grid[0][0].draws()
    grid[-1][-1].color_change(BLACK)
    grid[-1][-1].draws()
    return grid

grid_array = set_up_grid(row,column)

def make_text(msg,color,x,y,bool,size):
    txt = pygame.font.SysFont("timesnewroman",size)
    txt.set_bold(bool)
    textSurface = txt.render(msg,True,color)
    textSurf, textRect = textSurface, textSurface.get_rect()
    textRect.center = (x,y)
    display.blit(textSurf,textRect)

display.fill(BLACK,(display_width,0,display_width+additional_display_width,additional_display_width/2))
display.fill(WHITE,(display_width,additional_display_width/2,display_width+additional_display_width,additional_display_width/2-5))
x = display_width + additional_display_width/2
make_text("PATHFINDING",WHITE,x,(h/3),True,26)
make_text("VISUALIZER",WHITE,x,(2*h/3),True,26)
make_text("LEGEND:",BLACK,x,4*h/3,True,20)
make_text("= START",BLACK,display_width+2*w/3,4*h/3+h/3,False,14)
make_text("= END",BLACK,display_width+2*w/3+w-w/12,4*h/3+h/3,False,14)
make_text("= WALL",BLACK,display_width+2*w/3,5*h/3+h/3,False,14)
make_text("= WEIGHT",BLACK,display_width+2*w/3+w+w/12,5*h/3+h/3,False,14)
pygame.draw.rect(display,RED,(display_width,4*h/3+h/6,w/3,h/3))
pygame.draw.rect(display,BLACK,(display_width+w,4*h/3+h/6,w/3,h/3))
pygame.draw.rect(display,PURPLE,(display_width,5*h/3+h/6,w/3,h/3))
pygame.draw.rect(display,YELLOW,(display_width+w,5*h/3+h/6,w/3,h/3))
pygame.draw.rect(display,BLACK,(display_width,additional_display_width/2,additional_display_width,h+h/12),3)

#set start and end nodes
start = grid_array[0][0]
end = grid_array[-1][-1]

def start_node(mouse,start,width,height):
    i = mouse[0]//width
    j = mouse[1]//height
    if grid_array[int(j)][int(i)] is not end:
        start.color_change(WHITE)
        start.draws()
        grid_array[int(j)][int(i)].color_change(RED)
        grid_array[int(j)][int(i)].draws()
        return grid_array[int(j)][int(i)]
    return start

def end_node(mouse,end,width,height):
    i = mouse[0]//width
    j = mouse[1]//height
    if grid_array[int(j)][int(i)] is not start:
        end.color_change(WHITE)
        end.draws()
        grid_array[int(j)][int(i)].color_change(BLACK)
        grid_array[int(j)][int(i)].draws()
        return grid_array[int(j)][int(i)]
    return end

def wall_node(node):
    if node is not start and node is not end:
        if node.dist is sys.maxsize:
            node.color_change(PURPLE)
            node.draws()
            node.dist = 0
        else:
            node.color_change(WHITE)
            node.draws()
            node.dist = sys.maxsize

def weight_node(mouse,width,height):
    i = mouse[0]//width
    j = mouse[1]//height
    if grid_array[int(j)][int(i)] is not start and grid_array[int(j)][int(i)] is not end and grid_array[int(j)][int(i)].color is not PURPLE:
        if grid_array[int(j)][int(i)].color is YELLOW:
            grid_array[int(j)][int(i)].color_change(WHITE)
            grid_array[int(j)][int(i)].draws()
        else:
            grid_array[int(j)][int(i)].color_change(YELLOW)
            grid_array[int(j)][int(i)].draws()

def clear():
    display.fill(WHITE,(0,0,display_width,display_height))
    for grid_row in grid_array:
        for node in grid_row:
            node.draws()
            node.prev = None
            node.color = None
            if node is not start:
                node.dist = sys.maxsize
    start.color_change(RED)
    start.draws()
    end.color_change(BLACK)
    end.draws()

def clear_path():
    display.fill(WHITE,(0,0,display_width,display_height))
    for grid_row in grid_array:
        for node in grid_row:
            if node is not start and node is not end and node.color is not PURPLE and node.color is not YELLOW:
                node.draws()
                node.prev = None
                node.color = None
                if node is not start:
                    node.dist = sys.maxsize
            else:
                node.prev = None
                node.color_change(node.color)
                node.draws()
                if node is not start and node.color is not PURPLE:
                    node.dist = sys.maxsize
                elif node.color is PURPLE:
                    node.dist = 0
    start.color_change(RED)
    start.draws()
    end.color_change(BLACK)
    end.draws()

def neighbor_helper(currNode, direction):
    if currNode.row is not 0 and direction is "Up":
        return grid_array[currNode.row-1][currNode.column],1
    elif currNode.row is not (row-1) and direction is "Down":
        return grid_array[currNode.row+1][currNode.column],1
    elif currNode.column is not 0 and direction is "Left":
        return grid_array[currNode.row][currNode.column-1],1
    elif currNode.column is not (column-1) and direction is "Right":
        return grid_array[currNode.row][currNode.column+1],1
    elif currNode.row is not 0 and currNode.column is not 0 and direction is "Up_Left":
        return grid_array[currNode.row-1][currNode.column-1],math.sqrt(2)
    elif currNode.row is not 0 and currNode.column is not (column-1) and direction is "Up_Right":
        return grid_array[currNode.row-1][currNode.column+1],math.sqrt(2)
    elif currNode.row is not (row-1) and currNode.column is not 0 and direction is "Down_Left":
        return grid_array[currNode.row+1][currNode.column-1],math.sqrt(2)
    elif currNode.row is not (row-1) and currNode.column is not (column-1) and direction is "Down_Right":
        return grid_array[currNode.row+1][currNode.column+1],math.sqrt(2)
    else:
        return None,None

#HERE begins the 5 path_finding algorithms.

def Dijkstra(start,end):
    initial_time = time.time()
    Q = []
    start.dist = 0
    counter = 0
    direction_list = ["Left","Up_Left","Up","Up_Right","Right","Down_Right","Down","Down_Left"]
    heapq.heappush(Q,(start.dist,counter,start))
    while len(Q) > 0:
        tempNode = heapq.heappop(Q)
        currNode = tempNode[2]
        if currNode is end:
            break
        if currNode is not start and currNode is not end and currNode.color is not YELLOW:
            currNode.color_change(GREEN)
            currNode.draws()
        for dir in direction_list:
            neighbor_help = neighbor_helper(currNode,dir)
            neighbor = neighbor_help[0]
            if neighbor is not None:
                counter += 1
                if neighbor.color is YELLOW and neighbor.dist is sys.maxsize:
                    neighbor.dist = currNode.dist + 5
                    neighbor.prev = currNode
                    heapq.heappush(Q,(neighbor.dist,counter,neighbor))
                elif neighbor.color is not YELLOW and neighbor.dist > currNode.dist + neighbor_help[1]:
                    neighbor.dist = currNode.dist + neighbor_help[1]
                    neighbor.prev = currNode
                    heapq.heappush(Q,(neighbor.dist,counter,neighbor))
        pygame.display.update()
        time.sleep(speed)
    if end.prev is None:
        end.prev = end
        print("There is no path from the start to the end.")
    else:
        currNode = end
        while currNode.prev is not None:
            if currNode is not end:
                currNode.color_change(BLUE)
                currNode.draws()
            currNode = currNode.prev
        pygame.display.update()
    end_time = time.time()
    return ("Dijkstra",end.dist,end_time-initial_time)

def heuristic(node,end):
    dist = math.sqrt((node.row - end.row)**2 + (node.column - end.column)**2)
    return dist

def A_Star(start,end):
    initial_time = time.time()
    Q = []
    counter = 0
    direction_list = ["Left","Up_Left","Up","Up_Right","Right","Down_Right","Down","Down_Left"]
    start.dist = 0
    heapq.heappush(Q,(heuristic(start,end)+start.dist,counter,start))
    while len(Q) > 0:
        currNode = heapq.heappop(Q)[2]
        if currNode is end:
            break
        if currNode is not start and currNode is not end and currNode.color is not YELLOW:
            currNode.color_change(GREEN)
            currNode.draws()
        for dir in direction_list:
            neighbor_help = neighbor_helper(currNode,dir)
            neighbor = neighbor_help[0]
            if neighbor is not None and neighbor.color is not GREEN:
                counter += 1
                if neighbor.color is YELLOW and neighbor.dist is sys.maxsize:
                    neighbor.dist = currNode.dist + 5
                    neighbor.prev = currNode
                    dist = heuristic(neighbor,end)+neighbor.dist
                    heapq.heappush(Q,(dist,counter,neighbor))
                elif neighbor.color is not YELLOW and neighbor.dist > currNode.dist + neighbor_help[1]:
                    neighbor.dist = currNode.dist + neighbor_help[1]
                    neighbor.prev = currNode
                    dist = heuristic(neighbor,end)+neighbor.dist
                    heapq.heappush(Q,(dist,counter,neighbor))
        pygame.display.update()
        time.sleep(speed)
    if end.prev is None:
        end.prev = end
        print("There is no path from the start to the end.")
    else:
        currNode = end
        while currNode is not start:
            if currNode is not end:
                currNode.color_change(BLUE)
                currNode.draws()
            currNode = currNode.prev
        pygame.display.update()
    end_time = time.time()
    return ("A_Star",end.dist,end_time-initial_time)

def best_first_search(start,end):
    initial_time = time.time()
    Q = []
    counter = 0
    direction_list = ["Left","Up_Left","Up","Up_Right","Right","Down_Right","Down","Down_Left"]
    start.dist = 0
    heapq.heappush(Q,(heuristic(start,end),counter,start))
    while len(Q) > 0:
        currNode = heapq.heappop(Q)[2]
        if currNode is end:
            break
        if currNode is not start and currNode is not end and currNode.color is not YELLOW:
            currNode.color_change(GREEN)
            currNode.draws()
        for dir in direction_list:
            neighbor_help = neighbor_helper(currNode,dir)
            neighbor = neighbor_help[0]
            if neighbor is not None and neighbor.color is not GREEN:
                counter += 1
                if neighbor.color is YELLOW and neighbor.dist is sys.maxsize:
                    neighbor.dist = currNode.dist + 5
                    neighbor.prev = currNode
                    heapq.heappush(Q,(heuristic(neighbor,end)+5,counter,neighbor))
                elif neighbor.color is not YELLOW and neighbor.dist > currNode.dist + neighbor_help[1]:
                    neighbor.dist = currNode.dist + neighbor_help[1]
                    neighbor.prev = currNode
                    heapq.heappush(Q,(heuristic(neighbor,end),counter,neighbor))
        pygame.display.update()
        time.sleep(speed)
    if end.prev is None:
        end.prev = end
        print("There is no path from the start to the end.")
    else:
        currNode = end
        while currNode is not start:
            if currNode is not end:
                currNode.color_change(BLUE)
                currNode.draws()
            currNode = currNode.prev
        pygame.display.update()
    end_time = time.time()
    return ("Best_First",end.dist,end_time-initial_time)

def depth_first_search(start,end): #purposefully does not account for weights
    initial_time = time.time()
    stack = [start]
    direction_list = ["Left","Up_Left","Up","Up_Right","Right","Down_Right","Down","Down_Left"]
    while len(stack) > 0:
        currNode = stack.pop()
        if currNode is end:
            break
        if currNode is not start and currNode is not end and currNode.color is not PURPLE:
            currNode.color_change(GREEN)
            currNode.draws()
        for dir in direction_list:
            neighbor_help = neighbor_helper(currNode,dir)
            neighbor = neighbor_help[0]
            if neighbor is not None and neighbor.prev is None and currNode.color is not PURPLE:
                neighbor.prev = currNode
                neighbor.dist = currNode.dist + neighbor_help[1]
                stack.append(neighbor)
        pygame.display.update()
        time.sleep(speed)
    if end.prev is None:
        end.prev = end
        print("There is no path from the start to the end.")
    else:
        currNode = end
        while currNode is not start:
            if currNode is not end:
                currNode.color_change(BLUE)
                currNode.draws()
            currNode = currNode.prev
        pygame.display.update()
    end_time = time.time()
    return ("Depth_First",end.dist,end_time-initial_time)

def breadth_first_search(start,end): #purposefully does not account for weights
    initial_time = time.time()
    Q = [start]
    direction_list = ["Left","Up_Left","Up","Up_Right","Right","Down_Right","Down","Down_Left"]
    while len(Q) > 0:
        currNode = Q.pop(0)
        if currNode is end:
            break
        if currNode is not start and currNode is not end and currNode.color is not PURPLE:
            currNode.color_change(GREEN)
            currNode.draws()
        for dir in direction_list:
            neighbor_help = neighbor_helper(currNode,dir)
            neighbor = neighbor_help[0]
            if neighbor is not None and neighbor.prev is None and neighbor.color is not PURPLE:
                neighbor.prev = currNode
                neighbor.dist = currNode.dist + neighbor_help[1]
                Q.append(neighbor)
        pygame.display.update()
        time.sleep(speed)
    if end.prev is None:
        end.prev = end
        print("There is no path from the start to the end.")
    else:
        currNode = end
        while currNode is not start:
            if currNode is not end:
                currNode.color_change(BLUE)
                currNode.draws()
            currNode = currNode.prev
        pygame.display.update()
    end_time = time.time()
    return ("Breadth_First",end.dist,end_time-initial_time)

#HERE begins the maze generation algorithms

def Kruskal(start,end):
    wall_list = []
    for row in grid_array:
        for node in row:
            node.set = set([node])
            wall_list.append(node)
            if node is not start and node is not end and node.color is not PURPLE:
                wall_node(node)
    direction_list = ["Left","Up_Left","Up","Up_Right","Right","Down_Right","Down","Down_Left"]
    while start not in end.set:
        pygame.display.update()
        time.sleep(speed)
        if start in wall_list:
            random_node = wall_list.pop(wall_list.index(start))
        elif end in wall_list:
            random_node = wall_list.pop(wall_list.index(end))
        else:
            rand = random.randint(0,len(wall_list)-1)
            random_node = wall_list[rand]
        neighbor = None
        while neighbor is None:
            randDir = random.randint(0,len(direction_list)-1)
            neighbor = neighbor_helper(random_node,direction_list[randDir])[0]
        if neighbor not in random_node.set:
            if random_node is start or random_node is end:
                wall_node(neighbor)
            elif random_node.color is not WHITE:
                wall_node(random_node)
            for dir in direction_list:
                neighbor = neighbor_helper(random_node,dir)[0]
                if neighbor is not None:
                    if random_node.color is not PURPLE and neighbor.color is not PURPLE:
                        union_set = neighbor.set.union(random_node.set)
                        for node in union_set:
                            node.set = union_set

def Prim_Jarnik(start,end):
    wall_list = []
    node_neighbors = []
    node_count = 0
    total_node_count = 0
    found_end = False
    for row in grid_array:
        for node in row:
            total_node_count += 1
            if node is not start and node is not end and node.color is not PURPLE:
                wall_node(node)
    direction_list = ["Left","Up_Left","Up","Up_Right","Right","Down_Right","Down","Down_Left"]
    for dir in direction_list:
        neighbor = neighbor_helper(start,dir)[0]
        if neighbor is not None:
            wall_list.append(neighbor)
            node_neighbors.append(neighbor)
            neighbor.prev = node
    while len(wall_list) > 0:
        node_count += 1
        if found_end and node_count/total_node_count > .40:
            break
        pygame.display.update()
        time.sleep(speed)
        if len(node_neighbors) > 0:
            node_temp = node_neighbors.pop(random.randint(0,len(node_neighbors)-1))
            node = wall_list.pop(wall_list.index(node_temp))
        else:
            node = wall_list.pop(random.randint(0,len(wall_list)-1))
        if node.color is PURPLE:
            wall_node(node)
            node_neighbors = []
            for direction in direction_list:
                neighbor = neighbor_helper(node,direction)[0]
                if neighbor is not None and neighbor not in wall_list and neighbor.color is not WHITE:
                    neighbor.prev = node
                    node_neighbors.append(neighbor)
                    wall_list.append(neighbor)
                    if neighbor is end:
                        found_end = True

#pull_analytics is called to track/display distance and time of path
analytic = False
def pull_analytics(run,stats):
    if run:
        window = tk.Tk()
        window.title(mode)
        for stat in stats:
            algorithm_label = tk.Label(text=stat[0] + " algorithm: ",font='Helvetica 15 bold',foreground="black",background="white",anchor="w",width=24).pack(fill=tk.X)
            time_label = tk.Label(text="The time elapsed was: " + str(round(stat[2],4)) + " s.",font='Helvetica 12',foreground="black",background="white",anchor="w").pack(fill=tk.X)
            distance_label = tk.Label(text="The distance traveled was: " + str(round(stat[1],4)) + ".",font='Helvetica 12',foreground="black",background="white",anchor="w").pack(fill=tk.X)
        window.lift()
        window.attributes("-topmost",True)
        window.mainloop()

#tutorial function is called when the 'How To Use' button is clicked
def tutorial():
    window = tk.Tk()
    window.title("Tutorial")
    sliders_section = tk.Label(text="Size/Speed: Hover above desired slider. Use your keyboard's LEFT and RIGHT arrow keys to decrease and increase the attributes respectively.",
                        font='Helvetica 15 bold',foreground="black",background="white",anchor="w").pack(fill=tk.X)
    top_section = tk.Label(text="Start/End/Wall/Weight: Hover above desired button. CLICK! Return to grid and click on a square.",
                        font='Helvetica 15 bold',foreground="black",background="white",anchor="w").pack(fill=tk.X)
    path_finding_algorithms_section = tk.Label(text="Dijkstra/A_Star/Depth_First/Breadth_First/Best_First/Run_All: Hover above desired button. CLICK! Watch the path unfold.",
                        font='Helvetica 15 bold',foreground="black",background="white",anchor="w").pack(fill=tk.X)
    maze_algorithms_section = tk.Label(text="Kruskal/Prim_Jarnik: Hover above desired button. CLICK! Watch the maze randomly generate.",
                        font='Helvetica 15 bold',foreground="black",background="white",anchor="w").pack(fill=tk.X)
    analytics_section = tk.Label(text="Analytics: Click analytics to turn the analytics mode ON/OFF. After a path's completion, an analytics tab will open. Close to return to VISUALIZER.",
                        font='Helvetica 15 bold',foreground="black",background="white",anchor="w").pack(fill=tk.X)
    clear_section = tk.Label(text="Clear: Click to Clear!",
                        font='Helvetica 15 bold',foreground="black",background="white",anchor="w").pack(fill=tk.X)
    window.lift()
    window.attributes("-topmost",True)
    window.mainloop()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        mouse = pygame.mouse.get_pos()
        for button in button_list:
            button.hover(mouse)
            if pygame.mouse.get_pressed()[0]:
                if button.set_mode(mouse) is not None:
                    mode = button.set_mode(mouse)
                    stats = []
                    if end.prev is not None:
                        clear_path()
                    if mode is "clear":
                        clear()
                        mode = "Start"
                    elif mode is "Analytics":
                        if analytic:
                            analytic = False
                        else:
                            analytic = True
                        mode = "Start"
                    if mode is "Dijkstra":
                        dijkstra_stats = Dijkstra(start, end)
                        stats.append(dijkstra_stats)
                        pull_analytics(analytic,stats)
                    elif mode is "Best_First":
                        best_stats = best_first_search(start,end)
                        stats.append(best_stats)
                        pull_analytics(analytic,stats)
                    elif mode is "Depth_First":
                        depth_stats = depth_first_search(start,end)
                        stats.append(depth_stats)
                        pull_analytics(analytic,stats)
                    elif mode is "Breadth_First":
                        breadth_stats = breadth_first_search(start,end)
                        stats.append(breadth_stats)
                        pull_analytics(analytic,stats)
                    elif mode is "Run_All":
                        print("Running Dijkstra...")
                        dijkstra_stats = Dijkstra(start, end)
                        stats.append(dijkstra_stats)
                        time.sleep(1)
                        clear_path()
                        print("Running A*...")
                        a_star_stats = A_Star(start,end)
                        stats.append(a_star_stats)
                        time.sleep(1)
                        clear_path()
                        print("Running Depth_First_Search...")
                        depth_stats = depth_first_search(start,end)
                        stats.append(depth_stats)
                        time.sleep(1)
                        clear_path()
                        print("Running Breadth_First_Search...")
                        breadth_stats = breadth_first_search(start,end)
                        stats.append(breadth_stats)
                        time.sleep(1)
                        clear_path()
                        print("Running Best_First_Search...")
                        best_stats = best_first_search(start,end)
                        stats.append(best_stats)
                        time.sleep(1)
                        clear_path()
                        pull_analytics(analytic,stats)
                        mode = "Start"
                    elif mode is "A_Star":
                        a_star_stats = A_Star(start,end)
                        stats.append(a_star_stats)
                        pull_analytics(analytic,stats)
                    elif mode is "Kruskal":
                        Kruskal(start,end)
                    elif mode is "Prim_Jarnik":
                        Prim_Jarnik(start,end)
                    elif mode is "How To Use":
                        clear()
                        tutorial()
        for slider in slider_list:
            if slider.detect(mouse) is not None:
                if event.type == pygame.KEYDOWN:
                    if slider.name is "Size":
                        clear()
                        if event.key == pygame.K_LEFT:
                            slider_value = slider.move_slider(-1)
                        elif event.key == pygame.K_RIGHT:
                            slider_value = slider.move_slider(1)
                        row = slider_value
                        column = slider_value
                        display.fill(WHITE,(0,0,display_width,display_height))
                        grid_array = set_up_grid(row,column)
                        #set start and end nodes
                        start = grid_array[0][0]
                        end = grid_array[-1][-1]
                    elif slider.name is "Speed":
                        if event.key == pygame.K_LEFT:
                            slider_value = slider.move_slider(0.01)
                        elif event.key == pygame.K_RIGHT:
                            slider_value = slider.move_slider(-0.01)
                        speed = slider_value
        if pygame.mouse.get_pressed()[0]:
            if 0 < mouse[0] < display_width and 0 < mouse[1] < display_height:
                w = display_width / column
                h = display_height / row
                if mode is "Start":
                    start = start_node(mouse,start,w,h)
                elif mode is "End":
                    end = end_node(mouse,end,w,h)
                elif mode is "Wall":
                    i = mouse[0]//w
                    j = mouse[1]//h
                    node = grid_array[int(j)][int(i)]
                    wall_node(node)
                elif mode is "Weight":
                    weight_node(mouse,w,h)
    pygame.display.update()
