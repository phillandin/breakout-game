from turtle import Turtle

ALIGNMENT = "center"
FONT = ("courier", 18, "normal")
END_FONT = ("courier", 30, "bold")

class Scoreboard(Turtle):
    def __init__(self, bricks, test=False):
        super().__init__()
        self.level = bricks.level + 1
        self.score = 0
        self.lives = 3
        self.color("white")
        self.penup()
        self.hideturtle()
        self.update_scoreboard()
        self.test = test
        start_message = "Hit SPACE to begin"
        if test:
            self.display_test_message()
        else:
            self.goto(-150, -100)
            self.write(start_message, False, "left", FONT)

    def display_test_message(self):
        self.goto(-150, -100)
        test_message = "Hit \"r\" to reset ball\n"\
                       "Hit \"n\" for next level\n"\
                       "Hit \"s\" to restart level"

        if self.level == 1:
            test_message = "     *TEST MODE*\n\nHit SPACE to begin\n" + test_message
        self.write(test_message, False, "left", FONT)

    def update_scoreboard(self):
        self.clear()
        self.goto(0, 217)
        if self.score < 10:
            self.write(f"Score: {self.score}     Lives: {self.lives}    Level: {self.level}", False, ALIGNMENT, FONT)
        else:
            self.write(f"Score: {self.score}    Lives: {self.lives}    Level: {self.level}", False, ALIGNMENT, FONT)

    def add_point(self):
        self.score += 1
        self.update_scoreboard()

    def lose_life(self):
        self.lives -= 1
        self.update_scoreboard()

    def add_life(self):
        self.lives += 1
        self.update_scoreboard()

    def next_level(self):
        self.level += 1
        self.update_scoreboard()

    def game_over(self):
        self.clear()
        self.color("red")
        self.goto(0, -100)
        self.write(f"GAME OVER\nFinal score: {self.score}", False, ALIGNMENT, END_FONT)

    def winner(self):
        self.clear()
        self.color("cyan")
        self.goto(0, -100)
        self.write(f"Winner!  Score: {self.score}", False, ALIGNMENT, END_FONT)


