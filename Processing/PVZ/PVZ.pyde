import time
add_library("minim")
import random
rows = list([{"Plants" : [None for ii in range(9)], "Zombies" : []} for i in range(6)])
column_pos = (80,183,279,385,467, 573) #The borders between rows from the very top to the very bottom
row_pos = (251, 334, 408, 493, 576, 654, 738, 812, 898, 987) #The borders between columns from the very left to the very right
spawn_pos_x = 1027

zombies = {"Football" : {"image" : {"size" : {"x" : 154, "y" : 160}, "pos" : {"x" : spawn_pos_x, "y" : 0}, "fill" : {"r" : 255, "g" : 255, "b" : 255, "a" : 255},"animation" : {"file_index" : "zombies/football/(", "file_type" : ").png", "start" : 0,"total_frames" : 11, "frame_duration" : 0.09}}, "Settings" : {"offset" : {"x" : 50, "y" : 0}, "speed" : 40, "last_moved" : time.time(), "last_attacked" : time.time(), "blocked" : False, "dps" : 3}},
           "Dancer" : {"image" : {
                                    "size" : {"x" : 331, "y" : 498}, 
                                    "pos" : {"x" : spawn_pos_x, "y" : 0}, 
                                    "fill" : {"r" : 255, "g" : 255, "b" : 255, "a" : 255},
                                    "animation" : {"file_index" : "zombies/dancer/(", 
                                                   "file_type" : ").png", 
                                                   "start" : 0,
                                                   "total_frames" : 34, 
                                                   "frame_duration" : 0.1}}, 
            "Settings" : {"offset" : {"x" : 0, "y" : 0}, 
                          "speed" : 15, 
                          "last_moved" : time.time(), 
                          "last_attacked" : time.time(), 
                          "blocked" : False, 
                          "dps" : 1}}
           
           
           
           }
plants = {"Wallnut" : {"image" : {"size" : {"x" : 148, "y" : 125},"pos" : {"x" : 0, "y" : 0},"fill" : {"r" : 255, "g" : 255, "b" : 255, "a" : 255}, "animation" : {"file_index" : "plants/wallnut/(", "file_type" : ").png","start" : 0,"total_frames" : 17, "frame_duration" : 0.08}}, "Settings" : {"offset" : {"x" : 25, "y" : 0}, "health" : 5}}}    
sounds = {"intro" : {"minim" : "The_Zombies_Are_Coming.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : True, "group" : 0}, "menu" : {"minim" : "Crazy Dave Intro Theme.mp3", "repeat" : -1, "play_from_start" : True, "isolate" : True,"group" : 0}, "game" : {"minim" : "Grasswalk (In-Game).mp3", "repeat" : -1, "play_from_start" : True, "isolate" : True, "group" : 0}}
           
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


sound_kys = ("minim", "repeat", "play_from_start", "isolate", "group")
def PlaySound(sound_name, enabled_keys):
    if not(sound_name in sounds.keys()):
        return
    sound = sounds[sound_name]
    m, repeat, play_from_start, isolate, group = map(None, (sound[ky] if ky in enabled_keys else None for ky in sound_kys))
    if m == None:
        return
    if isolate == True:
        for ky in sounds:
            if ky == sound_name:
                continue
            same_group = True if "group" in sounds[ky].keys() and sounds[ky]["group"] == group else False
            if same_group:
                sounds[ky]["minim"].pause()
    if m.isPlaying() == False:
        if play_from_start == True:
            m.rewind()
        if repeat == -1:
            m.loop()
        else:
            m.play()

img_kys = ("name", "size", "pos", "fill", "animation")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
def RENDERIMAGE(object, enabled_keys): #object is a dictionary, enabled_keys is a tuple storing all the keys that are in the object (assumed to be there)
    img = object["image"]
    img_name, img_size, pos, f, anim = map(None, (img[ky] if ky in enabled_keys else None for ky in img_kys))
    if anim != None:
        fd, tf = anim["frame_duration"], anim["total_frames"], 
        elapsed = (time.time() - anim["start"]) % (tf * fd) if tf * fd > 0 else 1
        img_name = anim["file_index"] + str(int(elapsed/fd if fd > 0 else 1)) + anim["file_type"]
        
    if img_name == None:
        return
    print(img_name)
    tint(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), fallback(f, "a", 255))
    image(loadImage(img_name), fallback(pos, "x", 0), fallback(pos, "y", 0), fallback(img_size, "x", 100), fallback(img_size, "y", 100))   


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
    minim = Minim(this)
    for ky in sounds:
        sounds[ky]["minim"] = minim.loadFile("sounds/" + sounds[ky]["minim"])
    PlaySound("intro", ("minim", "repeat", "play_from_start", "isolate", "group"))
cooldown = time.time()+1
start_music = time.time() + 4
def draw():    
    global rows, cooldown
    if time.time() >= cooldown:        
        Spawn(zombies["Football"], random.randint(0,4), None, True)
        cooldown = time.time() + 1
        
    if start_music <= time.time():    # if mousePressed:
        PlaySound("game", ("minim", "repeat", "play_from_start", "isolate", "group"))    #     print(mouseX, mouseY)

    copy(loadImage("Lawn.png"), 0, 0, 1400, 600, 0, 0, 1400, 600)
    x, y = GetLocation(mouseX, mouseY)
    if x != None and y != None:
        noStroke()
        fill(255, 255, 255, 125)
        rect(row_pos[x], column_pos[y], row_pos[x + 1] - row_pos[x], column_pos[y + 1] - column_pos[y])
        
        if mousePressed and mouseButton == LEFT and can_place(x, y):
            Spawn(plants["Wallnut"], y, x, False)
    for i, row in enumerate(rows):
        for ii, plant in enumerate(row["Plants"]):
            if not(plant):
                continue
            settingp, imagp  = plant["Settings"], plant["image"]
            imagp["pos"]["y"] = column_pos[i + 1] + settingp["offset"]["y"] - imagp["size"]["y"]
            imagp["pos"]["x"] = row_pos[ii+1] + settingp["offset"]["x"] - imagp["size"]["x"]
            RENDERIMAGE(plant, ("animation", "pos", "size", "fill"))
            
        for ii, zombie in enumerate(row["Zombies"]):    
            settingz, imagz = zombie["Settings"], zombie["image"]
            imagz["pos"]["y"] = column_pos[i + 1] + settingz["offset"]["y"] - imagz["size"]["y"]
            elapsed = time.time() - settingz["last_moved"]
            zombie["Settings"]["last_moved"] = time.time()
            x, y = GetLocation(imagz["pos"]["x"] + settingz["offset"]["x"], imagz["pos"]["y"] + imagz["size"]["y"]/2) #x + 1 so the zombie target plants infront and in the current tile
            target_plant = rows[y]["Plants"][x] if x != None and y != None else (rows[y]["Plants"][x + 1] if x != None and y != None and x + 1 < len(rows[y]["Plants"][x]) else None)
            settingz["blocked"] = True if target_plant != None else False
            if not(settingz["blocked"]):
                imagz["pos"]["x"] -= settingz["speed"] * elapsed        
            imagz["animation"]["file_index"] =  "zombies/football/(" if not(settingz["blocked"]) else "zombies/footballeat/("
            
            if target_plant != None:
                target_plant["Settings"]["health"] -= (time.time() - settingz["last_attacked"]) * settingz["dps"]
                if target_plant["Settings"]["health"] <= 0:
                    rows[y]["Plants"][x] = None
            settingz["last_attacked"] = time.time()
            RENDERIMAGE(zombie, ("animation", "pos", "size", "fill"))
