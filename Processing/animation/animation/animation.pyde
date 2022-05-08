import time
add_library("minim")
animation = []
img_kys = ("name", "size", "pos", "fill", "animation")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
sounds = {"intro" : {"minim" : "Crazy Dave Intro Theme.mp3", "repeat" : -1, "play_from_start" : False, "isolate" : True, "group" : 0}, 
          "seed" : {"minim" : "Choose Your Seeds.mp3", "repeat" : -1, "play_from_start" : True, "isolate" : True, "group" : 0}}
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
def setup():
    size(2000,1200)
    minim = Minim(this)
    for ky in sounds:
        sounds[ky]["minim"] = minim.loadFile("sounds/" + sounds[ky]["minim"])

    #default settings
for x in range(5):
    for y in range(5):
        animation.append({"image" : {"animation" : {"file_index" : "pvz/football/", "file_type" : ".png", "start" : 0, "total_frames" : 10, "frame_duration" : 0.09}, "size" : {"x" : 200, "y" : 200}, "pos" : {"x" : x * 200, "y" : y * 200}}})
def draw():
    background(100)
    #print(frameRate)
    
    if keyPressed:
        if key == "i":
            PlaySound("intro", ("minim", "repeat", "play_from_start", "isolate", "group"))
        if key == "s":
            PlaySound("seed", ("minim", "repeat", "play_from_start", "isolate", "group"))
    for object in animation:
        x, y = object["image"]["pos"]["x"] + 100, object["image"]["pos"]["y"] + 100
        if ((x - mouseX)**2 + (y - mouseY)**2) ** 0.5 < 200:
            object["image"]["animation"]["file_index"] = "pvz/footballeat/"  
            object["image"]["animation"]["total_frames"] = 9
        else:
            object["image"]["animation"]["file_index"] = "pvz/football/"
            object["image"]["animation"]["total_frames"] = 10
        
        RENDERIMAGE(object, ("size", "pos", "animation")) #REDERS IMAGES 
