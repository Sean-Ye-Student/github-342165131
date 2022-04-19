def setup():
    background(100)
    size(200, 200)
lines = [(40,40,30,50), 
         (30,50, 40, 60), 
         (40,60,30,70), 
         (60,40,70,60), 
         (80,40,70,60), 
         (70,80,70,60), 
         (50, 70, 50, 70),
         (145, 160, 145, 110, 20, (255, 0, 255)),
         (120, 135, 170, 135, 20, (255, 0, 255)),
         (125, 120, 170, 160, 20, (255, 0, 255)),
         (125, 160, 170, 120, 20, (255, 0, 255)),
         (145, 135, 145, 135, 20, (229, 251, 38)),
        
         ]
def draw():
    global letters
    print(mouseX, mouseY)
    fill(0, 50, 0)
    strokeWeight(0)
    rect(145, 135, 15, 100)
    fill(0, 255, 0)
    ellipse(134, 175, 25, 10)
    fill(0, 255, 0)
    ellipse(180, 180, 50, 10)
    for l in lines:
        strokeWeight(10 if len(l) < 5 else l[4]) 
        stroke(0 if len(l) < 6 else l[5][0], 0 if len(l) < 6 else l[5][1], 0 if len(l) < 6 else l[5][2])   
        line(l[0], l[1], l[2], l[3])
        
