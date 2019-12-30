import sys
import copy
import random

class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Board:
    def __init__(self,dimension):
        self.dimension = dimension # Coordinate object
        self.board = self.createBoard()
    
    def createBoard(self):
        board = []
        for x in range(0,self.dimension.x):
            board.append([])
            for y in range(0,self.dimension.y):
                board[x].append("E")
        return board
    
    def addObstacle(self, obstacle):
        self.board[obstacle.x-1][obstacle.y-1] = "O"
    
    def addPitfall(self, pitfall):
        self.board[pitfall.x-1][pitfall.y-1] = "P"
    
    def addGoalState(self, goal):
        self.board[goal.x-1][goal.y-1] = "G"

    def getCell(self,coordinate):
        if(self.onBoard(coordinate)):
            return self.board[coordinate.x-1][coordinate.y-1]
        else:
            return -1
    
    def onBoard(self,coordinate):
        if(coordinate.x<1 or coordinate.y<1 or coordinate.x>self.dimension.x or coordinate.y>self.dimension.y):
            return False
        else:
            return True

class ValueIteration:
    def __init__(self,theta,gamma,board,rewards):
        self.position = Coordinate(1,1)
        self.theta = theta
        self.gamma = gamma
        self.board = board # Board object
        self.rewards = rewards
        self.state_space = self.initializeStates()
    
    def initializeStates(self):
        state_space = []
        for x in range(1,self.board.dimension.x+1):
            state_space.append([])
            for y in range(1,self.board.dimension.y+1):
                '''
                if(self.board.getCell(Coordinate(x,y)) == "P"):
                    state_space[x-1].append(self.rewards[2])
                elif(self.board.getCell(Coordinate(x,y)) == "O"):
                    state_space[x-1].append(self.rewards[1])
                elif(self.board.getCell(Coordinate(x,y)) == "G"):
                    state_space[x-1].append(self.rewards[2])
                else:
                '''
                state_space[x-1].append(0)
        return state_space

    
    def learn(self):
        updated_state_space = copy.deepcopy(self.state_space)
        break_flag = False
        first_pass = True
        delta = 0
        while(first_pass or delta > self.theta):
            delta = 0
            for x in range(0,self.board.dimension.x):
                if(break_flag):
                    break
                for y in range(0,self.board.dimension.y):
                    if(self.board.getCell(Coordinate(x+1,y+1)) == "O"):
                        continue
                    updated_state_space[x][y] =  self.calculateMax(Coordinate(x+1,y+1))
                    if(abs(updated_state_space[x][y]-self.state_space[x][y]) > delta):
                        delta = abs(updated_state_space[x][y]-self.state_space[x][y])
            first_pass = False
            self.state_space = copy.deepcopy(updated_state_space)
        #print(self.state_space)
        return None
    
    def goObi(self):
        for x in range(1,self.board.dimension.x + 1):
            for y in range(1,self.board.dimension.y + 1):
                (next_state,index) = self.findBestState(Coordinate(x,y))
                if(index == 0):
                    key = '0'
                elif(index == 1):
                    key = '2'
                elif(index == 2):
                    key = "1"
                else:
                    key = "3"
                self.output_file.write("{} {} {}\n".format(x,y,key))

            

    def findBestState(self,coordinate):
        next_states = [0,0,0,0]
        next_state_coordinates = []
        next_state_coordinates.append(Coordinate(coordinate.x,coordinate.y+1))
        next_state_coordinates.append(Coordinate(coordinate.x,coordinate.y-1))
        next_state_coordinates.append(Coordinate(coordinate.x-1,coordinate.y))
        next_state_coordinates.append(Coordinate(coordinate.x+1,coordinate.y))
        for i in range(0,4):
            if(self.board.getCell(next_state_coordinates[i]) == -1):
                next_states[i] = -1
            else:
                next_states[i] = self.calculateReward(next_state_coordinates[i]) + self.state_space[next_state_coordinates[i].x-1][next_state_coordinates[i].y-1]
        max_value = -1
        max_index = []
        for i in range(0,4):
            if(next_states[i]>max_value):
                max_index = []
                max_value = next_states[i]
                max_index.append(i)
            elif(next_states[i] == max_value):
                max_index.append(i)
        if(len(max_index) == 1):
            return (next_state_coordinates[max_index[0]],max_index[0])
        else:
            random_number = random.randint(0,len(max_index)-1)
            return (next_state_coordinates[max_index[random_number]],max_index[random_number])

    def calculateMax(self,coordinate):
        actions = [0,0,0,0]
        action_coordinates = []
        action_coordinates.append(Coordinate(coordinate.x,coordinate.y+1))
        action_coordinates.append(Coordinate(coordinate.x,coordinate.y-1))
        action_coordinates.append(Coordinate(coordinate.x-1,coordinate.y))
        action_coordinates.append(Coordinate(coordinate.x+1,coordinate.y))
        for i in range(0,4):
            action_coordinate = action_coordinates[i]
            reward = self.calculateReward(action_coordinate)
            if(self.board.getCell(action_coordinate) == -1):
                actions[i] = reward + 0.25*self.gamma * self.state_space[coordinate.x-1][coordinate.y-1]
            else:
                actions[i] = reward + 0.25*self.gamma * self.state_space[action_coordinate.x-1][action_coordinate.y-1]
        return max(actions)
    
    def calculateReward(self,coordinate):
        if(self.board.getCell(coordinate) == -1):
            return self.rewards[1]
        elif(self.board.getCell(coordinate) == "E"):
            return self.rewards[0]
        elif(self.board.getCell(coordinate) == "O"):
            return self.rewards[1]
        elif(self.board.getCell(coordinate) == "P"):
            return self.rewards[2]
        elif(self.board.getCell(coordinate) == "G"):
            return self.rewards[3]

    def addFile(self,file):
        self.output_file = file

class QLearning():
    def __init__(self,number_of_episodes,alpha,gamma,epsilon,board,rewards):
        self.number_of_episodes = number_of_episodes
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.board = board # Board object
        self.rewards = rewards

def create_learning_object(input_file_name):
    input_file = open(input_file_name,"r")
    lines = input_file.read().split("\n")
    if(lines[0]=="V"):
         return create_value_iteration(lines)
    elif(lines[0]=="Q"):
        return create_q_learning(lines)
    else:
        print "Errorneous input"
        return None

def create_value_iteration(lines):
    theta = float(lines[1])
    gamma = float(lines[2])
    y_dimension = int((lines[3].split(" "))[0])
    x_dimension = int((lines[3].split(" "))[1])
    dimension = Coordinate(x_dimension,y_dimension)
    board = Board(dimension)
    number_of_obstacles = int(lines[4])
    obstacles = []
    for i in range(5,5+number_of_obstacles):
        line = lines[i].split(" ")
        x = int(line[0])
        y = int(line[1])
        coordinate = Coordinate(x,y)
        obstacles.append(coordinate)
    for obstacle in obstacles:
        board.addObstacle(obstacle)
    number_of_pitfalls = int(lines[i+1])
    pitfall_index = i+2
    pitfalls = []
    for i in range(pitfall_index,pitfall_index+number_of_pitfalls):
        line = lines[i].split(" ")
        x = int(line[0])
        y = int(line[1])
        coordinate = Coordinate(x,y)
        pitfalls.append(coordinate)
    for pitfall in pitfalls:
        board.addPitfall(pitfall)
    goal_state_index = i+1
    line = lines[goal_state_index].split(" ")
    goal_state = Coordinate(int(line[0]),int(line[1]))
    board.addGoalState(goal_state)
    rewards = lines[goal_state_index+1].split(" ")
    for i in range(len(rewards)):
        rewards[i] = int(rewards[i])
    value_iteration = ValueIteration(theta,gamma,board,rewards)
    return (0,value_iteration)

def create_q_learning(lines):
    number_of_episodes = int(lines[1])
    alpha = float(lines[2])
    gamma = float(lines[3])
    epsilon = float(lines[4])
    y_dimension = int((lines[5].split(" "))[0])
    x_dimension = int((lines[5].split(" "))[1])
    dimension = Coordinate(x_dimension,y_dimension)
    board = Board(dimension)
    number_of_obstacles = int(lines[6])
    for i in range(7,7+number_of_obstacles):
        line = lines[i].split(" ")
        x = int(line[0])
        y = int(line[1])
        coordinate = Coordinate(x,y)
        board.addObstacle(coordinate)
    number_of_pitfalls = int(lines[i+1])
    pitfall_index = i+2
    for i in range(pitfall_index,pitfall_index+number_of_pitfalls):
        line = lines[i].split(" ")
        x = int(line[0])
        y = int(line[1])
        coordinate = Coordinate(x,y)
        board.addPitfall(coordinate)
    goal_state_index = i+1
    line = lines[goal_state_index].split(" ")
    goal_state = Coordinate(int(line[0]),int(line[1]))
    board.addGoalState(goal_state)
    rewards = lines[goal_state_index+1].split(" ")
    for i in range(len(rewards)):
        rewards[i] = int(rewards[i])
    q_learning = QLearning(number_of_episodes,alpha,gamma,epsilon,board,rewards)
    return (1,q_learning)

def main():
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    output_file = open(output_file_name,"w")
    (type_of_object, learning_object) = create_learning_object(input_file_name)
    if(type_of_object):
        return
    else:
        learning_object.learn()
        learning_object.addFile(output_file)
        learning_object.goObi()
    
if __name__=="__main__":
    main()
