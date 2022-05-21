from turtle import Turtle

STARTING_POSITIONS = [(i, -200) for i in range(-60, 80, 20)]


class Paddle:
    def __init__(self):
        self.segments = []
        self.create_paddle()
        self.left_edge = self.segments[0]
        self.right_edge = self.segments[-1]
        self.center = self.segments[3]

    def create_paddle(self):
        for position in STARTING_POSITIONS:
            segment = Turtle("square")
            segment.penup()
            segment.color("white")
            segment.goto(position)
            self.segments.append(segment)

    def impact(self, item):
        for segment in self.segments:
            if item.distance(segment) < 18:
                return True

    def move_left(self):
        for segment in self.segments:
            if segment.xcor() < -380:
                break
            segment.forward(-10)

    def move_right(self):
        for segment in self.segments[::-1]:
            if segment.xcor() > 370:
                break
            segment.forward(10)