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
        #CUSTOM JUST TO COMPENSATE FOR WINNER ANIMATION
        if anim["file_index"] == "images/winner/frame_": 
            frame = int(elapsed/fd if fd > 0 else 1)
            img_name = anim["file_index"] + ("0" if frame < 100 else "") + ("0" if frame < 10 else "") + str(frame) + anim["file_type"]
            print(img_name)
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



sounds = {"menu" : {"minim" : "Nitrome Music - Bad Ice-Cream (Menu).mp3", "repeat" : -1, "play_from_start" : True, "isolate" : True, "group" : 0},
          "game" : {"minim" : "Nitrome Music Bad Ice Cream In Game.mp3", "repeat" : -1, "play_from_start" : False, "isolate" : True, "group" : 0},
          "win" : {"minim" : "Nitrome Music - Bad Ice-Cream (Win).mp3", "repeat" : -1, "play_from_start" : True, "isolate" : True, "group" : 0},
          "finish" : {"minim" : "Fortnite default dance sound.mp3", "repeat" : -1, "play_from_start" : True, "isolate" : True, "group" : 0}}
images = []
for x in range(3):
    a = []
    for y in range(3):
        a.append({"image" : {"size" : {"x" : 180, "y" : 180}, "pos" : {"x" : x * 200 + 10, "y" : y * 200 + 10}, "animation" : {"file_index" : "images/o/", "file_type" : ".png", "start" : 0, "total_frames" : 13, "frame_duration" : 0.09}}})
    images.append(a)

winner_image = {"image" : {"size" : {"x" : 320, "y" : 270}, "pos" : {"x" : 140, "y" : 80}, "animation" : {"file_index" : "images/winner/frame_", "file_type" : "_delay-0.04s.png", "start" : 0, "total_frames" : 176, "frame_duration" : 0.04}}}

combos = tuple(tuple([(0, y), (1, y), (2, y)]) for y in range(3))
combos += tuple(tuple([(x, 0), (x, 1), (x, 2)]) for x in range(3)) 
combos += tuple([tuple([(0, 0), (1, 1), (2, 2)]), tuple([(2, 0), (1, 1), (0, 2)])])
reset, prevent_input = -1, -1
message = {"text" : { "font" : "fonts/comic.ttf", "fill" : {"r" : 0, "g" : 0, "b" : 0, "a" : 255},"word" : "PLAYER X HAS WON", "size" : 45, "showtime" : 5, "startshow" : 0, "pos" : {"x" : 124, "y" : 350, "z" : 0}}}
max_score_message =  {"text" : { "font" : "fonts/comic.ttf", "fill" : {"r" : 0, "g" : 0, "b" : 255, "a" : 255},"word" : "", "size" : 20, "pos" : {"x" : 75, "y" : 318, "z" : 0}}}
score_message = {"text" : { "font" : "fonts/comic.ttf", "fill" : {"r" : 0, "g" : 0, "b" : 0, "a" : 255},"word" : "0:0", "size" : 45, "pos" : {"x" : 265, "y" : 318, "z" : 0}}}
#info_messages = [{"text" : { "font" : "fonts/comic.ttf", "fill" : {"r" : 0, "g" : 0, "b" : 0, "a" : 255},"word" : "0:0", "size" : 45, "pos" : {"x" : 265, "y" : 318, "z" : 0}}} for i in range(0, 600)]
grid = [[None, None, None] for i in range(3)]
score, turn, game_started, max_score, is_pressing, game_ended, numbers  = {True : 0, False : 0}, True, False, 3, False, None, [str(i) for i in range(10)]
max_score_message["text"]["word"] = "Playing to " + str(max_score)

title = "tic tac toe"
title_images = tuple({"image" : {"size" : {"x" : 100, "y" : 100}, "pos" : {"x" : 100 * i - 100 * (int(i/4) * 2.5), "y" : 100 * int(i/4)}, "animation" : {"file_index" : "images/" + title[i] + "/", "file_type" : ".png", "start" : 0, "total_frames" : 13, "frame_duration" : 0.09}}}
                     if c != " " else None for i, c in enumerate(title))
phrases = (("Instructions", 225), ("Press any number key to change the target!", 45), ("Press undo to remove digit! 0 or 1 is single game!", 10), ("Press play to start! Make sure to bring a friend!", 10))
           
instructions = [{"text" : { "font" : "fonts/comic.ttf", "fill" : {"r" : 0, "g" : 0, "b" : 255, "a" : 255}, "word" : phrase[0], "size" : 25, "pos" : {"x" : phrase[1], "y" : 520 + i * 20, "z" : 0}}}
                for i, phrase in enumerate(phrases)]
def PLAY():
    global game_started
    game_started = True
    print(game_started)
    
def UNDO():
    global max_score
    if game_started:
        return
    
    max_score = int(max_score/10)
buttons = []
buttons.append({"image" : {"name" : "images/play.png", "size" : {"x" : 150, "y" : 75}, "pos" : {"x" : 225, "y" : 375}},"button" : {"mouse" : LEFT, "function" : PLAY, "area" : {"pos" : {"x" : 225, "y" : 375}, "pos2" : {"x" : 375, "y" : 450}}}})
buttons.append({"image" : {"name" : "images/undo.png", "size" : {"x" : 100, "y" : 50}, "pos" : {"x" : 75, "y" : 320}}, "button" : {"mouse" : LEFT, "function" : UNDO, "area" : {"pos" : {"x" : 75, "y" : 320}, "pos2" : {"x" : 175, "y" : 370}}}})

def setup():
    size(600,600)
    minim = Minim(this)
    for ky in sounds:
        sounds[ky]["minim"] = minim.loadFile("sounds/" + sounds[ky]["minim"])
    #default settings
    
button_kys = ("area", "function", "mouse")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
def keyPressed():
    global max_score, max_score_message 
    if game_started == False:
        for i, string in enumerate(numbers):
            if string == key:
                max_score = max_score * 10 + i
                return
            
def mouseReleased():
    global buttons
    for i, object in enumerate(buttons):
        button = object["button"]
        a, f, m = fallback(button, "area", None), fallback(button, "function", None), fallback(button, "mouse", None)
        p, p2 = fallback(a, "pos", None), fallback(a, "pos2", None)
        x, y, x2, y2 = fallback(p, "x", 0), fallback(p, "y", 0), fallback(p2, "x", 0), fallback(p2, "y", 0)
        if min(x, x2) <= mouseX <= max(x, x2) and min(y, y2) <= mouseY <= max(y, y2):
            if f != None and mouseButton == m:
                f()
                return
#MAKE THE MAIN MENU POPUP AFTER WINNING
def draw():
    global grid, turn, score, max_score, is_pressing, message, prevent_input, game_ended, game_started, title_images
    global reset, grid
    background(255)
    for x in range(len(images)):
        for y in range(len(images[x])):
            a = "images/x/" if grid[x][y] else "images/o/"
            images[x][y]["image"]["animation"]["file_index"] = a
            RENDERIMAGE(images[x][y], ("size", "pos", "animation") if grid[x][y] != None else ()) #REDERS IMAGES 
    strokeWeight(20)
    fill(0,0,0)
    for x in range(200, 600, 200):
        line(x, 0, x, 600)
    for y in range(200, 600, 200):
        line(0, y, 600, y)
    if game_started == False:
        PlaySound("menu", ("minim", "repeat", "play_from_start", "isolate", "group"))
        for object in title_images:
            if object == None:
                continue
            RENDERIMAGE(object, ("animation", "pos", "size"))
        for button in buttons:
            RENDERIMAGE(button, ("name", "pos", "size"))
        max_score_message["text"]["word"] = "Playing to " + str(max_score)
        RENDERTEXT(max_score_message, ("font", "word", "fill", "pos", "size"))
        for object in instructions:
            RENDERTEXT(object, ("font", "word", "fill", "pos", "size"))
        return
    
    if game_ended:
        for i in range(3):
            RENDERIMAGE(winner_image, ("size", "pos", "animation"))
    
    RENDERTEXT(score_message, ("font", "word", "fill", "pos", "size"))
    for i in range(3):
        RENDERTEXT(message, ("font", "word", "fill", "pos", "size", "startshow", "showtime"))
    if reset > 0: #Make sure things are still being drawn
        if time.time() > reset:
            if score[True] >= max(max_score, 1) or score[False] >= max(max_score, 1):
                PlaySound("finish", ("minim", "repeat", "play_from_start", "isolate", "group"))
                winner_image["image"]["animation"]["start"] = time.time()
                message["text"]["fill"]["r"], message["text"]["fill"]["g"], message["text"]["fill"]["b"] = map(None, (250, 50, 50) if not(turn) else (50, 250, 50))
                message["text"]["word"] = "      Player " + ("X" if score[True] >= max(max_score, 1) else "O")
                score_message["text"]["word"] = ""
                message["text"]["startshow"] = time.time()
                score[True], score[False] = 0, 0
                game_ended = True
                reset = time.time() + 7
                prevent_input = time.time() + 8
                return
            PlaySound("win", ("minim", "repeat", "play_from_start", "isolate", "group"))
            if game_ended:
                game_ended = False
                game_started = False
                return
            score_message["text"]["word"] = str(score[True]) + ":" + str(score[False]) 
            grid = [[None, None, None] for i in range(3)]
            turn = True #set it back to X players turn
            reset = -1
        else:
            return
    PlaySound("game", ("minim", "repeat", "play_from_start", "isolate", "group"))
    if mousePressed and mouseButton == LEFT and (prevent_input < 0 or time.time() > prevent_input):
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
                message["text"]["word"] = "Player " + ("X" if not(turn) else "O") + " has Won!"
                message["text"]["startshow"] = time.time()
                reset = time.time() + 5
                prevent_input = time.time() + 6
                return
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
            prevent_input = time.time() + 6
            return
