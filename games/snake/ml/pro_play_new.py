from astar_python.astar import Astar
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
        class Astar:

            def __init__(self, matrix):
                self.mat = self.prepare_matrix(matrix)

            class Node:
                def __init__(self, x, y, weight=0):
                    self.x = x
                    self.y = y
                    self.weight = weight
                    self.heuristic = 0
                    self.parent = None

                def __repr__(self):
                    return str(self.weight)

            def print(self):
                for y in self.mat:
                    print(y)

            def prepare_matrix(self, mat):
                matrix_for_astar = []
                for y, line in enumerate(mat):
                    tmp_line = []
                    for x, weight in enumerate(line):
                        tmp_line.append(self.Node(x, y, weight=weight))
                    matrix_for_astar.append(tmp_line)
                return matrix_for_astar

            def equal(self, current, end):
                return current.x == end.x and current.y == end.y

            def heuristic(self, current, other):
                return abs(current.x - other.x) + abs(current.y - other.y)

            def neighbours(self, matrix, current):
                neighbours_list = []
                if current.x - 1 >= 0 and matrix[current.y][current.x - 1].weight is not None:
                    neighbours_list.append(matrix[current.y][current.x - 1])
                if current.y - 1 >= 0 and matrix[current.y - 1][current.x].weight is not None:
                    neighbours_list.append(matrix[current.y - 1][current.x])
                if current.y + 1 < len(matrix) and matrix[current.y + 1][current.x].weight is not None:
                    neighbours_list.append(matrix[current.y + 1][current.x])
                if current.x + 1 < len(matrix[0]) and matrix[current.y][current.x + 1].weight is not None:
                    neighbours_list.append(matrix[current.y][current.x + 1])

                return neighbours_list

            def build(self, end):
                node_tmp = end
                path = []
                while (node_tmp):
                    path.append([node_tmp.x, node_tmp.y])
                    node_tmp = node_tmp.parent
                return list(reversed(path))

            def run(self, point_start, point_end):
                matrix = self.mat
                start = self.Node(point_start[0], point_start[1])
                end = self.Node(point_end[0], point_end[1])
                closed_list = []
                open_list = [start]

                while open_list:
                    current_node = open_list.pop()

                    for node in open_list:
                        if node.heuristic < current_node.heuristic:
                            current_node = node

                    if self.equal(current_node, end):
                        return self.build(current_node)

                    for node in open_list:
                        if self.equal(current_node, node):
                            open_list.remove(node)
                            break

                    closed_list.append(current_node)

                    for neighbour in self.neighbours(matrix, current_node):
                        if neighbour in closed_list:
                            continue
                        if neighbour.heuristic < current_node.heuristic or neighbour not in open_list:
                            neighbour.heuristic = neighbour.weight + self.heuristic(neighbour, end)
                            neighbour.parent = current_node
                        if neighbour not in open_list:
                            open_list.append(neighbour)

                return None
        
                    
        if scene_info["status"] == "GAME_OVER":
            return "RESET"
        
        # 30 x 30 矩陣
        maze  = [[0 for i in range(30)] for j in range(30)]
        
        head = scene_info["snake_head"]
        start = (head[1]//10, head[0]//10)
        food = scene_info["food"]

        #障礙物
        body = scene_info["snake_body"]
        #print(body)
        for i in range(len(body)):
            maze[body[i][0]//10][body[i][1]//10] = None 
            
        astar = Astar(maze)
        result = astar.run([start[0], start[1]], [food[1]//10, food[0]//10])
        #print(result)
        
        if result != None:
            fx = result[0][0]
            fy = result[0][1]
            sx = result[1][0]
            sy = result[1][1]

            if (sx - fx) == 1: return "DOWN"
            if (sx - fx) == -1: return "UP"
            if (sy - fy) == 1: return "RIGHT"
            if (sy - fy) == -1: return "LEFT"
        else:
            if head[0] != 290:
                if (head[0]+10, head[1]) not in body: return "RIGHT"
            if head[0] != 0:
                if (head[0]-10, head[1]) not in body: return "LEFT"
            if head[1] != 290:
                if (head[0], head[1]+10) not in body: return "DOWN"
            if head[1] != 0:
                if (head[0], head[1]-10) not in body: return "UP"

    def reset(self):
        """
        Reset the status if needed
        """
        pass
