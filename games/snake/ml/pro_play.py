import numpy as np
import sys
import os

"""
The template of the script for playing the game in the ml mode
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        pass
                
    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        #以下是A*演算法
        class Node:

            def __init__(self, parent=None, position=None):
                self.parent = parent
                self.position = position

                self.g = 0
                self.h = 0
                self.f = 0
            def __eq__(self, other):
                return self.position == other.position

        #This function return the path of the search
        def return_path(current_node,maze):
            path = []
            no_rows, no_columns = np.shape(maze)
            # here we create the initialized result maze with -1 in every position
            result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            # Return reversed path as we need to show from start to end path
            path = path[::-1]
            start_value = 0
            # we update the path of start to end found by A-star serch with every step incremented by 1
            for i in range(len(path)):
                result[path[i][0]][path[i][1]] = start_value
                start_value += 1
            return result


        def search(maze, cost, start, end):

            # Create start and end node with initized values for g, h and f
            start_node = Node(None, tuple(start))
            start_node.g = start_node.h = start_node.f = 0
            end_node = Node(None, tuple(end))
            end_node.g = end_node.h = end_node.f = 0

            # Initialize both yet_to_visit and visited list
            # in this list we will put all node that are yet_to_visit for exploration. 
            # From here we will find the lowest cost node to expand next
            yet_to_visit_list = []  
            # in this list we will put all node those already explored so that we don't explore it again
            visited_list = [] 

            # Add the start node
            yet_to_visit_list.append(start_node)

            # Adding a stop condition. This is to avoid any infinite loop and stop 
            # execution after some reasonable number of steps
            outer_iterations = 0
            max_iterations = (len(maze) // 2) ** 10

            # what squares do we search . serarch movement is left-right-top-bottom 
            #(4 movements) from every positon

            move  =  [[-1, 0 ], # go up
                      [ 0, -1], # go left
                      [ 1, 0 ], # go down
                      [ 0, 1 ]] # go right

            #find maze has got how many rows and columns 
            no_rows, no_columns = np.shape(maze)

            # Loop until you find the end

            while len(yet_to_visit_list) > 0:

                # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
                outer_iterations += 1    


                # Get the current node
                current_node = yet_to_visit_list[0]
                current_index = 0
                for index, item in enumerate(yet_to_visit_list):
                    if item.f < current_node.f:
                        current_node = item
                        current_index = index

                # if we hit this point return the path such as it may be no solution or 
                # computation cost is too high
                if outer_iterations > max_iterations:
                    print ("giving up on pathfinding too many iterations")
                    del start_node, end_node, new_node
                    return return_path(current_node,maze)

                # Pop current node out off yet_to_visit list, add to visited list
                yet_to_visit_list.pop(current_index)
                visited_list.append(current_node)

                # test if goal is reached or not, if yes then return the path
                if current_node == end_node:
                    del start_node, end_node, new_node
                    return return_path(current_node,maze)

                # Generate children from all adjacent squares
                children = []

                for new_position in move: 

                    # Get node position
                    node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                    # Make sure within range (check if within maze boundary)
                    if (node_position[0] > (no_rows - 1) or 
                        node_position[0] < 0 or 
                        node_position[1] > (no_columns -1) or 
                        node_position[1] < 0):
                        continue

                    # Make sure walkable terrain
                    if maze[node_position[0]][node_position[1]] != 0:
                        continue

                    # Create new node
                    new_node = Node(current_node, node_position)

                    # Append
                    children.append(new_node)

                # Loop through children
                for child in children:

                    # Child is on the visited list (search entire visited list)
                    if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                        continue

                    # Create the f, g, and h values
                    child.g = current_node.g + cost
                    ## Heuristic costs calculated here, this is using eucledian distance
                    child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                               ((child.position[1] - end_node.position[1]) ** 2)) 

                    child.f = child.g + child.h

                    # Child is already in the yet_to_visit list and g cost is already lower
                    if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                        continue

                    # Add the child to the yet_to_visit list
                    yet_to_visit_list.append(child)
                    
        if scene_info["status"] == "GAME_OVER":
            os._exit()
            cmd = 'start cmd.exe /K python.exe %s ^&^& exit'
            os.system(cmd)
            return "RESET"
        
        # 30 x 30 矩陣
        maze  = [[0 for i in range(30)] for j in range(30)]
        head = scene_info["snake_head"]
        food = scene_info["food"]
        #起點、終點 
        start = (head[1]//10, head[0]//10)
        end = (food[1]//10, food[0]//10)
        #障礙物
        body = scene_info["snake_body"]
        
        for i in range(len(body)):
            maze[body[i][1]//10][body[i][0]//10] = 1    
            
        path = search(maze, 1, start, end)
#         print('\n\n\n')
#         for i in range(30):
#             for j in range(30):
#                 print(path[i][j], end=' ' )
#             print('\n')
        #way = (path[1][0] - path[0][0], path[1][1] - path[0][1])
        
#         print(path[start[1]-1][start[0]])
#         print(path[start[1]+1][start[0]])
#         print(path[start[1]][start[0]-1])
#         print(path[start[1]][start[0]+1])
        if start[1] != 0:
            if path[start[0]][start[1]-1] == 1: return "LEFT"
        if start[1] != 29:
            if path[start[0]][start[1]+1] == 1: return "RIGHT"
        if start[0] != 0:
            if path[start[0]-1][start[1]] == 1: return "UP"
        if start[0] != 29:
            if path[start[0]+1][start[1]] == 1: return "DOWN"
#         if way == (0,-1): return "LEFT"
#         elif way == (0,1): return "RIGHT" 
#         elif way == (-1,0): return "UP"
#         elif way == (1,0): return "DOWN"

    def reset(self):
        """
        Reset the status if needed
        """
        pass
