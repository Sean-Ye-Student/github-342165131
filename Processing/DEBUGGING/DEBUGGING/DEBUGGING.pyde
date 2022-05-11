import time
objects = []

def LERPTEXT(start, tim):
    a_lerp = 255
    if start == None or tim == None:
        return a_lerp
    if time.time() - start > tim:
        return 0 #WILL NOT DRAW TEXT IF NOT SHOWING
    elif time.time() - start > (tim + 0.0)/2:#FADE HIDE AFFECT
        a_lerp = 255 - ((255*(time.time() - start)/tim) if tim > 0 else 0)
    else:#FADE SHOW AFFECT
        a_lerp = 255/(tim/(time.time() - start)) if (time.time() - start) > 0 else 0
        
    return int(a_lerp)

fallback = lambda dic, ky, default: dic[ky] if dic != None else default
text_kys = ("font", "word", "fill", "pos", "size", "startshow",  "showtime")
def RENDERTEXT(object, enabled_keys):
    t = object["text"]
    font, word, f, pos, s, start, tim = map(None, (t[ky] if ky in enabled_keys else None for ky in text_kys))
    a_lerp = LERPTEXT(start, tim)
    a = a_lerp if a_lerp != 255 else fallback(f, "a", 255)
    #print(start, tim, a_lerp, a)
    fill(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), a)
    if font != None:
        textFont(createFont(font, s if s != None else 12))
    else:
        textSize(s if s != None else 12)

    text(word if word != None else "PLACEHOLDER", fallback(pos, "x", 0), fallback(pos, "y", 0), fallback(pos, "z", 0))            
objects.append({"text" : {
  "font" : "comic.ttf",
  "fill" : {"r" : 255, "g" : 255, "b" : 255, "a" : 255},
  "word" : "PLAYER X HAS WON",
  "size" : 45,
  "showtime" : 1,
  "startshow" : time.time(),
  "pos" : {"x" : 20, "y" : 250, "z" : 0}}
})

def setup():

    size(500, 500)
            
def draw():
    global objects
    background(100)
    for object in objects:
        RENDERTEXT(object, ("font", "word", "fill", "size", "pos", "showtime", "startshow")) #REDERS text
        if objects[0]["text"]["startshow"] + objects[0]["text"]["showtime"] < time.time():
            objects[0]["text"]["startshow"] = time.time()
