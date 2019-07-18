import argparse
import json
import os
import random
from random import choice


command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0
jangan_ngulang = 0

current_map_PDF = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                   ]

current_map_status = [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]
                      ]

ship_target = [False, False, False, False, False]  # ship_length = 5,4,3,3,2
ship_length_global = [5, 4, 3, 3, 2]
current_ship_target_index = 3
max_length = 10  # panjang maksimal row/column
target_descending = True

# kayaknya ini gak perlu deh, karena program di run ulang setiap turn
def resetPDF():
    global current_map_PDF
    global current_map_status

    for i in range(max_length):
        for j in range(max_length):
            current_map_PDF[i][j] = 0
            current_map_status[i][j] = "~"


def isShipSank():
    global current_ship_target_index
    global target_descending

    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)

    submarine = state['OpponentMap']['Ships'][0]
    destroyer = state['OpponentMap']['Ships'][1]
    battleship = state['OpponentMap']['Ships'][2]
    carrier = state['OpponentMap']['Ships'][3]
    cruiser = state['OpponentMap']['Ships'][4]

    # if target_descending:
    #     if destroyer['Destroyed']:
    #         current_ship_target_index = 3
    #         if submarine['Destroyed'] or cruiser['Destroyed']:
    #             current_ship_target_index = 2
    #             if submarine['Destroyed'] and cruiser['Destroyed']:
    #                 current_ship_target_index = 1
    #                 if battleship['Destroyed']:
    #                     current_ship_target_index = 0
    # else:
    #     if carrier['Destroyed']:
    #         current_ship_target_index = 1
    #         if battleship['Destroyed']:
    #             current_ship_target_index = 2
    #             if submarine['Destroyed'] or cruiser['Destroyed']:
    #                 current_ship_target_index = 3
    #                 if submarine['Destroyed'] and cruiser['Destroyed']:
    #                     current_ship_target_index = 4
    if carrier['Destroyed']:
        current_ship_target_index = 1
    if battleship['Destroyed']:
        current_ship_target_index = 2
    if submarine['Destroyed'] or cruiser['Destroyed']:
        current_ship_target_index = 3
    if submarine['Destroyed'] and cruiser['Destroyed']:
        current_ship_target_index = 4


def isvalidCoor(X, Y):
    global max_length
    return X >= 0 and X < max_length and Y >= 0 and Y < max_length

def calculatePDF():
    global current_map_status
    global current_map_PDF
    global max_length
    global current_ship_target_index
    global ship_length_global

    ship_length = ship_length_global[current_ship_target_index]

    # cek horizontal
    for i in range(max_length):
        for j in range(max_length - ship_length):
            isHit = 1
            isMiss = False
            for k in range(ship_length):
                if current_map_status[i][j+k] == "!":
                    isMiss = True
                    break
            if isMiss == False:
                for k in range(ship_length):
                    if current_map_status[i][j+k] == "*":
                        adder = ship_length
                        for l in range(k+1,ship_length):
                            if isvalidCoor(i, j+l):
                                current_map_PDF[i][j+l] += adder
                                adder -= 1
                        adder = ship_length
                        for l in range(k-1,-1,-1):
                            if isvalidCoor(i, j+l):
                                current_map_PDF[i][j+l] += adder
                                adder -= 1
                for k in range(ship_length):
                    if current_map_status[i][j+k] == "*" or current_map_status[i][j+k] == "!":
                        current_map_PDF[i][j+k] = 0
                    else:
                        current_map_PDF[i][j+k] += isHit

    # cek vertikal
    for i in range(max_length - ship_length):
        for j in range(max_length):
            isHit = 1
            isMiss = False
            for k in range(ship_length):
                if current_map_status[i+k][j] == "!":
                    isMiss = True
                    break
            if isMiss == False:
                for k in range(ship_length):
                    if current_map_status[i+k][j] == "*":
                        adder = ship_length
                        for l in range(k+1,ship_length):
                            if isvalidCoor(i+l, j):
                                current_map_PDF[i+l][j] += adder
                                adder -= 1
                        adder = ship_length
                        for l in range(k-1,-1,-1):
                            if isvalidCoor(i+l, j):
                                current_map_PDF[i+l][j] += adder
                                adder -= 1
                for k in range(ship_length):
                    if current_map_status[i+k][j] == "*" or current_map_status[i+k][j] == "!":
                        current_map_PDF[i+k][j] = 0
                    else:
                        current_map_PDF[i+k][j] += isHit


def choicePDF():
    global current_map_PDF
    global max_length
    global jangan_ngulang
    max_value = 0
    max_index = [0, 0]

    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)

#    targets = []
    counter_i = 0
    current_map = state['OpponentMap']['Cells']
#    for cell in current_map:
#        if not cell['Damaged'] and not cell['Missed']:
#            valid_cell = cell['X'], cell['Y']
#            targets.append(valid_cell)

    for i in range(max_length):
        for j in range(max_length):
            if current_map_PDF[i][j] > max_value:
                max_value = current_map_PDF[i][j]
                max_index[0] = i
                max_index[1] = j
                
    # coba implementasi random choice jika max_value ada lebih dari 1 index
    max_index_arr = []
    for i in range(max_length):
        for j in range(max_length):
            if current_map_PDF[i][j] == max_value:
                max_index_arr.append([i, j])
            counter_i+=1

    #print("MAX_INDEX_ARR =", max_index_arr)
    max_index = choice(max_index_arr)
    print("INDEX TEMBAK ROW-COLUMN", max_index)

    # ubah koordinat row-column jadi kartesian
    # (i,j) = (1,2) -> (x,y) = (2, 8)
    # x = j, i+y = max_length-1
    y = (max_length - 1) - max_index[0]
    x = max_index[1]
    max_index[0] = x
    max_index[1] = y
    
    
    print("INDEX TEMBAK CARTESIAN", max_index)
    return tuple(max_index)


def hunt():
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)

    targets = []
    current_map = state['OpponentMap']['Cells']
    for cell in current_map:
        if not cell['Damaged'] and not cell['Missed']:
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)

    return choice(targets)


def best_movement():
    counter = 0
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    shield = state['PlayerMap']['Owner']['Shield']['CurrentCharges']
    energy = state['PlayerMap']['Owner']['Energy']
    submarine = state['PlayerMap']['Owner']['Ships'][0]
    destroyer = state['PlayerMap']['Owner']['Ships'][1]
    battleship = state['PlayerMap']['Owner']['Ships'][2]
    carrier = state['PlayerMap']['Owner']['Ships'][3]
    cruiser = state['PlayerMap']['Owner']['Ships'][4]

    if submarine['Destroyed']:
        counter = counter + 1
    if cruiser['Destroyed']:
        counter = counter + 1
    if battleship['Destroyed']:
        counter = counter + 1
    if carrier['Destroyed']:
        counter = counter + 1
    if destroyer['Destroyed']:
        counter = counter + 1
    if shield > 6:
        counter = counter + 1

    if counter == 5:
        if not submarine['Destroyed']:
            if submarine['Cells'][0]['Hit']:
                counter = counter + 1
            elif submarine['Cells'][1]['Hit']:
                counter = counter + 1
            elif submarine['Cells'][2]['Hit']:
                counter = counter + 1
        if not destroyer['Destroyed']:
            if destroyer['Cells'][0]['Hit']:
                counter = counter + 1
            elif destroyer['Cells'][1]['Hit']:
                counter = counter + 1
        if not battleship['Destroyed']:
            if battleship['Cells'][0]['Hit']:
                counter = counter + 1
            elif battleship['Cells'][1]['Hit']:
                counter = counter + 1
            elif battleship['Cells'][2]['Hit']:
                counter = counter + 1
            elif battleship['Cells'][3]['Hit']:
                counter = counter + 1
        if not carrier['Destroyed']:
            if carrier['Cells'][0]['Hit']:
                counter = counter + 1
            elif carrier['Cells'][1]['Hit']:
                counter = counter + 1
            elif carrier['Cells'][2]['Hit']:
                counter = counter + 1
            elif carrier['Cells'][3]['Hit']:
                counter = counter + 1
            elif carrier['Cells'][4]['Hit']:
                counter = counter + 1
        if not cruiser['Destroyed']:
            if cruiser['Cells'][0]['Hit']:
                counter = counter + 1
            elif cruiser['Cells'][1]['Hit']:
                counter = counter + 1
            elif cruiser['Cells'][2]['Hit']:
                counter = counter + 1
                
    if counter > 5 and not state['PlayerMap']['Owner']['Shield']['Active']:
        return 8
    
    elif energy > 36 and not battleship['Destroyed'] :
        return 5
    
    elif energy > 30 and not carrier['Destroyed'] and battleship['Destroyed']:
        return 4
    
    elif energy > 42 and not cruiser['Destroyed'] and carrier['Destroyed'] and battleship['Destroyed'] :
        return 6
    
    elif energy > 36 and not submarine['Destroyed'] and cruiser['Destroyed'] and carrier['Destroyed'] and battleship['Destroyed']:
        return 7
    
    elif energy > 24 and not destroyer['Destroyed'] and submarine['Destroyed'] and cruiser['Destroyed'] and carrier['Destroyed'] and battleship['Destroyed']:
        return choice([2,3])

    else:
        return 1
     

def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(state['OpponentMap']['Cells'])


def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    ships = ['Battleship 4 1 West',
             'Carrier 4 8 East',
             'Cruiser 0 4 North',
             'Destroyer 6 6 West',
             'Submarine 2 6 North'
             ]

    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)

    global current_map_status
    global max_length
    global current_ship_target_index
    global current_map_PDF

    resetPDF()
    isShipSank()

    for cell in opponent_map:
        # cek semua kondisi map sekarang
        if cell['Damaged']:
            j = cell['X']
            i = max_length - 1 - cell['Y']
            current_map_status[i][j] = "*"
        elif cell['Missed']:
            j = cell['X']
            i = max_length - 1 - cell['Y']
            current_map_status[i][j] = "!"
        else:
            j = cell['X']
            i = max_length - 1 - cell['Y']
            current_map_status[i][j] = "~"

    calculatePDF()
    target = choicePDF()

    print("TARGET = ", target)
    #print("Current ship length target = ", ship_length_global[current_ship_target_index])
    for i in range(10):
        for j in range(10):
            print(current_map_PDF[i][j], end =" ")
        print()
    
    for i in range(10):
        for j in range(10):
            print(current_map_status[i][j], end =" ")
        print()
    #print("\n\n")

    output_shot(*target)
    return


def output_shot(x, y):
    move = best_movement()  # 1=fire shot command code
    if move == 8:
        use_shield()
    else:
        print("MOVE = ",move)
        with open(os.path.join(output_path, command_file), 'w') as f_out:
            f_out.write('{},{},{}'.format(move, x, y))
            f_out.write('\n')
    pass

def use_shield():
    targets = []
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)

    submarine = state['PlayerMap']['Owner']['Ships'][0]
    destroyer = state['PlayerMap']['Owner']['Ships'][1]
    battleship = state['PlayerMap']['Owner']['Ships'][2]
    carrier = state['PlayerMap']['Owner']['Ships'][3]
    cruiser = state['PlayerMap']['Owner']['Ships'][4]

    if not submarine['Destroyed']:
        targets = submarine['Cells'][1]['X'], submarine['Cells'][1]['Y']
    if not destroyer['Destroyed']:
        targets = destroyer['Cells'][1]['X'], destroyer['Cells'][1]['Y']
    if not battleship['Destroyed']:
        targets = battleship['Cells'][2]['X'], battleship['Cells'][2]['Y']
    if not carrier['Destroyed']:
        targets = carrier['Cells'][2]['X'], carrier['Cells'][2]['Y']
    if not cruiser['Destroyed']:
        targets = cruiser['Cells'][1]['X'], cruiser['Cells'][1]['Y']
    
    output_shield(*targets)
    return

def output_shield(x,y):
    move = best_movement()  # 1=fire shot command code
    print("MOVE = ", move)
    with open(os.path.join(output_path, command_file), 'w') as f_out:
            f_out.write('{},{},{}'.format(move, x, y))
            f_out.write('\n')
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?',
                        help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(
    ), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
