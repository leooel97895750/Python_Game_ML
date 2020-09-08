import random

class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        self.last_command = "SPEED"

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        #print(scene_info)
        self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"

        command = self.last_command
        roadcenter = [35, 105, 175, 245, 315, 385, 455, 525, 595]
        #roadwidth = [0, 70, 140, 210, 280, 350, 420, 490, 560, 630]
        #玩家的道路
        road = -1
        for i in range(9):
            if self.car_pos != ():
                if abs(self.car_pos[0] - roadcenter[i]) <= 5:
                    road = i
                    break

        if road != -1:
            #電腦車輛資訊
            cars = [[],[],[],[],[],[],[],[],[]]
            cars_info = scene_info["cars_info"]
            for i in range(len(cars_info)):
                carx = cars_info[i]["pos"][0]
                for j in range(len(roadcenter)):
                    if roadcenter[j] == carx:
                        cars[j].append(cars_info[i])
                        break
            #print(cars)

            #判斷相撞
            for i in cars[road]:
                if i["pos"][1] > 0 and i["pos"][1] < self.car_pos[1] and i["velocity"] < self.car_vel:

                    if road > 4:
                        check = 0
                        for j in cars[road-1]:
                            if j["pos"][1] < self.car_pos[1] and (self.car_pos[1] - j["pos"][1]) < 160: 
                                check += 1
                            if j["pos"][1] > self.car_pos[1] and (j["pos"][1] - self.car_pos[1]) < 100: 
                                check += 1
                        if check == 0: 
                            command = "MOVE_LEFT"
                        else:
                            if road != 8:
                                check = 0
                                for j in cars[road+1]:
                                    if j["pos"][1] < self.car_pos[1] and (self.car_pos[1] - j["pos"][1]) < 160: 
                                        check += 1
                                    if j["pos"][1] > self.car_pos[1] and (j["pos"][1] - self.car_pos[1]) < 100: 
                                        check += 1
                                if check == 0: 
                                    command = "MOVE_RIGHT"
                                else: 
                                    command = "BRAKE"
                            else: 
                                command = "BRAKE"
                    else:
                        check = 0
                        for j in cars[road+1]:
                            if j["pos"][1] < self.car_pos[1] and (self.car_pos[1] - j["pos"][1]) < 160: 
                                check += 1
                            if j["pos"][1] > self.car_pos[1] and (j["pos"][1] - self.car_pos[1]) < 100: 
                                check += 1
                        if check == 0: 
                            command = "MOVE_RIGHT"
                        else:
                            if road != 0:
                                check = 0
                                for j in cars[road-1]:
                                    if j["pos"][1] < self.car_pos[1] and (self.car_pos[1] - j["pos"][1]) < 160: 
                                        check += 1
                                    if j["pos"][1] > self.car_pos[1] and (j["pos"][1] - self.car_pos[1]) < 100: 
                                        check += 1
                                if check == 0: 
                                    command = "MOVE_LEFT"
                                else: 
                                    command = "BRAKE"
                            else: 
                                command = "BRAKE"
                                
                else: command = "SPEED"
  
        self.last_command = command
        return command

    def reset(self):
        """
        Reset the status
        """
        pass
