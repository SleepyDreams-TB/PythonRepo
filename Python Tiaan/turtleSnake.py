from turtle import Turtle, Screen
import random
my_screen = Screen()
my_screen.mode("logo") 
my_screen.setup(width=800, height=800)

global GameOver 
GameOver= False
direction = 0

class Snake(Turtle):
    def __init__(self, color="blue", speed=1):
            super().__init__()
            self.shape("turtle")
            self.color(color)
            self.penup()
            self.speed(speed)
    
    def move(self):
        self.forward(10)
        
        if abs(self.xcor()) > 390 or abs(self.ycor()) > 390:
            global GameOver
            GameOver= True
            print("Game Over!")
            return
        if not GameOver:
            # Check for collision with the apple
            if self.distance(my_apple) < 15:
               my_apple.goto(random.choice(range(-400, 400)), random.choice(range(-400, 400)))
               global Score
               Score += 1
               
        my_screen.ontimer(self.move, 200)

    def go_up(self):
        if self.heading() != 180:
            self.setheading(0)

    def go_down(self):
        if self.heading() != 0:
            self.setheading(180)

    def go_left(self):
        if self.heading() != 90:
            self.setheading(270)

    def go_right(self):
        if self.heading() != 270:
            self.setheading(90)

    #def grow():     

class apple(Turtle):
    def __init__(self, color="red", speed=0):
        super().__init__()
        self.shape("turtle")
        self.color(color)
        self.penup()
        self.speed(speed)
        

def draw_border():
    my_border.hideturtle()
    my_border.penup()
    my_border.goto(-400, -400)
    my_border.pendown()
    
    for i in range(4):
        my_border.forward(800)
        my_border.left(90)


my_border = Turtle()
my_snake = Snake()
my_screen.listen()
my_screen.onkeypress(my_snake.go_up, "Up")
my_screen.onkeypress(my_snake.go_down, "Down")
my_screen.onkeypress(my_snake.go_left, "Left")
my_screen.onkeypress(my_snake.go_right, "Right")


if not GameOver:
    draw_border()
    my_snake.move()
    my_apple = apple()
    my_apple.goto((random.choice(range(-400, 400))), (random.choice(range(-400, 400))))
    
my_screen.mainloop()