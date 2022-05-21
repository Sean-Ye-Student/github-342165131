import time
import random
# lines = [[[220, 250, 210, 200], [1, -1]],
#          [[210, 200, 250, 175], [1, -1]],
#          [[200, 300, 301, 0], [1, -1]],
#          [[200, 300, 301, 0], [1, -1]],
#          [[200, 300, 301, 0], [1, -1]]]
lines = list([[list([random.randint(0, 500) for i in range(4)]), list([random.randint(-2, 2)+0.1, random.randint(-2, 2)+0.1])] for i in range(5)])
player_scale = 10
player_offset = (250, 250)
player_points = [lambda s, a, o: s*cos(a) + o, lambda s, a, o: s*sin(a) + o,
        lambda s, a, o: -s*cos(-a + 150) + o, lambda s, a, o: s*sin(-a + 150) + o,
        lambda s, a, o: -s*(2.5/6)*cos(a) + o, lambda s, a, o: -s*(2.5/6)*sin(a) + o,
        lambda s, a, o: -s*cos(a + 150) + o, lambda s, a, o: -s*sin(a + 150) + o]
player_angle = 0
player_origin = [250, 250] #spawn location, but will change when player moves
player_velocity = [0,0]#will change when player moves
player_speed = 5
player_control_minimum_range = 10
time_elapsed = time.time()
def setup():
    size(500, 500)
    
is_vertical = lambda x, x2: x == x2
is_horizontal = lambda y, y2: y == y2
def LineIntersection(x, y, x2, y2, vx, vy, xx, yy, xx2, yy2, vx2, vy2):
    slope, slope2 = ((y2 - y + 0.0)/(x2 - x)) if (x2 - x) != 0 else 0, ((yy2 - yy + 0.0)/(xx2 - xx)) if (xx2 - xx) != 0 else 0
    b, b2 = y - slope * x, yy - slope2 * xx
    xi = ((b2 - b)/(slope - slope2)) if (slope - slope2) != 0 else 0
    yi = (slope * xi + b) if slope != 0 else 0
    in_x_range2 = min(xx, xx2) <= xi <= max(xx, xx2)
    in_y_range2 = min(yy, yy2) <= yi <= max(yy, yy2)
    in_x_range = min(x, x2) <= xi <= max(x, x2)
    in_y_range = min(y, y2) <= yi <= max(y, y2)
    collided_x, collided_y = False, False
    collided_x = (in_x_range and in_y_range2 and vx != 0) or (in_y_range and in_x_range2 and vx2 != 0)
    collided_y = (in_y_range and in_x_range2 and vy != 0) or (in_x_range and in_y_range2 and vy2 != 0)
    return collided_x, collided_y, xi, yi


#def keyPressed():

def draw():
    global player_angle, player_origin, player_velocity
    background(0)
    stroke(255)
    offsetX = mouseX - player_origin[0] + 0.0
    offsetY = -(mouseY - player_origin[1] + 0.0)
    if (offsetX**2 + offsetY **2)**0.5 >= player_control_minimum_range:
        if keyPressed and key == "w":
            player_velocity = [player_speed * cos(player_angle), player_speed * sin(player_angle)]
            player_origin[0] += player_velocity[0]+0.0001
            player_origin[1] += player_velocity[1]+0.0001
        
        player_angle = -atan(offsetY/offsetX) if offsetX != 0 else 0
        player_angle = -(atan(offsetY/offsetX)+3.1) if offsetX != 0 and offsetX < 0 else player_angle
    points = tuple(formula(player_scale, player_angle, player_origin[0] if i%2 == 0 else player_origin[1]) for i, formula in enumerate(player_points))
    line(points[0], points[1], points[2], points[3])
    line(points[2], points[3], points[4], points[5])
    line(points[4], points[5], points[6], points[7])
    line(points[6], points[7], points[0], points[1])

    for i in range(0, len(points), 2):
        for ii, target_line in enumerate(lines):
            s, a, o, o2 = player_scale, player_angle, player_origin[0], player_origin[1]
            x, y = player_points[i](s, a, o), player_points[i + 1](s, a, o2)
            x2, y2 = player_points[i + 1 if i + 1 < len(player_points) else 0](s, a, o), player_points[i + 2 if i + 2 < len(player_points) else 1](s, a, o2)
            collided_x, collided_y, xi, yi = LineIntersection(x, y, x2, y2, 
                                                              player_velocity[0], player_velocity[1], target_line[0][0], target_line[0][1], target_line[0][2], target_line[0][3], target_line[1][0], target_line[1][1])

            if collided_x or collided_y:
                ellipse(xi, yi, 4, 4)
                stroke(255,0,0)
            else:
                stroke(255)
                    
                    
    for current_line in lines:
        line(current_line[0][0], current_line[0][1], current_line[0][2], current_line[0][3])
        for i in range(len(current_line[0])):            
            current_line[0][i] += current_line[1][1 if i%2 else 0]

        


    
