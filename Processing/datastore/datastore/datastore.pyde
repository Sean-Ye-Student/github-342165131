def UpdateLeaderboard():
    global leaderboard
    f = open("leaderboard.txt", "r+")
    leaderboard = []
    #replace with binary search if you want
    lines = f.readlines()
    for s in map(lambda x : x.strip("\n"), lines):
        if len(leaderboard) < 1:
            leaderboard.append(s)
            continue
            
        i = 0
        while True:
            v = int(s.split()[1])
            if i + 1 >= len(leaderboard) or v < int(leaderboard[i + 1].split()[1]):
                a = 1 if i + 1 >= len(leaderboard) and v > int(leaderboard[len(leaderboard) - 1].split()[1]) else 0
                leaderboard = leaderboard[:i + a] + [s] + leaderboard[i + a:]
                break
            i += 1
    leaderboard = leaderboard[::-1]
    f.close()
    
def AddScore(name, score):
    f = open("leaderboard.txt", "a")
    f.write("\n" + name + " " + str(score))
    f.close()
    UpdateLeaderboard()

def setup():
    size(1000, 1000)
    UpdateLeaderboard()

stage = 0
score = 0
space, back, enter, up, down, left, right = 32, 8, 10, 38, 40, 37, 34
start, amount = 0, 3
name = ""
numbers = "0123456789"
def keyReleased():
    global score, stage, name, start
    if keyCode == enter:
        stage = 0 if stage > 1 else stage + 1
        if stage == 2:
            AddScore(name, score)
        return
    
    if keyCode == up:
        start = 0 if start + 1 >= len(leaderboard) else start + 1
    if keyCode == down:
        start = 0 if start - 1 < -len(leaderboard) else start - 1
        
    #if keyCode
    if stage == 0:
            ky = key
            if keyCode == back:
                score = int(score/10)
            elif str(ky) in numbers: #str prevents error with integers (like keyCodes)
                score *= 10
                score += int(ky)
    if stage == 1:
        if keyCode == back:
            name = name[0:len(name) - 1]
        else:
            name += str(key).upper()
    

def draw():
    global score, stage
    background(0)
    textSize(30)
    textAlign(LEFT)
    fill(255)
    for i in range(len(leaderboard)):
        new_index = i + start
        if i + start >= len(leaderboard):

            new_index -= len(leaderboard)
        elif i + start < 0:
            new_index += len(leaderboard)
        text(leaderboard[new_index], 300, 100 + i * 40, 1000, 200 + i * 40)
    
    if stage == 0:
        text("My Score: " + str(score), 0, 0, 1000, 100)
    elif stage == 1:
        text("My Name: " + str(name), 0, 0, 1000, 100)
    else:
        text("Uploaded " + str(name) + " with a score of " + str(score), 0, 0, 1000, 100)
    #print(chr(keyCode), keyCode)
