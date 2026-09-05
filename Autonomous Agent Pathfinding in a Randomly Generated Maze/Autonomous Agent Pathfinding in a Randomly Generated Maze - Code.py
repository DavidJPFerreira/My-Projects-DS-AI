from tkinter.constants import X
import PySimpleGUI as sg           
import numpy as np
import math
import random as rand 

def makeMaze(dimX, dimY):

    # Make a starter gir of zeros:
    starterMap = np.zeros((dimX, dimY), dtype=int) #1.[]v 2.[]>
    # add rows and columns:
    for x in range(_VARS['rowColCount']):
        randRow = rand.randint(1, dimX-1)
        randColumn = rand.randint(1, dimY-1)
        starterMap[randRow-1:randRow] = 1
        starterMap[:, randColumn-1] = 1
        # poke holes in said rows and columns:
        for x in range(_VARS['falhas']):
            starterMap[randRow-1][rand.randint(0, dimY-1)] = 0
            starterMap[rand.randint(0, dimX-1)][randColumn-1] = 0
    # Add blank cells fro entrance,exit and around them:

    starterMap[0][0] = 0 
    starterMap[0][1] = 0 
    starterMap[1][0] = 0
    starterMap[1][1] = 0


    for _ in range(_VARS['nKeys']):
        
        xChave = rand.randint(2,_VARS['cellCount'] - 2)
        yChave = rand.randint(2,_VARS['cellCount'] - 2)

        starterMap[xChave][yChave] = 3  # chave RANDOMIZER

        aux = 0
        while aux == 0:
            if [[xChave],[yChave]] not in terminationStates:
                terminationStates.append([xChave,yChave])
                aux = 1
            else:
                xChave = rand.randint(2,_VARS['cellCount'] - 2)
                yChave = rand.randint(2,_VARS['cellCount'] - 2)
        

        if starterMap[xChave][yChave-1] == 2 or starterMap[xChave][yChave-1] == 3: 
            pass
        else:
            starterMap[xChave][yChave-1] = 0

        if starterMap[xChave][yChave+1] == 2 or starterMap[xChave][yChave+1] == 3:
            pass
        else:
            starterMap[xChave][yChave+1] = 0
        
        if starterMap[xChave-1][yChave] == 2 or starterMap[xChave-1][yChave] == 3:
            pass
        else:
            starterMap[xChave-1][yChave] = 0
        
        if starterMap[xChave+1][yChave] == 2 or starterMap[xChave+1][yChave] == 3:
            pass
        else:
            starterMap[xChave+1][yChave] = 0
    

    return starterMap
#----------------------------------------------------------------------------------------------------------------------------------------------
def drawGrid():
    cells = _VARS['cellCount']
    _VARS['canvas'].TKCanvas.create_rectangle(
        1, 1, _VARS['gridSize'], _VARS['gridSize'], outline='darkgreen',fill='palegreen', width=1)
    for x in range(cells):
        _VARS['canvas'].TKCanvas.create_line(
            ((cellSize * x), 0), ((cellSize * x), _VARS['gridSize']),
            fill='darkgreen', width=1)
        _VARS['canvas'].TKCanvas.create_line(
            (0, (cellSize * x)), (_VARS['gridSize'], (cellSize * x)),
            fill='darkgreen', width=1)
#-----------------------------------------------------------------------------------------------------------------------------------------------
def drawCell(x, y, color1, color2):
    _VARS['canvas'].TKCanvas.create_rectangle(
        x, y, x + cellSize, y + cellSize,
        outline=color1, fill=color2, width=1)
#-----------------------------------------------------------------------------------------------------------------------------------------------
def placeCells():
    for row in range(_VARS['cellMAP'].shape[0]):
        for column in range(_VARS['cellMAP'].shape[1]):
            if(_VARS['cellMAP'][column][row] == 1):
                drawCell((cellSize*row), (cellSize*column), 'black', 'gray' ) #Parede
            elif(_VARS['cellMAP'][column][row] == 3):
                drawCell((cellSize*row), (cellSize*column) ,'gold', 'DarkGoldenrod1')  #KEY
#-----------------------------------------------------------------------------------------------------------------------------------------------
def actionRewardFunction(initialPosition, action): #important
    
    if initialPosition in terminationStates:
        return initialPosition, 0
    
    reward = _VARS['rewardSize']
    finalPosition = np.array(initialPosition) + np.array(action)
    if -1 in finalPosition or 15 in finalPosition: 
        finalPosition = initialPosition
        
    return finalPosition, reward
#-----------------------------------------------------------------------------------------------------------------------------------------------
def LegalMoves():        #[0,1]
    
    if _VARS['XYreal'][0] - 1 < 0 : # Left
        del Legal[3]

    if _VARS['XYreal'][0] + 1  > _VARS['cellCount'] - 1: # Right
        del Legal[2]

    if _VARS['XYreal'][1] - 1 < 0 : # Up
        del Legal[0]

    if _VARS['XYreal'][1] + 1 > _VARS['cellCount'] - 1: # Down
        del Legal[1]
    
    y , x = _VARS['XYreal'][0]  ,  _VARS['XYreal'][1]

    if _VARS['XYreal'][0] - 1  > 0:
        if _VARS['cellMAP'][x][y-1] == 0:
            if _VARS['XYreal'][0] - 2  > 0:
                if _VARS['cellMAP'][x][y-2] == 1:
                    if _VARS['XYreal'][1] + 1  < _VARS['cellCount'] - 1:
                        if _VARS['cellMAP'][x+1][y-1] == 1:
                            if _VARS['XYreal'][1] - 1  > 0:
                                if _VARS['cellMAP'][x-1][y-1] == 1:
                                    del Legal[3] # Left
    
    if _VARS['XYreal'][0] + 1  < _VARS['cellCount'] - 1:
        if _VARS['cellMAP'][x][y+1] == 0:
            if _VARS['XYreal'][0] + 2  < _VARS['cellCount'] - 1:
                if _VARS['cellMAP'][x][y+2] == 1:
                   if _VARS['XYreal'][1] + 1  < _VARS['cellCount'] - 1: 
                        if _VARS['cellMAP'][x+1][y+1] == 1:
                            if _VARS['XYreal'][1] - 1  > 0:
                                if _VARS['cellMAP'][x-1][y+1] == 1:
                                     del Legal[2] # Right

    if _VARS['XYreal'][1] - 1  > 0:
        if _VARS['cellMAP'][x-1][y] == 0:
            if _VARS['XYreal'][1] - 2  > 0:
                if _VARS['cellMAP'][x-2][y] == 1:
                    if _VARS['XYreal'][0] - 1  > 0:
                        if _VARS['cellMAP'][x-1][y-1] == 1:
                            if _VARS['XYreal'][0] + 1  < _VARS['cellCount'] - 1:
                                if _VARS['cellMAP'][x-1][y+1] == 1:
                                    del Legal[0] # Up

    if _VARS['XYreal'][1] + 1  < _VARS['cellCount'] - 1:
        if _VARS['cellMAP'][x+1][y] == 0:
            if _VARS['XYreal'][1] + 2  < _VARS['cellCount'] - 1:
                if _VARS['cellMAP'][x+2][y] == 1:
                    if _VARS['XYreal'][0] - 1  > 0:
                        if _VARS['cellMAP'][x+1][y-1] == 1:
                            if _VARS['XYreal'][0] + 1  < _VARS['cellCount'] - 1:
                                if _VARS['cellMAP'][x+1][y+1] == 1:
                                    del Legal[1] # Down                    
#-----------------------------------------------------------------------------------------------------------------------------------------------
def Mover(move):
    global Legal
    if move == "Up":
        _VARS['XYreal'][1] = _VARS['XYreal'][1] - 1
    elif move == "Down":
        _VARS['XYreal'][1] = _VARS['XYreal'][1] + 1
    elif move == "Right":
        _VARS['XYreal'][0] = _VARS['XYreal'][0] + 1
    elif move == "Left":
        _VARS['XYreal'][0] = _VARS['XYreal'][0] - 1
    
    Legal = ["Up","Down","Right","Left"]
#-----------------------------------------------------------------------------------------------------------------------------------------------
def ValueCheck(): 
    
    global last
    
    LegalMoves()

    bestMove = []           #bestmove=[-7,"Up"]

    y , x = _VARS['XYreal'][0]  ,  _VARS['XYreal'][1]

    
    for move in Legal:
        if move == "Up":                        #[ [1,2,3],[4,5,6],[7,8,9] ]
            bestMove.append([valueMap[x-1][y] , move])
        if move == "Down":
            bestMove.append([valueMap[x+1][y] , move])

        if move == "Right":
            bestMove.append([valueMap[x][y+1] , move])

        if move == "Left":
            bestMove.append([valueMap[x][y-1] , move])

  
    bestMove.sort()
    bestMove = bestMove[::-1]
        
    if last != None:
        for i in range(len(bestMove)):
            if bestMove[i][1] == last:
                del bestMove[i]
                break


    if len(bestMove) == 0:              #no stuckerino
        bestMove.append(0 ,last)

    for val , move in bestMove:
        if move == "Up":           
            if _VARS['cellMAP'][x-1][y] != 1:
                Mover(move)
                last = "Down"
                break

        if move == "Down":
            if _VARS['cellMAP'][x+1][y] != 1:
                Mover(move)
                last = "Up"
                break

        if move == "Right":
            if _VARS['cellMAP'][x][y+1] != 1:
                Mover(move)
                last = "Left"
                break

        if move == "Left":
            if _VARS['cellMAP'][x][y-1] != 1:
                Mover(move)
                last = "Right"
                break
#------------------------------------------------------------------------------------------------------------------------------------------------    
def Facil():
    _VARS = {'cellCount': 15, 'gridSize': 400, 'canvas': False, 'window': False,'playerPos': [0, 0], 'cellMAP': False, 'rowColCount' : 5 , 'falhas' : 15 , 
            'nKeys' : 5 , 'XYreal' : [0,0] , 'drawReal' : [0,0] , 'SpeedMs' : 100, 'AppFont': 'Free Pixel', 'rewardSize': -1, 'actions': [[-1, 0], [1, 0], [0, 1], [0, -1]], 
            'deltas': [], 'gamma': 1}
    return _VARS
#------------------------------------------------------------------------------------------------------------------------------------------------
def Medio():
    _VARS = {'cellCount': 15, 'gridSize': 400, 'canvas': False, 'window': False,'playerPos': [0, 0], 'cellMAP': False, 'rowColCount' : 10 , 'falhas' : 15 , 
            'nKeys' : 10 , 'XYreal' : [0,0] , 'drawReal' : [0,0] , 'SpeedMs' : 100, 'AppFont': 'Free Pixel', 'rewardSize': -1, 'actions': [[-1, 0], [1, 0], [0, 1], [0, -1]], 
            'deltas': [], 'gamma': 1}
    return _VARS
#------------------------------------------------------------------------------------------------------------------------------------------------
def Dificil():
    _VARS = {'cellCount': 15, 'gridSize': 400, 'canvas': False, 'window': False,'playerPos': [0, 0], 'cellMAP': False, 'rowColCount' : 10 , 'falhas' : 10 , 
            'nKeys' : 10 , 'XYreal' : [0,0] , 'drawReal' : [0,0] , 'SpeedMs' : 100, 'AppFont': 'Free Pixel', 'rewardSize': -1, 'actions': [[-1, 0], [1, 0], [0, 1], [0, -1]], 
            'deltas': [], 'gamma': 1}
    return _VARS
    
#------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        aux = 1

        for i in range(aux):
        
            _VARS = {'cellCount': 15, 'gridSize': 400, 'canvas': False, 'window': False,'playerPos': [0, 0], 'cellMAP': False, 'rowColCount' : 10 , 'falhas' : 10 , 
            'nKeys' : 5 , 'XYreal' : [0,0] , 'drawReal' : [0,0] , 'SpeedMs' : 100, 'AppFont': 'Free Pixel', 'rewardSize': -1, 'actions': [[-1, 0], [1, 0], [0, 1], [0, -1]], 
            'deltas': [], 'gamma': 1}

            sg.theme('DarkGreen5')

            gif = r"C:\Users\david\Desktop\Outros\Imagens\TIA23.gif"

            layout = [[sg.Image(key='-IMAGE-')],
                        [sg.Button('Facil',font=(_VARS['AppFont'],15),button_color='black on green'),sg.Button('Medio',font=(_VARS['AppFont'],15),button_color='black on yellow'),
                        sg.Button('Dificil',font=(_VARS['AppFont'],15),button_color='black on red')],
                    ]
                       
            _VARS['window'] = sg.Window('', layout, resizable=True, finalize=True, return_keyboard_events=True)

            image = _VARS['window']['-IMAGE-']

            while True:
                event, values = _VARS['window'].read(timeout= _VARS['SpeedMs'])

                image.update_animation_no_buffering(gif)

                if event in (None, 'Facil'):
                    _VARS['window'].close()
                    _VARS = Facil()
                    break
                
                if event in (None, 'Medio'):
                    _VARS['window'].close()
                    _VARS = Medio()
                    break
                
                if event in (None, 'Dificil'):
                    _VARS['window'].close()
                    _VARS = Dificil()
                    break

            states = [[i, j] for i in range(_VARS['cellCount']) for j in range(_VARS['cellCount'])]

            terminationStates = [] #key_pos

            last = None

            Legal = ["Up","Down","Right","Left"]
            
            _VARS['cellMAP'] = makeMaze(_VARS['cellCount'], _VARS['cellCount'])
            

            cellSize = _VARS['gridSize']/_VARS['cellCount']
            
            layout = [[sg.Canvas(size=(_VARS['gridSize'], _VARS['gridSize']), background_color='white', key='canvas')],
                [sg.Button('New',font=(_VARS['AppFont'],20)),sg.Exit(font=(_VARS['AppFont'],20))]]

            _VARS['window'] = sg.Window('', layout, resizable=True, finalize=True, return_keyboard_events=True)

            _VARS['canvas'] = _VARS['window']['canvas']

            drawGrid()
            drawCell(_VARS['playerPos'][0], _VARS['playerPos'][1],'darkcyan', 'deepskyblue')
            placeCells()

            valueMap = np.zeros((_VARS['cellCount'], _VARS['cellCount']))

            while True:

                numIterations = 15

                for i in range(numIterations):
                    copyValueMap = np.copy(valueMap)
                    deltaState = []
                    for state in states:
                        weightedRewards = 0
                        for action in _VARS['actions']:
                            finalPosition, reward = actionRewardFunction(state, action)
                            weightedRewards += (1/len(_VARS['actions']))*(reward+(_VARS['gamma']*valueMap[finalPosition[0], finalPosition[1]]))
                        deltaState.append(np.abs(copyValueMap[state[0], state[1]]-weightedRewards))
                        copyValueMap[state[0], state[1]] = weightedRewards
                    _VARS['deltas'].append(deltaState)
                    valueMap = copyValueMap
 
                numIterations = 0

                if valueMap[_VARS['XYreal'][1]][_VARS['XYreal'][0]] == 0:
                        terminationStates.remove([_VARS['XYreal'][1] ,   _VARS['XYreal'][0]])

                ValueCheck()

                _VARS['drawReal'] = cellSize*_VARS['XYreal'][0] , cellSize*_VARS['XYreal'][1]

                event, values = _VARS['window'].read(timeout= _VARS['SpeedMs'])
                
                drawCell(_VARS['drawReal'][0], _VARS['drawReal'][1],'darkcyan', 'deepskyblue')

                if event in (None, 'Exit'):
                    break

                if event in (None, 'New'):
                    break
                    
                if len(terminationStates) == 0:
                    break

        if event in (None, 'Exit'):
                    break
        
        if len(terminationStates) == 0:
                    break
                   
        _VARS['window'].close()