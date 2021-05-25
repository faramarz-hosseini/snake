# Snake Game
a simple classic snake game written in Python using the Pygame library. The game starts
with 0 score and at level 1. Each time the player eats an apple the snake size and score increases by 1.
Moreover, the player loses the game when they hit the walls and obstacles. There are 5 levels with
different colors for the background and the player progresses through these levels whenever their score
is a multiple of 25 (25, 50, 75, 100).

# Requirements
```python
pip install pygame
```
# How it works

Below is a list classes and their methods that work together to bring the snake and its food to life. 

## The Manager Class
The class attributes hold some of the static files I've used in the game. Such as sound effects and background pictures. Fonts for different events in the game (game over and score) are also defined as class attributes of this class.

Each instance of this class is created with the following fields:
```python
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
```

###Method: run
This method is the heart of the game. It calls different methods of the class in a somewhat infinite while loop to keep the game running.
```python
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

```

###Method: check_quit_event
This method exists solely to check for the quit event which triggers when the player clicks on the "X" on the top right corner.

###Method: get_directions
A method to take directional inputs from the player and in turn change the direction in which the snake is moving. Pygame makes taking keyboard inputs relatively easy.

###Method: progress_level
Based on the current score of the player, the method changes the level. As the levels change, the snake moves faster and the color of the background changes to imply the increased difficulty. The player progresses through levels whenever their score is a multiple of 25. (25, 50...)

###Method: collision_check
The game uses to method to check if player has collided (or in snake terms, eaten) an apple. Apples are spawn on the screen with randomized coordinates (x and y on the pygame screen), this method checks to see if the snake head coordinates are within the range of an apple coordinates. If so, the method removes the food from the screen and increases score by 1.

###Method: generate_food
The first conditional line of this method:
```python
    def generate_food(self):
        if not self.fail and self.direction is not None:
```
cleverly restricts food spawning to when the snake is still alive and when it's begun moving. (Or in technical terms, the game's started)
This way, the screen won't fill up with apples if the players chooses to wait a few seconds to start to playing/moving the snake.

Furthermore, the method uses the python built-in **time** and **random** modules to generate apples every 5 seconds on different parts of the screen. (random decides a random integer for the x and y coordinates and time allows it to happen every 5 seconds)


###Methood: add_to_snake
As the name suggests, this short method exists to add "body parts" to our snake whenever it eats apples and the score increases.
In fact the method does not care for the food and only sees the score. This way, another method deals with checking collision with the food and increasing the score and this method receives that score (basically the number of apples the snake has eaten.) and adds to the snake based on it.

###Method: generate_visuals
```python
    def generate_visuals(self):
        self.change_background_level()
        self.draw_play_box()
        self.show_food()
        self.show_score()
        self.show_level()
        self.draw_obstacles()
        self.detect_wall_fail()
        self.detect_obstacle_fail()
        self.draw_snake()
        pygame.display.update()
```
A method of methods. This mother method calls a number of other methods that are each responsible for generating something visually on the screen. The method names should be pretty self-explanatory as to what they're trying to achieve.
The methods called are mostly written using the Pygame tools.


###Method: move
```python
def move(self):
        if not self.fail:
            ...
```
Before anything else, the methods checks to see if the fail attribute (which is a boolean) is False. If so, it allows the player the control and move the snake. The method uses the directions from the **get_directions** method to change the snake's x and y coordinates either horizontally or vertically (depending on the player input) every millisecond and thus creating the illusion of a moving snake.


###Method: close_reset_game
When the snake has hit a wall or an obstacle, this method takes keyboard input from the player and either resets or closes the game based on it. (Space to close and R to reset the game)


#The Snake Class
a simple class that holds the snake graphics, starting x and y coordinates, and width and height as its attributes.
```python
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
```


#The Food Class
```python
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
```
The apples are actually the instances of this class. The class holds food graphics and width and heigh as its attributes.



#The Obstacle and Background Classes
These two classes exist to serve different graphical static files as their attributes. Similar to how the food and snake class worked

#The Directions Class
Another simple class that provides values for different directions (UP, DOWN, RIGHT, LEFT) as its attributes.

Have fun!
