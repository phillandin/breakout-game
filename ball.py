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
        # ensure ball doesn't get stuck bouncing side-to-side
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
                # detect heading of ball so that it doesn't change heading twice due to close proximity to a
                # different brick than the one it hits
                if 0 < self.heading() < 90 or 270 < self.heading() < 360:  # defines hit from left side
                    # If the distance between ball's xcor and brick's xcor is greater than 15 and the distance between
                    # their respective ycors is less than 9.5, this is likely a hit from the side
                    if self.xcor() < block.xcor() and abs(abs(self.xcor()) - abs(block.xcor())) > 15 and \
                        abs(self.ycor() - block.ycor()) < 9.5:
                        self.setheading(180 - self.heading())
                        return True
                # same as above, but from right side
                elif 90 < self.heading() < 270 and self.xcor() > block.xcor() and abs(
                    abs(self.xcor()) - abs(block.xcor())) > 15 and abs(self.ycor() - block.ycor()) < 9.5:
                    self.setheading(180 - self.heading())
                    return True

    # hits from the bottom and hits from above are separated to make sure the heading of the ball doesn't change twice
    # in rapid succession because of proximity to a different brick
    def bottom_hit(self, brick):
        for block in brick.blocks:
            if self.distance(block) < 25:
                if 0 < self.heading() < 180 and abs(abs(self.xcor()) - abs(block.xcor())) < 17 and -20 < abs(
                    self.ycor()) - abs(block.ycor()) < 0:
                    self.setheading(-self.heading())
                    return True

    def top_hit(self, brick):
        for block in brick.blocks:
            if self.distance(block) < 25:
                if 180 < self.heading() < 360 and abs(abs(self.xcor()) - abs(block.xcor())) < 17 and 0 < abs(
                    self.ycor()) - abs(block.ycor()) < 20:
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
        # rocks = unbreakable bricks
        for rock in self.bricks.rocks:
            if self.side_hit(rock) or self.bottom_hit(rock) or self.top_hit(rock):
                # pass ensures the rock doesn't get removed from bricks.rocks
                pass
        for brick in self.bricks.bricks:
            if self.side_hit(brick) or self.bottom_hit(brick) or self.top_hit(brick):
                if brick.life:  # if life brick, turn into turtle and begin to fall
                    brick.extra_life(self.bricks.bricks, self.bricks.falling)
                else:
                    brick.remove(self.bricks.bricks, self.bricks.destroyed_bricks)
                self.scoreboard.add_point()

    def restart(self):
        self.goto(self.paddle.center.xcor(), self.paddle.center.ycor() + 19)
        self.setheading(75)
        self.move = False
