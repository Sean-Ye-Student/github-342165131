import random
screenSizeX, screenSizeY = 500, 500
def setup():
    background(100)
    size(screenSizeX, screenSizeY)
    
balls = [[0,0,25,(255, 255, 255)]]
balls_spawns = 20
max_magnitude = 150
sizeMin, sizeMax  = 5, 100

centerX, centerY = screenSizeX/2, screenSizeY/2
for i in range(balls_spawns):
    x = random.randint(centerX-max_magnitude * 2, centerX+max_magnitude * 2)
    y = random.randint(centerY-max_magnitude * 2, centerY+max_magnitude * 2)
    if (x**2 + y**2)**0.5 > max_magnitude:
        c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        balls.append([x, y, random.randint(sizeMin, sizeMax), c])

def mouseWheel(event):
    balls[0][2] -= event.getCount()

def draw():
    setup()
    balls[0][0] = mouseX
    balls[0][1] = mouseY
    
    for ball in balls:
        stroke(0)
        fill(ball[3][0], ball[3][1], ball[3][2])
        ellipse(ball[0], ball[1], ball[2], ball[2])
    i = 0
    while i < len(balls):
        for bigger_ball in balls:
            big_r = bigger_ball[2]
            ball_r = balls[i][2]
            bpX, bpY, pX, pY = bigger_ball[0], bigger_ball[1], balls[i][0], balls[i][1]
            
            magnitude = (bpX**2 + pX**2)**0.5 + (bpY**2 + pY**2)**0.5
            print(magnitude)
            if i < len(balls) and big_r > ball_r and magnitude <= big_r + ball_r:
                area = 6.28 * balls[i][2]
                bigger_area = 6.28 * bigger_ball[2]
                bigger_ball[2] = area + bigger_area
                balls.pop(i)
                print(balls)
            continue
        i += 1 
            
