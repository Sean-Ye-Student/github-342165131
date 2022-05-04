import random
def setup():
    size(400, 400)
    background('#004477')

direction = (5, 0)
x, y = 0, 0
rx, ry = random.randint(0, 380), random.randint(0, 380)
gx, gy = random.randint(0, 380), random.randint(0, 380)
score = 0
in_area = lambda cx, cy, cx2, cy2, ax, ay: min(cx, cx2) < ax < max(cx, cx2) and min(cy, cy2) < ay < max(cy, cy2)
def draw():
    global x, y, rx, ry, gx, gy, in_area, score, direction
    setup()
    if keyPressed:
        print(key)
        if key == "w":
            direction = (0, -5)
        if key == "s":
            direction = (0, 5)
        if key == "a":
            direction = (-5, 0)
        if key == "d":
            direction = (5, 0)
            
    x = -20 if x > 400 else x
    x = 400 if x < -20 else x
    y = -20 if y > 400 else y
    y = 400 if y < -20 else y
    x, y = x + direction[0], y + direction[1]
    if in_area(gx, gy, gx + 20, gy + 20, x, y) or in_area(gx, gy, gx + 20, gy + 20, x + 20, y) or in_area(gx, gy, gx + 20, gy + 20, x, y + 20) or in_area(gx, gy, gx + 20, gy + 20, x + 20, y + 20):
        score += 1
        gx, gy = random.randint(0, 380), random.randint(0, 380)
    
    if in_area(rx, ry, rx + 20, ry + 20, x, y) or in_area(rx, ry, rx + 20, ry + 20, x + 20, y) or in_area(rx, ry, rx + 20, ry + 20, x, y + 20) or in_area(rx, ry, rx + 20, ry + 20, x + 20, y + 20):
        score += 1
        rx, ry = random.randint(0, 380), random.randint(0, 380)
        x, y = random.randint(0, 380), random.randint(0, 380)
    noStroke()
    textSize(12)
    fill(0, 255, 0)
    text("Score: " + str(score), 325, 12, 1)

    fill(255)
    rect(x, y, 20, 20)
    fill(255, 0, 0)
    rect(rx, ry, 20, 20)
    fill(0, 255, 0)
    rect(gx, gy, 20, 20)
            
    
    
          
