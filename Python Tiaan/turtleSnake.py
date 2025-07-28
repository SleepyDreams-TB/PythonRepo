from turtle import Turtle, Screen
import random
my_screen = Screen()
my_screen.mode("logo") 
my_screen.setup(width=800, height=800)

global GameOver 
GameOver= False
global Score
Score = 0
direction = 0

my_border = Turtle()
my_screen.listen()
my_screen.listen()


scoreboard = Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.goto(-380, 360)
scoreboard.color("black")
scoreboard.write(f"Score: {Score}", align="left", font=("Arial", 18, "normal"))

def draw_border():
    my_border.hideturtle()
    my_border.penup()
    my_border.goto(-400, -400)
    my_border.pendown()
    
    for i in range(4):
        my_border.forward(800)
        my_border.left(90)

    #Grid
    for i in range(1, 800, 80):
        my_border.speed(0)
        my_border.penup()
        my_border.goto(-400 + i, -400)
        my_border.pendown()
        my_border.goto(-400 + i, 400)
        my_border.penup()
        my_border.setheading(0)
        my_border.goto(-400, -400 + i)
    
    for i in range(1, 800, 80):
        my_border.speed(0)
        my_border.penup()
        my_border.goto(-400, -400 + i)
        my_border.setheading(0)
        my_border.pendown()
        my_border.goto(400, -400 + i)

class Snake:
    def __init__(self):
        self.segments = []
        self.color = "blue"
        self.create_snake()
        self.head = self.segments[0]
        self.direction = 0  

    def create_snake(self):
        starting_positions = [(0, 0), (-20, 0), (-40, 0)]
        for position in starting_positions:
            self.add_segment(position)

    def add_segment(self, position):
        segment = Turtle("turtle")
        segment.color("blue")
        segment.penup()
        segment.goto(position)
        self.segments.append(segment)

    def move(self):
        global GameOver, Score
        for i in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[i - 1].xcor()
            new_y = self.segments[i - 1].ycor()
            self.segments[i].goto(new_x, new_y)

        self.head.forward(80) 
        if abs(self.head.xcor()) > 390 or abs(self.head.ycor()) > 390:
            GameOver = True
            print("Game Over!")
            return

        if self.head.distance(my_apple) < 20:
            my_apple.AppleGoto()
            self.grow()
            Score += 1
            scoreboard.clear()
            scoreboard.write(f"Score: {Score}", align="left", font=("Arial", 18, "normal"))

        if not GameOver:
            my_screen.ontimer(self.move, 1000)

    def go_up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def go_down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def go_left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def go_right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def grow(self):
        self.add_segment(self.segments[-1].position())


class apple(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("red")
        self.penup()
        self.speed(0)
        
    def AppleGoto(self):
        x = random.choice(range(-360, 360, 20))
        y = random.choice(range(-360, 360, 20))
        self.goto(x, y)
    

my_snake = Snake()
my_screen.onkey(my_snake.go_up, "Up")
my_screen.onkey(my_snake.go_down, "Down")
my_screen.onkey(my_snake.go_left, "Left")
my_screen.onkey(my_snake.go_right, "Right")

if not GameOver:
    draw_border()
    my_apple = apple()
    my_snake.move()
    if my_snake.move():
        my_snake.move()

my_screen.mainloop()