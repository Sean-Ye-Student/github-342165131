import random
objects = [
{"rect" : {
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
"pos" : {"x" : 0, "y" : 0},
"size" : {"x" : 10, "y" : 10}
}}
]

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
                print(f)
                if f != None:
                    f()
            
def draw():
    global objects
    #setup()
    x = g_c_key(objects, (0, "rect", "pos", "x"))
    y = g_c_key(objects, (0, "rect", "pos", "y")) 
    if x != None and y != None:
        objects[0]["rect"]["pos"]["x"] += 1 if x < mouseX else -1
        objects[0]["rect"]["pos"]["y"] += 1 if y < mouseY else -1
        # objects[0]["rect"]["fill"]["r"] = random.randint(0, 255)
        # objects[0]["rect"]["fill"]["g"] = random.randint(0, 255)
        # objects[0]["rect"]["fill"]["b"] = random.randint(0, 255)
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
                
        #RENDERS RECT
        re = g_c_key(object, "rect")
        if re != None:
            f = g_c_key(re, "fill")
            r, g, b, a = g_c_key(f, "r"), g_c_key(f, "g"), g_c_key(f, "b"), g_c_key(f, "a")
            w = g_c_key(re, "weight")
            p = g_c_key(re, "pos")
            s = g_c_key(re, "size")
            st = g_c_key(re, "stroke")
            hidden = g_c_key(re, ("stroke", "hidden")
            if hidden:
                noStroke()
            else:
                print("make this into stroke")
                #stroke(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255)
                
            x, y, sx, sy = g_c_key(p, "x"), g_c_key(p, "y"), g_c_key(s, "x"), g_c_key(s, "y")
            if x != None and y != None and sx != None and sy != None:
                fill(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255) 
                strokeWeight(w if w != None else None)
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
                rgb = g_c_key(img, ("tint", "rgb")) if g_c_key(img, ("tint", "rgb")) else 255
                a = g_c_key(img, ("tint", "alpha")) if g_c_key(img, ("tint", "alpha")) else 255
                tint(rgb, a)
                image(loadImage(img_name), x, y, sx, sy)
        

               
