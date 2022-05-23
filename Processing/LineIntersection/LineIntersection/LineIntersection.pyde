import time
import random
asteroid_type, asteroid_origin, asteroid_velocity = 0, 1, 2
asteroid_type_size, asteroid_type_lines = 0, 1
asteroid_types = [
                  ((91, 92), ((13, 15, 38, 0), (38, 0, 51, 25), (51, 25, 78, 13), (78, 13, 91, 40), (91, 40, 74, 58), (74, 58, 77, 81), (77, 81, 42, 92), (42, 92, 14, 83), (14, 83, 0, 56), (0, 56, 13, 15))),
                ((111, 97), ((0, 25, 42, 25), (42, 25, 28, 0), (28, 0, 69, 0), (69, 0, 111, 26), (111, 26, 111, 36), (111, 36, 70, 48), (70, 48, 110, 72), (110, 72, 83, 97), (83, 97, 70, 83), (70, 83, 29, 96), (29, 96, 0, 60), (0, 60, 0, 25))),
                ((98, 105), ((13, 75, 25, 55), (25, 55, 18, 31), (18, 31, 40, 14), (40, 14, 60, 27), (60, 27, 82, 20), (82, 20, 98, 43), (98, 43, 78, 51), (78, 51, 95, 76), (95, 76, 71, 105), (71, 105, 41, 90), (41, 90, 30, 99), (30, 99, 13, 75))),
]
 
asteroids = [
[random.randint(0, len(asteroid_types) - 1), [0, 0], [1,1]] for i in range(5)
]

# lines = list([[list([random.randint(0, 500) for i in range(4)]), list([random.randint(-2, 2)+0.1, random.randint(-2, 2)+0.1])] for i in range(5)])
player_scale = 10
player_offset = (250, 250)
player_points = [lambda s, a, o: s*cos(a) + o, lambda s, a, o: s*sin(a) + o,
        lambda s, a, o: -s*cos(-a + 150) + o, lambda s, a, o: s*sin(-a + 150) + o,
        lambda s, a, o: -s*(2.5/6)*cos(a) + o, lambda s, a, o: -s*(2.5/6)*sin(a) + o,
        lambda s, a, o: -s*cos(a + 150) + o, lambda s, a, o: -s*sin(a + 150) + o]
player_angle = 0
player_velocity_angle = 0
player_origin = [250, 250] #spawn location, but will change when player moves
player_velocity = [0,0]#will change when player moves
player_acceleration = 5
player_friction = 65
player_control_minimum_range = 10
time_elapsed = time.time()
def setup():
    global asteroids
    size(1000, 562)
    
    for asteroid in asteroids:
        asteroid[asteroid_origin][0] = random.randint(0, width - asteroid_types[asteroid[asteroid_type]][asteroid_type_size][0])
        asteroid[asteroid_origin][1] = random.randint(0, height - asteroid_types[asteroid[asteroid_type]][asteroid_type_size][1])

def LineIntersection(x, y, x2, y2, vx, vy, xx, yy, xx2, yy2, vx2, vy2):
    slope = (y2 - y + 0.0)/((x2 - x) + 0 if (x2 - x) != 0 else 0.001) 
    slope2 = (yy2 - yy + 0.0)/((xx2 - xx) + 0 if (xx2 - xx) != 0 else 0.001)
    b, b2 = y - slope * x, yy - slope2 * xx
    xi = ((b2 - b)/(slope - slope2)) if (slope - slope2) != 0 else 0
    yi = (slope * xi + b) if slope != 0 else 0
    in_x_range2 = min(xx, xx2) <= xi <= max(xx, xx2)
    in_y_range2 = min(yy, yy2) <= yi <= max(yy, yy2)
    in_x_range = min(x, x2) <= xi <= max(x, x2)
    in_y_range = min(y, y2) <= yi <= max(y, y2)
    collided_x = (in_x_range and in_y_range2) and (in_y_range and in_x_range2)
    collided_y = (in_y_range and in_x_range2) and (in_x_range and in_y_range2)
    return collided_x, collided_y, xi, yi

def ScreenEdgeTeleport(origin, sizeX, sizeY):
    new_originX =  -sizeX if origin[0] > width + sizeX else (width + sizeX if origin[0] < -sizeX else origin[0])
    new_originY =  -sizeY if origin[1] > height + sizeY else (height + sizeY if player_origin[1] < -sizeY else origin[1])
    return new_originX, new_originY
   


def PlayerController():
    global  player_angle, player_origin, player_velocity, time_elapsed, player_acceleration, player_velocity_angle
    offsetX = mouseX - player_origin[0] + 0.0
    offsetY = -(mouseY - player_origin[1] + 0.0)
    if (offsetX**2 + offsetY **2)**0.5 >= player_control_minimum_range:
        player_angle = -atan(offsetY/offsetX) if offsetX != 0 else 0
        player_angle = -(atan(offsetY/offsetX)+3.1) if offsetX != 0 and offsetX < 0 else player_angle
    if keyPressed and key == "w":
        player_velocity_angle = player_angle
        player_velocity[0] += cos(player_velocity_angle) * player_acceleration * (time.time() - time_elapsed)
        player_velocity[1] += sin(player_velocity_angle) * player_acceleration * (time.time() - time_elapsed)
    else:
        friction = player_friction*(time.time() - time_elapsed)
        player_velocity[0] *= min(0.99, friction)
        player_velocity[1] *= min(0.99, friction)
            
    player_origin[0] += player_velocity[0]
    player_origin[1] += player_velocity[1]
    player_origin[0], player_origin[1] = ScreenEdgeTeleport(player_origin, player_scale, player_scale)
    time_elapsed = time.time()
def draw():
    background(0)
    stroke(255)
    PlayerController()
    points = tuple(formula(player_scale, player_angle, player_origin[0] if i%2 == 0 else player_origin[1]) for i, formula in enumerate(player_points))
    line(points[0], points[1], points[2], points[3])
    line(points[2], points[3], points[4], points[5])
    line(points[4], points[5], points[6], points[7])
    line(points[6], points[7], points[0], points[1])
    #print(frameRate)
    for asteroid in asteroids:
        for i, l in enumerate(asteroid_types[asteroid[asteroid_type]][asteroid_type_lines]):
            ao = asteroid[asteroid_origin]
            xx, yy, xx2, yy2 = l[0] + ao[0], l[1] + ao[1], l[2] + ao[0], l[3] + ao[1]
            for iii in range(0, len(player_points), 2):
                s, a, o, o2 = player_scale, player_angle, player_origin[0], player_origin[1]
                x, y = player_points[iii](s, a, o), player_points[iii + 1](s, a, o2)
                x2, y2 = player_points[iii + 1 if iii + 1 < len(player_points) else 0](s, a, o), player_points[iii + 2 if iii + 2 < len(player_points) else 1](s, a, o2)
                collided_x, collided_y, xi, yi = LineIntersection(x, y, x2, y2, player_velocity[0], player_velocity[1], xx, yy, xx2, yy2, asteroid[asteroid_velocity][0], asteroid[asteroid_velocity][1])
                if collided_x or collided_y:
                    fill(255, 0, 0)
                    noStroke()
                    ellipse(xi, yi, 4, 4)
                    stroke(255)
                    print(frameRate)
                    break
                else:
                    fill(255)
            line(xx, yy, xx2, yy2)
    for asteroid in asteroids:
        asteroid[asteroid_origin][0] += asteroid[asteroid_velocity][0]
        asteroid[asteroid_origin][1] += asteroid[asteroid_velocity][1]
        sizes = asteroid_types[asteroid[asteroid_type]][asteroid_type_size]
        origin = (asteroid[asteroid_origin][0] + sizes[0] / 2, asteroid[asteroid_origin][1] + sizes[1] / 2)
        newX, newY = ScreenEdgeTeleport(origin, sizes[0], sizes[1])
        asteroid[asteroid_origin][0], asteroid[asteroid_origin][1] = newX - sizes[0] / 2, newY - sizes[1] / 2
                    


        


    
