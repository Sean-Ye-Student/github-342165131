import time
objects = []
objects.append({"image" : {"name" : "dvd-logo.png","size" : {"x" : 100, "y" : 45},"pos" : {"x" : 0, "y" : 0},"tint" : {"r" : 0, "g" : 255, "b" : 255, "a" : 255}},"body" : {"velocity" : {"x" : 1, "y" : 1},"mass" : 1,"weld" : ("image", "box collider")},"box collider" : {"pos" : {"x" : 0, "y" : 0}, "size" : {"x" : 100, "y": 45}}})
objects.append({"image" : {"name" : "dvd-logo.png","size" : {"x" : 100, "y" : 45},"pos" : {"x" : 400, "y" : 455},"tint" : {"r" : 0, "g" : 255, "b" : 0, "a" : 255}},"body" : {"velocity" : {"x" : -1, "y" : -1},"mass" : 1,"weld" : ("image", "box collider")},"box collider" : {"pos" : {"x" : 400, "y" : 455}, "size" : {"x" : 100, "y": 45}}})
objects.append({"box collider" : {"pos" : {"x" : -6, "y" : -1}, "size" : {"x" : 5, "y": 501}}})#LEFT
objects.append({"box collider" : {"pos" : {"x" : -1, "y" : -6}, "size" : {"x" : 501, "y": 5}}})#TOP
objects.append({"box collider" : {"pos" : {"x" : 501, "y" : -1}, "size" : {"x" : 5, "y": 501}}})#RIGHT
objects.append({"box collider" : {"pos" : {"x" : -1, "y" : 501}, "size" : {"x" : 501, "y": 5}}})#BOTTOM
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
on_line = lambda s, m, e: min(s, e) <= m <= max(s, e)
def RUNCOLLISIONS():#simplified does not account for already passed colliders A.K.A fast collisions
    global objects, in_area
    collided = []
    collidable = tuple(i for i in range(len(objects)) if g_c_key(objects[i], "box collider"))
    for i in range(len(collidable)):
        for ii in range(len(collidable)):
            if (i, ii) in collided or (ii, i) in collided:
                continue
            
            kys, kys2 = (("pos", "x"), ("pos", "y"), ("size", "x"), ("size", "y")), ((i, "body", "velocity", "x"), (i, "body", "velocity", "y"), (ii, "body", "velocity", "x"), (ii, "body", "velocity", "y"))
            x, y, xs, ys = map(lambda n : n if n != None else 0, (g_c_key(objects[i]["box collider"], ky) for ky in kys))
            x2, y2, xs2, ys2 = map(lambda n : n if n != None else 0, (g_c_key(objects[ii]["box collider"], ky) for ky in kys))            
            xv, yv, xv2, yv2 = map(lambda n : n if n != None else 0, (g_c_key(objects, ky) for ky in kys2))
            swap_x = (on_line(y, y2, y + ys) or on_line(y, y2 + ys2, y + ys)) and (x2 + xs2 == x or x2 == x + xs)
            swap_y = (on_line(x, x2, x + xs) or on_line(x, x2 + xs2, x + xs)) and (y2 + ys2 == y or y2 == y + ys)
            
            if not(swap_x or swap_y):
                continue
            collided.append((ii, i))
            kys = ((i, "body", "velocity", "x"), (i, "body", "velocity", "y"), (ii, "body", "velocity", "x"), (ii, "body", "velocity", "y"))
            o, oo, ooo, oooo = map(lambda x : True if x != None else False, (g_c_key(objects, ky) for ky in kys))
            if swap_x:
                if o:
                    objects[i]["body"]["velocity"]["x"] = -xv if xv else xv
                if ooo:
                    objects[ii]["body"]["velocity"]["x"] = -xv2 if xv2 else xv2            
            if swap_y:
                if oo:
                    objects[i]["body"]["velocity"]["y"] = -yv if yv else yv
                if oooo:
                    objects[ii]["body"]["velocity"]["y"] = -yv2 if yv2 else yv2
                    
def RENDERIMAGE(object):
    global objects
    img = g_c_key(object, "image")
    if img == None:
        return
    kys = ("name", "size", ("pos", "x"), ("pos", "y"), ("size", "x"), ("size", "y"), ("tint", "r"), ("tint", "g"), ("tint", "b"), ("tint", "a"))
    img_name, img_size, x, y, sx, sy, r, g, b, a = map(None, (g_c_key(img, ky) for ky in kys))
    tint(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255)
    image(loadImage(img_name if img_name != None else ""), x if x != None else 0, y if y != None else 0, sx if sx != None else 0, sy)      

def RENDERBODY(object):
    global objects
    body = g_c_key(object, "body")
    if body == None:
        return
    kys = (("velocity", "x"), ("velocity", "y"), "mass", "weld")
    vx, vy, m, w = map(None, (g_c_key(body, ky) for ky in kys))
    for ky in w:
        p = g_c_key(object, (ky, "pos"))
        if p != None:
            x, y = g_c_key(p, "x"), g_c_key(p, "y")
            if x != None:
                object[ky]["pos"]["x"] = (x + vx if x != None and vx != None else 0) + 0.0
            if y != None:
                object[ky]["pos"]["y"] = (y + vy if y != None and vy != None else 0) + 0.0
def setup():
    background(0)
    size(500, 500)

def draw():
    global objects
    setup()
    RUNCOLLISIONS()
    for object in objects:
        RENDERIMAGE(object)
        RENDERBODY(object)
