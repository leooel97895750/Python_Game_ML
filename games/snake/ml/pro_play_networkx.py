import sys
import os
import networkx as nx

G=nx.grid_graph(dim=[3,3])
print(G.nodes())

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
        if scene_info["status"] == "GAME_OVER":
            return "RESET"
        
        # 30 x 30 矩陣
        G = nx.grid_graph(dim=[30,30])
        
        head = scene_info["snake_head"]
        food = scene_info["food"]

        #print(G.nodes())
        #障礙物
        body = scene_info["snake_body"]
        #print(body)
        for i in range(len(body)):
            try:
                G.remove_node((body[i][1]//10, body[i][0]//10))
            except:
                pass
            
        result = nx.astar_path(G,(head[1]//10, head[0]//10),(food[1]//10, food[0]//10))
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
