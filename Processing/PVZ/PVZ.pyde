import time
rows = list([{"Plants" : [], "Zombies" : []} for i in range(5)])
column_pos = (166,266,372, 456, 560)
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
                         "blocked" : False
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
def DuplicateCollection(original, ky=None): #probably iwll not work
    if not(ky):
        new = [] if type(original) == types[0] else ({} if type(original) == types[1] else None)
        if not(new):
            return
        if type(new) == types[0]: #list
            for i in range(len(original)):
                new.append(DuplicateCollection(original[i]))
            
        else: #dictionary
            for ky in original.keys():
                new[ky] = DuplicateCollection(original[ky])
                
        return new

def setup():
    size(1024, 626)

def draw():
    global rows
    rows[0]["Zombies"].append()
    print(rows[0]["Zombies"][0]["rect"]["pos"], zombies["Basic"]["rect"]["pos"])
    image(loadImage("Lawn.png"), 0, 0, width, height)
    for i, row in enumerate(rows):
        for ii, zombie in enumerate(row["Zombies"]):    
            settingz = zombie["Settings"]
            rezt = zombie["rect"]
            rows[i]["Zombies"][ii]["rect"]["pos"]["y"] = column_pos[i] + settingz["offset"]["y"] - rezt["size"]["y"]
            elapsed = time.time() - settingz["last_moved"]
            zombie["Settings"]["last_moved"] = time.time()
            
            #maybe add some blocking logic for wallnuts
             
            zombie["Settings"]["blocked"] = True if mousePressed else False
            if not(settingz["blocked"]):
                zombie["rect"]["pos"]["x"] -= settingz["speed"] * elapsed
            RENDERRECT(zombie, ("fill", "weight", "pos", "size", "stroke"))
