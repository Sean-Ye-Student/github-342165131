import time
add_library("minim") #Libraries
animations = {} #saves animation
img_kys = ("name", "size", "pos", "fill", "animation")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
text_kys = ("font", "word", "fill", "pos", "size", "startshow",  "showtime")
def RENDERTEXT(object, enabled_keys): #object is a dictionary, enabled_keys is a tuple storing all the keys that are in the object (assumed to be there)
    t = object["text"]
    font, word, f, pos, s, start, tim = map(None, (t[ky] if ky in enabled_keys else None for ky in text_kys))
    fill(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), 255)
    stroke(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), 0)
    if font != None:
        textFont(createFont(font, s if s != None else 12))
    else:
        textSize(s if s != None else 12)

    text(word if word != None else "PLACEHOLDER", fallback(pos, "x", 0), fallback(pos, "y", 0), fallback(pos, "z", 0))  

def RENDERIMAGE(object, enabled_keys):
    img = object["image"]
    img_name, img_size, pos, f, anim = map(None, (img[ky] if ky in enabled_keys else None for ky in img_kys))
    if anim != None:
        fd, tf = anim["frame_duration"], anim["total_frames"], 
        elapsed = (time.time() - anim["start"]) % (tf * fd) if tf * fd > 0 else 1
        frame = int(elapsed/fd if fd > 0 else 1)
        img_name = anim["file_index"] + str(frame) + anim["file_type"]
    if img_name == None:
        return
    tint(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), fallback(f, "a", 255))
    image(loadImage(img_name), fallback(pos, "x", 0), fallback(pos, "y", 0), fallback(img_size, "x", 100), fallback(img_size, "y", 100))        

sounds = {"Player win round" : {"minim" : "Player win round/sound.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : True, "group" : 0}, "Player win" : {"minim" : "Player win/sound.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : True, "group" : 0}, "Player2 win round" : {"minim" : "Player2 win round/sound.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : True, "group" : 0}, "Player2 win" : {"minim" : "Player2 win/sound.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : True, "group" : 0}, "Draw" : {"minim" : "Draw/sound.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : True, "group" : 0}, "Show" : {"minim" : "Game/sound.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : True, "group" : 0}}
disable_sounds = []
sound_kys = ("minim", "repeat", "play_from_start", "isolate", "group")

def DisableSound():
    global disable_sounds
    i = 0
    while i < len(disable_sounds):
        sound_name, disable_time = map(None, disable_sounds[i])
        if disable_time <= time.time():
            sounds[sound_name]["minim"].pause()
            disable_sounds.pop(i)
        else:
            i += 1

    
def PlaySound(sound_name, enabled_keys):
    if not(sound_name in sounds.keys()):
        return
    sound = sounds[sound_name]
    m, repeat, play_from_start, isolate, group = map(None, (sound[ky] if ky in enabled_keys else None for ky in sound_kys))

    if isolate == True:
        for ky in sounds:
            if ky == sound_name:
                continue
            same_group = True if "group" in sounds[ky].keys() and sounds[ky]["group"] == group else False
            if same_group:
                sounds[ky]["minim"].pause()
                
    if m == None:
        return
    if m.isPlaying() == False:
        if play_from_start == True:
            m.rewind()
        m.loop()
        if repeat > -1:
            disable_sounds.append((sound_name, time.time() + (m.length() + 0.0)/1000 * repeat if repeat != None else 1))

images = [] #maybe just reference parts of animation from images to make it easier to reference scenes with correct settings!
player_symbols = {True : {"image" : {"name" : "Symbols/Player Rock.png", "size" : {"x" : 310, "y" : 338}, "pos" : {"x" : 0, "y" : 0}}}, False : {"image" : {"name" : "Symbols/Player2 Rock.png", "size" : {"x" : 360, "y" : 338}, "pos" : {"x" : 240, "y" : 0}}}}
clear_images = []
def DisableScene():#Removes scenes from image list
    i = 0
    r = 0
    while i + r < len(images) and len(clear_images) > 0:
        if clear_images[0][1] <= time.time() and i + r == clear_images[0][0]:
            images.pop(i)
            clear_images.pop(0)
            r += 1
        else:
            i += 1

def LoadScene(scenes, sound_scene): #Loads a scene by adding it to image list
    global images, clear_images
    images = []
    for scene in scenes:
        animations[scene]["image"]["animation"]["start"] = time.time()
        images.append(animations[scene])
        clear_images.append((len(images) - 1, time.time() + animations[scene]["image"]["animation"]["total_frames"] * animations[scene]["image"]["animation"]["frame_duration"]))
    PlaySound(sound_scene, ("minim", "repeat", "play_from_start", "isolate", "group"))
    
def setup():
    global animations
    size(600,338)
    minim = Minim(this)
    for ky in sounds:
        sounds[ky]["minim"] = minim.loadFile(sounds[ky]["minim"])
    #Requires Width and Height meaning that animations must be declared in setup
    animations["Player win"] = {"image" : {"animation" : {"file_index" : "Player win/frames/frame (", "file_type" : ").jpg", "start" : time.time(), "total_frames" : 294,  "frame_duration" : 0.04}, "size" : {"x" : width, "y" : height}, "pos" : {"x" : 0, "y" : 0}}}
    animations["Player2 win"] = {"image" : {"animation" : {"file_index" : "Player2 win/frames/frame (", "file_type" : ").jpg", "start" : time.time(), "total_frames" : 210, "frame_duration" : 0.04}, "size" : {"x" : width, "y" : height}, "pos" : {"x" : 0, "y" : 0}}}
    animations["Player2 win round"] = {"image" : {"animation" : {"file_index" : "Player2 win round/frames/frame (", "file_type" : ").jpg", "start" : time.time(), "total_frames" : 123, "frame_duration" : 0.04}, "size" : {"x" : width, "y" : height}, "pos" : {"x" : 0, "y" : 0}}}
    animations["Player win round"] = {"image" : {"animation" : {"file_index" : "Player win round/frames/frame (", "file_type" : ").jpg", "start" : time.time(), "total_frames" : 110, "frame_duration" : 0.04}, "size" : {"x" : width, "y" : height}, "pos" : {"x" : 0, "y" : 0}}}
    animations["Draw"] = {"image" : {"animation" : {"file_index" : "Draw/frames/frame (","file_type" : ").jpg", "start" : time.time(), "total_frames" : 20, "frame_duration" : 0.04}, "size" : {"x" : width, "y" : height}, "pos" : {"x" : 0, "y" : 0}}}
    animations["Show"] = {"image" : {"animation" : {"file_index" : "Game/frames/frame (","file_type" : ").jpg", "start" : time.time(), "total_frames" : 54, "frame_duration" : 0.04}, "size" : {"x" : width, "y" : height}, "pos" : {"x" : 0, "y" : 0}}}

player_1_turn = True #Starts from left to right
player_1_wins = (-2, 1)#The winning remainders from player1
symbols = ("Rock", "Paper", "Scissors") #Converts index to name
picked = {True : 0, False : 0} #The option the player picked
scores = {True : 0, False : 0} #Players scores
text_titles = [{"text" : {"font" : "eastwest.ttf", "fill" : {"r" : 255, "g" : 255, "b" : 255, "a" : 255}, "word" : "Player", "size" : 45, "pos" : {"x" : 90, "y" : 45, "z" : 0}}} ,{"text" : {"font" : "eastwest.ttf", "fill" : {"r" : 255, "g" : 255, "b" :255, "a" : 255}, "word" : "Player 2", "size" : 45, "pos" : {"x" : 410, "y" : 325, "z" : 0}}}]
score_text = {True : {"text" : {"font" : "eastwest.ttf", "fill" : {"r" : 255, "g" : 255, "b" : 255, "a" : 255}, "word" : "999", "size" : 45, "pos" : {"x" : 130, "y" : 90, "z" : 0}}}, False :  {"text" : {"font" : "eastwest.ttf", "fill" : {"r" : 255, "g" : 255, "b" :255, "a" : 255}, "word" : "999", "size" : 45, "pos" : {"x" : 463, "y" : 280, "z" : 0}}}}
#game text

game_state = "Player 1 Picking" #Stores the current state of the game
show_symbols = -1
reset = -1

def mouseWheel(y):
    if game_state != "Player 1 Picking" and game_state != "Player 2 Picking":
        return
    y = y.getCount()
    picked[player_1_turn] -= y
    if picked[player_1_turn] >= len(symbols):
        picked[player_1_turn]  = 0
    elif picked[player_1_turn] < 0:
        picked[player_1_turn] = len(symbols) - 1
    player_symbols[player_1_turn]["image"]["name"] = "Symbols/" + ("Player " if player_1_turn else "Player2 ") + symbols[picked[player_1_turn]] + ".png"

def mouseClicked():
    global player_1_turn, game_state, reset, show_symbols
    if game_state != "Player 1 Picking" and game_state != "Player 2 Picking":
        return
    if mouseButton == LEFT:
        player_1_turn = not(player_1_turn)
        if player_1_turn:
            #print("Player 1 Wins" if picked[True] - picked[False] in player_1_wins else ("Draw" if picked[True] - picked[False] == 0 else "Player 2 Wins") )
            game_state = "Show" 
            LoadScene(("Show",), "Show")
            show_symbols = time.time() + 1.6
            reset = time.time() + 2.5
        else:
            game_state = "Player 2 Picking"
def draw():
    global game_state, reset, show_symbols, picked, scores
    background(100)
    DisableSound()
    DisableScene()
    RENDERIMAGE({"image" : {"name" : "Game/background.png", "size" : {"x" : 600, "y" : 338}, "pos" : {"x" : 0, "y" : 0}}}, ("name", "size", "pos"))
    for animation in images:
        RENDERIMAGE(animation, ("size", "pos", "animation")) #REDERS IMAGES 
        
    if reset > 0:
        if time.time() >= reset:
            if game_state == "Show":
                if "win" in game_state or game_state == "Draw":
                    game_state = "Player 1 Picking"
                game_state = "Player win round" if picked[True] - picked[False] in player_1_wins else ("Draw" if picked[True] - picked[False] == 0 else "Player2 win round")
                
                
                if game_state == "Player win round":
                    scores[True] += 1
                elif game_state == "Player2 win round":
                    scores[False] += 1
                
                game_state = "Player win" if scores[True] >= 3 else ("Player2 win" if scores[False] >= 3 else game_state)
                
                LoadScene((game_state,), game_state)
                reset = time.time() + animations[game_state]["image"]["animation"]["total_frames"] * animations[game_state]["image"]["animation"]["frame_duration"]
                if game_state == "Player win" or game_state == "Player2 win":
                    scores[True], scores[False] = 0, 0
            else:
                game_state = "Player 1 Picking"
                reset = -1
            show_symbols = -1
    
    if game_state == "Player 1 Picking" or (show_symbols > -1 and time.time() >= show_symbols):
        RENDERIMAGE(player_symbols[True], ("name", "pos", "size"))
    if game_state == "Player 2 Picking" or (show_symbols > -1 and time.time() >= show_symbols): 
        RENDERIMAGE(player_symbols[False], ("name", "pos", "size"))

    if game_state == "Player 1 Picking" or game_state == "Player 2 Picking":
        for title in text_titles:
            RENDERTEXT(title, ("word", "fill", "font", "size", "pos"))
        for ky in score_text.keys():
            score_text[ky]["text"]["word"] = str(scores[ky])
        RENDERTEXT(score_text[True], ("word", "fill", "font", "size", "pos"))
        RENDERTEXT(score_text[False], ("word", "fill", "font", "size", "pos"))
        
        for ky in sounds:
            sounds[ky]["minim"].pause()
