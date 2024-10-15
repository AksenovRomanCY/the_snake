"""This module implements a "Snake" game using the Pygame library.

The game involves controlling a snake that grows in length as it eats apples,
while avoiding collisions with itself, rotten apple, or rock.

Classes and functionalities provided:
- Constants for screen and grid dimensions, as well as game element colors.
- GameObject: A base class for all game entities, providing common attributes.
- GameObjectThings: A subclass of GameObject for drawable objects
  (like apples and rocks).
- Apple: Represents the main item the snake consumes to grow.
- RottenApple: A variant of Apple that may have negative effects if consumed.
- Snake: Represents the player-controlled snake, with functionalities
  for movement, growth, and collision detection.
- Rock: Represents a stationary obstacle on the game field.
- handle_keys: Manages user input for controlling the snake's direction.
- game_interaction: Handles the game's core mechanics, including
  object movement, collisions, and resetting game state.

To play the game:
1. Use arrow keys to control the snake's movement.
2. Avoid colliding with the snake's own body or obstacles.
3. Consume apples to grow the snake longer and score points.
"""
from random import randint, choice

import pygame as pg

# Constants for field and grid sizes:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Driving directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

KEYS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT)}

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

# The default color of the GameObject class
DEFAULT_COLOR = (200, 200, 200)

# The speed of the snake:
SPEED = 10

# Customize the game window:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Title of the playing field window:
pg.display.set_caption('The Snake')

# Setting the time:
clock = pg.time.Clock()


class GameObject:
    """Parent class for all game classes."""

    def __init__(self, position: tuple[int, int] = None,
                 body_color: tuple[int, int, int] = None):
        """Initialization of parent class attributes.

        1. position - responsible for the position on the game screen
           (in this case the center of the screen)
        2. body_color - color of the object
        """
        self.position = position or SCREEN_CENTER
        self.body_color = body_color or DEFAULT_COLOR

    def draw(self) -> None:
        """Method that is intended to be overridden in child classes."""
        raise NotImplementedError(
            "This method should be overridden in a child class")


class GameObjectThings(GameObject):
    """A parent class for all subject classes."""

    def draw(self) -> None:
        """Draws an object on the playing surface."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(
            self, occupied_positions: set[tuple[int, int]] = None) -> None:
        """Sets the random position of the object on the playing field."""
        while True:
            # Generate random coordinates
            x_coordinate = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_coordinate = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            coordinates = (x_coordinate, y_coordinate)

            # Checks if the new coordinates are in the busy list
            if (coordinates not in occupied_positions
                    or occupied_positions is None):
                self.position = coordinates
                break

    @property
    def object_position(self):
        """Returns the position of the object."""
        return self.position


class Snake(GameObject):
    """The class responsible for the snake object."""

    def __init__(self, position: tuple[int, int] = SCREEN_CENTER,
                 body_color: tuple[int, int, int] = SNAKE_COLOR):
        """Initialization of attributes of this class.

        1. position - responsible for the position on the game screen
           (inherits from the parent class and packs it into a list)
        2. length - length of the snake (Initial value 1)
        3. direction - direction of snake movement (Initial value is RIGHT)
        4. next_direction - the next direction of movement that
           will be applied
           after the key press is processed
        5. body_color - object color
        """
        super().__init__(body_color=body_color)
        self.next_direction = None
        self.direction = None
        self.length = None
        self.positions = None
        self.reset(position=position)

    def update_direction(self) -> None:
        """Updates the direction of the snake's movement."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def snake_is_growing(self) -> None:
        """Increases length of the snake."""
        self.length += 1

    def snake_is_shrinking(self) -> None:
        """Shrinking length of the snake."""
        if self.length > 1:
            self.length -= 1

    def move(self) -> None:
        """Change the snake's position.

        Updates the snake's position by adding a new
        head to the beginning of the positions list and deleting
        the last element if the snake's length has not increased.
        the length of the snake has not increased.
        """
        # Get the coordinates of the current head position
        x_coordinate, y_coordinate = self.get_head_position()

        # Get the changes in x and y based on the current direction
        x_direction, y_direction = self.direction

        # Calculate the new head position
        # Handle collision with x boundary and y boundary
        new_head_position = (
            (x_coordinate + x_direction * GRID_SIZE)
            % (SCREEN_WIDTH + GRID_SIZE),
            (y_coordinate + y_direction * GRID_SIZE)
            % (SCREEN_HEIGHT + GRID_SIZE))

        # Add the new head position to the top of the list
        self.positions.insert(0, new_head_position)

        # Removes the last value from the snake coordinate list until it
        # match the length of the snake
        while len(self.positions) > self.length:
            del self.positions[-1]

    def draw(self) -> None:
        """Draws the snake on the screen."""
        for position in self.positions[1:]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Sketching a snake's head
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Not property because it doesn't pass the autotests
    def get_head_position(self) -> tuple[int, int]:
        """Returns the position of the snake's head."""
        return self.positions[0]

    @property
    def body_positions(self) -> set[tuple[int, int]]:
        """Returns the position of the snake's body."""
        return self.positions[1:] if len(self.positions) > 1 else {}

    def reset(self, position: tuple[int, int] = None) -> None:
        """Resets the snake to its initial state."""
        self.positions = [position or SCREEN_CENTER]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


class Apple(GameObjectThings):
    """The class responsible for the apple object."""

    def __init__(self,
                 occupied_positions: set[tuple[int, int]] = SCREEN_CENTER,
                 body_color: tuple[int, int, int] = APPLE_COLOR):
        """Initialization of attributes of this class.

        1. position - responsible for the position on the game screen
           (calls static function randomize_position)
        2. body_color - color of the object
        """
        super().__init__(
            position=self.randomize_position(occupied_positions),
            body_color=body_color)


class RottenApple(GameObjectThings):
    """The class responsible for the rotten apple object."""

    def __init__(self, occupied_positions: set[tuple[int, int]] = None,
                 body_color: tuple[int, int, int] = None):
        """Initialization of attributes of this class."""
        super().__init__(
            body_color=body_color or ROTTEN_APPLE_COLOR)
        self.randomize_position(occupied_positions)


class Rock(GameObjectThings):
    """The class responsible for the rock object."""

    def __init__(self, occupied_positions: set[tuple[int, int]] = None,
                 body_color: tuple[int, int, int] = None):
        """Initialization of attributes of this class."""
        super().__init__(
            body_color=body_color or ROCK_COLOR)
        self.randomize_position(occupied_positions)


def handle_keys(game_object: Snake) -> None:
    """Processes keystrokes to change the direction of the snake."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit("Quitting the game")
        elif event.type == pg.KEYDOWN:
            # Get a new direction or None
            new_direction = KEYS.get(event.key, None)
            # Checking the old direction
            if new_direction and game_object.direction != new_direction[1]:
                # Set a new direction
                game_object.next_direction = new_direction[0]


def game_interaction(snake: Snake, apple: Apple,
                     rotten_apple: RottenApple, rock: Rock) -> None:
    """Handles all basic game interactions.

    Such as::
    dropping the snake, moving objects, zooming in
    and zooming in and out of the snake.
    """
    # Checking for a game reset when the snake collides with itself
    # and colliding with a rock
    if (snake.get_head_position() in snake.body_positions
            or snake.get_head_position() == rock.object_position):
        # Reset the state of the snake
        snake.reset()

        # Creates a variable with all occupied positions
        # And moves the apple
        occupied_positions_pull = set().union(
            {snake.get_head_position()})
        apple.randomize_position(occupied_positions_pull)

        # Add to pull new value of apple coordinates
        # And moves the rotten apple
        occupied_positions_pull.union(
            {snake.get_head_position(),
             apple.object_position})
        rotten_apple.randomize_position(occupied_positions_pull)

        # Add to pull new value of rotten_apple coordinates
        # And moves the rock
        occupied_positions_pull.union(
            {snake.get_head_position(),
             apple.object_position,
             rotten_apple.object_position})
        rock.randomize_position(occupied_positions_pull)
    # Checks to see if the snake's head collides with the apple,
    # and if passed, enlarges the snake and moves the apple
    elif snake.get_head_position() == apple.object_position:
        # Creates a variable with all occupied positions
        occupied_positions_pull = set(snake.body_positions or {}).union(
            {snake.get_head_position(),
             apple.object_position,
             rotten_apple.object_position,
             rock.object_position})

        # Increases the snake
        snake.snake_is_growing()

        # Moves the apple
        apple.randomize_position(occupied_positions_pull)
    # Checks to see if the snake's head collides with a rotten apple,
    # and if passed, shrinks the snake and moves the rotten apple
    elif snake.get_head_position() == rotten_apple.object_position:
        # Creates a variable with all occupied positions
        occupied_positions_pull = set(snake.body_positions or {}).union(
            {snake.get_head_position(),
             apple.object_position,
             rotten_apple.object_position,
             rock.object_position})

        # Shrinks the snake
        snake.snake_is_shrinking()

        # Moves the rotten apple
        rotten_apple.randomize_position(occupied_positions_pull)


def main() -> None:
    """The main function that starts the main code of the game."""
    # PyGame initialization:
    pg.init()

    # Initialization of game classes:
    snake = Snake()
    apple = Apple(occupied_positions={snake.get_head_position()})
    rotten_apple = RottenApple(occupied_positions={snake.get_head_position(),
                                                   apple.object_position})
    rock = Rock(occupied_positions={snake.get_head_position(),
                                    apple.object_position,
                                    rotten_apple.object_position})

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
        # Tried to use the proposed precode to erase cells,
        # but in places where the snake crawled formed a
        # cell that overlapped the snake itself, apples, etc.
        # In my opinion, this is just the closest option.
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Drawing an apple and a snake
        apple.draw()
        snake.draw()
        rotten_apple.draw()
        rock.draw()

        # Screen refresh
        pg.display.update()


if __name__ == '__main__':
    main()
