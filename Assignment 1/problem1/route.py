#!/usr/bin/env python

#Assignment 1 ; Question1
#Team: Apurva Gupta, Anshul Jain, Chirag Gilani
#To find good driving directions between pair of cities given by the user using four algorithms.
#We have included our observations in readme file of question1.

import sys
import Queue
import pandas
import numpy
import math

#Heurisitc function:To calculate great circle distance between city to goal.
#We require the lattitude and longitudes of city and goal to estimate the distance between them.
def calculate_heuristic(city,goal):
 i = 0
 found_city = False
 found_goal = False 
 if city==goal:
  return 0.00
 
 lat_city = city_gps1[city][0]
 long_city = city_gps1[city][1]
 lat_goal = city_gps1[goal][0]
 long_goal = city_gps1[goal][1] 
 long_city = float(long_city) * 0.0174
 long_goal = float(long_goal) * 0.0174
 lat_city = float(lat_city) * 0.0174
 lat_goal = float(lat_goal) * 0.0174
 
 longitude_distance = long_goal - long_city
 lattitude_distance = lat_goal - lat_city
 temp = (numpy.sin(lattitude_distance/2.0))**2 + (numpy.cos(lat_city) * numpy.cos(lat_goal) * ((numpy.sin(longitude_distance/2.0))**2))
 great_circle_distance = 2 * numpy.arcsin(numpy.sqrt(temp))
 mile_distance = float(3959 * great_circle_distance)
 return (mile_distance)

#It calculates the longest route between two cities using a star algorithm.
def astar_longtour(adjacency_list,start,goal):
  visited = []
  highway_list =[]
  h1 = 0
  h2 = 0
  q1 = Queue.PriorityQueue()
  error = ["None"]
  error1 = ["None1"]
  if start not in adjacency_list.keys() or goal not in adjacency_list.keys():
   return error
  g = 0
  h = calculate_heuristic(start,goal)
  q1.put((float(g)+float(h),float(g),start,start))
  goal1 = False
  t_cost = 0
  visited1 = []
  a = 0
  while q1.empty()==False:

    f,cost_path,vertex, path = q1.get()
    if vertex==goal:
      goal1= True
      t_cost = cost_path
      path1 = path
      #print "visited nodes",len(visited)
      return path1
    for next in adjacency_list[vertex]:
      speed = int(speed_list[vertex][next])
      if vertex not in visited and next not in visited and next not in visited1 and int(speed) != int(0):
       cost_node = float(float(adjacency_list[vertex][next])+float(cost_path))
       if next in city_data:
        h1 = calculate_heuristic(next,goal)
        f1 = float(float(cost_node)+float(h1))
        q1.put((-1*f1,float(cost_node),next,path+"#"+next))
       else:
        next2 = next
        for next_node in adjacency_list[next2]:
         speed1 = int(speed_list[next2][next_node])
         if next_node not in visited1 and speed1!=0:
          cost_node1 =  float(float(adjacency_list[next2][next_node])+float(cost_node))
          path_node1 = path+"#"+next2+"#"+next_node
          highway_list.append((next_node,cost_node1,path_node1))
        visited1.append(next2)
        while len(highway_list) != 0:
         next_t,cost_t,path_t = highway_list.pop()
         if next_t in visited1:
          a = a+1
         else:
          if next_t in city_data:
           h2 = calculate_heuristic(next_t,goal)
           f2 = float(float(cost_t)+float(h2))
           q1.put((-1*f2,float(cost_t),next_t,path_t))
          else:
           for next_node1 in adjacency_list[next_t]:
            speed2 = int(speed_list[next_t][next_node1])
            if next_node1 not in visited1 and speed2!=0:
             cost_node2 =  float(float(adjacency_list[next_t][next_node1])+float(cost_t))
             path_node2 = path_t+"#"+next_node1
             highway_list.append((next_node1,cost_node2,path_node2))

           visited1.append(next_t)

    visited.append(vertex)

  if goal1 == False:
    return error1


#For A star to find shortest distance,we use Heurisitic as the great circle distance between two cities.
#For handling highway intersections, we have explored all reachable cities from highway intersections and calculated great circle distance from those cities.
#Assumption:We ignored paths will zero speed or null speed.
def astar_distance(adjacency_list,start,goal):
  visited = []
  highway_list =[]
  h1 = 0
  h2 = 0
  q1 = Queue.PriorityQueue()
  error = ["None"]
  error1 = ["None1"]
  if start not in adjacency_list.keys() or goal not in adjacency_list.keys():
   return error
  g = 0
  h = calculate_heuristic(start,goal)
  q1.put((float(g)+float(h),float(g),start,start))
  goal1 = False
  t_cost = 0
  visited1 = []
  a = 0

  while q1.empty()==False:

    f,cost_path,vertex, path = q1.get()
    if vertex==goal:
      goal1= True
      t_cost = cost_path
      path1 = path
      #print "visited nodes",len(visited)
      return path1
    for next in adjacency_list[vertex]:
      speed = int(speed_list[vertex][next])
      if vertex not in visited and next not in visited and vertex not in visited1 and int(speed) != int(0): 
       cost_node = float(float(adjacency_list[vertex][next])+float(cost_path))
       if next in city_data:
        h1 = calculate_heuristic(next,goal)
        f1 = float(float(cost_node)+float(h1))
        q1.put((f1,float(cost_node),next,path+"#"+next))
  
       else:
        next2 = next
        for next_node in adjacency_list[next2]:
         speed1 = int(speed_list[next2][next_node])
         if next_node not in visited1 and speed1!=0:
          cost_node1 =  float(float(adjacency_list[next2][next_node])+float(cost_node))
          path_node1 = path+"#"+next2+"#"+next_node
          highway_list.append((next_node,cost_node1,path_node1))
        visited1.append(next2)
        while len(highway_list) != 0:
         next_t,cost_t,path_t = highway_list.pop()
         if next_t in visited1:
          a = a+1
         else:
          if next_t in city_data:
           h2 = calculate_heuristic(next_t,goal)
           f2 = float(float(cost_t)+float(h2))
           q1.put((f2,float(cost_t),next_t,path_t))
          else:
           for next_node1 in adjacency_list[next_t]:
            speed2 = int(speed_list[next_t][next_node1])
            if next_node1 not in visited1 and speed2!=0:
             cost_node2 =  float(float(adjacency_list[next_t][next_node1])+float(cost_t))
             path_node2 = path_t+"#"+next_node1
             highway_list.append((next_node1,cost_node2,path_node2))
             
           visited1.append(next_t)

    visited.append(vertex)

  if goal1 == False:
    return error1

#For a star with minimum amount of time, we have take heuristic as the great circle distance to  reach from A to goal/speed from A's previous city to A).
#We assumed that the speed with which a person was travelling remains constant till he reaches goal.
#Also,we didnt had the exact coordinates for highway intersections,so we calculated distances from all connecting cities to highway intersection.
#Assumption : It ignores the path with zero speed or null speed.
def astar_time(time_list,start,goal):
  visited = []
  highway_list =[]
  h1 = 0
  h2 = 0
  q1 = Queue.PriorityQueue()
  error = ["None"]
  error1 = ["None1"]
  if start not in time_list.keys() or goal not in time_list.keys():
   return error
  g = 0
  h = calculate_heuristic(start,goal)
  q1.put((float(g)+float(h),float(g),start,start))
  goal1 = False
  t_cost = 0
  visited1 = []
  a = 0

  while q1.empty()==False:

    f,cost_path,vertex, path = q1.get()

    if vertex==goal:
      goal1= True
      t_cost = cost_path
      path1 = path
      #print "visited nodes",len(visited)
      return path1
    for next in time_list[vertex]:
      if vertex not in visited and next not in visited:
       cost_node = float(float(time_list[vertex][next])+float(cost_path))
       if next in city_data:
        h1 = calculate_heuristic(next,goal)
        speed1 = speed_list[vertex][next]
        if float(speed1)!=float(0):
         ex_time = float(float(h1)/float(speed1))
         f1 = float(float(cost_node)+float(ex_time))
         q1.put((f1,float(cost_node),next,path+"#"+next))
  
       else:
        next2 = next
        for next_node in adjacency_list[next2]:
         if next_node not in visited1:
          cost_node1 =  float(float(time_list[next2][next_node])+float(cost_node))
          path_node1 = path+"#"+next2+"#"+next_node
          speed_node1 = float(speed_list[next2][next_node])
          if float(speed_node1)!=float(0):
           highway_list.append((next_node,cost_node1,path_node1,speed_node1))
          visited1.append(next2)
        while len(highway_list) != 0:
         next_t,cost_t,path_t,speed_t = highway_list.pop()
         if next_t in visited1:
          a = a+1
         else:
          if next_t in city_data:
           h2 = calculate_heuristic(next_t,goal)
          
           if float(speed_t)!=float(0):
            ex_time1 = float(float(h2)/float(speed_t))
            f2 = float(float(cost_t)+float(ex_time1))
            q1.put((f2,float(cost_t),next_t,path_t))
          else:
           for next_node1 in time_list[next_t]:
            if next_node1 not in visited1:
             cost_node2 =  float(float(time_list[next_t][next_node1])+float(cost_t))
             path_node2 = path_t+"#"+next_node1
             speed_node2 = float(speed_list[next_t][next_node1])
             if float(speed_node2)!=float(0):
              highway_list.append((next_node1,cost_node2,path_node2,speed_node2))
             
           visited1.append(next_t)
    
    visited.append(vertex)

  if goal1 == False:
    return error1

#Astar algorithm uses a heurisitc function to reduce the state space and finds the optimal answer.
#For Astar,with smallest number of segments, we have taken heuristic = 1.
def astar_segment(start,goal):
  visited = []
  highway_list =[]
  h1 = 1
  h2 = 1
  q1 = Queue.PriorityQueue()
  error = ["None"]
  error1 = ["None1"]
  if start not in adjacency_list.keys() or goal not in adjacency_list.keys():
   return error
  g = 0
  h = 1
  q1.put((int(g)+int(h),int(g),start,start))
  goal1 = False
  t_cost = 0

  while q1.empty()==False:
    f1,cost_path,vertex, path = q1.get()
    if vertex==goal:
      goal1= True
      t_cost = cost_path
      path1 = path
      #print "visited",len(visited)
      return path1

    for next in adjacency_list[vertex]:
      speed = int(speed_list[vertex][next])
      if vertex not in visited and next not in visited and speed!=0:
       cost_node = int(1) + int(cost_path)
       h1 = 1
       f = int(h1)+cost_node
       q1.put((f,int(cost_node),next,path+"#"+next))
 
    visited.append(vertex)

  if goal1 == False:
    return error1

#uniform cost search-time
#It returns a path with smallest amount of time but explores a lot of state space.
#It takes a priority queue and explores the path which takes the smallest amount of time.
#It finds an optimal answer.
def ucs_time(time_list,start,goal):
  visited = []
  q1 = Queue.PriorityQueue()
  error = ["None"]
  error1 = ["None1"]
  if start not in time_list.keys() or goal not in time_list.keys():
   return error
  for next in time_list[start]:
    w = float((time_list[start][next]))
    speed = int(speed_list[start][next])
    if speed!=0:
     q1.put((float(w),next,start+"#"+next))
    
  goal1 = False
  t_cost = 0
  visited.append(start)
  while q1.empty()==False:
    cost_path,vertex, path = q1.get()
    
    if vertex==goal:
      goal1= True
      t_cost = cost_path
      path1 = path
      #print "visited nodes",len(visited)
      return path1

    for next in time_list[vertex]:
      speed = int(speed_list[vertex][next])
      if vertex not in visited and next not in visited and speed!=0:
       cost_node = float((time_list[vertex][next]))+float((cost_path))
       q1.put((float(cost_node),next,path+"#"+next))
     
    visited.append(vertex)

  if goal1 == False:
    return error1

#Uniform cost search-segments
#We take a priority queue and store the number of edges we have traversed. It tries
#to find a path with smallest number of edges
#It returns an optimal answer with minimum number of edges.
#BFS also returns apath with miniumum edges but the path returned by both the algorithms might be different
def ucs_segment(start,goal):
  visited = []
  q1 = Queue.PriorityQueue()
  error = ["None"]
  error1 = ["None1"]
  if start not in adjacency_list.keys() or goal not in adjacency_list.keys():
   return error
  for next in adjacency_list[start]:
    w =0
    speed = int(speed_list[start][next])
    if speed!=0:
     q1.put((int(w),next,start+"#"+next))
  goal1 = False
  t_cost = 0
  visited.append(start)
  while q1.empty()==False:
    cost_path,vertex, path = q1.get()
    if vertex==goal:
      goal1= True
      t_cost = cost_path
      path1 = path
      #print "visited",len(visited)
      return path1

    for next in adjacency_list[vertex]:
      speed = int(speed_list[vertex][next])
      if vertex not in visited and next not in visited and speed!=0:
       cost_node = int(1) + int(cost_path)
       q1.put((int(cost_node),next,path+"#"+next))

    visited.append(vertex)

  if goal1 == False:
    return error1

#uniform cost search-distance
#The algorithm takes a priority queue and traverses where it finds the shortest cumulative value
#It explores a lot of state space but returns an optimal answer.
def ucs_distance(adjacency_list,start,goal):
  visited = []
  q1 = Queue.PriorityQueue()
  error = ["None"]
  error1 = ["None1"]
  if start not in adjacency_list.keys() or goal not in adjacency_list.keys():
   return error
  for next in adjacency_list[start]:
    w = adjacency_list[start][next]
    speed = int(speed_list[start][next])
    if speed!=0:
     q1.put((int(w),next,start+"#"+next))
  goal1 = False
  t_cost = 0
  visited.append(start)
  while q1.empty()==False:
    cost_path,vertex, path = q1.get()
    if vertex==goal:
      goal1= True
      t_cost = cost_path
      path1 = path
      #print "visited",len(visited)
      return path1

    for next in adjacency_list[vertex]:
      speed = int(speed_list[vertex][next])
      if vertex not in visited and next not in visited and speed!=0:
       cost_node = int(adjacency_list[vertex][next])+int(cost_path)
       q1.put((int(cost_node),next,path+"#"+next))
       
    visited.append(vertex)

  if goal1 == False:
    return error1

def ucs_longtour(adjacency_list,start,goal):
  visited = []
  q1 = Queue.PriorityQueue()
  error = ["None"]
  error1 = ["None1"]
  if start not in adjacency_list.keys() or goal not in adjacency_list.keys():
   return error
  for next in adjacency_list[start]:
    w = adjacency_list[start][next]
    speed = int(speed_list[start][next])
    if speed!=0:
#referred https://stackoverflow.com/questions/15124097/priority-queue-with-higher-priority-first-in-python to find how to put element with high value first
     q1.put((-1*int(w),next,start+"#"+next))
  goal1 = False
  t_cost = 0
  visited.append(start)
  while q1.empty()==False:
    cost_path,vertex, path = q1.get()
    if vertex==goal:
      goal1= True
      t_cost = cost_path
      path1 = path
      #print "visited",len(visited)
      return path1

    for next in adjacency_list[vertex]:
      speed = int(speed_list[vertex][next])
      if vertex not in visited and next not in visited and speed!=0:
       cost_node = int(adjacency_list[vertex][next])-int(cost_path)
       q1.put((-1*int(cost_node),next,path+"#"+next))

    visited.append(vertex)

  if goal1 == False:
    return error1

#It calculates total time taken to go from source to destination
def calculate_time(p):
  time = 0
  i = 0
  while i<len(p):
   if i != len(p)-1:  
     first_city = p[i]
     next_city = p[i+1]
     time += time_list[first_city][next_city]
     
   i = i+1
  return time

#It calculates total distance travelled from source to destination
def calculate_distance(p):
  distance = 0
  i = 0
  while i<len(p)-1:
   first_city = p[i]
   next_city = p[i+1]
   distance += int(adjacency_list[first_city][next_city])
   i = i+1
  return distance

#print data according to format
def print_data(path):
 final_path= []
 final_path1 = []
 p = ""
 if "None" in path:
  print "Start node or goal node doesnot exist"
  return 0
 elif "None1" in path:
  print "There is no goal from source to destination"
  return 0
 else:
  if routing_algo == "uniform" or routing_algo == "astar":
   final_path= path.split("#")
  else:
   final_path = path
 
 start = final_path[0] + " "
 p = start
 for i in range(1,len(final_path)):
  next = final_path[i] + " "
  p = p + next
 
 i = 0
 while i<len(final_path)-1:
   start = final_path[i]
   next = final_path[i+1]
   speed = speed_list[start][next]
   highway = highway_list[start][next]
   distance = adjacency_list[start][next]
   print start,"To",next,"Distance:",distance,"Speed Limit:",speed,"Travel From Highway number:",highway
   i = i +1
 
 time = calculate_time(final_path)
 cost = calculate_distance(final_path)
 print cost,round(time,3),p
 return 1
  
#Breadth first search
#Assumption:When speed is 0 or null,It doesnot consider that path
def bfs(adjacency_list,start,goal):
  queue  = [(start,[start])]
  visited =[]
  error = ["None"]
  error1 = ["None1"]
  IsGoal = False
  if start not in adjacency_list.keys() or goal not in adjacency_list.keys():
       return error
  while queue:
    (vertex,path) = queue.pop(0)
    
    for next in adjacency_list[vertex]:
     speed = int(speed_list[vertex][next])
     if vertex not in visited and speed!=0:
      if next==goal:
        IsGoal = True
       # print "visited nodes",len(visited)
        return path + [next]
      else:
        queue.append((next,path + [next]))
        
    visited.append(vertex)
  if IsGoal == False:
   return error1

#Depth first search
#We use a visited list to avoid cycles
#Assumption:When speed is 0 or null, It doesnot consider that path
def dfs(adjacency_list,start,goal):
  queue1  = [(start,[start])]
  visited =[]
  error = ["None"]
  error1 = ["None1"]
  IsGoal = False
  if start not in adjacency_list.keys() or goal not in adjacency_list.keys():
       return error
  while queue1:
   (vertex,path) = queue1.pop()
   for next in adjacency_list[vertex]:
     speed = int(speed_list[vertex][next])
     if vertex not in visited and speed!=0:
      if next==goal:
        IsGoal = True
        #print "visited nodes",len(visited)
        return path + [next]
      else:
        queue1.append((next,path+[next]))
   visited.append(vertex)
  if IsGoal== False:
   return error1

i = 0
adjacency_list = {}
splitlines=[]
time_list={}
speed_list={}
highway_list={}

#Reading road-segments file and storing it in a lists of list
with open('road-segments.txt','r') as route_file:
  lines = route_file.read().splitlines()
newline = [i.split(" ") for i in lines]

#Creating dictionaries for storing distance,speed and highway
for i in range(0,len(newline)-1):
  start_city = newline[i][0]
  next_city = newline[i][1]
  distance = newline[i][2]
  if len(newline[i][3].strip())==0:
   speed = int(0)
  else:
   speed = int(newline[i][3])
  highway = newline[i][4]
      
  if start_city not in adjacency_list.keys():
     adjacency_list[start_city]={}
     adjacency_list[start_city][next_city]=distance
     speed_list[start_city]={}
     speed_list[start_city][next_city]=int(speed)
     time_list[start_city]={}
     if int(speed)!=0:  #DivideByZero error handling
      time_list[start_city][next_city]=float(int(distance))/float(int(speed))
     else:
      time_list[start_city][next_city] = float(0)
  else:
     adjacency_list[start_city][next_city] = distance
     speed_list[start_city][next_city] = int(speed)
     if int(speed)!=0:  #DivideByZero error handling
      time_list[start_city][next_city] = float(int(distance))/float(int(speed))
     else:
      time_list[start_city][next_city] = float(0)
  if start_city not in highway_list.keys():
     highway_list[start_city] = {}
     highway_list[start_city][next_city]=highway
  else:
     highway_list[start_city][next_city] = highway
  if next_city not in adjacency_list.keys():
     adjacency_list[next_city] = {}
     adjacency_list[next_city][start_city] = distance
     speed_list[next_city] = {}
     speed_list[next_city][start_city] = int(speed)
     time_list[next_city]={}
     if int(speed)!=0:  #DivideByZero error handling
      time_list[next_city][start_city]=float(int(distance))/float(int(speed))
     else:
      time_list[next_city][start_city] = float(0)
  else:
     
     adjacency_list[next_city][start_city] = distance
     speed_list[next_city][start_city] = int(speed)
     if int(speed)!=0:  #DivideByZero error handling
      time_list[next_city][start_city] = float(int(distance))/float(int(speed))
     else:
      time_list[next_city][start_city] = float(0)
  if next_city not in highway_list.keys():
     highway_list[next_city] = {}
     highway_list[next_city][start_city] = highway
  else:
     highway_list[next_city][start_city]= highway
     
city_gps1={}
#Reading city master data and storing it in list
city_data = []
with open('city-gps.txt','r') as city_gps:
  lines = city_gps.read().splitlines()
newline = [i.split(" ") for i in lines]
for city_name,lattitude,longitude in newline:
      city_data.append(city_name)
      city_gps1[city_name] = [lattitude,longitude]

#Accepting data from command line inputs
start = sys.argv[1]
goal = sys.argv[2]
routing_algo = sys.argv[3]
cost_function = sys.argv[4]

#Conditions for various routing algorithms and cost functions
if routing_algo == "bfs" and (cost_function=="distance" or cost_function=="time" or cost_function=="segments" or cost_function=="longtour"):#BFS is same for all cost functions.It returns a path with minimum number of segments
  total_path1 = bfs(adjacency_list,start,goal)
  print_data(total_path1)
elif routing_algo == "dfs" and (cost_function=="distance" or cost_function=="time" or cost_function=="segments" or cost_function=="longtour"):#DFS is same for all cost functions. It does not return a optimal solution.
  total_path1 = dfs(adjacency_list,start,goal)
  print_data(total_path1)
elif routing_algo == "uniform" and cost_function=="distance":
  total_path1 = ucs_distance(adjacency_list,start,goal)
  print_data(total_path1)
elif routing_algo == "uniform" and cost_function == "time":
  total_path1 = ucs_time(time_list,start,goal)
  print_data(total_path1)
elif routing_algo == "uniform" and cost_function == "segments":
  total_path1 = ucs_segment(start,goal)
  print_data(total_path1)
elif  routing_algo == "uniform" and cost_function == "longtour":
  total_path1 = ucs_longtour(adjacency_list,start,goal)
  print_data(total_path1)
elif routing_algo == "astar" and cost_function == "distance":
  total_path1 = astar_distance(adjacency_list,start,goal)
  print_data(total_path1)
elif routing_algo == "astar" and cost_function == "time":
  total_path1 = astar_time(time_list,start,goal)
  print_data(total_path1)
elif routing_algo == "astar" and cost_function == "segments":
  total_path1 = astar_segment(start,goal)
  print_data(total_path1)
elif routing_algo == "astar" and cost_function == "longtour":
  total_path1 = astar_longtour(adjacency_list,start,goal)
  print_data(total_path1)
else:#In case of wrong command line inputs
   print "Please enter the correct routing algorithm and cost function!(bfs,dfs,uniform,astar) and (distance,segments,time,longtour)"


