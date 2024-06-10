import math
from copy import deepcopy 
import numpy as np 

# Lehmer random number generation, using MINSTD parameters
a = 16807
m = 2147483647
piece_list = ["z", "l", "o", "s", "i", "j", "t"]

def next_seed(seed):
    # Returns the next seed
    seed = a * seed % m
    return seed

def next_float(seed):
    # Returns a random float between 0 and 1, as well as the next seed
    new_seed = next_seed(seed)
    return (new_seed - 1) / (m-1), new_seed


def shuffle_array(l, seed):
    #  Fisher–Yates shuffle, returns shuffled list and the next seed
    shuffled_list = l.copy()

    for i in range(len(shuffled_list) - 1, 0, - 1):
        random_float, seed = next_float(seed)
        r = math.floor(random_float * (i + 1))
        shuffled_list[i], shuffled_list[r] = shuffled_list[r], shuffled_list[i]

    return shuffled_list, seed

def get_next_piece(queue, seed):
    if not queue:
        queue = self.shuffle_array(piece_list, seed)

    return self.queue.pop(0), queue, seed


## Usage :

# Initialisation de la seed et de la queue
seed = 12345
queue = []

# Pour récupérer la prochaine pièce et mettre à jour la queue et seed si nécessaire :
next_piece, queue, seed = get_next_piece(queue, seed)

board = [[0 for _ in range(10)] for _ in range(40)]

def emptyline(line):
    for i in range(len(line)): 
        if line[i]!=0 : return False 
    return True 

def fullline(line):
    for i in range(len(line)): 
        if line[i]!=1 : return False 
    return True 

def clearline(i,board):
    for j in range(i,len(board-1)): 
            board[j]=board[j+1]
            board[len(board)]=[0 for _ in range(10)]
    return board 

def height(board): 
    for i in range(40):
        if emptyline(board[i])==True :
            return(i)
    return(20)
        
def updateboard(board) :
    for i in range(40): 
        if fullline(board[i])==True : 
            board=clearline(i,board)  
    return board    

#Lpieces 
dict_pieces = {
"t" : [[
[0, 1, 0],
[1, 1, 1],
[0, 0, 0],
], [
[0, 1, 0],
[0, 1, 1],
[0, 1, 0],
], [
[0, 0, 0],
[1, 1, 1],
[0, 1, 0],
],
[
[0, 1, 0],
[1, 1, 0],
[0, 1, 0],
]],

"s" : [[
[0, 1, 1],
[1, 1, 0],
[0, 0, 0],
], [
[0, 1, 0],
[0, 1, 1],
[0, 0, 1],
], [
[0, 0, 0],
[0, 1, 1],
[1, 1, 0],
],
[
[1, 0, 0],
[1, 1, 0],
[0, 1, 0],
]],

"z" : [[
[1, 1, 0],
[0, 1, 1],
[0, 0, 0],
], [
[0, 0, 1],
[0, 1, 1],
[0, 1, 0],
], [
[0, 0, 0],
[1, 1, 0],
[0, 1, 1],
],
[
[0, 1, 0],
[1, 1, 0],
[1, 0, 0],
]],

"l" : [[
[0, 0, 1],
[1, 1, 1],
[0, 0, 0],
], [
[0, 1, 0],
[0, 1, 0],
[0, 1, 1],
], [
[0, 0, 0],
[1, 1, 1],
[1, 0, 0],
],
[
[1, 1, 0],
[0, 1, 0],
[0, 1, 0],
]],

"j" : [[
[1, 0, 0],
[1, 1, 1],
[0, 0, 0],
], [
[0, 1, 1],
[0, 1, 0],
[0, 1, 0],
], [
[0, 0, 0],
[1, 1, 1],
[0, 0, 1],
],
[
[0, 1, 0],
[0, 1, 0],
[1, 1, 0],
]],
"i" : [[
[0, 0, 0, 0],
[1, 1, 1, 1],
[0, 0, 0, 0],
[0, 0, 0, 0],
], [
[0, 0, 1, 0],
[0, 0, 1, 0],
[0, 0, 1, 0],
[0, 0, 1, 0],
], [
[0, 0, 0, 0],
[0, 0, 0, 0],
[1, 1, 1, 1],
[0, 0, 0, 0],
], [
[0, 1, 0, 0],
[0, 1, 0, 0],
[0, 1, 0, 0],
[0, 1, 0, 0],
]],
"o" : [[
[1, 1],
[1, 1],
], [
[1, 1],
[1, 1],
], [
[1, 1],
[1, 1],
], [
[1, 1],
[1, 1],
]]
}


# Rotation CW pour 't', 's', 'z', 'l', 'j'
[
    [[-1, 0],[-1,+1],[ 0,-2],[-1,-2]], # Position initiale
    [[+1, 0],[+1,-1],[ 0,+2],[+1,+2]], # CW par rapport à initiale
    [[+1, 0],[+1,+1],[ 0,-2],[+1,-2]], # 180 par rapport à initiale
    [[-1, 0],[-1,-1],[ 0,+2],[-1,+2]], # CCW par rapport à initiale
]

# Rotation CCW pour 't', 's', 'z', 'l', 'j'
[
    [[+1, 0],[+1,+1],[ 0,-2],[+1,-2]], # Position initiale
    [[+1, 0],[+1,-1],[ 0,+2],[+1,+2]], # CW par rapport à initiale
    [[-1, 0],[-1,+1],[ 0,-2],[-1,-2]], # 180 par rapport à initiale
    [[-1, 0],[-1,-1],[ 0,+2],[-1,+2]], # CCW par rapport à initiale
]

# Rotation CW pour 'i'
[
    [[+1, 0],[-2, 0],[+1,+2],[-2,-1]], # Position initiale
    [[-1, 0],[+2, 0],[-1,+2],[+2,-1]], # CW par rapport à initiale
    [[+2, 0],[-1, 0],[+2,+1],[-1,-2]], # 180 par rapport à initiale
    [[+1, 0],[-2, 0],[+1,-2],[-2,+1]], # CCW par rapport à initiale
]

# Rotation CCW pour 'i'
[
    [[-1, 0],[+2, 0],[-1,+2],[+2,-1]], # Position initiale
    [[+2, 0],[-1, 0],[+2,+1],[-1,-2]], # CW par rapport à initiale
    [[-2, 0],[+1, 0],[-2,+1],[+1,-2]], # 180 par rapport à initiale
    [[-2, 0],[+1, 0],[-2,-1],[+1,+2]], # CCW par rapport à initiale
]

# Rotation 180 't', 's', 'z', 'l', 'j', 'i' (inutile au dela du premier kick pour I)
[
    [[0, +1],[+1,+1],[-1,+1],[+1, 0],[-1, 0]], # Position initiale
    [[+1, 0],[+1,+2],[+1,+1],[ 0,+2],[ 0,+1]], # CW par rapport à initiale
    [[0, -1],[-1,-1],[+1,-1],[-1, 0],[+1, 0]], # 180 par rapport à initiale
    [[-1, 0],[-1,+2],[-1,+1],[ 0,+2],[ 0,+1]], # CCW par rapport à initiale
]

def spawnpiece(piece):
    if piece in ["z", "l", "s", "j", "t","i"]: 
        pos=(3,22)
    if piece == "o":
        pos=(4,22)
    return pos

def get_queue(piecesplaced,seed):
    for i in range(piecesplaced) : 
        next_piece, queue, seed = get_next_piece(queue, seed)
    return queue 

#Handling 

Handling = replay["endcontext"][0]["handling"]
arr = Handling["arr"]
das = Handling["das"]
dcd = Handling["dcd"]
sdf = Handling["sdf"]

def checkmovepiece(piece, rot, pos, board, move):
    Lpiece = dict_pieces[piece][rot]
    newpos = []
    newpos.append(pos[0]+move[0])
    newpos.append(pos[1]+move[1])
    n=len(Lpiece)

    for i in range(n): 
        for j in range(n):
            if Lpiece[i][j]==1 :
                if newpos[1]+j < 0 or newpos[1]+j > 10 : return False 
                if newpos[0]-i < 0 : return False 
                if board[newpos[0]-i][newpos[1]+j] == 1 : return False
    return True 

calcrot = {"rotateCW" : 1, "rotateCCW" : -1, "rotate180" : 2}

def rotate(piece, rot, pos, board, move): 
    newrot = (rot +calcrot[move])%4
    if checkmovepiece(piece, newrot, pos, board, move) == True : 
        return(piece[newrot])
    if checkmovepiece(piece, newrot, pos, board, move) == False : 
        get_kick(piece,rot,move)


def get_kick(piece, rot, move):
    if move == "rotateCW":
        if piece in ["t", "s", "z", "l", "j"]:
        # Rotation CW pour 't', 's', 'z', 'l', 'j'
            return [
                [[-1, 0],[-1,+1],[ 0,-2],[-1,-2]], # Position initiale
                [[+1, 0],[+1,-1],[ 0,+2],[+1,+2]], # CW par rapport à initiale
                [[+1, 0],[+1,+1],[ 0,-2],[+1,-2]], # 180 par rapport à initiale
                [[-1, 0],[-1,-1],[ 0,+2],[-1,+2]], # CCW par rapport à initiale
                 ][rot]

        elif piece == "i":
        # Rotation CW pour 'i'
            return [
            [[+1, 0],[-2, 0],[+1,+2],[-2,-1]], # Position initiale
            [[-1, 0],[+2, 0],[-1,+2],[+2,-1]], # CW par rapport à initiale
            [[+2, 0],[-1, 0],[+2,+1],[-1,-2]], # 180 par rapport à initiale
            [[+1, 0],[-2, 0],[+1,-2],[-2,+1]], # CCW par rapport à initiale
            ][rot]

        else:
        #No kicks for 'o'
            return []
    elif move == "rotateCCW":
        if piece in ["t", "s", "z", "l", "j"]:
    # Rotation CCW pour 't', 's', 'z', 'l', 'j'
            return [
        [[+1, 0],[+1,+1],[ 0,-2],[+1,-2]], # Position initiale
        [[+1, 0],[+1,-1],[ 0,+2],[+1,+2]], # CW par rapport à initiale
        [[-1, 0],[-1,+1],[ 0,-2],[-1,-2]], # 180 par rapport à initiale
        [[-1, 0],[-1,-1],[ 0,+2],[-1,+2]], # CCW par rapport à initiale
        ][rot]

        elif piece == "i":
    # Rotation CCW pour 'i'
            return [
        [[-1, 0],[+2, 0],[-1,+2],[+2,-1]], # Position initiale
        [[+2, 0],[-1, 0],[+2,+1],[-1,-2]], # CW par rapport à initiale
        [[-2, 0],[+1, 0],[-2,+1],[+1,-2]], # 180 par rapport à initiale
        [[-2, 0],[+1, 0],[-2,-1],[+1,+2]], # CCW par rapport à initiale
        ][rot]

        else:
        # No kicks for 'o'
            return []

    else:
        if piece != "o" :
        # Rotation 180 't', 's', 'z', 'l', 'j', 'i' (inutile au dela du premier kick pour I)
            return [
            [[0, +1],[+1,+1],[-1,+1],[+1, 0],[-1, 0]], # Position initiale
            [[+1, 0],[+1,+2],[+1,+1],[ 0,+2],[ 0,+1]], # CW par rapport à initiale
            [[0, -1],[-1,-1],[+1,-1],[-1, 0],[+1, 0]], # 180 par rapport à initiale
            [[-1, 0],[-1,+2],[-1,+1],[ 0,+2],[ 0,+1]], # CCW par rapport à initiale
            ][rot]

        else:
            return []

def currentspeed(frame): 
    return 0.02+0.0035*(frame//7200)


def CheckTspin(board_array): 
    c=0
    setupTspin=[[1,0,0],
                [0,0,0],
                [1,0,1]]
    for i in range(7):
        for j in range(37): 
            if board_array[i:i+3,j:j+3] == setupTspin : c+=1
    return c

def CheckTspintriple(board_array): 
    c=0
    setupTspintriple=[[1,1,0,0],
                    [1,0,0,0],
                    [1,0,1,1],
                    [1,0,0,1],
                    [1,0,1,1]]
    for i in range(6):
        for j in range(35): 
            if board_array[i:i+4,j:j+5] == setupTspintriple : c+=1
    return c

def Countholes(board_array): 
    c=0
    hole=[[1],[0]]
    for i in range(9):
        for j in range(39): 
            if board_array[i:i+1,j:j+1] == hole : c+=1
    return c

def onfloor(piece, pos, rot, board):
    Lpiece = dict_pieces[piece][rot]
    for i in range(len(Lpiece)):
        for j in range(len(Lpiece)): 
            if Lpiece[i][j]==1 :
                if board[pos[0]-i][pos[1]+j]==1 : return True
    return False 

def chute_naturelle(frame1 , frame2):
    """Fonction qui calcule la chute d'une pièce a cause de la gravité

    Args:
        frame1 (int): numero de frame avant
        frame2 (int): numero de frame après
    Returns:
        int: nombre de case de laquelle à chuter la pièce
    """
    dt = frame2 - frame1
    v = currentspeed(frame2)
    return round(v*dt)


def evolveboard(stream): 
    seed = replay["events"][1]["data"]["options"]["seed"]
    replay = stream["data"][0]["replays"][0]
    piecesplaced = replay["events"][len(replay["events"])-1]["data"]["export"]["stats"]["piecesplaced"]
    queue = get_queue(piecesplaced,seed)                    #donne les prochaines pièces
    board = [[0 for _ in range(10)] for _ in range(40)]
    for i in replay : 
        j=0
        if i["frame"] != 0 : 
            


        
            




        





    











    
