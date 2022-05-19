import time
import random
rows = list([{"Plants" : [None for ii in range(9)], "Zombies" : []} for i in range(6)])
column_pos = (80,183,279,385,467, 573) #The borders between rows from the very top to the very bottom
row_pos = (251, 334, 408, 493, 576, 654, 738, 812, 898, 987) #The borders between columns from the very left to the very right
spawn_pos_x = 1027

zombies = {
           "Basic" : {"rect" : {
        "fill" : {"r" : 121, "g" : 135, "b" : 102,"a" : 255},
        "stroke" :{"r" : 255, "g" : 255, "b" : 255, "a" : 255},
        "weight" : 0,
        "pos" : {"x" : spawn_pos_x, "y" : 0},
        "size" : {"x" : 50, "y" : 100}},
           "Settings" : {
                         "offset" : {"x" : 0, "y" : -15},
                         "speed" : 20,
                         "last_moved" : time.time(),
                         "last_attacked" : time.time(),
                         "blocked" : False,
                         "dps" : 1,
                         }
           
           }
           
           }

plants = {
          "Wallnut" : {"rect" : {
        "fill" : {"r" : 210, "g" : 171, "b" : 57,"a" : 255},
        "stroke" :{"r" : 255, "g" : 255, "b" : 255, "a" : 255},
        "weight" : 0,
        "pos" : {"x" : 0, "y" : 0},
        "size" : {"x" : 50, "y" : 50}},
           "Settings" : {
                         "offset" : {"x" : -15, "y" : -15},
                         "health" : 5
                         }
          }
}
           
           
rect_kys = ("fill", "weight", "pos", "size", "stroke")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
def RENDERRECT(object, enabled_keys):
    global objects
    re = object["rect"]
    f, w, p, s, st,  = map(None, (re[ky] if ky in enabled_keys else None for ky in rect_kys))
    strokeWeight(w if w != None else 1)
    fill(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), fallback(f, "a", 255)) 
    stroke(fallback(st, "r", 255), fallback(st, "g", 255), fallback(st, "b", 255), fallback(st, "a", 255))
    rect(fallback(p, "x", 0), fallback(p, "y", 0), fallback(s, "x", 0), fallback(s, "y", 0))

types = (type([]), type({}))
def copycollection(coll):
    is_list, is_dict = type(coll) == types[0], type(coll) == types[1]
    n = [] if is_list else ({} if is_dict else None)
    if n == None:
        return coll
    if is_list:
        for i in range(len(coll)):
            n[i] = copycollection(coll[i])
    elif is_dict:
        for ky in coll.keys():
            n[ky] = copycollection(coll[ky])

    return n
can_place = lambda x, y: rows[y]["Plants"][x] == None
def Spawn(object, row, column, is_zombie):
    new = copycollection(object)
    if is_zombie:
        new["Settings"]["last_moved"] = time.time()
        rows[row]["Zombies"].append(new)
    else:
        rows[row]["Plants"][column] = new

def GetLocation(ax, ay):
    for y, y_pos in enumerate(column_pos):
        for x, x_pos in enumerate(row_pos):
            if y + 1 == len(column_pos) or x + 1 == len(row_pos):
                break
            if x_pos <= ax < row_pos[x + 1] and y_pos <= ay < column_pos[y + 1]:
                return x, y
    return None, None
def setup():
    size(1000, 600)
cooldown = time.time()+1
def draw():    
    global rows, cooldown
    if time.time() >= cooldown:        
        Spawn(zombies["Basic"], random.randint(0,4), None, True)
        cooldown = time.time() + 1
    if mousePressed:
        print(mouseX, mouseY)
    copy(loadImage("Lawn.png"), 0, 0, 1400, 600, 0, 0, 1400, 600)
    for i, row in enumerate(rows):
        for ii, zombie in enumerate(row["Zombies"]):    
            settingz = zombie["Settings"]
            rezt = zombie["rect"]
            zombie["rect"]["pos"]["y"] = column_pos[i + 1] + settingz["offset"]["y"] - rezt["size"]["y"]
            elapsed = time.time() - settingz["last_moved"]
            zombie["Settings"]["last_moved"] = time.time()
            #maybe add some blocking logic for wallnuts
            x, y = GetLocation(zombie["rect"]["pos"]["x"], zombie["rect"]["pos"]["y"] + zombie["rect"]["size"]["y"]/2)
            target_plant = rows[y]["Plants"][x] if x != None and y != None else None
            settingz["blocked"] = True if target_plant != None else False
            if not(settingz["blocked"]):
                zombie["rect"]["pos"]["x"] -= settingz["speed"] * elapsed
            
            if target_plant:
                target_plant["Settings"]["health"] -= (time.time() - settingz["last_attacked"]) * settingz["dps"]
                if target_plant["Settings"]["health"] <= 0:
                    rows[y]["Plants"][x] = None
            settingz["last_attacked"] = time.time()
            RENDERRECT(zombie, ("fill", "weight", "pos", "size", "stroke"))
            
            
        for ii, plant in enumerate(row["Plants"]):
            if not(plant):
                continue
            settingp = plant["Settings"]
            rept = plant["rect"]
            rows[i]["Plants"][ii]["rect"]["pos"]["y"] = column_pos[i + 1] + settingp["offset"]["y"] - rept["size"]["y"]
            rows[i]["Plants"][ii]["rect"]["pos"]["x"] = row_pos[ii+1] + settingp["offset"]["x"] - rept["size"]["x"]
            RENDERRECT(plant, ("fill", "weight", "pos", "size", "stroke"))
    noStroke()
    for y, y_pos in enumerate(column_pos):
        for x, x_pos in enumerate(row_pos):
            if y + 1 == len(column_pos) or x + 1 == len(row_pos):
                break
            if x_pos <= mouseX < row_pos[x + 1] and y_pos <= mouseY <  column_pos[y + 1]:
                fill(255, 255, 255, 125)
                if mousePressed and mouseButton == LEFT and can_place(x, y):
                    Spawn(plants["Wallnut"], y, x, False)
                    print(len(plants))
            else:
                fill(255, 0,0,10)
            rect(x_pos, y_pos, row_pos[x + 1] - row_pos[x], column_pos[y + 1] - column_pos[y])
