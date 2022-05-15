import time
add_library("minim")
animations = []
img_kys = ("name", "size", "pos", "fill", "animation")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default


def RENDERIMAGE(object, enabled_keys):
    img = object["image"]
    img_name, img_size, pos, f, anim = map(None, (img[ky] if ky in enabled_keys else None for ky in img_kys))
    if anim != None:
        fd, tf = anim["frame_duration"], anim["total_frames"], 
        elapsed = (time.time() - anim["start"]) % (tf * fd) if tf * fd > 0 else 1
        frame = int(elapsed/fd if fd > 0 else 1)
        img_name = anim["file_index"] + ("0" if frame < 100 and tf > 100 else "") + ("0" if frame < 10 and tf > 10 else "") + str(frame) + anim["file_type"]
    if img_name == None:
        return

    tint(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), fallback(f, "a", 255))
    print(width, height)
    image(loadImage(img_name), fallback(pos, "x", 0), fallback(pos, "y", 0), fallback(img_size, "x", 100), fallback(img_size, "y", 100))        

sounds = {"Player win round" : {"minim" : "Player win round/sound.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : True, "group" : 0}}
disable_sounds = []
sound_kys = ("minim", "repeat", "play_from_start", "isolate", "group")
def DisableSound():
    print(disable_sounds)
    remove_indexes = []#removes keys that were already used
    for sound in disable_sounds:
        sound_name, disable_time = map(None, sound)
        if disable_time <= time.time():
            sounds[sound_name]["minim"].pause()
            
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
        if repeat == -1:
            m.loop()
        else:
            m.play()
            disable_sounds.append((sound_name, time.time() + m.length()))
def setup():
    global animation
    size(600,338)
    minim = Minim(this)
    for ky in sounds:
        sounds[ky]["minim"] = minim.loadFile("sounds/" + sounds[ky]["minim"])
    PlaySound("Player win round", ("minim", "repeat", "play_from_start", "isolate", "group"))
    #default settings
    animations.append({"image" : {"animation" : {"file_index" : "animations/Player win round/frames/frame_", "file_type" : "_delay-0.1s.jpg", "start" : time.time(), "total_frames" : 41, "frame_duration" : 0.1}, "size" : {"x" : width, "y" : height}, "pos" : {"x" : 0, "y" : 0}}})
def draw():
    background(100)
    #print(frameRate)
    #DisableSound()
    for animation in animations:
        RENDERIMAGE(animation, ("size", "pos", "animation")) #REDERS IMAGES 