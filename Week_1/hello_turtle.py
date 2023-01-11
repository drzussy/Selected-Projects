import turtle

def draw_triangle():
    '''draw triangle'''
    turtle.down()
    for i in range(3):
        turtle.forward(45)
        turtle.right(120)

def draw_sail():
    '''draw sail'''
    turtle.down()
    turtle.left(90)
    turtle.forward(50)
    turtle.right(150)
    draw_triangle()
    turtle.right(30)
    turtle.up()
    turtle.forward(50)
    turtle.down()
    turtle.left(90)

def draw_ship():
    '''draw ship that has three sails'''
    turtle.down()
    turtle.right(90)
    #draw top of ship
    for i in range(3):
        turtle.forward(50)
        draw_sail()
    turtle.forward(50)
    #draw bottom of ship
    turtle.right(120)
    turtle.forward(20)
    turtle.right(60)
    turtle.forward(180)
    turtle.right(60)
    turtle.forward(20)
    turtle.right(30)
    turtle.up()

def draw_fleet():
    '''draw two ships and return to original spot'''
    #reorient turtle
    turtle.left(90)
    draw_ship()
    #walk to next ship and draw
    turtle.left(90)
    turtle.forward(300)
    turtle.right(90)
    draw_ship()
    #go back to start
    turtle.right(90)
    turtle.forward(300)

if __name__ == '__main__':
    draw_fleet()
    
    #end of code
    turtle.done()


