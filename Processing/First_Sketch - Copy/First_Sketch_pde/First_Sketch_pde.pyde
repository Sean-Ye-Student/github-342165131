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
        
draw_x = False
def SWITCH():
    global draw_x
    draw_x = not(draw_x)
    for object in objects:
        name = g_c_key(object, ("image", "name"))
        if name == "X.png" or name == "O.png":
            x, y = g_c_key(object, ("image", "pos", "x")), g_c_key(object, ("image", "pos", "y"))
            object["image"]["name"] = "X.png" if draw_x else "O.png"
            object["image"]["pos"]["x"], object["image"]["pos"]["y"] = mouseX - object["image"]["size"]["x"]/2, mouseY - object["image"]["size"]["y"]/2

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
    size(500, 500)
    
    #default settings

    
def mousePressed():
    for object in objects:
        button = g_c_key(object, "button")
        if button != None:
            kys = (("area", "pos", "x"), ("area", "pos", "y"), ("area", "pos2", "x"), ("area", "pos2", "y"))
            x, y, x2, y2 = map(None, (g_c_key(button, ky) for ky in kys))
            if min(x, x2) <= mouseX <= max(x, x2) and min(y, y2) <= mouseY <= max(x, x2):
                f, m = g_c_key(button, "function"), g_c_key(button, "mouse") 
                if f != None and mouseButton == m:
                    f()

objects.append({"image" : {"name" : "house.jpg","size" : {"x" : 564, "y" : 442},"pos" : {"x" : 0, "y" : 0}}})
objects.append({"image" : {"name": "canada.png", "size" : {"x" : 564, "y" : 442},"tint" : {"r" : 255, "g" : 255, "b" : 255, "a" : 127},"pos" : {"x" : 0, "y" : 0}, }})
objects += [{"line" : {"r" : 69,"g" : 255,"b" : 69,"a" : 255,"weight" : 12,"pos" : {"x" : i * 166.666666667, "y" : 0},"pos2" : {"x" : i * 166.666666667, "y" : 500}}} for i in range(1, 3)]
objects += [{"line" : {"r" : 69,"g" : 255,"b" : 69,"a" : 255,"weight" : 12,"pos" : {"x" : 0, "y" : i * 166.666666667},"pos2" : {"x" : 500, "y" : i * 166.666666667}}} for i in range(1, 3)]
objects.append({"image" : {"name" : "X.png", "size" : {"x" : 500.0 / 3.0, "y" : 500.0 / 3.0}, "pos" : {"x" : 500.0 / 3.0, "y" : 500.0 / 3.0}}, "button" : {"mouse" : LEFT,"function" : SWITCH,"area" : {"pos" : {"x" : 0, "y" : 0},"pos2" : {"x" : 500, "y" : 500}}}})

            
def draw():
    global objects
    setup()
    for object in objects:
        RENDERIMAGE(object) #REDERS IMAGES 
        RENDERLINE(object) #REDERS LINES     
