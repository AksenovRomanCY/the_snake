from random import randint

import pygame

# Constants for field and grid sizes:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Driving directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# The background color is black:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Cell border color
BORDER_COLOR = (93, 216, 228)

# The color of an apple
APPLE_COLOR = (255, 0, 0)

# The color of the snake
SNAKE_COLOR = (0, 255, 0)

# The color of a rotten apple
ROTTEN_APPLE_COLOR = (128, 128, 0)

# The color of the stone
ROCK_COLOR = (169, 169, 169)

# The speed of the snake:
SPEED = 10

# Customize the game window:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Title of the playing field window:
pygame.display.set_caption('The Snake')

# Setting the time:
clock = pygame.time.Clock()


class GameObject:
    """Parent class for all game classes
    (such as 'Snake' and 'GameObjectThings')

    """

    def __init__(self):
        """Initialization of parent class attributes
        1. position - responsible for the position on the game screen
           (in this case the center of the screen)
        2. body_color - color of the object

        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """An abstract method that is intended
        to be overridden in child classes

        """
        pass


class GameObjectThings(GameObject):
    """A parent class for all subject classes
    (such as 'Apple', 'RottenApple' and 'Rock')

    """

    def __init__(self):
        """Initialization of parent class attributes"""
        super().__init__()

    def draw(self) -> None:
        """Draws an object on the playing surface"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @staticmethod
    def randomize_position(first_position: tuple[int, int],
                           second_position: tuple[int, int],
                           third_position: tuple[int, int]):
        """A static method that is intended
        to be overridden in child classes

        """
        pass


class Apple(GameObjectThings):
    """The class responsible for the apple object,
    in particular for its position and drawing on the
    playing field

    """

    def __init__(self):
        """Initialization of attributes of this class
        1. position - responsible for the position on the game screen
           (calls static function randomize_position)
        2. body_color - color of the object

        """
        super().__init__()
        self.position = self.randomize_position([self.position])
        self.body_color = APPLE_COLOR

    @staticmethod
    def randomize_position(snake_positions: list[tuple[int, int]],
                           rotten_apple_position: tuple[int, int] = None,
                           rock_position: tuple[int, int] = None
                           ) -> tuple[int, int]:
        """Sets the random position of the apple
        on the playing field

        """
        while True:
            x_coordinate = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_coordinate = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            # Creates a generator that every iteration of the generator checks
            # the coordinates of the snake against the coordinates of the
            # apple.
            # all() checks that all items in the list are True
            is_snake_position = all(
                x_coordinate != part[0] and y_coordinate != part[1]
                for part in snake_positions)

            if rotten_apple_position:
                # Check the coordinates of a rotten apple against the
                # coordinates of a normal apple.
                is_rotten_apple_position = (
                    x_coordinate != rotten_apple_position[0]
                    and y_coordinate != rotten_apple_position[1])
            else:
                is_rotten_apple_position = True

            if rock_position:
                # Check the coordinates of the stone against the coordinates
                # of the apple.
                is_rock_position = (
                    x_coordinate != rock_position[0]
                    and y_coordinate != rock_position[1])
            else:
                is_rock_position = True

            # Checking that the coordinates don't match the snake's position
            # the rotten apple and the rock
            if (is_snake_position and is_rotten_apple_position
                    and is_rock_position):
                return x_coordinate, y_coordinate


class Snake(GameObject):
    """The class responsible for the snake object,
    specifically, changing it, moving it,
    rendering and resetting

    """

    def __init__(self):
        """Initialization of attributes of this class
        1. position - responsible for the position on the game screen
           (inherits from the parent class and packs it into a list)
        2. length - length of the snake (Initial value 1)
        3. direction - direction of snake movement (Initial value is RIGHT)
        4. next_direction - the next direction of movement that
           will be applied
           after the key press is processed
        5. body_color - object color

        """
        super().__init__()
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self) -> None:
        """Updates the direction of the snake's movement"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Updates the snake's position by adding a new
        head to the beginning of the positions list and deleting
        the last element if the snake's length has not increased.
        the length of the snake has not increased.

        """
        if self.direction == UP:
            # Checks to see if the snake has collided with the upper barrier
            if self.get_head_position[1] <= 0:
                new_head_position = (self.get_head_position[0], 460)
            else:
                new_head_position = (self.get_head_position[0],
                                     self.get_head_position[1] - 20)
            self.positions.insert(0, new_head_position)
        elif self.direction == DOWN:
            # Checks to see if the snake has encountered the lower barrier
            if self.get_head_position[1] >= 460:
                new_head_position = (self.get_head_position[0], 0)
            else:
                new_head_position = (self.get_head_position[0],
                                     self.get_head_position[1] + 20)
            self.positions.insert(0, new_head_position)
        elif self.direction == LEFT:
            # Checks to see if the snake has collided with the left barrier
            if self.get_head_position[0] <= 0:
                new_head_position = (620, self.get_head_position[1])
            else:
                new_head_position = (self.get_head_position[0] - 20,
                                     self.get_head_position[1])
            self.positions.insert(0, new_head_position)
        elif self.direction == RIGHT:
            # Checks to see if the snake has collided with the right barrier
            if self.get_head_position[0] >= 620:
                new_head_position = (0, self.get_head_position[1])
            else:
                new_head_position = (self.get_head_position[0] + 20,
                                     self.get_head_position[1])
            self.positions.insert(0, new_head_position)

        # Removes the last value from the snake coordinate list until it
        # match the length of the snake
        while len(self.positions) > self.length:
            del self.positions[-1]

    def draw(self) -> None:
        """Draws the snake on the screen"""
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Sketching a snake's head
        head_rect = pygame.Rect(self.get_head_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    @property
    def get_head_position(self) -> tuple[int, int] | None:
        """Returns the position of the snake's head
        (the first element in the positions list)

        """
        try:
            return self.positions[0]
        except IndexError:
            return None

    def reset(self) -> None:
        """Resets the snake to its initial state"""
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


class RottenApple(GameObjectThings):
    """The class responsible for the rotten apple object,
    in particular for its position and rendering on the game board
    (inherits most of the functions and attributes from the
    parent class)

    """

    def __init__(self, apple_position: tuple[int, int]):
        """Initialization of attributes of this class
        1. body_color - object color

        """
        super().__init__()
        self.position = self.randomize_position(
            [self.position], apple_position)
        self.body_color = ROTTEN_APPLE_COLOR

    @staticmethod
    def randomize_position(snake_positions: list[tuple[int, int]],
                           apple_position: tuple[int, int],
                           rock_position: tuple[int, int] = None
                           ) -> tuple[int, int]:
        """Sets the random position of the rotten apple
        on the playing field

        """
        while True:
            x_coordinate = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_coordinate = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            # Creates a generator that every iteration of the generator checks
            # the coordinates of the snake against the coordinates
            # of the apple.
            # all() checks that all items in the list are True
            is_snake_position = all(
                x_coordinate != part[0] and y_coordinate != part[1]
                for part in snake_positions)

            # Check the coordinates of a rotten apple against the
            # coordinates of a normal apple.
            is_apple_position = (
                x_coordinate != apple_position[0]
                and y_coordinate != apple_position[1])

            if rock_position:
                # Check the coordinates of the stone against the
                # coordinates of the apple.
                is_rock_position = (
                    x_coordinate != rock_position[0]
                    and y_coordinate != rock_position[1])
            else:
                is_rock_position = True

            # Checking that the coordinates don't match the
            # snake's position the rotten apple and the rock
            if is_snake_position and is_apple_position and is_rock_position:
                return x_coordinate, y_coordinate


class Rock(GameObjectThings):
    """The class responsible for the stone object,
    in particular for its position and rendering on the playing field
    (inherits most of the functions and attributes from the
    parent class)

    """

    def __init__(self, apple_position: tuple[int, int],
                 rotten_apple_position: tuple[int, int]):
        """Initialization of attributes of this class
        1. body_color - object color

        """
        super().__init__()
        self.position = self.randomize_position(
            [self.position], apple_position, rotten_apple_position)
        self.body_color = ROCK_COLOR

    @staticmethod
    def randomize_position(snake_positions: list[tuple[int, int]],
                           apple_position: tuple[int, int],
                           rotten_apple_position: tuple[int, int]
                           ) -> tuple[int, int]:
        """Randomizes the position of the apple
        on the playing field

        """
        while True:
            x_coordinate = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_coordinate = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            # Creates a generator that every iteration of the generator checks
            # the coordinates of the snake against the coordinates
            # of the apple.
            # all() checks that all items in the list are True
            is_snake_position = all(
                x_coordinate != part[0] and y_coordinate != part[1]
                for part in snake_positions)

            # Check the coordinates of a rotten apple against the
            # coordinates of a normal apple.
            is_apple_position = (
                x_coordinate != apple_position[0]
                and y_coordinate != apple_position[1])

            # Check the coordinates of the stone against the
            # coordinates of the apple.
            is_rotten_apple_position = (
                x_coordinate != rotten_apple_position[0]
                and y_coordinate != rotten_apple_position[1])

            # Checking that the coordinates don't match the snake's position #
            # the rotten apple and the rock
            if (is_snake_position and is_apple_position
                    and is_rotten_apple_position):
                return x_coordinate, y_coordinate


def handle_keys(game_object: Snake) -> None:
    """Processes keystrokes to change the direction
    of the snake

    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def game_interaction(snake: Snake, apple: Apple,
                     rotten_apple: RottenApple, rock: Rock) -> None:
    """Handles all basic game interactions,
    such as dropping the snake, moving objects, zooming in
    and zooming in and out of the snake

    """
    # Checking for a game reset when the snake collides with itself #
    # Reducing to 0 and colliding with a rock
    if (snake.get_head_position in snake.positions[1:]
            or snake.length < 1
            or snake.get_head_position == rock.position):
        snake.reset()  # Reset the state of the snake
        apple.position = apple.randomize_position(
            snake.positions)
        rotten_apple.position = rotten_apple.randomize_position(
            snake.positions, apple.position)
        rock.position = rock.randomize_position(
            snake.positions, apple.position, rotten_apple.position)
    # Checks to see if the snake's head collides with the apple,
    # and if passed, enlarges the snake and moves the apple
    elif snake.get_head_position == apple.position:
        snake.length += 1
        apple.position = apple.randomize_position(
            snake.positions, rotten_apple.position, rock.position)
    # Checks to see if the snake's head collides with a rotten apple,
    # and if passed, shrinks the snake and moves the rotten apple
    elif snake.get_head_position == rotten_apple.position:
        snake.length -= 1
        rotten_apple.position = rotten_apple.randomize_position(
            snake.positions, apple.position, rock.position)


def main() -> None:
    """Главная функция запускающая основной код игры"""
    # PyGame initialization:
    pygame.init()

    # Initialization of game classes:
    apple = Apple()
    snake = Snake()
    rotten_apple = RottenApple(apple.position)
    rock = Rock(apple.position, rotten_apple.position)

    while True:
        # Paces the game
        clock.tick(SPEED)

        # Processing keyboard input
        handle_keys(game_object=snake)

        # Updating the direction and movement of the snake
        snake.update_direction()
        snake.move()

        # Handles game interactions
        game_interaction(snake, apple, rotten_apple, rock)

        # Clears the screen before drawing
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Drawing an apple and a snake
        apple.draw()
        snake.draw()
        rotten_apple.draw()
        rock.draw()

        # Screen refresh
        pygame.display.update()


if __name__ == '__main__':
    main()
