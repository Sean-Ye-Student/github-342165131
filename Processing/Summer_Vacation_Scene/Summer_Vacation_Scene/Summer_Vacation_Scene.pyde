import time
import random#Import libraries and modules
add_library('minim')
minim = Minim(this)
lines = []#Arrays used to store object infomation
clouds = []
confettis = []

def setup():#Loads the screen and the song
    global song
    size(420, 420)
    song = minim.loadFile("Song.mp3")
    song.play()
    #default settings
s = 15#list of clouds and reletive scaling
clouds.append({"image" : {"speed" : 5, "name" : "cloud.png", "pos" : {"x" : 50, "y" : 0}, "size" : {"x" : 841/(100/s), "y" : 813/(100/s)} }})
clouds.append({"image" : {"speed" : 12, "name" : "cloud1.png", "pos" : {"x" : 150, "y" : 100}, "size" : {"x" : 618/(100/s), "y" : 554/(100/s)} }})
clouds.append({"image" : {"speed" : 8, "name" : "cloud2.png", "pos" : {"x" : 267, "y" : 80}, "size" : {"x" : 753/(100/s), "y" : 616/(100/s)} }})
clouds.append({"image" : {"speed" : 16, "name" : "cloud3.png", "pos" : {"x" : 300, "y" : 30}, "size" : {"x" : 289/(100/s), "y" : 275/(100/s)} }})
message = {"speed" : 6, "pos" : {"x" : 420, "y" : 50}, "size" : 23}#message properties




last_change_day = 0
turn_night = False#Day settings
days_past = 0
time_cycle = 30#How many seconds a cycle lasts
x_offset = 0
paused = False

def keyPressed():#Controls the song
    global song, paused
    if key == "p":
        paused = not(paused)
    if key == "r":
        song.rewind()
    if paused:
        song.pause()
    else:
        song.play()

def draw():
    global objects, last_change_day, time_cycle, turn_night, x_offset, confettis, message, days_past
    time_elapsed = time.time() - last_change_day 
    if time_elapsed >= time_cycle:#Logic for day cycle
        turn_night = not(turn_night)
        last_change_day = time.time()
        days_past += 1
        time_elapsed = 0
        
        for i in range(250):
            #Creates randomly generated confetti that have different colors, positions and speeds. 
            confettis.append({"touched ground" : -1, "speed" : random.randint(1, 5), "fill" : {"r" : random.randint(0, 2) * 127.5, "g" : random.randint(0, 2) * 127.5, "b" : random.randint(0, 2) * 127.5, "a" : 255}, "fill2" : {"r" : random.randint(0, 2) * 127.5, "g" : random.randint(0, 2) * 127.5, "b" : random.randint(0, 2) * 127.5, "a" : 255}, "size" : {"x" : random.randint(10, 20), "y" : random.randint(10, 20)}, "pos" : {"x" : random.randint(0, 420), "y" :  random.randint(0, 100)}})
            
    x_offset = int(600 * ((time_elapsed + 0.0)/time_cycle))
    if turn_night:#Controls the background
        copy(loadImage("day.png"), x_offset, 90, 420, 420, 0, 0, 420, 420)
        copy(loadImage("night.png"), x_offset - 600, 90, 420, 420, 0, 0, 420, 420)
    else:
        copy(loadImage("night.png"), x_offset, 90, 420, 420, 0, 0, 420, 420)
        copy(loadImage("day.png"), x_offset - 600, 90, 420, 420, 0, 0, 420, 420)
    
    remove_confettis = []
    for i, c in enumerate(confettis):#Runs logic for all the confetti, also adds them to remove array when it reaches the ground after 5 seconds
        f = c["fill"] if ((time.time()+0.0/10) - round(time.time()+0.0/10)) > 0 else c["fill2"]
        fill(f["r"], f["g"], f["b"], f["a"])
        c["pos"]["y"] += c["speed"]
        if c["pos"]["y"] + c["size"]["y"] > 420:
            c["pos"]["y"] = 420 - c["size"]["y"]            
            c["touched ground"] = time.time() if c["touched ground"] < 0 else c["touched ground"]
            if time.time() - c["touched ground"] >= 5:
                remove_confettis.append(i)
        rect(c["pos"]["x"], c["pos"]["y"], c["size"]["x"], c["size"]["y"])
    r = 0
    i = 0
    while len(remove_confettis) > 0: #Deletes selected confetti in the array
        if i == remove_confettis[0]:
            confettis.pop(i - r)
            remove_confettis.pop(0)
            r += 1
        else:
            i += 1
    if turn_night: #Toggles the sun and moon depending on the time of day
        fill(254, 241, 125)  
        ellipse(100,75,100, 100)
        image(loadImage("sean.png"), 70, 25, 59, 100)
    else:
        fill(184, 184, 184)  
        ellipse(100,75,100, 100)
        image(loadImage("sean2.png"), 70, 25, 59, 100)
        
    for cloud in clouds: #Runs logic for clouds
        img = cloud["image"]
        img["pos"]["x"] -= img["speed"] 
        if img["pos"]["x"] < -img["size"]["x"]:
            img["pos"]["x"] = 420
        image(loadImage(img["name"]), img["pos"]["x"], img["pos"]["y"], img["size"]["x"], img["size"]["y"])

    if days_past > 3: #Makes the message appear after 3 daytime cycles
        fill(255, 255, 0)
        textFont(createFont("Minecraftia-Regular.ttf", message["size"]))
        message["pos"]["x"] = message["pos"]["x"] - message["speed"] if message["pos"]["x"] > -420 else 420
        text("Coding before midnight on vacation!", message["pos"]["x"], message["pos"]["y"])
