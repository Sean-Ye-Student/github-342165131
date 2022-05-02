import random
import time
objects = []

types = {"str" : type(""), "list" : type([]), "tuple" : type(()), "dict" : type({})}
def g_c_key(d, kys):
    global types, objects
    new_d = d

    if not(type(kys) == types["tuple"]):
        kys = (kys,)
    for k in kys:
        if (type(new_d) == types["list"] and k < len(new_d) and new_d[k]) or (type(new_d) == types["dict"] and k in new_d.keys()):
            if k == kys[len(kys) - 1]:
                return new_d[k]
            new_d = new_d[k]
        else:
            return None

objects.append({"rect" : {"fill" : {"r" : 255,"g" : 255,"b" : 255,"a" : 255}, "stroke" :{"r" : 255, "g" : 255, "b" : 255, "a" : 0}, "weight" : 1, "pos" : {"x" : 240, "y" : 240}, "size" : {"x" : 20, "y" : 20}}})
objects.append({"rect" : {"fill" : {"r" : 0,"g" : 255,"b" : 0,"a" : 255},"stroke" :{"r" : 255,"g" : 255,"b" : 255,"a" : 0},"weight" : 1,"pos" : {"x" : 440, "y" : 240},"size" : {"x" : 20, "y" : 20}}})
objects.append({"rect" : {"fill" : {"r" : 255,"g" : 0,"b" : 0,"a" : 255},"stroke" :{"r" : 255,"g" : 255,"b" : 255,"a" : 0},"weight" : 1,"pos" : {"x" : 60, "y" : 240},"size" : {"x" : 20, "y" : 20}}})
objects.append({"text" : {"font" : "Minecraftia-Regular.ttf","fill" : {"r" : 0,"g" : 255,"b" : 0,"a" : 255},"word" : "Score: 0","size" : 25,"pos" : {"x" : 325, "y" : 50, "z" : 0}}})
objects.append({"text": {"font" : "Minecraftia-Regular.ttf","fill" : {"r" : 255,"g" : 0,"b" : 0,"a" : 0},"word" : "Hit","size" : 25,"pos" : {"x" : 280, "y" : 50, "z" : 0},"startshow" : 0,"showtime" : 0.5}})

playing = False
def HIDE():
     for object in objects:
        name = g_c_key(object, ("image", "name"))
        if name == "play.png" or name == "pause.png":
            x = name == "play.png"
            object["image"]["tint"]["a"] = 0 if x == playing else 255
    
def PAUSE():
    global playing
    playing = False
    HIDE()
objects.append({"button" : {"mouse" : LEFT, "function" : PAUSE, "area" : {"pos" : {"x" : 475, "y" : 0}, "pos2" : {"x" : 500, "y" : 25}}}, "image" : {"name" : "pause.png","tint" : {  "r" : 255,"g" : 255,"b" : 255,"a" : 0},"size" : {"x" : 25, "y" : 25},"pos" : {"x" : 475, "y" : 0}}        })


def PLAY():
    global playing, is_playing
    is_playing = True
    playing = True
    objects[7]["image"]["tint"]["a"] = 0
    HIDE()
    
objects.append({"button" : {"mouse" : LEFT,"function" : PLAY,"area" : {"pos" : {"x" : 200, "y" : 225}, "pos2" : {"x" : 300, "y" : 275}}},"image" : {"name" : "play.png","tint" : {  "r" : 255,"g" : 255,"b" : 255,"a" : 255},"size" : {"x" : 100, "y" : 50},"pos" : {"x" : 200, "y" : 225}}})
gameMode = "d"
is_playing = False
increment_move = 5 #Set by gamemode
direction = [increment_move, 0]
def SwitchGameMode():
    global gameMode, is_playing, increment_move, direction
    is_playing == False if is_playing == False and not(playing) else True
    if is_playing:
        return
    gameMode = "a" if gameMode == "d" else "d"
    increment_move = 20 if gameMode == "a" else 5
    direction = [increment_move, 0]
    objects[7]["image"]["name"] = "dynamic.png" if gameMode == "d" else "arcade.png"
    
objects.append({"button" : {"mouse" : LEFT,"function" : SwitchGameMode, "area" : {"pos" : {"x" : 200, "y" : 290}, "pos2" : {"x" : 300, "y" : 390}}},"image" : {"name" : "dynamic.png","tint" : {"r" : 255,"g" : 255,"b" : 255,"a" : 255},"size" : {"x" : 100, "y" : 100},"pos" : {"x" : 200, "y" : 290}}})

def setup():
    background('#004477')
    size(500, 500)

def mousePressed():
    for object in objects:
        button = g_c_key(object, "button")
        if button != None:
            x = g_c_key(button, ("area", "pos", "x"))
            y = g_c_key(button, ("area", "pos", "y"))
            x2 = g_c_key(button, ("area", "pos2", "x"))
            y2 = g_c_key(button, ("area", "pos2", "y"))
            if min(x, x2) <= mouseX <= max(x, x2) and min(y, y2) <= mouseY <= max(y, y2):
                f = g_c_key(button, "function")
                if f != None:
                    f()
speed = 1
positions = [(-100, -100) for i in range(1)]
min_spawn_magnitude_red = 100 #red must spawn these many pixels away from other objects
min_spawn_magnitude_to_green = 300 #white must spawn these many pixels away from green
score = 0
last_time = 0
def PlayerControl():
    global direction, score, speed, min_spawn_magnitude_to_green, positions, last_time, gameMode
    i = 0
    x, y = g_c_key(objects, (i, "rect", "pos", "x")), g_c_key(objects, (i, "rect", "pos", "y")) 
    sx, sy = g_c_key(objects, (i, "rect", "size", "x")), g_c_key(objects, (i, "rect", "size", "y"))
    i = 1          
    gx, gy = g_c_key(objects, (i, "rect", "pos", "x")), g_c_key(objects, (i, "rect", "pos", "y")) 
    gsx, gsy = g_c_key(objects, (i, "rect", "size", "x")), g_c_key(objects, (i, "rect", "size", "y"))
    
    i = 2 
    rx, ry = g_c_key(objects, (i, "rect", "pos", "x")), g_c_key(objects, (i, "rect", "pos", "y")) 
    rsx, rsy = g_c_key(objects, (i, "rect", "size", "x")), g_c_key(objects, (i, "rect", "size", "y"))
    

    
   
    #LOGIC FOR PLAYER CONTROLLER, CHECKS IF VARIABLES EXIST         
    if x != None and y != None and sx != None and sy != None and gx != None and gy != None and gsx != None and gsy != None and rx != None and ry != None and rsx != None and rsy != None:
        if keyPressed:
            print(key)
            if key == "w":
                direction = [0, -increment_move]
            elif key == "s":
                direction = [0, increment_move]
            elif key == "a":
                direction = [-increment_move, 0]
            elif key == "d":
                direction = [increment_move, 0]
        #OUT OF BOUNDS LOGIC
        if x < -20:
            objects[0]["rect"]["pos"]["x"] = 500
        elif x > 500:
            objects[0]["rect"]["pos"]["x"] = -20
        if y < -20:
            objects[0]["rect"]["pos"]["y"] = 500
        elif y > 500:
            objects[0]["rect"]["pos"]["y"] = -20
        
        #DETECTS IF THE BLOCK IS ON GREEN
        in_green = lambda x, y, top_left_corner: (gx < x < gx + gsx and gy < y < gy + gsy) or (top_left_corner and x == gx and y == gy and x + sx == gx + gsx and y + sy == gy + gsy) 
        if in_green(x, y, True) or in_green(x + sx, y, False) or in_green(x, y + sy, False) or in_green(x + sx, y + sy, False):
            speed = speed*1.1
            objects[1]["rect"]["pos"]["x"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
            objects[1]["rect"]["pos"]["y"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
            score += 1
            
            objects[4]["text"]["fill"]["r"] = 0
            objects[4]["text"]["fill"]["g"] = 255
            objects[4]["text"]["fill"]["b"] = 0
            objects[4]["text"]["startshow"] = time.time()#EFFECT FOR HIT TEXT
            
            objects[3]["text"]["word"] = "Score: " + str(score)
            objects[3]["text"]["startshow"] = time.time()
            
        #DETECTS IF THE BLOCK IS ON RED
        in_red = lambda x, y, top_left_corner: (rx < x < rx + rsx and ry < y < ry + rsy) or (top_left_corner and x == rx and y == ry and x + sx == rx + rsx and y + sy == ry + rsy) 
        if in_red(x, y, True) or in_red(x + sx, y, False) or in_red(x, y + sy, False) or in_red(x + sx, y + sy, False):
            x = 0
            objects[4]["text"]["fill"]["r"] = 255
            objects[4]["text"]["fill"]["g"] = 0
            objects[4]["text"]["fill"]["b"] = 0
            objects[4]["text"]["startshow"] = time.time()#EFFECT FOR HIT TEXT
            
            while x < 1000: #spawns the player first
                x += 1
                objects[0]["rect"]["pos"]["x"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
                objects[0]["rect"]["pos"]["y"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
                #CANNOT SPAWN PLAYER NEAR GREEN
                x, y = g_c_key(objects, (0, "rect", "pos", "x")), g_c_key(objects, (0, "rect", "pos", "y")) 
                if ((x - gx)**2 + (y - gy)**2 + 0.0)**0.5 >= min_spawn_magnitude_to_green:
                    break
            x = 0#SPAWNS RED BLOCK
            while x < 1000:
                x += 1
                
                objects[2]["rect"]["pos"]["x"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
                objects[2]["rect"]["pos"]["y"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
                

                #RED BLOCK CANNOT BE NEAR GREEN
                rx, ry = g_c_key(objects, (1, "rect", "pos", "x")), g_c_key(objects, (1, "rect", "pos", "y")) 
                if ((rx - gx)**2 + (ry - gy)**2 + 0.0)**0.5 >= min_spawn_magnitude_red and ((rx - x)**2 + (ry - y)**2 + 0.0)**0.5 >= min_spawn_magnitude_red:
                    break
        #MOVES THE PLAYER AT A INCREMENTED SPEED, LOOKS LIKE AN ARCADE GAME
        if gameMode == "a":
            if time.time() - last_time >= 0.5/speed:
                objects[0]["rect"]["pos"]["x"] += direction[0]
                objects[0]["rect"]["pos"]["y"] += direction[1]
                last_time = time.time()
        elif gameMode == "d":
            objects[0]["rect"]["pos"]["x"] += direction[0] * speed
            objects[0]["rect"]["pos"]["y"] += direction[1] * speed
            


                
def RENDERRECT(object):
    global objects
    re = g_c_key(object, "rect")
    if re == None:
        return
    kys = ("fill", "weight", "pos", "size", "stroke", ("fill", "r"), ("fill", "g"), ("fill", "b"), ("fill", "a"), ("stroke", "r"), ("stroke", "g"), ("stroke", "b"), ("stroke", "a"), ("pos", "x"), ("pos", "y"), ("size", "x"), ("size", "y"))
    f, w, p, s, st, r, g, b, a, rst, gst, bst, ast, x, y, sx, sy = map(None, (g_c_key(re, ky) for ky in kys))
    strokeWeight(w if w != None else 1)
    fill(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255) 
    stroke(rst if rst != None else 255, gst if gst != None else 255, bst if bst != None else 255, ast if ast != None else 255)
    rect(x if x != None else 0, y if y != None else 0, sx if sx != None else 0, sy if sy != None else 0)

            
def RENDERTEXT(object):
    global objects
    t = g_c_key(object, "text")
    if t == None:
        return
    word, s, f = g_c_key(t, "word"), g_c_key(t, "size"), g_c_key(t, "font")
    r, g, b, a = g_c_key(t, ("fill", "r")),  g_c_key(t, ("fill", "g")), g_c_key(t, ("fill", "b")), g_c_key(t, ("fill", "a"))
    x, y, z, F = g_c_key(t, ("pos", "x")), g_c_key(t, ("pos", "y")), g_c_key(t, ("pos", "z")), createFont(f if f != None else "", 16)
    a_lerp, start, tim  = 255, g_c_key(t, "startshow"), g_c_key(t, "showtime")
    if start != None and tim != None:
        if time.time() - start > tim:
            return#WILL NOT DRAW TEXT IF NOT SHOWING
        elif time.time() - start > (tim + 0.0)/2:#FADE HIDE AFFECT
            a_lerp = 255 - ((255*(time.time() - start)/tim) if tim > 0 else 0)
        else:#FADE SHOW AFFECT
            a_lerp = 255/(tim/(time.time() - start)) if (time.time() - start) > 0 else 0
    textFont(F)
    a = a_lerp if a_lerp != 255 else a
    fill(r if r != None else 255, g if g != None else 255, z if z != None else 255, a if a != None else 255)
    textSize(s if s != None else 12)
    text(word if word != None else "PLACEHOLDER", x if x != None else 0, y if y != None else 0, z if z != None else 0)            
           

def RENDERIMAGE(object):
    global objects
    img = g_c_key(object, "image")
    if img == None:
        return
    img_name, img_size  = g_c_key(img, "name"), g_c_key(img, "size")
    x, y, sx, sy = g_c_key(img, ("pos","x")),  g_c_key(img, ("pos","y")), g_c_key(img, ("size","x")), g_c_key(img, ("size","y"))
    r,g,b,a = g_c_key(img, ("tint", "r")), g_c_key(img, ("tint", "g")), g_c_key(img, ("tint", "b")), g_c_key(img, ("tint", "a"))    
    tint(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255)
    image(loadImage(img_name if img_name != None else ""), x if x != None else 0, y if y != None else 0, sx if sx != None else 0, sy)              
        
def draw():
    global objects, playing
    setup()#DRAWS BACKGROUND 
    if playing:#PLAYER WONT MOVE WHEN PAUSED
        PlayerControl()
    for object in objects:
       
        RENDERRECT(object)#RENDERS RECT
        RENDERTEXT(object)#RENDERS TEXT
        RENDERIMAGE(object)#RENDERS THE IMAGE
          
