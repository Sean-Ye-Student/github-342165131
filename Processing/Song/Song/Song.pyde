add_library('minim')
song = None
def setup():
    global song
    background(69)
    size(500, 500)
    minim = Minim(this)
    song = minim.loadFile("Song.mp3")
    song.play()
    
def keyPressed():
    global song
    print(key)
    if key == "p":
        if song.isPlaying():
                print("paused song")
                song.pause()
        else:
            print("play song")
            song.play()
    elif key == "r":
        song.rewind()
def draw():
    print(key)
       
