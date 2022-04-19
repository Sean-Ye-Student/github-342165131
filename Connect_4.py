#Connect 4 game
import colorama
import time
from colorama import Fore
from colorama import Style
from colorama import Back

player_1 = "Unknown"
player_2 = "Unknown"

player_1_icon = "⬤"
player_2_icon = "⬤"

players_turn = 1
player_won = 0

blank_icon = "⬤"

icon_1 = "▮▮▮▮▮▮▮▮▮"
icon_2 = "▮▮▮▮▮▮▮▮▮▮▮"
icon_3 = "▮▮▮▮▮▮▮▮▮▮▮▮▮"
#icon_4 = "▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮"

print(Back.BLUE + Fore.YELLOW + Style.BRIGHT +
      " ▮▮▮▮▮ ▮▮▮▮▮▮  ▮        ▮        ▮▮▮▮    ▮▮▮▮▮     ▮      ▮   ▮")
print(Back.BLUE + Fore.YELLOW + Style.BRIGHT +
      "▮      ▮     ▮ ▮▮▮▮▮▮   ▮▮▮▮▮▮  ▮    ▮  ▮         ▮▮▮▮    ▮   ▮")
print(Back.BLUE + Fore.YELLOW + Style.BRIGHT +
      "▮      ▮     ▮ ▮     ▮  ▮     ▮ ▮▮▮▮▮   ▮          ▮      ▮▮▮▮")
print(Back.BLUE + Fore.YELLOW + Style.BRIGHT +
      "▮      ▮     ▮ ▮     ▮  ▮     ▮  ▮      ▮          ▮          ▮ ")
print(Back.BLUE + Fore.YELLOW + Style.BRIGHT +
      " ▮▮▮▮▮ ▮▮▮▮▮▮  ▮     ▮  ▮     ▮   ▮▮▮▮   ▮▮▮▮▮     ▮          ▮")

error_message = ""

player_1_color = Fore.RED
player_2_color = Fore.YELLOW
green_color = Style.BRIGHT + Fore.GREEN
blank_color = Fore.BLACK
debug_stats = Style.NORMAL + Fore.RESET
error_stats = Style.BRIGHT + Fore.RED
normal_message = Style.NORMAL + Fore.RESET
winner_stats = Style.BRIGHT + Fore.GREEN

# 0 - 7
grid_x = range(1, 8)

# 0 - 6
grid_y = range(1, 7)

grid_status = {}


def create_key(x, y):
    return str(x) + "," + str(y)


#give the first offset cord and the direction
def get__key(key, direction):
    x_str = key[0]
    y_str = key[2]
    x = int(x_str)
    y = int(y_str)

    if direction == "N":
        return create_key(x, y - 1)

    if direction == "NE":
        return create_key(x - 1, y - 1)

    if direction == "E":
        return create_key(x, y - 1)

    if direction == "W":
        return create_key(x + 1, y)

    if direction == "NW":
        return create_key(x + 1, y + 1)


#create the grid
for x in grid_x:
    for y in grid_y:
        key = create_key(x, y)
        grid_status[key] = 0


def valid_column(string_num):
    for x in grid_x:
        if str(x) == str(string_num):
            return True


def add_coin(column, player):
    x = column
    for y in grid_y:
        target_y = y
        if grid_status[create_key(x, target_y)] == 0:
            grid_status[create_key(x, target_y)] = player
            return True


def are_all_same(valuelist):
    first_value = valuelist[0]
    for i in valuelist:
        #print(debug_stats + str(i) + " " + str(first_value))
        if i != first_value:
            return False

    return first_value


def replace_direction(dir_array):
    new = dir_array
    for i in range(0, len(dir_array)):
        key_value = grid_status.get(new[i], 0)
        new[i] = key_value

    return new


def four_row(x, y):
    #Must specify that we are using a global variable when using a function
    global player_won
    global grid_status

    N = [
        create_key(x, y),
        create_key(x, y + 1),
        create_key(x, y + 2),
        create_key(x, y + 3)
    ]
    NE = [
        create_key(x, y),
        create_key(x + 1, y + 1),
        create_key(x + 2, y + 2),
        create_key(x + 3, y + 3)
    ]
    E = [
        create_key(x, y),
        create_key(x + 1, y),
        create_key(x + 2, y),
        create_key(x + 3, y)
    ]
    W = [
        create_key(x, y),
        create_key(x - 1, y),
        create_key(x - 2, y),
        create_key(x - 3, y)
    ]
    NW = [
        create_key(x, y),
        create_key(x - 1, y + 1),
        create_key(x - 2, y + 2),
        create_key(x - 3, y + 3)
    ]

    #when sending dictionaries it refers
    #using dict creates a copy
    Nvalue = replace_direction(N.copy())
    NEvalue = replace_direction(NE.copy())
    Evalue = replace_direction(E.copy())
    Wvalue = replace_direction(W.copy())
    NWvalue = replace_direction(NW.copy())

    N_state = are_all_same(Nvalue)
    if N_state != False:
        #also set the  cord to be green
        for n in N:
            grid_status[n] = "G"

        player_won = N_state

    NE_state = are_all_same(NEvalue)
    if NE_state != False:
        #also set the  cord to be green

        for ne in NE:
            grid_status[ne] = "G"

        player_won = NE_state

    E_state = are_all_same(Evalue)
    if E_state != False:
        #also set the  cord to be green

        for e in E:
            grid_status[e] = "G"

        player_won = E_state

    W_state = are_all_same(Wvalue)
    if W_state != False:
        #also set the  cord to be green

        for w in W:
            grid_status[w] = "G"
        player_won = W_state

    NW_state = are_all_same(NWvalue)
    if NW_state != False:
        #also set the  cord to be green

        for nw in NW:
            grid_status[nw] = "G"

        player_won = NW_state


def check_for_four_row():
    for x in grid_x:
        for y in grid_y:
            if player_won == 0:
                four_row(x, y)
            else:
                break
        if player_won != 0:
            break


def refresh_data():
    global player_won
    global players_turn
    global grid_status

    player_won = 0
    players_turn = 1
    for i in grid_status:
        grid_status[i] = 0


def display_grid():
    print_col = Style.NORMAL + Fore.RESET + ""

    for x in grid_x:
        print_col = print_col + str(x) + "               "

    print("        " + print_col)
    for y in grid_y:
        value_array = []
        print_row = ["" for i in range(8)]

        for x in grid_x:
            key = create_key(x, max(grid_y) - y + 1)
            value_array.append(grid_status[key])

        for value in value_array:
            print_value = ["" for i in range(8)]

            if str(value) == "1":
                print_value[0] = Style.NORMAL + player_1_color + icon_1
                print_value[1] = Style.NORMAL + player_1_color + icon_2
                print_value[2] = Style.NORMAL + player_1_color + icon_3
                print_value[3] = Style.NORMAL + player_1_color + icon_3
                print_value[4] = Style.NORMAL + player_1_color + icon_3
                print_value[5] = Style.NORMAL + player_1_color + icon_2
                print_value[6] = Style.NORMAL + player_1_color + icon_1
            elif str(value) == "2":
                print_value[0] = Style.NORMAL + player_2_color + icon_1
                print_value[1] = Style.NORMAL + player_2_color + icon_2
                print_value[2] = Style.NORMAL + player_2_color + icon_3
                print_value[3] = Style.NORMAL + player_2_color + icon_3
                print_value[4] = Style.NORMAL + player_2_color + icon_3
                print_value[5] = Style.NORMAL + player_2_color + icon_2
                print_value[6] = Style.NORMAL + player_2_color + icon_1
            elif str(value) == "G":
                print_value[0] = Style.NORMAL + green_color + icon_1
                print_value[1] = Style.NORMAL + green_color + icon_2
                print_value[2] = Style.NORMAL + green_color + icon_3
                print_value[3] = Style.NORMAL + green_color + icon_3
                print_value[4] = Style.NORMAL + green_color + icon_3
                print_value[5] = Style.NORMAL + green_color + icon_2
                print_value[6] = Style.NORMAL + green_color + icon_1
            else:
                print_value[0] = Style.DIM + blank_color + icon_1
                print_value[1] = Style.DIM + blank_color + icon_2
                print_value[2] = Style.DIM + blank_color + icon_3
                print_value[3] = Style.DIM + blank_color + icon_3
                print_value[4] = Style.DIM + blank_color + icon_3
                print_value[5] = Style.DIM + blank_color + icon_2
                print_value[6] = Style.DIM + blank_color + icon_1

            print_row[0] = print_row[0] + "   " + print_value[0] + "    "
            print_row[1] = print_row[1] + "  " + print_value[1] + "   "
            print_row[2] = print_row[2] + " " + print_value[2] + "  "
            print_row[3] = print_row[3] + " " + print_value[3] + "  "
            print_row[4] = print_row[4] + " " + print_value[4] + "  "
            print_row[5] = print_row[5] + "  " + print_value[5] + "   "
            print_row[6] = print_row[6] + "   " + print_value[6] + "    "

        for i in print_row:
            print(Back.BLUE + i)
            time.sleep(0.005)

        print(Back.RESET + "")


#print the grid
#for key, value in grid_status.items():
#print("key > " + key)
#print("value >" + str(value))

while True:
    name1_input = input("Player 1 name is? > ")
    name2_input = input("Player 2 name is? > ")
    for i in range(0, 300):
        print("")
    print("Player 1: " + name1_input)
    print("Player 2: " + name2_input)
    correct = input("Are these names correct? y/n")
    if correct == "y":
        player_1 = name1_input
        player_2 = name2_input
        break
    for i in range(0, 300):
        print("")

while True:
    for i in range(0, 300):
        print("")

    check_for_four_row()
    display_grid()

    if player_won == "G":
        print("player_won is G for some resion")

    if player_won == 1:
        print(winner_stats + player_1 + " is the WINNER!")

    if player_won == 2:
        print(winner_stats + player_2 + " is the WINNER!")

    #Refresh data
    if player_won != 0:
        input(normal_message + "Press Enter to replay!")
        refresh_data()
        print(debug_stats + str(players_turn))
        #after resetting display a new board
        for i in range(0, 300):
            print("")
        display_grid()

    #check if the grid is full after the player winning has been considered
    #adding the items methord allows you to get the key and it's value
    all_slots_filled = True
    for key, value in grid_status.items():
        if value == 0:
            all_slots_filled = False
            break

    if all_slots_filled == True:
        #all slots are filled
        print(winner_stats + "Tie")
        input(normal_message + "Type anything to replay!")
        refresh_data()
        #after resetting display a new board
        for i in range(0, 300):
            print("")

        display_grid()

    #prints the current error message
    if (error_message == "") == False:
        print(error_message)
        error_message = ""
        player_name = ""

    if players_turn == 1:
        player_name = player_1
    else:
        player_name = player_2

    drop_column_input = input(
        normal_message + player_name +
        " which column would you like to drop your coin into? > ")

    if valid_column(drop_column_input) == True:
        current_x = int(drop_column_input)
        if add_coin(current_x, players_turn) == True:

            #changes the current players turn
            if players_turn == 1:
                players_turn = 2
            else:
                players_turn = 1

        else:
            error_message = error_stats + "Cannot add coin to column " + str(
                current_x)

    else:
        error_message = error_stats + drop_column_input + " was not a valid column"
