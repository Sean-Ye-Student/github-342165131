origin = [250, 250]

def setup():
    size(500, 500)
get_quad = lambda x, y: (2 if y >= 0 else 4) if (x >= 0) != (y >= 0) else (1 if x >= 0 and y >= 0 else 3)
get_quad_angle = lambda is_sin, is_cos, is_tan, a: (sin(a%360) if 0 <= a < 180 else -sin(a%360)) if is_sin else ((cos(a%360) if 0 <= a <= 90 or 270 <= a < 360 else -cos(a%360)) if is_cos else (tan(a%360) if 0 <= a <= 90 or 180 <= a < 270 else -tan(a%360)) if is_tan else None)
angle = 0
s = 100
offset = 0
speed = 5
def mouseWheel(event):
    global offset
    offset += event.getCount()*0.1
is_pressed = {"w" : False, "a" : False, "s" : False, "d" : False}
def keyPressed():
    global is_pressed
    is_pressed[key] = True
def keyReleased():
    global is_pressed
    is_pressed[key] = False
def draw():
    global angle, new_points,s, origin
    background(255)
    if is_pressed["w"]:
        origin[0] += speed * cos(angle)
        origin[1] += speed * sin(angle)
    offsetX = mouseX - origin[0] + 0.0
    offsetY = -(mouseY - origin[1] + 0.0)
    angle = -atan(offsetY/offsetX) if offsetX != 0 else 0 #(atan(offsetY/offsetX) if (offsetX > 0 and offsetY < 0) or (offsetX < 0 and offsetY > 0) else -atan(offsetY/offsetX)) if offsetX != 0 else 0
    angle = -(atan(offsetY/offsetX)+3.1) if offsetX != 0 and offsetX < 0 else angle
    print(offsetX, offsetY)    
    
    pos_x = s*cos(angle) + origin[0]
    pos_y = s*sin(angle) + origin[1]
    pos_x1 = -s*cos(-angle + 150) + origin[0]
    pos_y1 = s*sin(-angle + 150) + origin[1]
    pos_x2 = -s*(2.5/6)*cos(angle) + origin[0]
    pos_y2 = -s*(2.5/6)*sin(angle) + origin[1]
    pos_x3 = -s*cos(angle + 150) + origin[0]
    pos_y3 = -s*sin(angle + 150) + origin[1]
    line(pos_x, pos_y, pos_x1, pos_y1)
    line(pos_x1, pos_y1, pos_x2, pos_y2)
    line(pos_x2, pos_y2, pos_x3, pos_y3)
    line(pos_x3, pos_y3, pos_x, pos_y)
    
    #pos_x2 = s*get_quad_angle(False, True, False, angle + 150) + origin[0]
    #pos_y2 = s*get_quad_angle(True, False, False, angle + 150) + origin[1]
    # line(pos_x, pos_y, pos_x1, pos_y1)
    # line(pos_x1, pos_y1, pos_x2, pos_y2)
    # line(pos_x2, pos_y2, pos_x, pos_y)
