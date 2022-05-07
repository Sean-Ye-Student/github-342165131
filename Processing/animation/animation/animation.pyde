import time
animation = []
img_kys = ("name", "size", "pos", "fill", "animation")
def RENDERIMAGE(object, enabled_keys):
    global objects
    img = object["image"]
    img_name, img_size, pos, f, anim = map(None, (img[ky] if ky in enabled_keys else None for ky in img_kys))
    if anim != None:
        fd, tf = anim["frame_duration"], anim["total_frames"], 
        elapsed = (time.time() - anim["start"]) % (tf * fd) if tf * fd > 0 else 1
        img_name = anim["file_index"] + str(int(elapsed/fd if fd > 0 else 1)) + anim["file_type"]
    if img_name == None or img_size == None:
        return
    x, y = 0, 0
    if pos != None:
        x, y = pos["x"], pos["y"]
        
    sx, sy =  0, 0
    if img_size != None:
        sx, sy = img_size["x"], img_size["y"] 
        
    r, g, b, a =  255, 255, 255, 255
    if f != None:
        r, g, b, a =f["r"], f["g"], f["b"], f["a"]
    tint(r,g,b,a)
    image(loadImage(img_name),x, y, sx, sy)        
      
add_library("minim")
def setup():
    size(2000,1200)
    
    #default settings
frame = 0
max_frame = 10 #64
max_c = 3 #0
c = 1 
for x in range(1):
    for y in range(1):
        animation.append({"image" : {"animation" : {"file_index" : "pvz/football/", "file_type" : ".png", "start" : 0, "total_frames" : 10, "frame_duration" : 0.09}, "size" : {"x" : 200, "y" : 200}, "pos" : {"x" : x * 200, "y" : y * 200}}})
def draw():
    global objects, c, frame, max_frame
    background(100)
    if c < 0:
        c = max_c
        frame = frame + 1 if frame + 1 <= max_frame else 0
    c -= 1
    print(frameRate)
    #image(loadImage("sus_animation/frame_" +str("0" if frame < 10 else "") + str(frame) + "_delay-0.1s.png"), 0, 0, width, height) #requires 64 max_frame
    # for i in range(1):
    #     for ii in range(1):
    #         x = 50 * i
    #         y = 50 * ii
            
    #             max_frame = 9
    #             image(loadImage("pvz/football/" + str(frame) + ".png"), 0, 0, 200, 200)
    #         else:
    #             max_frame = 9
    #             image(loadImage("pvz/football/" + str(frame) + ".png"), x, y, 200, 200)
    for object in animation:
        x, y = object["image"]["pos"]["x"] + 100, object["image"]["pos"]["y"] + 100
        if ((x - mouseX)**2 + (y - mouseY)**2) ** 0.5 < 200:
            object["image"]["animation"]["file_index"] = "pvz/footballeat/"  
            object["image"]["animation"]["total_frames"] = 9
        else:
            object["image"]["animation"]["file_index"] = "pvz/football/"
            object["image"]["animation"]["total_frames"] = 10
        
        RENDERIMAGE(object, ("size", "pos", "animation")) #REDERS IMAGES 
