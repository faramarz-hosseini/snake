import pygame
import random
import time

pygame.init()
win = pygame.display.set_mode((900, 500))
pygame.display.set_caption("BruhSnake")


class Manager:
    EAT_SOUND = pygame.mixer.Sound('Cartoon_Munch_Sound_Effect.medium.mp3')
    SCORE_FONT = pygame.font.Font("freesansbold.ttf", 14)
    FAIL_FONT = pygame.font.Font("freesansbold.ttf", 64)
    FAIL_FONT_2 = pygame.font.Font("freesansbold.ttf", 32)
    FAIL_SOUND = pygame.mixer.Sound('Bruh.mp3')
    _BACK_GROUND = pygame.image.load("Graphics/background1.jpg").convert_alpha()
    BACK_GROUND = pygame.transform.scale(_BACK_GROUND, (900, 500))

    def __init__(self, window, window_width, window_height, food_generation_period=2.5, speed=6, food_limit=5,
                 level_requirement=25):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.speed = speed
        self.delay = 50
        self.running = True
        self.direction = None
        self.foods = []
        self.score = 1
        self.start = 0
        self.snake = Snake(50, 50)
        self.obstacles = [
            Obstacle(115, 100, 40, 155),
            Obstacle(156, 101, 200, 40),
            Obstacle(115, 320, 40, 115),
            Obstacle(156, 394, 200, 40),
            Obstacle(420, 394, 200, 40),
            Obstacle(420, 101, 200, 40),
            Obstacle(621, 100, 40, 155),
            Obstacle(621, 320, 40, 115),
            Obstacle(365, 250, 50, 50),
            Obstacle(662, 225, 100, 30),
            Obstacle(662, 320, 100, 30)
        ]

        self.fail = False
        self.food_generation_period = food_generation_period
        self.food_limit = food_limit
        self.level = 1
        self.level_requirement = level_requirement

    def run(self):
        self.start = time.time()
        while self.running:
            pygame.time.delay(self.delay)
            self.check_quit_event()
            self.get_direction()
            self.progress_level()
            self.collision_check()
            self.generate_food()
            self.add_to_snake()
            self.generate_visuals()
            self.move()
            self.close_reset_game()

    def check_quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def get_direction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.direction is not Direction.RIGHT:
            self.direction = Direction.LEFT
        if keys[pygame.K_RIGHT] and self.direction is not Direction.LEFT:
            self.direction = Direction.RIGHT
        if keys[pygame.K_UP] and self.direction is not Direction.DOWN:
            self.direction = Direction.UP
        if keys[pygame.K_DOWN] and self.direction is not Direction.UP:
            self.direction = Direction.DOWN

    def move(self):
        if not self.fail:
            if self.direction == Direction.LEFT and self.snake.x > self.speed:
                self.snake.x -= self.speed
            elif self.direction == Direction.RIGHT and self.snake.x < self.window_width - Snake.WIDTH - self.speed:
                self.snake.x += self.speed
            elif self.direction == Direction.UP and self.snake.y > self.speed + 20:
                self.snake.y -= self.speed
            elif self.direction == Direction.DOWN and self.snake.y < self.window_height - Snake.HEIGHT - self.speed:
                self.snake.y += self.speed

    def collision_check(self):
        trash_food = list()
        for food in self.foods:
            if self.check_collision_food(self.snake, food):
                trash_food.append(food)
        for trash in trash_food:
            Manager.EAT_SOUND.play()
            self.foods.remove(trash)
            self.score += 1

    def generate_food(self):
        if not self.fail and self.direction is not None:
            if len(self.foods) == self.food_limit:
                return None
            end = time.time()
            second = end - self.start
            if second >= self.food_generation_period:
                food_x = random.randint(Food.WIDTH * 2, self.window_width - Food.WIDTH * 2)
                food_y = random.randint(Food.HEIGHT * 2, self.window_height - Food.HEIGHT * 2)
                for obstacle in self.obstacles:
                    if (
                            obstacle.x - 20 <= food_x <= obstacle.x + obstacle.WIDTH + 20 and
                            obstacle.y - 20 <= food_y <= obstacle.y + obstacle.HEIGHT + 20
                    ):
                        return None
                self.foods.append(Food(food_x, food_y))
                self.start = time.time()

    def add_to_snake(self):
        self.snake.body.insert(0, (self.snake.x, self.snake.y))
        while len(self.snake.body) >= self.score:
            del self.snake.body[-1]

    def draw_play_box(self):
        pygame.draw.line(self.window, pygame.Color('brown'), (self.speed, Snake.HEIGHT + 10),
                         (self.window_width - self.speed, Snake.HEIGHT + 10))
        pygame.draw.line(self.window, pygame.Color('brown'), (self.speed, Snake.HEIGHT + 10),
                         (self.speed, self.window_height - self.speed))
        pygame.draw.line(self.window, pygame.Color('brown'), (self.speed, self.window_height - self.speed),
                         (self.window_width - self.speed, self.window_height - self.speed))
        pygame.draw.line(self.window, pygame.Color('brown'),
                         (self.window_width - self.speed, self.window_height - self.speed),
                         (self.window_width - self.speed, Snake.HEIGHT + 10))

    def show_food(self):
        for food in self.foods:
            fruit_rect = pygame.Rect(int(food.x), int(food.y), Food.WIDTH, Food.HEIGHT)
            self.window.blit(Food.FOOD_IMG, fruit_rect)

    def show_score(self):
        x_pos = 10
        y_pos = 10
        x = Manager.SCORE_FONT.render("Score: ", True, pygame.Color('black'))
        y = Manager.SCORE_FONT.render(str(self.score-1), True, pygame.Color('brown'))
        self.window.blit(x, (x_pos, y_pos))
        self.window.blit(y, (60, y_pos))

    def immobolize_text(self):
        fail_text = Manager.FAIL_FONT.render("YOU HIT THE WALL!", True, pygame.Color("red"))
        fail_text2 = Manager.FAIL_FONT_2.render("Press SPACE to close - R to respawn", True, pygame.Color("white"))
        self.fail = True
        self.window.blit(fail_text, (130, 195))
        self.window.blit(fail_text2, (130, 250))

    def detect_wall_fail(self):
        if (
                self.snake.y <= self.snake.HEIGHT + 10 or
                self.snake.y + self.snake.HEIGHT >= self.window_height - self.speed or
                self.snake.x <= self.speed or
                self.snake.x + self.snake.WIDTH >= self.window_width - self.speed
        ):
            self.immobolize_text()

    def detect_obstacle_fail(self):
        for obstacle in self.obstacles:
            if self.check_collision_obs(obstacle, self.snake):
                self.immobolize_text()

    @staticmethod
    def check_collision_obs(object1, object2):
        if (
                (
                        object1.y + 10 <= object2.y <= object1.y + object1.HEIGHT - 10 and
                        object1.x + 10 <= object2.x <= object1.x + object1.WIDTH - 10
                ) or
                (
                        object1.y + 10 <= object2.y + object2.HEIGHT <= object1.y + object1.HEIGHT - 10 and
                        object1.x + 10 <= object2.x + object2.WIDTH <= object1.x + object1.WIDTH - 10
                ) or
                (
                        object1.x + 10 <= object2.x <= object1.x + object1.WIDTH - 10 and
                        object1.y + 10 <= object2.y + object2.HEIGHT <= object1.y + object1.HEIGHT - 10
                ) or
                (
                        object1.x + 10 <= object2.x + object2.WIDTH <= object1.x + object1.WIDTH - 10 and
                        object1.y + 10 <= object2.y <= object1.y + object1.HEIGHT - 10
                )
        ):
            return True
        return False

    @staticmethod
    def check_collision_food(object1, object2):
        if (
                (
                        object1.y <= object2.y <= object1.y + object1.HEIGHT and
                        object1.x <= object2.x <= object1.x + object1.WIDTH
                ) or
                (
                        object1.y <= object2.y + object2.HEIGHT <= object1.y + object1.HEIGHT and
                        object1.x <= object2.x + object2.WIDTH <= object1.x + object1.WIDTH
                ) or
                (
                        object1.x <= object2.x <= object1.x + object1.WIDTH and
                        object1.y <= object2.y + object2.HEIGHT <= object1.y + object1.HEIGHT
                ) or
                (
                        object1.x <= object2.x + object2.WIDTH <= object1.x + object1.WIDTH and
                        object1.y <= object2.y <= object1.y + object1.HEIGHT
                )
        ):
            return True
        return False

    def draw_current_body(self):
        for block in self.snake.body:
            if self.direction == Direction.DOWN:
                self.window.blit(Snake.SNAKE_BODY_IMG_DOWN, (block[0], block[1]))
                self.window.blit(Snake.SNAKE_IMG_DOWN, (self.snake.x, self.snake.y))
            elif self.direction == Direction.UP:
                self.window.blit(Snake.SNAKE_BODY_IMG_UP, (block[0], block[1]))
                self.window.blit(Snake.SNAKE_IMG_UP, (self.snake.x, self.snake.y))
            elif self.direction == Direction.RIGHT:
                self.window.blit(Snake.SNAKE_BODY_IMG_RIGHT, (block[0], block[1]))
                self.window.blit(Snake.SNAKE_IMG_RIGHT, (self.snake.x, self.snake.y))
            elif self.direction == Direction.LEFT:
                self.window.blit(Snake.SNAKE_BODY_IMG_LEFT, (block[0], block[1]))
                self.window.blit(Snake.SNAKE_IMG_LEFT, (self.snake.x, self.snake.y))

    def draw_snake_head(self):
        if self.direction is None:
            self.window.blit(Snake.SNAKE_IMG_RIGHT, (self.snake.x, self.snake.y))
        if self.direction == Direction.RIGHT:
            self.window.blit(Snake.SNAKE_IMG_RIGHT, (self.snake.x, self.snake.y))
        elif self.direction == Direction.UP:
            self.window.blit(Snake.SNAKE_IMG_UP, (self.snake.x, self.snake.y))
        elif self.direction == Direction.DOWN:
            self.window.blit(Snake.SNAKE_IMG_DOWN, (self.snake.x, self.snake.y))
        elif self.direction == Direction.LEFT:
            self.window.blit(Snake.SNAKE_IMG_LEFT, (self.snake.x, self.snake.y))

    def draw_snake(self):
        self.draw_snake_head()
        self.draw_current_body()

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pos = pygame.Rect(obstacle.x, obstacle.y, obstacle.WIDTH, obstacle.HEIGHT)
            self.window.blit(obstacle.OBSTACLE_IMG, pos)

    def progress_level(self):
        if self.level == 5:
            return None
        elif self.score != 1 and (self.score - 1) % self.level_requirement == 0:
            self.score += 1
            self.delay -= 6
            self.level += 1

    def change_background_level(self):
        if self.level == 1:
            self.window.blit(Manager.BACK_GROUND, (0, 0))
        elif self.level == 2:
            self.window.blit(BackgroundLevel.BACK_GROUND2, (0, 0))
        elif self.level == 3:
            self.window.blit(BackgroundLevel.BACK_GROUND3, (0, 0))
        elif self.level == 4:
            self.window.blit(BackgroundLevel.BACK_GROUND4, (0, 0))
        elif self.level >= 5:
            self.window.blit(BackgroundLevel.BACK_GROUND5, (0, 0))

    def show_level(self):
        x_pos = 840
        y_pos = 10
        x = Manager.SCORE_FONT.render("Level: ", True, pygame.Color('black'))
        y = Manager.SCORE_FONT.render(str(self.level), True, pygame.Color('red'))
        self.window.blit(x, (x_pos, y_pos))
        self.window.blit(y, (885, y_pos))

    def close_reset_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.running = False
        if keys[pygame.K_r]:
            self.__init__(win, 900, 500)

    def generate_visuals(self):
        self.change_background_level()
        # self.window.fill(pygame.Color("black"))
        self.draw_play_box()
        self.show_food()
        self.show_score()
        self.show_level()
        self.draw_obstacles()
        self.detect_wall_fail()
        self.detect_obstacle_fail()
        self.draw_snake()
        pygame.display.update()


class Snake:
    WIDTH = 30
    HEIGHT = 30
    _SNAKE_IMG_DOWN = pygame.image.load("Graphics/snake_head_down.png").convert_alpha()
    SNAKE_IMG_DOWN = pygame.transform.scale(_SNAKE_IMG_DOWN, (30, 30))
    _SNAKE_IMG_UP = pygame.image.load("Graphics/snake_head_up.png").convert_alpha()
    SNAKE_IMG_UP = pygame.transform.scale(_SNAKE_IMG_UP, (30, 30))
    _SNAKE_IMG_RIGHT = pygame.image.load("Graphics/snake_head_right.png").convert_alpha()
    SNAKE_IMG_RIGHT = pygame.transform.scale(_SNAKE_IMG_RIGHT, (30, 30))
    _SNAKE_IMG_LEFT = pygame.image.load("Graphics/snake_head_left.png").convert_alpha()
    SNAKE_IMG_LEFT = pygame.transform.scale(_SNAKE_IMG_LEFT, (30, 30))
    _SNAKE_BODY_IMG_RIGHT = pygame.image.load("Graphics/snake_body_right.png").convert_alpha()
    SNAKE_BODY_IMG_RIGHT = pygame.transform.scale(_SNAKE_BODY_IMG_RIGHT, (30, 30))
    _SNAKE_BODY_IMG_LEFT = pygame.image.load("Graphics/snake_body_left.png").convert_alpha()
    SNAKE_BODY_IMG_LEFT = pygame.transform.scale(_SNAKE_BODY_IMG_LEFT, (30, 30))
    _SNAKE_BODY_IMG_UP = pygame.image.load("Graphics/snake_body_up.png").convert_alpha()
    SNAKE_BODY_IMG_UP = pygame.transform.scale(_SNAKE_BODY_IMG_UP, (30, 30))
    _SNAKE_BODY_IMG_DOWN = pygame.image.load("Graphics/snake_body_down.png").convert_alpha()
    SNAKE_BODY_IMG_DOWN = pygame.transform.scale(_SNAKE_BODY_IMG_DOWN, (30, 30))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.head = (self.x, self.y)
        self.body = []


class Food:
    _FOOD_IMG = pygame.image.load("Graphics/apple.png").convert_alpha()
    FOOD_IMG = pygame.transform.scale(_FOOD_IMG, (30, 30))
    WIDTH = 30
    HEIGHT = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} {self.y}"


class Obstacle:
    _OBSTACLE_IMG = pygame.image.load("Graphics/obstacle.jpg").convert_alpha()

    def __init__(self, x, y, width=40, height=70):
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.OBSTACLE_IMG = pygame.transform.scale(Obstacle._OBSTACLE_IMG, (self.WIDTH, self.HEIGHT))


class BackgroundLevel:

    _BACK_GROUND2 = pygame.image.load("Graphics/background2.jpg").convert_alpha()
    BACK_GROUND2 = pygame.transform.scale(_BACK_GROUND2, (900, 500))
    _BACK_GROUND3 = pygame.image.load("Graphics/background3.jpg").convert_alpha()
    BACK_GROUND3 = pygame.transform.scale(_BACK_GROUND3, (900, 500))
    _BACK_GROUND4 = pygame.image.load("Graphics/background4.jpg").convert_alpha()
    BACK_GROUND4 = pygame.transform.scale(_BACK_GROUND4, (900, 500))
    _BACK_GROUND5 = pygame.image.load("Graphics/background5.jpg").convert_alpha()
    BACK_GROUND5 = pygame.transform.scale(_BACK_GROUND5, (900, 500))


class Direction:
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4



manager = Manager(win, 900, 500)
manager.run()
