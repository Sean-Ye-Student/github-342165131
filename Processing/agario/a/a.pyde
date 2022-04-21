import random
import time
screenSizeX, screenSizeY = 1000, 1000


balls_spawns = 40
max_magnitude = 2000
starting_size = 250
min_magnitude = starting_size * 2
sizeMin, sizeMax = 100, 2000

# balls_spawns = 1
# max_magnitude = 100
# min_magnitude = 100
# starting_size = 250
# sizeMin, sizeMax  = 250, 250

centerX, centerY = screenSizeX/2, screenSizeY/2
globalX, globalY = centerX, centerY
balls = [[centerX,centerY, min_magnitude,(255, 255, 255)]]
#Later on ball properties can be a dictionary for readability 

rendered_size = lambda ball: (ball[2] + 0.0) / (balls[0][2] + 0.0) * starting_size
            
def InRange(ball_index, bigger_ball_index):
    global globalX, globalY, centerX, centerY
    ball = balls[ball_index]
    bigger_ball = balls[bigger_ball_index]
    ball_r = rendered_size(ball)/2
    ball2_r = rendered_size(bigger_ball)/2
    p2X = centerX if bigger_ball_index == 0 else bigger_ball[0] + globalX
    p2Y = centerY if bigger_ball_index == 0 else bigger_ball[1] + globalY
    pX = centerX if ball_index == 0 else ball[0] + globalX
    pY = centerY if ball_index == 0 else ball[1] + globalY
    
    magnitude = ((p2X - pX)**2 + (p2Y - pY)**2)**0.5
    if magnitude <= ball2_r + ball_r:
        return True

def CanEat(ball_index, bigger_ball_index):
    global balls
    if ball_index >= len(balls) or bigger_ball_index >= len(balls):
        return False
    
    if balls[bigger_ball_index][2] > balls[ball_index][2] and InRange(ball_index, bigger_ball_index):
        area = 1.57 * balls[ball_index][2] **2
        bigger_area = 1.57 * balls[bigger_ball_index][2] **2
        balls[bigger_ball_index][2] = (((area + bigger_area) / 3.14)**0.5)*2
        balls.pop(ball_index)
    
        if ball_index == 0:
            time.sleep(1)
            print("Player Got Eaten by!", bigger_ball_index+1, balls[bigger_ball_index+1][2])
            while True:
                time.sleep(1)
        return True


def setup():
    global balls, centerX, centerX, max_magnitude, sizeMin, sizeMax, starting_size
    size(screenSizeX, screenSizeY)
    for i in range(balls_spawns):
        tries = 0
        while tries < 250:
            x = random.randint(centerX-max_magnitude, centerX+max_magnitude)
            y = random.randint(centerY-max_magnitude, centerY+max_magnitude)
            if (x**2 + y**2)**0.5 > max_magnitude:
                c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                balls.append([x, y, random.randint(sizeMin, sizeMax), c])
                overlapped = False
                for ii in range(len(balls)):
                    if not(i + 1 == ii) and InRange(i + 1, ii):
                        print("removed overlapping ball")
                        balls.pop(i + 1)
                        overlapped = True
                        break
                if not(overlapped):
                    break
                else:
                    tries += 1
        if tries >= 250:
            balls.append([0, 0, 0, (0,0,0)])#creates a placeholder ball
        
    print(balls)
    time.sleep(1)
def mouseWheel(event):
    balls[0][2] -= event.getCount()
    
def draw():
    global balls, globalX, globalY, centerX, centerY
    background(100)
    if len(balls) < 1:
        return
    
    if starting_size/2 < abs(mouseX - balls[0][0]) < starting_size * 2 and starting_size/2 < abs(mouseY - balls[0][1]) < starting_size * 2:
        if mouseX > balls[0][0]:
            globalX -= 1
        elif mouseX < balls[0][0]:
            globalX += 1
            
        if mouseY > balls[0][1]:
            globalY -= 1
        elif mouseY < balls[0][1]:
            globalY += 1
    first = True
    #print(globalX, globalY)
    for ball in balls:
        if first:
            first = False
            fill(ball[3][0], ball[3][1], ball[3][2])
            ellipse(ball[0], ball[1], starting_size, starting_size)
            continue
        stroke(0)
        fill(ball[3][0], ball[3][1], ball[3][2])
        ellipse(ball[0] + globalX, ball[1] + globalY, rendered_size(ball), rendered_size(ball))
    for i in range(len(balls)):
        for ii in range(len(balls)):
            if CanEat(i, ii):
                break
