# def RENDERIMAGE(object):
#     global objects
#     img = g_c_key(object, "image")
#     if img == None:
#         return
#     kys = ("name", "size", ("pos", "x"), ("pos", "y"), ("size", "x"), ("size", "y"), ("tint", "r"), ("tint", "g"), ("tint", "b"), ("tint", "a"))
#     img_name, img_size, x, y, sx, sy, r, g, b, a = map(None, (g_c_key(img, ky) for ky in kys))
#     tint(r if r != None else 255, g if g != None else 255, b if b != None else 255, a if a != None else 255)
#     image(loadImage(img_name if img_name != None else ""), x if x != None else 0, y if y != None else 0, sx if sx != None else 0, sy)          
add_library("minim")
def setup():
    size(2000,1200)
    
    #default settings

#animation.append({"image" : {"name" : "house.jpg","size" : {"x" : 564, "y" : 442},"pos" : {"x" : 0, "y" : 0}}})
frame = 0
max_frame = 0 #64
max_c = 3 #0
c = 1

def draw():
    global objects, c, frame, max_frame, x, y
    background(100)
    # if c < 0:
        # c = max_c
    frame = frame + 1 if frame + 1 <= max_frame else 0
    # c -= 1
    print(frameRate)
    #image(loadImage("sus_animation/frame_" +str("0" if frame < 10 else "") + str(frame) + "_delay-0.1s.png"), 0, 0, width, height) #requires 64 max_frame
    for i in range(120):
        for ii in range(120):
            x = 50 * i
            y = 50 * ii
            if ((x - mouseX)**2 + (y - mouseY)**2) ** 0.5 < 200:
                max_frame = 9
                image(loadImage("pvz/footballeat/" + str(frame) + ".png"), x, y, 200, 200)
            else:
                max_frame = 9
                image(loadImage("pvz/football/" + str(frame) + ".png"), x, y, 200, 200)
    # for object in objects:
    #     RENDERIMAGE(object) #REDERS IMAGES 
    #     RENDERLINE(object) #REDERS LINES     
