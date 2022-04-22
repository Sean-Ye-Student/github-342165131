def setup():
    background(100)
    size(500, 500)
    
def img(name):
    return loadImage(name)
i_e = lambda d, i : d[i] if (type(d) == type([]) and d[i]) or (type(d) == type({"A" : 0}) and i in d.keys()) else False
images = [{
           "image" : "house.jpg", 
           "pos" : {"x" : 0, "y" : 0}, 
           "size" : {"x" : 564, "y" : 442}
           },
          
          {
           "image" : "canada.png", 
           "pos" : {"x" : 0, "y" : 0}, 
           "size" : {"x" : 564, "y" : 442},
           "tint" : {"rgb" : 255, "alpha" : 1}
           },
          
          #{
           #"image" : "board.jpg", #draw the board not a image
#"pos" : {"x" : 0, "y" : 0}, 
           #"size" : {"x" : 564, "y" : 442}
           #},
          ]
          
          
def draw():
    global images
    for img in images:
        if img["image"] and img["pos"]:
            tint(img["tint"]["rgb"] if i_e(i_e(img, "tint"), "rgb") else: 255)
            image(loadImage(img["image"]), img["pos"]["x"], img["pos"]["y"], img["size"]["x"], img["size"]["y"])

               
