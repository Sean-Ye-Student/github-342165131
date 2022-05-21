import time
import random
lines = [[[220, 250, 210, 200], [1, -1]],
         [[210, 200, 250, 175], [1, -1]],
         [[200, 300, 301, 0], [1, -1]],
         [[200, 300, 301, 0], [1, -1]],
         [[200, 300, 301, 0], [1, -1]]]

player_scale = 10
player_offset = (250, 250)
player = [[0,0], [-1,2], [0,1.5], [1,2]]

player_angle = 0
player_velocity = [0,0]
player_acceleration = [0,0]
time_elapsed = time.time()
# player_bounds = [10**6, 10**6, -1, -1]
for pos in player:
    for i in range(len(pos)):
        pos[i] *= player_scale
        pos[i] += player_offset[0 if i%2 == 0 else 1]
#         if i%2 == 0:
#             player_bounds[0] = min(player_bounds[0], pos[i])
#             player_bounds[2] = max(player_bounds[0], pos[i])
#         else:
#             player_bounds[1] = min(player_bounds[1], pos[i])
#             player_bounds[3] = max(player_bounds[1], pos[i])
# player_center = [((player_bounds[0] - player_bounds[2]) / 2) + player_bounds[0] , ((player_bounds[1] - player_bounds[3]) / 2) + player_bounds[1]]
# print(player_center)
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

# def mouseClicked():
#     global , line2_velocity
#     line1_velocity[1] *= -1

get_quad = lambda x, y: (2 if y >= 0 else 4) if (x >= 0) != (y >= 0) else (1 if x >= 0 and y >= 0 else 3)
def keyPressed():
    #global player_angle
    # player_angle = player_angle - 0.1 if key == "a" else (player_angle + 0.1 if key == "d" else 0)
    
    # player[1][0] = 2*player_scale*cos(player_angle) + player_center[0]
    # player[1][1] = 2*player_scale*sin(player_angle) + player_center[1]
    
    # player[2][0] = 3*player_scale*cos(player_angle) + player_center[0]
    # player[2][1] = 3*player_scale*sin(player_angle) + player_center[1]
    print(player[1])
    player_velocity[0] = -10 if key == "a" else (10 if key == "d" else 0)
    player_velocity[1] = -10 if key == "w" else (10 if key == "s" else 0)
def keyReleased():
    player_velocity[0] = 0
    player_velocity[1] = 0
def draw():
    global time_elapsed, player_acceleration, player_velocity
    background(0)
    stroke(255)
    for x, pos in enumerate(player):
        pos[0] += player_velocity[0]
        pos[1] += player_velocity[1]
    for x, pos in enumerate(player):
        line(pos[0], pos[1], player[(x + 1) if x + 1 < len(player) else 0][0], player[(x + 1) if x + 1 < len(player) else 0][1])
    
   #  if not(keyPressed):
   #      player_acceleration[1] += -0.1 if player_velocity[1] > 0 else 0.1
   #      if abs(player_acceleration[1]) < 0.2:
   #          player_acceleration[1] = 0
        
   #  player_velocity[1] = player_acceleration[1] * (time.time()-time_elapsed)
   #  print(player_velocity[1])
   #  time_elapsed = time.time()
    for i, pos in enumerate(player):
        for  ii, target_line in enumerate(lines):
            if i == ii:
                continue
            pos2 = player[(x + 1) if x + 1 < len(player) else 0][0], player[(x + 1) if x + 1 < len(player) else 0][1]
            collided_x, collided_y, xi, yi = LineIntersection(pos[0], pos[1], pos2[0], pos2[0], 
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

        


    
