import time
add_library("minim")

img_kys = ("name", "size", "pos", "fill", "animation")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
def RENDERIMAGE(object, enabled_keys):
    img = object["image"]
    img_name, img_size, pos, f, anim = map(None, (img[ky] if ky in enabled_keys else None for ky in img_kys))
    if anim != None:
        fd, tf = anim["frame_duration"], anim["total_frames"], 
        elapsed = (time.time() - anim["start"]) % (tf * fd) if tf * fd > 0 else 1
        img_name = anim["file_index"] + str(int(elapsed/fd if fd > 0 else 1)) + anim["file_type"]
        
    if img_name == None:
        return

    tint(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), fallback(f, "a", 255))
    image(loadImage(img_name), fallback(pos, "x", 0), fallback(pos, "y", 0), fallback(img_size, "x", 100), fallback(img_size, "y", 100))      

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
    print(a_lerp)
    return int(a_lerp)

fallback = lambda dic, ky, default: dic[ky] if dic != None else default
text_kys = ("font", "word", "fill", "pos", "size", "startshow",  "showtime")
def RENDERTEXT(object, enabled_keys): #object is a dictionary, enabled_keys is a tuple storing all the keys that are in the object (assumed to be there)
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


sounds = {"intro" : {"minim" : "Nitrome Music Bad Ice Cream In Game.mp3", "repeat" : -1, "play_from_start" : False, "isolate" : True, "group" : 0}}
images = []
for x in range(3):
    a = []
    for y in range(3):
        a.append({"image" : {"size" : {"x" : 180, "y" : 180}, "pos" : {"x" : x * 200 + 10, "y" : y * 200 + 10}, "animation" : {"file_index" : "o/", "file_type" : ".png", "start" : 0, "total_frames" : 13, "frame_duration" : 0.09}}})
    images.append(a)


combos = tuple(tuple([(0, y), (1, y), (2, y)]) for y in range(3))
combos += tuple(tuple([(x, 0), (x, 1), (x, 2)]) for x in range(3)) 
combos += tuple([tuple([(0, 0), (1, 1), (2, 2)]), tuple([(2, 0), (1, 1), (0, 2)])])
reset = -1
message = {"text" : { "font" : "fonts/comic.ttf", "fill" : {"r" : 0, "g" : 0, "b" : 0, "a" : 255},"word" : "PLAYER X HAS WON", "size" : 45, "showtime" : 5, "startshow" : 0, "pos" : {"x" : 124, "y" : 280, "z" : 0}}}
score_message = {"text" : { "font" : "fonts/comic.ttf", "fill" : {"r" : 0, "g" : 0, "b" : 0, "a" : 255},"word" : "0:0", "size" : 45, "pos" : {"x" : 265, "y" : 318, "z" : 0}}}
grid = [[None, None, None] for i in range(3)]
score = {True : 0, False : 0}
turn = True #On X players turn

def setup():
    size(600,600)
    minim = Minim(this)
    for ky in sounds:
        sounds[ky]["minim"] = minim.loadFile("sounds/" + sounds[ky]["minim"])
    PlaySound("intro", ("minim", "repeat", "play_from_start", "isolate", "group"))
    #default settings


def draw():
    global grid, turn, score, reset, message
    background(255)
    for x in range(len(images)):
        for y in range(len(images[x])):
            a = "x/" if grid[x][y] else "o/"
            images[x][y]["image"]["animation"]["file_index"] = a
            RENDERIMAGE(images[x][y], ("size", "pos", "animation") if grid[x][y] != None else ()) #REDERS IMAGES 
            
    for x in range(0, 600, 200):
        for y in range(0, 600, 200):
            fill(0,0,0)
            strokeWeight(20)
            line(x, y, x, y + 600)
            line(x, y, x + 600, y)
    RENDERTEXT(score_message, ("font", "word", "fill", "pos", "size"))
    RENDERTEXT(message, ("font", "word", "fill", "pos", "size", "startshow", "showtime"))
    RENDERTEXT(message, ("font", "word", "fill", "pos", "size", "startshow", "showtime"))
    RENDERTEXT(message, ("font", "word", "fill", "pos", "size", "startshow", "showtime"))
    if reset > 0: #Make sure things are still being drawn
        if time.time() > reset:
            grid = [[None, None, None] for i in range(3)]
            turn = True #set it back to X players turn
            reset = -1
        else:
            return
    
    if mouseButton == LEFT:
        x, y, is_x = mouseX, mouseY, turn
        xc, yc = 0, 0
        for xg in range(len(grid)):
            for yg, state in enumerate(grid[xg]):
                if xg * 200 < x < (xg + 1) * 200 and yg * 200 < y < (yg + 1) * 200 and state == None:
                    grid[xg][yg] = turn
                    xc, yc = xg, yg
                    turn = not(turn)
                    continue
        for combo in combos:
            t = True
            for coor in combo:
                if turn == grid[coor[0]][coor[1]] or grid[coor[0]][coor[1]] == None:
                    t = False
                    break
            if t:
                score[not(turn)] += 1
                score_message["text"]["word"] = str(score[True]) + ":" + str(score[False]) 
                message["text"]["fill"]["r"], message["text"]["fill"]["g"], message["text"]["fill"]["b"] = map(None, (250, 50, 50) if not(turn) else (50, 250, 50))
                message["text"]["word"] = "Player " + ("x" if not(turn) else "o") + " has Won!"
                message["text"]["startshow"] = time.time()
                reset = time.time() + 5
                break
        blanks = False
        for row in grid:
            if None in row:
                blanks = True
                break
            
        if not(blanks):
            message["text"]["word"] = "Both Players Draw!"
            message["text"]["fill"]["r"], message["text"]["fill"]["g"], message["text"]["fill"]["b"] = 69, 69, 69
            message["text"]["startshow"] = time.time()
            reset = time.time() + 5
