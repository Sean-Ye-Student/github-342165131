import time
add_library("minim")
animation = []
img_kys = ("name", "size", "pos", "fill", "animation")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
sounds = {"intro" : {"minim" : "WhatsApp Trap Car.mp3", "repeat" : -1, "play_from_start" : False, "isolate" : True, "group" : 0}}
def RENDERIMAGE(object, enabled_keys):
    img = object["image"]
    img_name, img_size, pos, f, anim = map(None, (img[ky] if ky in enabled_keys else None for ky in img_kys))
    if anim != None:
        fd, tf = anim["frame_duration"], anim["total_frames"], 
        elapsed = (time.time() - anim["start"]) % (tf * fd) if tf * fd > 0 else 1
        frame = int(elapsed/fd if fd > 0 else 1)
        img_name = anim["file_index"] + ("0" if frame < 100 else "") + ("0" if frame < 10 else "") + str(frame) + anim["file_type"]
    if img_name == None:
        return

    tint(fallback(f, "r", 255), fallback(f, "g", 255), fallback(f, "b", 255), fallback(f, "a", 255))
    image(loadImage(img_name), 0, 0, 800, 600)        

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
animation.append({"image" : {"animation" : {"file_index" : "animation/frame_", "file_type" : "_delay-0.2s.jpg", "start" : 0, "total_frames" : 162, "frame_duration" : 0.2}, "size" : {"x" : screenX, "y" : screenY}, "pos" : {"x" : 0, "y" : 0}}})
def draw():
    background(100)
    PlaySound("intro", ("minim", "repeat", "play_from_start", "isolate", "group"))
    RENDERIMAGE(animation[0], ("size", "pos", "animation")) #REDERS IMAGES 
