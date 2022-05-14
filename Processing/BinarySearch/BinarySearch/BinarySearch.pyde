import random
load = 20
numbers = [random.randint(100, 999) for i in range(load)]
in_order = [-1, 1000] #No numbers can exceed these ranges
def setup():
    size(1000, 125)

s_index = 0 #Usedto run binary search, draw is treated as a while loop
e_index = len(in_order) - 1
c_index = int((e_index - s_index)/2) + s_index
def draw():
    global numbers, in_order, s_index, e_index, c_index
    delay(1000)
    background(255)
    textSize(10)
    fill(0,0,0)
    s = ""
    for number in numbers:
        padding = int((13-len(str(number)))/2)
        s += str(" " * padding + str(number) + " " * padding )
    text(s, 0, 50, 0)

    
    s = ""
    for number in in_order:
        padding = int((13-len(str(number)))/2)
        s += str(" " * padding + str(number) + " " * padding )
    text(s, 0, 100, 0)        
    if len(numbers) < 1: #Above is visualizing the numbers
        return #Below is visualizing the indexes and running binary search
    offset = -10
    fill(255, 255, 0)
    rect(s_index * 50 + offset, 100, 50, 25)
    rect(e_index * 50 + offset, 100, 50, 25)
    fill(0, 255, 255)
    rect((c_index * 50 + offset + (25 if c_index == s_index else 0)), 100, 50, 25)
    
    x = numbers[0]
    if e_index - s_index <= 1 or x == in_order[c_index]:
        numbers.pop(0)
        in_order = in_order[:c_index + 1] + [x] + in_order[c_index + 1:]
        s_index = 0
        e_index = len(in_order) - 1
        return
    if x < in_order[c_index]:
        e_index = c_index
    elif x > in_order[c_index]:
        s_index = c_index
    c_index = int((e_index - s_index)/2) + s_index
