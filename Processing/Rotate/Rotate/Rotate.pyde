origin = (250, 250)
def setup():
    size(500, 500)
get_quad = lambda x, y: (2 if y >= 0 else 4) if (x >= 0) != (y >= 0) else (1 if x >= 0 and y >= 0 else 3)
angle = 0

def draw():
    global angle, new_points
    background(255)
    if keyPressed:
        angle += 5 if key == "d" else (-5 if key == "a" else 0)
    
    pos_x = cos(angle)
    pos_y = 
    
