def setup():
    background(100)
    size(200, 200)
lines = [(40,40,30,50), (30,50, 40, 60), (40,60,30,70), (60,40,70,60), (80,40,70,60), (70,80,70,60), (50, 70, 50, 70)]


def draw():
    global letters
    print(mouseX, mouseY)
    for l in lines:
        strokeWeight(10)
        line(l[0], l[1], l[2], l[3])
