from turtle import Turtle, Screen
import random

# Screen setup
my_screen = Screen()
my_screen.mode("logo")
my_screen.setup(width=800, height=800)
my_screen.register_shape("C:/Users/Tiaan/Desktop/Tiaan Program/Python Projects/PythonTiaan/Snake/snake.gif")
my_screen.register_shape("C:/Users/Tiaan/Desktop/Tiaan Program/Python Projects/PythonTiaan/Snake/snakebody.gif")
my_screen.register_shape("C:/Users/Tiaan/Desktop/Tiaan Program/Python Projects/PythonTiaan/Snake/apple.gif")
my_screen.bgcolor("lightblue")
my_screen.title("Turtle Snake Game")

# Global game state
GameOver = False
Score = 0

# Scoreboard and border
my_border = Turtle()
scoreboard = Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.goto(-380, 360)
scoreboard.color("black")
scoreboard.write(f"Score: {Score}", align="left", font=("Arial", 18, "normal"))

def draw_border():
    my_border.hideturtle()
    my_border.speed(0)
    for i in range(1, 800, 80):
        my_border.penup()
        my_border.goto(-400 + i, -400)
        my_border.pendown()
        my_border.goto(-400 + i, 400)
        my_border.penup()
        my_border.goto(-400, -400 + i)
        my_border.pendown()
        my_border.goto(400, -400 + i)

class Snake:
    def __init__(self):
        self.segments = []
        self.direction = "right"
        self.next_direction = "right"
        self.create_snake()
        self.can_turn = True

    def create_snake(self):
        starting_positions = [(40, 0), (-40, 0), (-120, 0)]
        for pos in starting_positions:
            self.add_segment(pos)
        self.head = self.segments[0]
        self.head.shape("C:/Users/Tiaan/Desktop/Tiaan Program/Python Projects/PythonTiaan/Snake/snake.gif")


    def add_segment(self, position):
        segment = Turtle("turtle")
        segment.shape("C:/Users/Tiaan/Desktop/Tiaan Program/Python Projects/PythonTiaan/Snake/snakebody.gif")
        segment.shapesize(stretch_wid=6, stretch_len=6)
        segment.penup()
        segment.goto(position)
        self.segments.append(segment)

    def move(self):
        global Score

        # Move body segments
        for i in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[i - 1].xcor()
            new_y = self.segments[i - 1].ycor()
            self.segments[i].goto(new_x, new_y)

        # Apply direction change
        if self.can_change_direction(self.next_direction):
            self.direction = self.next_direction

        x, y = self.head.position()
        if self.direction == "up":
            self.head.goto(x, y + 80)
        elif self.direction == "down":
            self.head.goto(x, y - 80)
        elif self.direction == "left":
            self.head.goto(x - 80, y)
        elif self.direction == "right":
            self.head.goto(x + 80, y)

        # Border collision
        if abs(self.head.xcor()) > 390 or abs(self.head.ycor()) > 390:
            self.game_over()
            return

        # Apple collision
        if self.head.distance(my_apple.position()) < 60: 
            my_apple.AppleGoto()
            self.grow()
            Score += 1
            scoreboard.clear()
            scoreboard.write(f"Score: {Score}", align="left", font=("Arial", 18, "normal"))

        # Self collision
        for segment in self.segments[1:]:
            if self.head.distance(segment) < 10:
                self.game_over()
                return

        self.can_turn = True
        
        if not GameOver:
            my_screen.ontimer(self.move, 200)

    def can_change_direction(self, new_dir):
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        return opposites[self.direction] != new_dir

    def go_up(self):
        if not GameOver:
            self.next_direction = "up"
            self.can_turn = False

    def go_down(self):
        if not GameOver:
            self.next_direction = "down"
            self.can_turn = False

    def go_left(self):
        if not GameOver:
            self.next_direction = "left"
            self.can_turn = False

    def go_right(self):
        if not GameOver:
            self.next_direction = "right"
            self.can_turn = False

    def grow(self):
        self.add_segment(self.segments[-1].position())

    def game_over(self):
        global GameOver
        GameOver = True
        scoreboard.goto(0, 0)
        scoreboard.write("Game Over!", align="center", font=("Arial", 24, "bold"))

class Apple(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("C:/Users/Tiaan/Desktop/Tiaan Program/Python Projects/PythonTiaan/Snake/apple.gif")
        self.shapesize(stretch_wid=6, stretch_len=6)
        self.penup()
        self.speed(0)

    def AppleGoto(self):
        x = random.choice(range(-360 , 361, 80))
        y = random.choice(range(-360 , 361, 80))
        self.goto(x, y)

# Setup
my_snake = Snake()
my_apple = Apple()
my_apple.AppleGoto()
draw_border()

# Controls
my_screen.onkey(my_snake.go_up, "Up")
my_screen.onkey(my_snake.go_down, "Down")
my_screen.onkey(my_snake.go_left, "Left")
my_screen.onkey(my_snake.go_right, "Right")
my_screen.listen()

# Start game
my_snake.move()
my_screen.mainloop()
