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
"image" : {
"name" : "house.jpg",
"size" : {"x" : 564, "y" : 442},
"pos" : {"x" : 0, "y" : 0}
},

})

objects.append({
   "image" : {
           "name": "canada.png", 
           "size" : {"x" : 564, "y" : 442},
           "tint" : {"rgb" : 255, "alpha" : 127},
           "pos" : {"x" : 0, "y" : 0}, 
   },

})

objects.append({
"line" : {
"r" : 69,
"g" : 255,
"b" : 69,
"a" : 255,
"weight" : 12,
"pos" : {"x" : 166.666666667, "y" : 0},
"pos2" : {"x" : 166.666666667, "y" : 500}
},

})

objects.append({
"line" : {
"r" : 69,
"g" : 255,
"b" : 69,
"a" : 255,
"weight" : 12,
"pos" : {"x" : 166.666666667*2, "y" : 0},
"pos2" : {"x" : 166.666666667*2, "y" : 500}
},

})

objects.append({
"line" : {
"r" : 69,
"g" : 255,
"b" : 69,
"a" : 255,
"weight" : 12,
"pos" : {"x" : 0, "y" : 166.666666667},
"pos2" : {"x" : 500, "y" : 166.666666667}
},

})

objects.append({
"line" : {
"r" : 69,
"g" : 255,
"b" : 69,
"a" : 255,
"weight" : 12,
"pos" : {"x" : 0, "y" : 166.666666667*2},
"pos2" : {"x" : 500, "y" : 166.666666667*2}
},

})

objects.append({
    "image" : {
               "name" : "X.png",
               "size" : {"x" : 170, "y" : 170},
               "pos" : {"x" : 500.0 / 3.0, "y" : 500.0 / 3.0}
               }
})

objects.append({
    "image" : {
               "name" : "O.png",
               "size" : {"x" : 170, "y" : 170},
               "pos" : {"x" : 500.0 / 3.0, "y" : 500.0 / 3.0}
               }
})


draw_x = False
X_size_x, X_size_y, O_size_x, O_size_y = -1, -1, -1, -1
def SWITCH():
    global draw_x, X_size_x, X_size_y, O_size_x, O_size_y
    draw_x = not(draw_x)
    for object in objects:
        name = g_c_key(object, ("image", "name"))
        print(draw_x)
        if name == "X.png" or name == "O.png":
            sx = g_c_key(object, ("image", "size", "x"))
            sy = g_c_key(object, ("image", "size", "y"))
            if sx != None and sy != None:
                nsx, nsy, d = 0,0, False
                if name == "X.png":
                    if X_size_x < 0:
                        X_size_x = sx
                        X_size_y = sy
                        
                    d = draw_x
                    nsx = X_size_x
                    nsy = X_size_y
                elif name == "O.png":
                    if O_size_x < 0:
                        O_size_x = sx
                        O_size_y = sy
                    d = not(draw_x)
                    nsx = O_size_x
                    nsy = O_size_y
                object["image"]["size"]["x"] = nsx if d else 0
                object["image"]["size"]["y"] = nsy if d else 0
                object["image"]["pos"]["x"] = mouseX - object["image"]["size"]["x"]/2
                object["image"]["pos"]["y"] = mouseY - object["image"]["size"]["y"]/2
        
            
objects.append({
  "button" : {
              "mouse" : LEFT,
              "function" : SWITCH,
              "area" : {
                        "pos" : {"x" : 187, "y" : 152},
                        "pos2" : {"x" : 500, "y" : 500}
                        }
            },
  "image" : {
             "name" : "swap.png",
             "size" : {"x" : 187, "y" : 152},
             "pos" : {"x" : 313, "y" : 348}
            }
})





def setup():
    background(100)
    size(500, 500)
    #default settings
    SWITCH()
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
                print(f)
                if f != None:
                    f()
            
def draw():
    global objects
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
                strokeWeight(w if w != None else None)
                line(x, y, x2, y2, )
            
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
                rgb = g_c_key(img, ("tint", "rgb")) if g_c_key(img, ("tint", "rgb")) else 255
                a = g_c_key(img, ("tint", "alpha")) if g_c_key(img, ("tint", "alpha")) else 255
                tint(rgb, a)
                image(loadImage(img_name), x, y, sx, sy)
        

               
