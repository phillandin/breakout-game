from turtle import Turtle


class Ball(Turtle):
    def __init__(self, paddle, scoreboard, bricks):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()
        self.setheading(75)
        self.shapesize(stretch_len=0.75, stretch_wid=0.75)
        self.paddle = paddle
        self.scoreboard = scoreboard
        self.bricks = bricks
        # set ball position to rest on center of user paddle
        self.goto(paddle.center.xcor(), paddle.center.ycor() + 19)
        self.move = False

    def release(self):
        self.move = True

    def go(self):
        self.forward(11)
        # set top border of playable area
        if self.ycor() > 240:
            self.setheading(-self.heading())
        # set left and right border
        if self.xcor() < -390 and 90 < self.heading() < 270:
            self.setheading(180 - self.heading())
        if self.xcor() > 379 and (self.heading() < 90 or self.heading() > 270):
            self.setheading(180 - self.heading())
        # if self.xcor() < -390 or self.xcor() > 379:
        #     self.setheading(180 - self.heading())
        if self.heading() == 180:
            self.setheading(self.heading() - 5)
        if self.heading() == 0:
            self.setheading(self.heading() + 5)

    def moving(self):
        if self.move:
            return True
        else:
            return False

    def side_hit(self, brick):
        for block in brick.blocks:
            if self.distance(block) < 25:
                if 0 < self.heading() < 90 or 270 < self.heading() < 360:
                    if self.xcor() < block.xcor() and abs(abs(self.xcor()) - abs(block.xcor())) > 15 and abs(self.ycor() - block.ycor()) < 9.5:
                        # print(self.position(), block.position())
                        # print(self.heading(), self.distance(block), "side hit")
                        self.setheading(180 - self.heading())
                        return True
                elif 90 < self.heading() < 270 and self.xcor() > block.xcor() and abs(abs(self.xcor()) - abs(block.xcor())) > 15 and abs(self.ycor() - block.ycor()) < 9.5:
                    # print(self.position(), block.position())
                    # print(self.heading(), self.distance(block), "side hit")
                    self.setheading(180 - self.heading())
                    return True

    def bottom_hit(self, brick):
        for block in brick.blocks:
            if self.distance(block) < 25:
                if 0 < self.heading() < 180 and abs(abs(self.xcor()) - abs(block.xcor())) < 17 and \
                     -20 < abs(self.ycor()) - abs(block.ycor()) < 0:
                    # print(self.position(), block.position())
                    # print(self.heading(), "bottom hit")
                    self.setheading(-self.heading())
                    return True

    def top_hit(self, brick):
        for block in brick.blocks:
            if self.distance(block) < 25:
                if 180 < self.heading() < 360 and abs(abs(self.xcor()) - abs(block.xcor())) < 17 and \
                    0 < abs(self.ycor()) - abs(block.ycor()) < 20:
                    # print(self.position(), block.position())
                    # print(self.heading(), "top hit ")
                    self.setheading(-self.heading())
                    return True


    def detect_impact(self):
        for segment in self.paddle.segments:
            if self.heading() > 180:  # ensure ball doesn't bounce immediately upon release
                if self.distance(segment) < 25:
                    if segment == self.paddle.right_edge:  # change angle for hits on right edge
                        self.setheading(-self.heading() - 25)
                    elif segment == self.paddle.left_edge:  # change angle for hits on left edge
                        self.setheading(-self.heading() + 25)
                    else:
                        self.setheading(-self.heading())
        for rock in self.bricks.rocks:
            if self.side_hit(rock) or self.bottom_hit(rock) or self.top_hit(rock):
                pass
        for brick in self.bricks.bricks:
            if self.side_hit(brick) or self.bottom_hit(brick) or self.top_hit(brick):
                if brick.life:
                    brick.extra_life(self.bricks.bricks, self.bricks.falling)
                else:
                    brick.remove(self.bricks.bricks, self.bricks.destroyed_bricks)
                self.scoreboard.add_point()

    def restart(self):
        self.goto(self.paddle.center.xcor(), self.paddle.center.ycor() + 19)
        self.setheading(75)
        self.move = False

