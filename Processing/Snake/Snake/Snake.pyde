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

objects.append({
          "rect" : {
                    "fill" : {
                              "r" : 255,
                              "g" : 255,
                              "b" : 255,
                              "a" : 255
                    },

                    "stroke" :{
                            "r" : 255,
                            "g" : 255,
                            "b" : 255,
                            "hidden" : True
                    },


                    "weight" : 1,
                    "pos" : {"x" : 240, "y" : 240},
                    "size" : {"x" : 20, "y" : 20}
                    }
})

objects.append({
      "rect" : {
                    "fill" : {
                              "r" : 0,
                              "g" : 255,
                              "b" : 0,
                              "a" : 255
                    },

                    "stroke" :{
                            "r" : 255,
                            "g" : 255,
                            "b" : 255,
                            "hidden" : True
                    },


                    "weight" : 1,
                    "pos" : {"x" : 440, "y" : 240},
                    "size" : {"x" : 20, "y" : 20}
                    }
                          
})

objects.append({
      "rect" : {
                    "fill" : {
                              "r" : 255,
                              "g" : 0,
                              "b" : 0,
                              "a" : 255
                    },

                    "stroke" :{
                            "r" : 255,
                            "g" : 255,
                            "b" : 255,
                            "hidden" : True
                    },


                    "weight" : 1,
                    "pos" : {"x" : 60, "y" : 240},
                    "size" : {"x" : 20, "y" : 20}
                    }
                          
})

playing = False
def HIDE():
     for object in objects:
        name = g_c_key(object, ("image", "name"))
        if name == "play.png" or name == "pause.png":
            x = name == "play.png"
            object["image"]["tint"]["a"] = 0 if x == playing else 255

def PLAY():
    global playing
    playing = True
    HIDE()
    
def PAUSE():
    global playing
    playing = False
    HIDE()
   

objects.append({
  "button" : {
          "mouse" : LEFT,
          "function" : PAUSE,
          "area" : {"pos" : {"x" : 475, "y" : 0}, "pos2" : {"x" : 500, "y" : 25}}
          },
          
  "image" : {
          "name" : "pause.png",
          "tint" : {  
                     "r" : 255,
                     "g" : 255,
                     "b" : 255,
                     "a" : 0
                     },
          "size" : {"x" : 25, "y" : 25},
          "pos" : {"x" : 475, "y" : 0}
          }        
})


objects.append({
    "button" : {
            "mouse" : LEFT,
	          "function" : PLAY,
	          "area" : {"pos" : {"x" : 200, "y" : 225}, "pos2" : {"x" : 300, "y" : 275}}
          },
          
          "image" : {
	          "name" : "play.png",
	          "tint" : {  
                     "r" : 255,
                     "g" : 255,
                     "b" : 255,
                     "a" : 255
                     },
	          "size" : {"x" : 100, "y" : 50},
	          "pos" : {"x" : 200, "y" : 225}
          }
})



def setup():
    background(100)
    size(500, 500)

def mousePressed():
    for object in objects:
        button = g_c_key(object, "button")
        if button != None:
            x = g_c_key(button, ("area", "pos", "x"))
            y = g_c_key(button, ("area", "pos", "y"))
            x2 = g_c_key(button, ("area", "pos2", "x"))
            y2 = g_c_key(button, ("area", "pos2", "y"))
            if min(x, x2) <= mouseX <= max(x, x2) and min(y, y2) <= mouseY <= max(x, x2):
                f = g_c_key(button, "function")
                if f != None:
                    f()
speed = 1
increment_move = 20
direction = [increment_move, 0]
positions = [(-100, -100) for i in range(1)]
min_spawn_magnitude_red = 100 #red must spawn these many pixels away from other objects
min_spawn_magnitude_to_green = 300 #white must spawn these many pixels away from green
score = 0
last_time = 0
def PlayerControl():
    global direction, score, speed, min_spawn_magnitude_to_green, positions, last_time
    i = 0
    x, y = g_c_key(objects, (i, "rect", "pos", "x")), g_c_key(objects, (i, "rect", "pos", "y")) 
    sx, sy = g_c_key(objects, (i, "rect", "size", "x")), g_c_key(objects, (i, "rect", "size", "y"))
    i = 1          
    gx, gy = g_c_key(objects, (i, "rect", "pos", "x")), g_c_key(objects, (i, "rect", "pos", "y")) 
    gsx, gsy = g_c_key(objects, (i, "rect", "size", "x")), g_c_key(objects, (i, "rect", "size", "y"))
    
    i = 2 
    rx, ry = g_c_key(objects, (i, "rect", "pos", "x")), g_c_key(objects, (i, "rect", "pos", "y")) 
    rsx, rsy = g_c_key(objects, (i, "rect", "size", "x")), g_c_key(objects, (i, "rect", "size", "y"))
    

    
   
             
    if x != None and y != None and sx != None and sy != None and gx != None and gy != None and gsx != None and gsy != None and rx != None and ry != None and rsx != None and rsy != None:
        if keyPressed:
            if key == "w":
                direction = [0, -increment_move]
            elif key == "s":
                direction = [0, increment_move]
            elif key == "a":
                direction = [-increment_move, 0]
            elif key == "d":
                direction = [increment_move, 0]
            
        if x < -20:
            objects[0]["rect"]["pos"]["x"] = 500
        elif x > 500:
            objects[0]["rect"]["pos"]["x"] = -20
        if y < -20:
            objects[0]["rect"]["pos"]["y"] = 500
        elif y > 500:
            objects[0]["rect"]["pos"]["y"] = -20
        
        in_green = lambda x, y, top_left_corner: (gx < x < gx + gsx and gy < y < gy + gsy) or (top_left_corner and x == gx and y == gy and x + sx == gx + gsx and y + sy == gy + gsy) 
        if in_green(x, y, True) or in_green(x + sx, y, False) or in_green(x, y + sy, False) or in_green(x + sx, y + sy, False):
            speed = speed*1.1
            objects[1]["rect"]["pos"]["x"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
            objects[1]["rect"]["pos"]["y"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible

        in_red = lambda x, y, top_left_corner: (rx < x < rx + rsx and ry < y < ry + rsy) or (top_left_corner and x == rx and y == ry and x + sx == rx + rsx and y + sy == ry + rsy) 
        if in_red(x, y, True) or in_red(x + sx, y, False) or in_red(x, y + sy, False) or in_red(x + sx, y + sy, False):
            x = 0
            while x < 1000: #spawns the player first
                x += 1
                objects[0]["rect"]["pos"]["x"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
                objects[0]["rect"]["pos"]["y"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
                
                x, y = g_c_key(objects, (0, "rect", "pos", "x")), g_c_key(objects, (0, "rect", "pos", "y")) 
                if ((x - gx)**2 + (y - gy)**2 + 0.0)**0.5 >= min_spawn_magnitude_to_green:
                    break
            x = 0
            while x < 1000:
                x += 1
                
                objects[2]["rect"]["pos"]["x"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
                objects[2]["rect"]["pos"]["y"] = random.randint(0, 480/20) * 20 #make sure the entire square is visible
                

                
                rx, ry = g_c_key(objects, (1, "rect", "pos", "x")), g_c_key(objects, (1, "rect", "pos", "y")) 
                if ((rx - gx)**2 + (ry - gy)**2 + 0.0)**0.5 >= min_spawn_magnitude_red and ((rx - x)**2 + (ry - y)**2 + 0.0)**0.5 >= min_spawn_magnitude_red:
                    break

        if time.time() - last_time >= 0.5/speed:
            objects[0]["rect"]["pos"]["x"] += direction[0]
            objects[0]["rect"]["pos"]["y"] += direction[1]
            last_time = time.time()
            # objects[0]["rect"]["fill"]["r"] = random.randint(0, 255)
            # objects[0]["rect"]["fill"]["g"] = random.randint(0, 255)
            # objects[0]["rect"]["fill"]["b"] = random.randint(0, 255)
def draw():
    global objects, playing
    setup()
    if playing:
        PlayerControl()
    for object in objects:
        #RENDERS LINES
        l = g_c_key(object, "line")
        if l != None:            
            r, g, b, a = g_c_key(l, "r"), g_c_key(l, "g"), g_c_key(l, "b"), g_c_key(l, "a")
            w = g_c_key(l, "weight")
            p, p2 = g_c_key(l, "pos"), g_c_key(l, "pos2")
            x, y, x2, y2 = g_c_key(p, "x"), g_c_key(p, "y"), g_c_key(p2, "x"), g_c_key(p2, "y")
            if x != None and y != None and x2 != None and y2 != None:
                stroke(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255) 
                strokeWeight(w if w != None else 1)
                line(x, y, x2, y2, )
                
        #RENDERS RECT
        re = g_c_key(object, "rect")
        if re != None:
            f = g_c_key(re, "fill")
            r, g, b, a = g_c_key(f, "r"), g_c_key(f, "g"), g_c_key(f, "b"), g_c_key(f, "a")
            w = g_c_key(re, "weight")
            p = g_c_key(re, "pos")
            s = g_c_key(re, "size")
            st = g_c_key(re, "stroke")
            rst, gst, bst, = g_c_key(st, "r"), g_c_key(st, "g"), g_c_key(st, "b")
            hidden = g_c_key(re, ("stroke", "hidden"))
            if hidden:
                noStroke()
            else:
                stroke(rst if rst != None else 255, gst if gst != None else 255, bst if bst != None else 255)
                
            x, y, sx, sy = g_c_key(p, "x"), g_c_key(p, "y"), g_c_key(s, "x"), g_c_key(s, "y")
            if x != None and y != None and sx != None and sy != None:
                fill(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255) 
                strokeWeight(w if w != None else 1)
                rect(x, y, sx, sy)
        
        #RENDERS THE IMAGE
        img = g_c_key(object, "image")
        if img != None:
            img_name = g_c_key(img, "name")
            img_size = g_c_key(img, "size")
            x = g_c_key(img, ("pos","x"))
            y = g_c_key(img, ("pos","y"))
            sx = g_c_key(img, ("size","x"))
            sy = g_c_key(img, ("size","y"))
            if img_name != None and x != None and y != None and sx != None and sy != None:
                r,g,b = g_c_key(img, ("tint", "r")), g_c_key(img, ("tint", "g")), g_c_key(img, ("tint", "b"))
                a = g_c_key(img, ("tint", "a"))
   
                tint(r if r != None else 0, g if g != None else 0, b if b != None else 0, a if a != None else 255)
                image(loadImage(img_name), x, y, sx, sy)            
