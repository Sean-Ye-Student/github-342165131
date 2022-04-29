add_library('minim')
s = None
s2 = None
def setup():
    global s, s2
    background(69)
    size(500, 500)
    minim = Minim(this)
    s = minim.loadFile("sound.mp3")
    s2 = minim.loadFile("sound2.mp3")
    
def keyPressed():
    global s, s2
    if key == "o":
        s.rewind()
        s.play()
    elif key == "i":
        s2.rewind()
        s2.play()
def draw():
    print(key)
       
