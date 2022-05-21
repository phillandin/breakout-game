from turtle import Turtle
import itertools as it

# brick positions for level 1
set1 = [(i, 80) for i in range(-285, 300, 114)]
set2 = [(i, 107) for i in range(-314, 314, 57)]
set3 = [(i, 134) for i in range(-228, 230, 114)]
extras = [(-330, 188), (330, 188)]
lvl_1_positions = {"bricks": set3 + set2 + set1 + extras}

# brick positions for level 2
set1 = [(x, y) for x in range(-300, -150, 57) for y in range(90, 160, 27)]
set2 = [(x, y) for x in range(-58, 60, 57) for y in range(40, 90, 27)]
set3 = [(x, y) for x in range(186, 325, 57) for y in range(90, 160, 27)]
rocks = [(x, 63) for x in it.chain(range(-300, -150, 57), range(186, 325, 57))]
lvl_2_positions = {"bricks": set1 + set2 + set3, "unbreakable": rocks}

# brick positions for level 3
set1 = [(x, y) for x in range(-114, 120, 57) for y in range(180, 210, 27)]
set2 = [(x, abs(x)/2 + 20) for x in range(-300, 360, 100)]
rocks = [(x, 153) for x in range(-85, 90, 57)] + [(-300, 143), (300, 143)]
lvl_3_positions = {"bricks":  set2, "unbreakable": rocks}

LVL_POSITIONS = [lvl_1_positions, lvl_2_positions, lvl_3_positions]


class Bricks:
    def __init__(self):
        self.level = 0
        self.bricks = []
        self.destroyed_bricks = []
        self.rocks = []
        self.falling = []
        self.create_bricks()

    def create_bricks(self):
        for (x, y) in LVL_POSITIONS[self.level]["bricks"]:
            block1 = Block()
            block2 = Block()
            block3 = Block()
            brick = Brick(block1, block2, block3)
            if (x, y) == LVL_POSITIONS[self.level]["bricks"][4]:
                block1.life_block()
                block2.life_block()
                block3.life_block()
                brick = Brick(block1, block2, block3)
                brick.life_brick()
            block1.goto(x - 16, y)
            block2.goto(x, y)
            block3.goto(x + 16, y)
            self.bricks.append(brick)

    def reuse_bricks(self):
        print(len(self.destroyed_bricks))
        for (x, y) in LVL_POSITIONS[self.level]["bricks"]:
            brick = self.destroyed_bricks[0]
            brick.blocks[0].goto(x - 16, y)
            brick.blocks[1].goto(x, y)
            brick.blocks[2].goto(x + 16, y)
            for block in brick.blocks:
                block.showturtle()
            if (x, y) == LVL_POSITIONS[self.level]["bricks"][4]:
                for block in brick.blocks:
                    block.life_block()
                brick.life_brick()
            self.destroyed_bricks.remove(brick)
            self.bricks.append(brick)
        if not self.rocks:
            try:
                for (x, y) in LVL_POSITIONS[self.level]["unbreakable"]:
                    b1, b2, b3 = Block(), Block(), Block()
                    b1.color("brown"), b2.color("brown"), b3.color("brown")
                    blck = Brick(b1, b2, b3)
                    blck.impervious()
                    b1.goto(x - 16, y)
                    b2.goto(x, y)
                    b3.goto(x + 16, y)
                    self.rocks.append(blck)
            except KeyError:
                pass
        else:
            try:
                for (x, y) in LVL_POSITIONS[self.level]["unbreakable"]:
                    rock = self.rocks[LVL_POSITIONS[self.level]["unbreakable"].index((x, y))]
                    rock.blocks[0].goto(x - 16, y)
                    rock.blocks[1].goto(x, y)
                    rock.blocks[2].goto(x + 16, y)
            except KeyError:
                for rock in self.rocks:
                    for block in rock.blocks:
                        block.goto(0, -370)





    def all_cleared(self):
        if not self.bricks:
            return True

    def fall(self):
        for item in self.falling:
            if item.ycor() > -450:
                item.forward(8)

    def remove_bricks(self):
        for brick in self.bricks[0:len(self.bricks)]:
            brick.remove(self.bricks, self.destroyed_bricks)

    def next_level(self):
        self.remove_bricks()
        self.level += 1
        self.reuse_bricks()

    def start_over(self):
        self.remove_bricks()
        self.reuse_bricks()


class Block(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.turtlesize()
        self.color("gray")
        self.penup()
        self.extra_life = False

    def life_block(self):
        self.color("pink")
        self.extra_life = True

    def fall(self):
        if self.ycor() > -450:
            self.forward(8)

    def power(self, scoreboard):
        self.reset()
        if self.extra_life:
            scoreboard.add_life()
            # scoreboard.lives += 1
            # return scoreboard.lives


class Brick:
    def __init__(self, block1, block2, block3):
        self.blocks = [block1, block2, block3]
        self.can_break = True
        self.life = False
        self.falling = False

    def remove(self, brick_set, used_bricks):
        self.life = False
        for block in self.blocks:
            block.color("gray")
            block.hideturtle()
            block.extra_life = False
        try:
            brick_set.remove(self)
        except ValueError:
            pass
        used_bricks.append(self)


    def extra_life(self, brick_set, falling_items):
        for i in range(0, 3, 2):
            self.blocks[i].reset()
            self.blocks[i].hideturtle()
            self.blocks[i].color("black")
        try:
            brick_set.remove(self)
        except ValueError:
            pass
        self.blocks[1].shape("turtle")
        self.blocks[1].setheading(270)
        falling_items.append(self.blocks[1])


    def life_brick(self):
        self.life = True

    def impervious(self):
        self.can_break = False