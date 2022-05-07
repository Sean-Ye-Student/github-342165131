import time
animation = []
img_kys = ("name", "size", "pos", "fill", "animation")
fallback = lambda dic, ky, default: dic[ky] if dic != None else default
def RENDERIMAGE(object, enabled_keys):
    global objects

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
      
add_library("minim")
def setup():
    size(2000,1200)
    
    #default settings
for x in range(20):
    for y in range(20):
        animation.append({"image" : {"animation" : {"file_index" : "pvz/football/", "file_type" : ".png", "start" : 0, "total_frames" : 10, "frame_duration" : 0.09}, "size" : {"x" : 200, "y" : 200}, "pos" : {"x" : x * 200, "y" : y * 200}}})
def draw():
    background(100)
    print(frameRate)
    for object in animation:
        x, y = object["image"]["pos"]["x"] + 100, object["image"]["pos"]["y"] + 100
        if ((x - mouseX)**2 + (y - mouseY)**2) ** 0.5 < 200:
            object["image"]["animation"]["file_index"] = "pvz/footballeat/"  
            object["image"]["animation"]["total_frames"] = 9
        else:
            object["image"]["animation"]["file_index"] = "pvz/football/"
            object["image"]["animation"]["total_frames"] = 10
        
        RENDERIMAGE(object, ("size", "pos", "animation")) #REDERS IMAGES 
