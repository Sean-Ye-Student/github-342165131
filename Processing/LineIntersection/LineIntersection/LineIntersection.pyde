import time
import random
add_library("minim")

asteroid_type, asteroid_scale, asteroid_origin, asteroid_velocity, asteroid_last_moved = 0, 1, 2, 3, 4
asteroid_type_size, asteroid_type_lines = 0, 1
#chosenLine[random.randint(0, 1)], origin[0], 1.0/2, (chosenLine[random.randint(0, 1) * 2] + origin[0]) * 2
asteroid_to_pixels = lambda i, o, s: i * s + o #lambda i, o, s: (i + o) * s
asteroid_draw_from_origin = lambda i, o, s: (i + o) * s
asteroid_draw_from_pixels = lambda i, o, s: i/s - o
asteroid_to_origin = lambda i, o, s: (i - o)/s#lambda i, o, s: i/s - o
asteroid_types = [
((91, 92), ((13, 15, 38, 0), (38, 0, 51, 25), (51, 25, 78, 13), (78, 13, 91, 40), (91, 40, 74, 58), (74, 58, 77, 81), (77, 81, 42, 92), (42, 92, 14, 83), (14, 83, 0, 56), (0, 56, 13, 15))),
((111, 97), ((0, 25, 42, 25), (42, 25, 28, 0), (28, 0, 69, 0), (69, 0, 111, 26), (111, 26, 111, 36), (111, 36, 70, 48), (70, 48, 110, 72), (110, 72, 83, 97), (83, 97, 70, 83), (70, 83, 29, 96), (29, 96, 0, 60), (0, 60, 0, 25))),
((98, 105), ((13, 75, 25, 55), (25, 55, 18, 31), (18, 31, 40, 14), (40, 14, 60, 27), (60, 27, 82, 20), (82, 20, 98, 43), (98, 43, 78, 51), (78, 51, 95, 76), (95, 76, 71, 105), (71, 105, 41, 90), (41, 90, 30, 99), (30, 99, 13, 75))),
]

asteroids = [
#[random.randint(0, len(asteroid_types) - 1), 1, [0, 0], [60,60], time.time()] for i in range(1)
]
minimum_asteroid_scale = 0.25

lazer_origin, lazer_start, lazer_velocity = 0, 1, 2
lazer_speed = 400
lazers = []
player_scale = 10
player_offset = (250, 250)
player_angle = 0
player_velocity_angle = 0
player_origin = [250, 250] #spawn location, but will change when player moves
player_velocity = [0,0]#will change when player moves
player_acceleration = 5
player_friction = 65
player_control_minimum_range = 10
player_reload_time = 0.25
player_last_shot = 0
player_points = [lambda s, a, o: s*cos(a) + o, lambda s, a, o: s*sin(a) + o,
        lambda s, a, o: -s*cos(-a + 150) + o, lambda s, a, o: s*sin(-a + 150) + o,
        lambda s, a, o: -s*(2.5/6)*cos(a) + o, lambda s, a, o: -s*(2.5/6)*sin(a) + o,
        lambda s, a, o: -s*cos(a + 150) + o, lambda s, a, o: -s*sin(a + 150) + o]

time_elapsed = time.time()
sounds = {"shoot" : {"minim" : "Shoot.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : False, "group" : 1},"explosion" : {"minim" : "Explosion.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : False, "group" : 1}, "siren" : {"minim" : "Siren.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : False, "group" : 1}, "siren2" : {"minim" : "Siren2.mp3", "repeat" : 1, "play_from_start" : True, "isolate" : False, "group" : 1}, "loop" : {"minim" : "Loop.mp3", "repeat" : -1, "play_from_start" : True, "isolate" : True, "group" : 0}}
    
    


sound_kys = ("minim", "repeat", "play_from_start", "isolate", "group")
def PlaySound(sound_name, enabled_keys):
    if not(sound_name in sounds.keys()):
        return
    sound = sounds[sound_name]
    m, repeat, play_from_start, isolate, group = map(None, (sound[ky] if ky in enabled_keys else None for ky in sound_kys))

    if isolate == True:
        for ky in sounds:
            if ky == sound_name:
                continue
            same_group = True if "group" in sounds[ky].keys() and sounds[ky]["group"] == group else False
            if same_group:
                sounds[ky]["minim"].pause()
                
    if m == None:
        return
    if m.isPlaying() == False:
        if play_from_start == True:
            m.rewind()

        if repeat > -1:
            m.loop(repeat - 1)
        else:
            m.loop()
def CreateAsteroid(type, s_scale, origin, velocity):
    global asteroids
    asteroids.append([type, s_scale, origin, [velocity[0], velocity[1]], time.time()])
    
def setup():
    global asteroids
    size(1000, 562)
    minim = Minim(this)
    for ky in sounds:
        sounds[ky]["minim"] = minim.loadFile("sounds/" + sounds[ky]["minim"])


    PlaySound("loop", ("minim", "repeat", "isolate", "group", "play_from_start"))
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
    global  player_angle, player_origin, player_velocity, time_elapsed, player_acceleration, player_velocity_angle, player_last_shot
    offsetX = mouseX - player_origin[0] + 0.0
    offsetY = -(mouseY - player_origin[1] + 0.0)
    if (offsetX**2 + offsetY **2)**0.5 >= player_control_minimum_range:
        player_angle = -atan(offsetY/offsetX) if offsetX != 0 else 0
        player_angle = -(atan(offsetY/offsetX)+3.1) if offsetX != 0 and offsetX < 0 else player_angle
    
    if mousePressed and mouseButton == LEFT and time.time() - player_last_shot > player_reload_time:
        x, y = player_points[0](player_scale, player_angle, player_origin[0]), player_points[1](player_scale, player_angle, player_origin[1])
        xv, yv = cos(player_angle) * lazer_speed, sin(player_angle) * lazer_speed
        lazers.append(((x, y), time.time(), (xv, yv)))
        player_last_shot = time.time()
        PlaySound("shoot", ("minim", "repeat", "isolate", "group", "play_from_start"))
    
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
    
def DrawPlayer():
    points = tuple(formula(player_scale, player_angle, player_origin[0] if i%2 == 0 else player_origin[1]) for i, formula in enumerate(player_points))
    line(points[0], points[1], points[2], points[3])
    line(points[2], points[3], points[4], points[5])
    line(points[4], points[5], points[6], points[7])
    line(points[6], points[7], points[0], points[1])
    
def Asteroids():
    global asteroids
    for asteroid in asteroids:
        elapsed = time.time() - asteroid[asteroid_last_moved]
        asteroid[asteroid_last_moved] = time.time()
        asteroid[asteroid_origin][0] += asteroid[asteroid_velocity][0] * elapsed/asteroid[asteroid_scale]
        asteroid[asteroid_origin][1] += asteroid[asteroid_velocity][1] * elapsed/asteroid[asteroid_scale]
        
        sizes = asteroid_types[asteroid[asteroid_type]][asteroid_type_size]
        sizeX, sizeY = sizes[0] * asteroid[asteroid_scale], sizes[1] * asteroid[asteroid_scale]
        origin = [(asteroid[asteroid_origin][0] * asteroid[asteroid_scale] + sizeX / 2), (asteroid[asteroid_origin][1] * asteroid[asteroid_scale] + sizeY / 2)]
        newX, newY = ScreenEdgeTeleport(origin, sizes[0] / 2, sizes[1] / 2)
        asteroid[asteroid_origin][0], asteroid[asteroid_origin][1] = (newX- sizeX / 2)/asteroid[asteroid_scale], (newY - sizeY / 2)/asteroid[asteroid_scale]
        # s, ao = asteroid[asteroid_scale], asteroid[asteroid_origin] 
        # sizes = asteroid_types[asteroid[asteroid_type]][asteroid_type_size]
        # sizeX, sizeY = sizes[0] * asteroid[asteroid_scale], sizes[1] * asteroid[asteroid_scale]
        # origin = [asteroid_draw_from_pixels(ao[0], sizeX/2, s), asteroid_draw_from_pixels(ao[1], sizeY/2, s)]
        # newX, newY = ScreenEdgeTeleport(origin, sizes[0] / 2, sizes[1] / 2)
        # asteroid[asteroid_origin][0], asteroid[asteroid_origin][1] = asteroid_draw_from_origin(newX, sizeX/2, s), asteroid_draw_from_origin(newY, sizeY/2, s)
        #asteroid_to_pixels(l[0], ao[0], s)
        #asteroid_to_pixels = lambda i, o, s: i * s + o
        #asteroid_to_origin = lambda i, o, s: (i - o)/s



        for i, l in enumerate(asteroid_types[asteroid[asteroid_type]][asteroid_type_lines]):
            s = asteroid[asteroid_scale]
            ao = asteroid[asteroid_origin] 
            # xx, yy = asteroid_draw_from_origin(l[0], ao[0], s), asteroid_draw_from_origin(l[1], ao[1], s)
            # xx2, yy2 =  asteroid_draw_from_origin(l[2], ao[0], s), asteroid_draw_from_origin(l[3], ao[1], s)
            #xx, yy, xx2, yy2 = asteroid_to_pixels(l[0], ao[0], s), asteroid_to_pixels(l[1], ao[1], s), asteroid_to_pixels(l[2], ao[0], s), asteroid_to_pixels(l[3], ao[1], s)
            
            xx, yy, xx2, yy2, axv, ayv = (l[0] + ao[0]) * s, (l[1] + ao[1]) * s, (l[2] + ao[0]) * s, (l[3] + ao[1]) * s, asteroid[asteroid_velocity][0], asteroid[asteroid_velocity][1]
            for iii in range(0, len(player_points), 2):
                s, a, o, o2 = player_scale, player_angle, player_origin[0], player_origin[1]
                x, y = player_points[iii](s, a, o), player_points[iii + 1](s, a, o2)
                x2, y2 = player_points[iii + 1 if iii + 1 < len(player_points) else 0](s, a, o), player_points[iii + 2 if iii + 2 < len(player_points) else 1](s, a, o2)
                collided_x, collided_y, xi, yi = LineIntersection(x, y, x2, y2, player_velocity[0], player_velocity[1], xx, yy, xx2, yy2, axv, ayv)
                #Shows player collisions
                if collided_x or collided_y: 
                    # fill(255, 0, 0)
                    # noStroke()
                    # ellipse(xi, yi, 4, 4)
                    # stroke(255)
                    PlaySound("siren2", ("minim", "repeat", "isolate", "group", "play_from_start"))
                    #print(frameRate)
                    break
                # else:
                #     fill(255)
            line(xx, yy, xx2, yy2)
            
def Lazers():
    global lazers
    remove_lazer_indexes = []
    for ii, lazer in enumerate(lazers):
        elapsed = time.time() - lazer[lazer_start]
        newX, newY = lazer[lazer_origin][0] + lazer[lazer_velocity][0] * elapsed, lazer[lazer_origin][1] + lazer[lazer_velocity][1] * elapsed
        x, y = ScreenEdgeTeleport((newX, newY), 1, 1)
        if x != newX or y != newY:
            remove_lazer_indexes.append(ii)
            continue
    
        noSmooth()
        point(newX, newY)
        closest_index, closest_intersection, closest_to_origin = -1, (-1, -1), 10**6
        for a, asteroid in enumerate(asteroids):
            ao = asteroid[asteroid_origin]
            for i, l in enumerate(asteroid_types[asteroid[asteroid_type]][asteroid_type_lines]):
                s = asteroid[asteroid_scale]
                
                xx, yy, xx2, yy2, axv, ayv = (l[0] + ao[0]) * s, (l[1] + ao[1]) * s, (l[2] + ao[0]) * s, (l[3] + ao[1]) * s, asteroid[asteroid_velocity][0], asteroid[asteroid_velocity][1]
                ox, oy, xv, yv = lazer[lazer_origin][0], lazer[lazer_origin][1], lazer[lazer_velocity][0], lazer[lazer_velocity][1]
                x, y, x2, y2 = ox, oy, ox + xv * elapsed, oy + yv * elapsed
                collidedX, collidedY, xi, yi = LineIntersection(x, y, x2, y2, xv, yv, xx, yy, xx2, yy2, axv, ayv)
                if collidedX and collidedY:
                    if ((ox - xi)**2 + (oy - yi)**2)**0.5 < closest_to_origin:
                        closest_to_origin = ((ox - xi)**2 + (oy - yi)**2)**0.5
                        closest_index, closest_intersection = a, (xi, yi)
                    break
                else:
                    fill(255)

        if closest_index > -1:
            # fill(255, 0, 0)
            # noStroke()
            # ellipse(closest_intersection[0], closest_intersection[1], 4, 4)
            # stroke(255)
            remove_lazer_indexes.append(ii)
            parent = asteroids.pop(closest_index)
            origin, scaleing, lines = parent[asteroid_origin], parent[asteroid_scale], asteroid_types[parent[asteroid_type]][asteroid_type_lines]
            PlaySound("explosion", ("minim", "repeat", "isolate", "group", "play_from_start"))
            for _ in range(2):
                if parent[asteroid_scale]/2.0 < minimum_asteroid_scale:
                    break

                # newOrigin = [asteroid_to_origin(awf, origin[0], 2), asteroid_to_origin(chosenLine[random.randint(0, 1) * 2 + 1], origin[1], 2)]
                # newVelocity = [parent[asteroid_velocity][0] * (1.5**0.5),  parent[asteroid_velocity][1] * (1.5**0.5)]
                # print(newOrigin[0], (awf + origin[0]) * 2)
                # CreateAsteroid(parent[asteroid_type], parent[asteroid_scale]/2.0, newOrigin, newVelocity)
                chosenLine = lines[random.randint(0, len(lines) - 1)]
                newOrigin = [(chosenLine[random.randint(0, 1) * 2] + origin[0]) * 2, (chosenLine[random.randint(0, 1) * 2 + 1] + origin[1]) * 2]
                newVelocity = [parent[asteroid_velocity][0] * (1.5**0.5),  parent[asteroid_velocity][1] * (1.5**0.5)]
                CreateAsteroid(parent[asteroid_type], parent[asteroid_scale]/2.0, newOrigin, newVelocity)
                
                # type = #random.randint(0, len(asteroid_types) - 1)
                # chosenLine = lines[random.randint(0, len(lines) - 1)]

                # newAsteroid = [type, saze/2.0, newOrigin, [random.randint(-60, 60),random.randint(-60, 60)], time.time()]
                # asteroids.append(newAsteroid)
    
    i = 0
    r = 0
    while i + r < len(lazers) and len(remove_lazer_indexes) > 0:
        if i + r == remove_lazer_indexes[0]:
            lazers.pop(i + r)
            remove_lazer_indexes.pop(0)
            r += 1
        else: 
            i += 1
spawn_cooldown = 3
last_spawned = time.time()
spawn_reduce = 0.5
min_spawn_cooldown = 1.0/1.5
maximum_asteroids = 1
def draw():
    global last_spawned, spawn_cooldown, asteroids
    #print(len(asteroids), (asteroid_to_pixels(asteroids[0][asteroid_origin][0], asteroid_types[asteroids[0][asteroid_type]][asteroid_type_size][0]/2, 0.5), asteroid_to_pixels(asteroids[0][asteroid_origin][1], asteroid_types[asteroids[0][asteroid_type]][asteroid_type_size][1]/2, 0.5)) if len(asteroids) > 0 else "none")
    #len(asteroids) < maximum_asteroids and
    if  time.time() > last_spawned + spawn_cooldown:
        type = random.randint(0, len(asteroid_types) - 1)
        minX, maxX = 0 - asteroid_types[type][asteroid_type_size][0], width + asteroid_types[type][asteroid_type_size][0]
        minY, maxY = 0 - asteroid_types[type][asteroid_type_size][0], height + asteroid_types[type][asteroid_type_size][0]
        on_sides = random.randint(0, 1) == 0
        originX = (minX if random.randint(0, 1) == 0 else maxX) if on_sides else random.randint(minX, maxX)
        originY = random.randint(minY, maxY) if on_sides else (minY if random.randint(0, 1) == 0 else maxY) 
        xv, yv = -1 if random.randint(0, 1) == 0 else 1, -1 if random.randint(0, 1) == 0 else 1
        CreateAsteroid(type, 1, [originX, originY], [60 * xv, 60 * yv])
        
        spawn_cooldown *= spawn_reduce
        spawn_cooldown = max(spawn_cooldown, min_spawn_cooldown)
        last_spawned = time.time()
    background(0)
    stroke(255)
    PlayerController()
    DrawPlayer()
    Asteroids()
    Lazers()
