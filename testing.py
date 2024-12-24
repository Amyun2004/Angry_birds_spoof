from graphics import *
from math import *
from random import *

# Constants
WIN_WIDTH = 1000
WIN_HEIGHT = 600
GROUND_HEIGHT = 50  # Ground height
ELASTICITY = 0.6 # Coefficient of restitution (0 for inelastic, 1 for elastic)
FRICTION = 0.98  # Friction coefficient for blocks and balls
FPS = 60
DT = 1 / FPS
GRAVITY = -300# Gravitational acceleration (pixels/s^2)
MAX_ELASTIC_LENGTH = 100  # Maximum stretch length for the elastic
Loaded = True
score = 0
def update_score(hit_object, score):
    if isinstance(hit_object, Ball):
        score += 10  # Ball = 10 points
    elif isinstance(hit_object, Block):
        score += 5   # Block = 5 points
    return score

class Ball:
    def __init__(self, win, x, y, radius, mass, color,loaded=False):
        self.win = win
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.vx = 0
        self.vy = 0
        self.loaded = loaded
        self.shape = Circle(Point(x, y), radius)
        self.shape.setFill(color)
        self.shape.draw(win)

    def move(self,x=0,y=0): 
        if self.loaded:
            return 
        # Update velocity due to gravity
        self.vy += GRAVITY * DT

        # Apply friction if on the ground
        if self.y - self.radius <= GROUND_HEIGHT:
            self.vx *= FRICTION
            self.vy = max(self.vy, 0)  # Prevent upward movement on the ground

        # Update position
        self.x += self.vx * DT
        self.y += self.vy * DT

        # Wall collisions
        if self.x - self.radius < 0 or self.x + self.radius > WIN_WIDTH:
            self.vx *= -ELASTICITY
            self.x = max(self.radius, min(self.x, WIN_WIDTH - self.radius))
        if self.y - self.radius < GROUND_HEIGHT:  # Ground collision
            self.vy *= -ELASTICITY
            self.y = GROUND_HEIGHT + self.radius

        self.update_shape()

    def update_shape(self):
        self.shape.move(self.x - self.shape.getCenter().getX(), self.y - self.shape.getCenter().getY())

    def set_velocity(self, ur, angle):
        """Launch the ball with an initial speed (ur) and angle (degrees)."""
        angle = radians(angle)
        self.vx = ur * cos(angle)
        self.vy = ur * sin(angle)
        self.loaded = False

    def is_dead(self): 
        # velocty zero checker
        return abs(self.vx)<0.1 and abs(self.vy) < 0.1


class Block:
    def __init__(self, win, x, y, width, height, mass, color, health = 2):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.vx = 0
        self.vy = 0
        self.health = health
        self.shape = Rectangle(Point(x - width / 2, y), Point(x + width / 2, y + height))
        self.shape.setFill(color)
        self.shape.draw(win)

    def move(self):
        # Update velocity due to gravity
        self.vy += GRAVITY * DT

        # Apply friction if on the ground
        if self.y <= GROUND_HEIGHT:
            self.vx *= FRICTION
            if self.vy < 0:
                self.vy = 0
  # Prevent upward movement on the ground

        # Update position
        self.x += self.vx * DT
        self.y += self.vy * DT

        # Wall collisions
        if self.x - self.width / 2 < 0 or self.x + self.width / 2 > WIN_WIDTH:
            self.vx *= -ELASTICITY
            if self.x < self.width / 2:  
                self.x = self.width / 2  # Prevent going beyond the left boundary
            elif self.x > WIN_WIDTH - self.width / 2:  
                self.x = WIN_WIDTH - self.width / 2  # Prevent going beyond the right boundary

        if self.y < GROUND_HEIGHT:  # Ground collision
            self.vy *= -ELASTICITY
            self.y = GROUND_HEIGHT

        self.update_shape()

    def update_shape(self):
        dx = self.x - (self.shape.getP1().getX() + self.shape.getP2().getX()) / 2
        dy = self.y - self.shape.getP1().getY()
        self.shape.move(dx, dy)

    def damage(self, ball_color): 
        if ball_color == "red": 
            self.health = 0 # destroy immediatly
        else: 
            self.health -= 1 
        if self.health<=0: 
            self.shape.undraw()
            return True # destroyed
        return False # 


def check_ball_ball_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = sqrt(dx ** 2 + dy ** 2)

    if distance < ball1.radius + ball2.radius:  # Collision detected
        # Find collision angle
        angle = atan2(dy, dx)

        # Velocity components along the collision axis
        v1 = ball1.vx * cos(angle) + ball1.vy * sin(angle)
        v2 = ball2.vx * cos(angle) + ball2.vy * sin(angle)

        # Post-collision velocities (1D elastic collision equations)
        # principle of momentum with elasticity 
        v1_final = ((ball1.mass - ELASTICITY * ball2.mass) * v1 +
                    (1 + ELASTICITY) * ball2.mass * v2) / (ball1.mass + ball2.mass)
        v2_final = ((ball2.mass - ELASTICITY * ball1.mass) * v2 +
                    (1 + ELASTICITY) * ball1.mass * v1) / (ball1.mass + ball2.mass)

        # Update velocities along the collision axis
        ball1.vx = v1_final * cos(angle) - ball1.vy * sin(angle)
        ball1.vy = v1_final * sin(angle) + ball1.vy * cos(angle)
        ball2.vx = v2_final * cos(angle) - ball2.vy * sin(angle)
        ball2.vy = v2_final * sin(angle) + ball2.vy * cos(angle)

        # Resolve overlap
        overlap = 0.5 * (ball1.radius + ball2.radius - distance)
        ball1.x -= overlap * cos(angle)
        ball1.y -= overlap * sin(angle)
        ball2.x += overlap * cos(angle)
        ball2.y += overlap * sin(angle)
        return True
    return False


def check_ball_block_collision(ball, block):
    # Simple bounding box check
    if ball.x < block.x - block.width / 2:
        closest_x = block.x - block.width / 2
    elif ball.x > block.x + block.width / 2:
        closest_x = block.x + block.width / 2
    else:
        closest_x = ball.x

    # Compute closest_y
    if ball.y < block.y:
        closest_y = block.y
    elif ball.y > block.y + block.height:
        closest_y = block.y + block.height
    else:
        closest_y = ball.y

    dx = ball.x - closest_x
    dy = ball.y - closest_y
    distance = sqrt(dx ** 2 + dy ** 2)

    if distance < ball.radius:  # Collision detected
        # Find angle of collision
        angle = atan2(dy, dx)

        # Momentum transfer from ball to block
        block.vx += (ball.mass / block.mass) * ball.vx * ELASTICITY
        block.vy += (ball.mass / block.mass) * ball.vy * ELASTICITY

        # Update ball velocity
        ball.vx *= -ELASTICITY
        ball.vy *= -ELASTICITY

        # Resolve overlap
        overlap = ball.radius - distance
        overlap_x = overlap * (dx / distance) if distance != 0 else 0
        overlap_y = overlap * (dy / distance) if distance != 0 else 0
        ball.x += overlap_x
        ball.y += overlap_y
        return True
    return False


def check_block_block_collision(block1, block2):
    # Simple bounding box check
    if (block1.x + block1.width / 2 > block2.x - block2.width / 2 and
        block1.x - block1.width / 2 < block2.x + block2.width / 2 and
        block1.y + block1.height > block2.y and
        block1.y < block2.y + block2.height):
        
        # Find overlap in both directions
        overlap_x = min(block1.x + block1.width / 2 - block2.x + block2.width / 2,
                        block2.x + block2.width / 2 - block1.x + block1.width / 2)
        overlap_y = min(block1.y + block1.height - block2.y, block2.y + block2.height - block1.y)
        
        # Push blocks apart to resolve overlap
        if overlap_x < overlap_y:  # Push horizontally
            push = overlap_x / 2
            if block1.x < block2.x:
                block1.x -= push
                block2.x += push
            else:
                block1.x += push
                block2.x -= push
        else:  # Push vertically
            push = overlap_y / 2
            if block1.y < block2.y:
                block1.y -= push
                block2.y += push
            else:
                block1.y += push
                block2.y -= push
        
        # Update velocities (basic elastic collision)
        block1.vx, block2.vx = block2.vx, block1.vx
        block1.vy, block2.vy = block2.vy, block1.vy



def check_all_collisions(balls, blocks,score):
     # Use the global score variable

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if check_ball_ball_collision(balls[i], balls[j]):
                score += 10
                print("Ball-to-Ball collision! +10 points")
                print(score)

    # Ball-to-Block collisions
    for ball in balls:
        for block in blocks:
            if check_ball_block_collision(ball, block):
                score += 5
                print("Ball-to-Block collision! +5 points")

    # Block-to-Block collisions
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            check_block_block_collision(blocks[i], blocks[j])
    return score
    

# Slingshot Class
class Slingshot:
    def __init__(self, win):
        self.win = win
        self.color = "brown"
        self.loaded = None
        self.elastic_left = None
        self.elastic_right = None
        self.object = None

    def draw_static_parts(self):
        # Base and arms
        base = Rectangle(Point(145, 40), Point(155, 100))
        base.setFill(self.color)
        base.draw(self.win)

        left_arm = Line(Point(150, 100), Point(125, 150))
        left_arm.setWidth(5)
        left_arm.setFill(self.color)
        left_arm.draw(self.win)

        right_arm = Line(Point(150, 100), Point(175, 150))
        right_arm.setWidth(5)
        right_arm.setFill(self.color)
        right_arm.draw(self.win)

    def draw_dynamic_parts(self):
        # Ensure elastic bands are cleared first
        if self.elastic_left:
            self.elastic_left.undraw()
        if self.elastic_right:
            self.elastic_right.undraw()

        # Fixed anchor points for elastic bands
        anchor_left = Point(135, 125)
        anchor_right = Point(165, 125)

        if self.loaded:
            # Calculate distance and enforce limit
            max_length = 100  # Maximum allowed length for the elastic
            dx = self.loaded.getX() - anchor_left.getX()
            dy = self.loaded.getY() - anchor_left.getY()
            distance = hypot(dx, dy)

            if distance > max_length:
                # Adjust position to be within max_length
                scale = max_length / distance
                adjusted_x = anchor_left.getX() + dx * scale
                adjusted_y = anchor_left.getY() + dy * scale
                self.loaded = Point(adjusted_x, adjusted_y)

            # Draw elastic bands
            self.elastic_left = Line(anchor_left, self.loaded)
            self.elastic_left.setWidth(3)
            self.elastic_left.setFill("black")
            self.elastic_left.draw(self.win)

            self.elastic_right = Line(anchor_right, self.loaded)
            self.elastic_right.setWidth(3)
            self.elastic_right.setFill("black")
            self.elastic_right.draw(self.win)

            # Update ball position if object is loaded
            if self.object and isinstance(self.object, Ball):
                center = self.object.shape.getCenter()
                dx = self.loaded.getX() - center.getX()
                dy = self.loaded.getY() - center.getY()
                self.object.shape.move(dx, dy)
                self.object.x = self.loaded.getX()
                self.object.y = self.loaded.getY()


    def attach_object(self, obj):
        self.object = obj

    def release_object(self, velocity, angle):
        global Loaded
        if self.object:
            self.object.set_velocity(velocity, angle)
            self.object = None
        if self.elastic_left:
            self.elastic_left.undraw()
        if self.elastic_right:
            self.elastic_right.undraw()
        Loaded = False