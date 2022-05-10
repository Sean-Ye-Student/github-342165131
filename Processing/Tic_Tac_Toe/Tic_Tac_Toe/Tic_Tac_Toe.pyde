import time
add_library("minim")
grid = [[None, None, None] for i in range(3)]
images = []
img_kys = ("name", "size", "pos", "fill", "animation")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
sounds = {"intro" : {"minim" : "HOME - Dream Head.mp3", "repeat" : -1, "play_from_start" : False, "isolate" : True, "group" : 0}}

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
for x in range(3):
    a = []
    for y in range(3):
        a.append({"image" : {"size" : {"x" : 180, "y" : 180},
                             "pos" : {"x" : x * 200, "y" : y * 200},
                             "tint" : {"r" : 255, "g" : 255, "b" : 255, "a" : 255},
                             "animation" : {"file_index" : "o/", 
                                            "file_type" : ".png",
                                            "start" : 0, 
                                            "total_frames" : 2,
                                            "frame_duration" : 0.5
                                            }
                             }
        })
    images.append(a)
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
def setup():
    size(600,600)
    minim = Minim(this)
    for ky in sounds:
        sounds[ky]["minim"] = minim.loadFile("sounds/" + sounds[ky]["minim"])
    PlaySound("intro", ("minim", "repeat", "play_from_start", "isolate", "group"))
    #default settings
turn = True #On X players turn
combos = tuple((i, i + 1, i + 2) for i in range(3))
combos += tuple((i, i + 3, i + 6) for i in range(3)) 
combos += tuple([tuple([0, 4, 8]), tuple([2, 4, 6])])
print(combos)
def draw():
    global grid, turn
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
            for i in combo:
                type 
    
    background(255)
    for x in range(len(images)):
        for y in range(len(images[x])):
            a = "x/" if grid[x][y] else "o/"
            a = "n/" if grid[x][y] == None else a
            images[x][y]["image"]["animation"]["file_index"] = a
            RENDERIMAGE(images[x][y], ("size", "pos", "animation")) #REDERS IMAGES 
    
    for x in range(0, 600, 200):
        for y in range(0, 600, 200):
            fill(0,0,0)
            strokeWeight(20)
            line(x, y, x, y + 600)
            line(x, y, x + 600, y)
