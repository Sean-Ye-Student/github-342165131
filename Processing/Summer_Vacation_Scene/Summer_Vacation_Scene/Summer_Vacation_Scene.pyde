import time
objects = []
types = {"str" : type(""), "list" : type([]), "tuple" : type(()), "dict" : type({})}
def g_c_key(d, kys):
    global types, objects
    new_d = d
    kys = (kys,) if not(type(kys) == types["tuple"]) else kys
    for k in kys:
        if (type(new_d) == types["list"] and k < len(new_d) and new_d[k]) or (type(new_d) == types["dict"] and k in new_d.keys()):
            if k == kys[len(kys) - 1]:
                return new_d[k]
            new_d = new_d[k]
        else:
            return None

def RENDERIMAGE(object):
    global objects
    img = g_c_key(object, "image")
    if img == None:
        return
    kys = ("name", "size", ("pos", "x"), ("pos", "y"), ("size", "x"), ("size", "y"), ("tint", "r"), ("tint", "g"), ("tint", "b"), ("tint", "a"))
    img_name, img_size, x, y, sx, sy, r, g, b, a = map(None, (g_c_key(img, ky) for ky in kys))
    tint(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255)
    image(loadImage(img_name if img_name != None else ""), x if x != None else 0, y if y != None else 0, sx if sx != None else 0, sy)          

def RENDERLINE(object):
    global objects
    l = g_c_key(object, "line")
    if l == None:
        return
    kys = ("r", "g", "b", "a", "weight", "pos", "pos2", ("pos", "x"), ("pos", "y"), ("pos2", "x"), ("pos2", "y"))
    r, g, b, a, w, p, p2, x, y, x2, y2  = map(None, (g_c_key(l, ky) for ky in kys))
    stroke(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255) 
    strokeWeight(w if w != None else 1)
    line(x if x != None else 0, y if y != None else 0, x2 if x2 != None else 0, y2 if y2 != None else 0)

def setup():
    background(100)
    size(420, 420)
    
    #default settings


objects.append({"image" : 
                {"name" : "night.png",
                "size" : {"x" : 800, "y" : 600},
                 "pos" : {"x" : 0, "y" : -600}
}})
objects.append({"image" :
                {"name": "day.png", 
                 "size" : {"x" : 800, "y" : 600},
                 "tint" : {"r" : 255, "g" : 255, "b" : 255, "a" : 255},
                 "pos" : {"x" : 0, "y" : -600}
}})
last_change_day = 0
turn_night = False
time_cycle = 30
x_offset = 0
def draw():
    global objects, last_change_day, time_cycle, turn_night, x_offset
    setup()
    print(time.time() - last_change_day, time_cycle)
    time_elapsed = time.time() - last_change_day 
    if time_elapsed > time_cycle:
        turn_night = not(turn_night)
        last_change_day = time.time()
    # DAY AND NIGHT CAN HAVE OBVIOUS CREASE IN THE MIDDLE BETWEENM THE TWO
    x_offset += 1
    print(x_offset)
    #255 - (time_elapsed * (255.0/time_cycle)) if turn_night else time_elapsed * (255.0/time_cycle))
    copy(loadImage(objects[1]["image"]["name"]), x_offset, 90, 420, 420, 0, 0, 420, 420)
    
    # fill(255, 255, 255)
    for object in objects:
        RENDERIMAGE(object) #REDERS IMAGES 
        RENDERLINE(object) #REDERS LINES     
