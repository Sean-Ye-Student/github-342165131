import random
import time
screenSizeX, screenSizeY = 500, 500

balls = [[0,0,25,(255, 255, 255)]]
#Later on ball properties can be a dictionary for readability 
balls_spawns = 20
max_magnitude = 150
sizeMin, sizeMax  = 5, 100

centerX, centerY = screenSizeX/2, screenSizeY/2

def setup():
    global balls
    size(screenSizeX, screenSizeY)
    for i in range(balls_spawns):
        x = random.randint(centerX-max_magnitude * 2, centerX+max_magnitude * 2)
        y = random.randint(centerY-max_magnitude * 2, centerY+max_magnitude * 2)
        if (x**2 + y**2)**0.5 > max_magnitude:
            c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            balls.append([x, y, random.randint(sizeMin, sizeMax), c])
            
    

def CanEat(ball_index, bigger_ball_index):
    global balls
    if ball_index >= len(balls) or bigger_ball_index >= len(balls):
        return False
    ball = balls[ball_index]
    bigger_ball = balls[bigger_ball_index]
    ball_r = ball[2]/2
    ball2_r = bigger_ball[2]/2
    p2X = bigger_ball[0]
    p2Y = bigger_ball[1]
    pX = ball[0]
    pY = ball[1]
    
    magnitude = ((p2X - pX)**2 + (p2Y - pY)**2)**0.5
    if bigger_ball_index == 0:
        print(magnitude, ball2_r, ball_r)
    if ball2_r > ball_r and magnitude <= ball2_r + ball_r:
        area = 3.14 * ball_r**2
        bigger_area = 3.14 * ball2_r**2
        balls[bigger_ball_index][2] = (((area + bigger_area) / 3.14)**0.5)*2
        balls.pop(ball_index)
        if ball_index == 0:
            print("Player Got Eaten!")
            while True:
                time.sleep(1)
        return True

def mouseWheel(event):
    balls[0][2] -= event.getCount()
    
setup()
def draw():
    
    global balls
    background(100)
    if len(balls) < 1:
        return
    balls[0][0] = mouseX
    balls[0][1] = mouseY
    
    for ball in balls:
        stroke(0)
        fill(ball[3][0], ball[3][1], ball[3][2])
        ellipse(ball[0], ball[1], ball[2], ball[2])
        
    for i in range(len(balls)):
        for ii in range(len(balls)):
            if CanEat(i, ii):
                break
    # for i in range(len(balls)):
    #     for bigger_ball in balls:
    #         big_r = bigger_ball[2]
    #         ball_r = balls[i][2]
    #         bpX = bigger_ball[0]
    #         bpY = bigger_ball[0]
    #         pX = balls[i][0]
    #         pY = balls[i][1]
            
    #         
            
            
