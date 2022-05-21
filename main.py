from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from bricks import Bricks
from scoreboard import Scoreboard
import time
import datetime


END_TIME_STAMPS = []

def start_game():
    scoreboard.update_scoreboard()
    ball.release()


def next_level():
    if scoreboard.level < 3:
        bricks.next_level()
        scoreboard.next_level()
        ball.restart()
        scoreboard.display_test_message()


def restart():
    scoreboard.score = 0
    scoreboard.lives = 3
    scoreboard.update_scoreboard()
    bricks.start_over()
    ball.restart()
    scoreboard.display_test_message()


def breakout():
    while True:
        screen.update()
        time.sleep(0.0325)
        if not ball.moving():
            ball.goto(paddle.center.xcor(), paddle.center.ycor()+19)
        else:
            ball.go()
            ball.detect_impact()
            # make falling objects move downward
            if len(bricks.falling) > 0:
                for item in bricks.falling:
                    item.fall()
                    if paddle.impact(item):
                        item.power(scoreboard)
                        bricks.falling.remove(item)
            if ball.ycor() < -350:
                ball.restart()
                scoreboard.lose_life()
            if bricks.all_cleared() and len(bricks.falling) == 0:
                if scoreboard.level == 3:
                    # timer to delay ending
                    global END_TIME_STAMPS
                    END_TIME_STAMPS.append(datetime.datetime.now() + datetime.timedelta(seconds=1))
                    try:
                        if datetime.datetime.now() > END_TIME_STAMPS[0]:
                            scoreboard.winner()
                            break
                    except KeyError:
                        pass
                else:
                    next_level()
            if scoreboard.lives == 0:
                ball.restart()
                scoreboard.game_over()
                break


screen = Screen()
screen.setup(width=800, height=500)
screen.title("Breakout")
screen.bgcolor("black")
screen.tracer(0)

paddle = Paddle()
bricks = Bricks()
scoreboard = Scoreboard(bricks, test=True)
ball = Ball(paddle, scoreboard, bricks)


screen.listen()
screen.onkeypress(key="Left", fun=paddle.move_left)
screen.onkeypress(key="Right", fun=paddle.move_right)
# set space key to release ball
screen.onkey(key="space", fun=start_game)
# developer mode -- reset ball
screen.onkey(key="r", fun=ball.restart)
screen.onkey(key="n", fun=next_level)
screen.onkey(key="s", fun=restart)

breakout()

screen.exitonclick()
