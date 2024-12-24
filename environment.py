from graphics import *
from math import *
from testing import *  # Assuming Ball and Block classes are defined in testing.py

# Constants
WIN_WIDTH = 1000
WIN_HEIGHT = 700
GROUND_HEIGHT = 50
FPS = 60
MAX_ELASTIC_LENGTH = 150  # Maximum stretch length


# Background function
def background(width, height):
    global win
    win = GraphWin("Angry Birds", width, height, autoflush=False)
    win.setCoords(0, 0, width, height)
    
    a = 120
    b = 221
    c =  250

    # Sky
    number_of_rectangles = 100
    rect_height = height // number_of_rectangles
    for i in range(number_of_rectangles, -1, -1):
        if a <= 207: 
            a += 2
        if b <= 234: 
            b += 2
        if c <= 247:
            c += 2
        rect = Rectangle(Point(0, rect_height * i), Point(width, rect_height * (i + 1)))
        rect.setFill(color_rgb(a, b, c))
        rect.setOutline(color_rgb(a, b, c))
        rect.draw(win)

    # Ground
    ground = Rectangle(Point(0, 0), Point(width, 30))
    ground.setFill("#594233")
    ground.draw(win)

    # Grass
    grass = Rectangle(Point(0, 30), Point(width, 40))
    grass.setFill("#bed93c")
    grass.draw(win)


# Main Function
def main():
    global score
    background(WIN_WIDTH, WIN_HEIGHT)
    score_text = Text(Point(50, 590), f"Score: {score}")  # Position it at the top
    score_text.setSize(12)
    score_text.setTextColor("Black")
    score_text.draw(win)
    # Blocks and Balls

    blocks = [
        Block(win, 620, GROUND_HEIGHT , 20, 100, 400, "brown"),
        Block(win, 880, GROUND_HEIGHT , 20, 100, 400, "black"),
        Block(win, 750, GROUND_HEIGHT , 20, 100, 400, "black"),
        Block(win, 815, GROUND_HEIGHT , 20, 100, 400, "black"),
        Block(win, 750, GROUND_HEIGHT + 50, 360, 30, 200, "purple"),
        Block(win, 650, GROUND_HEIGHT + 150, 20, 100, 100, "green"),
        
        Block(win, 820, GROUND_HEIGHT + 150, 20, 100, 100, "red"),
        Block(win, 750, GROUND_HEIGHT + 150, 20, 100, 100, "green"),
        Block(win, 750, GROUND_HEIGHT + 200, 260, 30, 100, "white"),
        Block(win, 700, GROUND_HEIGHT + 250, 20, 100, 50, "blue"),
        Block(win, 780, GROUND_HEIGHT + 250, 20, 100, 50, "yellow"),
        
        Block(win, 745, GROUND_HEIGHT + 300, 150, 30, 5, "lightblue"),
    ]
    balls = [
        Ball(win, 150, 125, 10, 100, "red",
             loaded=True),
        Ball(win, 700, 300, 15, 80, "green"),
        Ball(win, 800, 100, 15, 200, "green"),
    ]

    # Create Slingshot
    slingshot = Slingshot(win)
    slingshot.draw_static_parts()

    # Attach the first ball to the slingshot
    current_ball = balls[0]
    slingshot.attach_object(current_ball)

    dragging = False
    bird_count = 0
    while bird_count!=5 :
        click = win.checkMouse()
        if click:
            # Check and limit the elastic length realistically
            anchor_x, anchor_y = 150, 125  # Slingshot anchor points
            dx = anchor_x - click.getX()
            dy = anchor_y - click.getY()
            distance = hypot(dx, dy)
            
            # Limit the elastic length
            if distance >= MAX_ELASTIC_LENGTH:
                scale = MAX_ELASTIC_LENGTH / distance
                click = Point(anchor_x - dx * scale, anchor_y - dy * scale)

            slingshot.loaded = click
            slingshot.draw_dynamic_parts()
            dragging = True

        key = win.checkKey()
        if key == "r" and dragging:
            # Calculate velocity based on elastic stretch
            dx = anchor_x - slingshot.loaded.getX()
            dy = anchor_y - slingshot.loaded.getY()
            stretch_length = hypot(dx, dy)

            # Assign velocity based on stretch length
            if stretch_length >= MAX_ELASTIC_LENGTH-50:
                velocity = 1000  # Max stretch → Max velocity
            elif stretch_length >= MAX_ELASTIC_LENGTH / 2:
                velocity = 500  # Half stretch → Medium velocity
            else:
                velocity = 200  # Less than half → Low velocity

            angle = degrees(atan2(dy, dx))  # Launch angle
            slingshot.release_object(velocity, angle)
            dragging = False

        # Update ball and blocks
        for ball in balls:
            ball.move()
        for block in blocks:
            block.move()
        
        current_ball.move()
        for block in blocks:
            block.move()

        score = check_all_collisions(balls, blocks,score)
        score_text.setText(f"Score: {score}")
        
        
        if current_ball.is_dead() and not slingshot.object:
            # Create a new ball and add it to the list
            new_ball = Ball(win, 150, 125, 10, 100, "red",loaded= True)
            bird_count +=1 
            balls.append(new_ball)
            slingshot.attach_object(new_ball)
            current_ball = new_ball

        
        update(FPS)

    # Display End Game Message
    if score > 100000: 
        congrats = Text(Point(500, 500), "Yeppp, You Won!")
        congrats.setSize(36)
        congrats.setTextColor("green")
        congrats.setStyle("bold")
        congrats.draw(win)
    else: 
        text = Text(Point(500, 500), "Try Again Next Time")
        text.setSize(36)
        text.setTextColor("red")
        text.setStyle("bold")
        text.draw(win)

    # Wait for user input to quit the game
    win.getMouse()
    win.close()
# Run the Game
main()

