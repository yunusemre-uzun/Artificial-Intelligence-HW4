import sys

class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Board:
    def __init__(self,dimension,obstacles,pitfalls,goal_state):
        self.dimension = dimension # Coordinate object
        self.obstacles = obstacles # List of obstacles
        self.pitfalls = pitfalls # List of pirfalls
        self.goal_state = goal_state # Coordinate of goal state

class ValueIteration:
    def __init__(self,theta,gamma,board,rewards):
        self.theta = theta
        self.gamma = gamma
        self.board = board # Board object
        self.rewards = rewards

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
    number_of_obstacles = int(lines[4])
    obstacles = []
    for i in range(5,5+number_of_obstacles):
        line = lines[i].split(" ")
        x = int(line[0])
        y = int(line[1])
        coordinate = Coordinate(x,y)
        obstacles.append(coordinate)
    number_of_pitfalls = int(lines[i+1])
    pitfall_index = i+2
    pitfalls = []
    for i in range(pitfall_index,pitfall_index+number_of_pitfalls):
        line = lines[i].split(" ")
        x = int(line[0])
        y = int(line[1])
        coordinate = Coordinate(x,y)
        pitfalls.append(coordinate)
    goal_state_index = i+1
    line = lines[goal_state_index].split(" ")
    goal_state = Coordinate(int(line[0]),int(line[1]))
    rewards = lines[goal_state_index+1].split(" ")
    for i in range(len(rewards)):
        rewards[i] = int(rewards[i])
    board = Board(dimension,obstacles,pitfalls,goal_state)
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
    number_of_obstacles = int(lines[6])
    obstacles = []
    for i in range(7,7+number_of_obstacles):
        line = lines[i].split(" ")
        x = int(line[0])
        y = int(line[1])
        coordinate = Coordinate(x,y)
        obstacles.append(coordinate)
    number_of_pitfalls = int(lines[i+1])
    pitfall_index = i+2
    pitfalls = []
    for i in range(pitfall_index,pitfall_index+number_of_pitfalls):
        line = lines[i].split(" ")
        x = int(line[0])
        y = int(line[1])
        coordinate = Coordinate(x,y)
        pitfalls.append(coordinate)
    goal_state_index = i+1
    line = lines[goal_state_index].split(" ")
    goal_state = Coordinate(int(line[0]),int(line[1]))
    rewards = lines[goal_state_index+1].split(" ")
    for i in range(len(rewards)):
        rewards[i] = int(rewards[i])
    board = Board(dimension,obstacles,pitfalls,goal_state)
    q_learning = QLearning(number_of_episodes,alpha,gamma,epsilon,board,rewards)
    return (1,q_learning)



def main():
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    (type_of_object, learning_object) = create_learning_object(input_file_name)
    if(type_of_object):
        return
    else:
        return
    

if __name__=="__main__":
    main()
