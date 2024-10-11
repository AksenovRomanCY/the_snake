from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """ Родительский класс для всех игровых классов
    (таких, как 'Snake' и 'Apple')

    """

    def __init__(self):
        """ Иницилизация атрибутов родительского класса
        1. position - отвечает за позицию на игровом экране
           (в данном случе центр экрана)
        2. body_color - цвет объекта

        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """ Абстрактный метод, который предназначен
        для переопределения в дочерних классах

        """
        pass


class Apple(GameObject):
    """ Класс отвечающий за объект яблока,
    в частности за его позицию и отрисовку на игровом поле

    """

    def __init__(self):
        """ Иницилизация атрибутов данного класса
        1. position - отвечает за позицию на игровом экране
           (вызывает статическиую функцию randomize_position)
        2. body_color - цвет объекта

        """
        super().__init__()
        self.position = self.randomize_position([self.position])
        self.body_color = APPLE_COLOR

    @staticmethod
    def randomize_position(snake_positions: list[tuple[int, int]]) -> tuple[int, int]:
        """ Устанавливает случайное положение яблока
        на игровом поле

        """
        while True:
            x_coordinate = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_coordinate = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            # Создаёт генератор который каждую свою итерацию проверяют координаты змеи на координаты яблока.
            # all() проверяет что все элементы списка были True
            if all(x_coordinate != part[0] and y_coordinate != part[1] for part in snake_positions):
                return x_coordinate, y_coordinate

    def draw(self) -> None:
        """ Отрисовывает яблоко на игровой поверхности

        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """ Класс отвечающий за объект змеи,
    в частности за его изменением, передвижением,
    отрисовкой и сбросом

    """

    def __init__(self):
        """ Иницилизация атрибутов данного класса
        1. position - отвечает за позицию на игровом экране
           (наследует из родительского класса и упаковывает в список)
        2. length - длина змейки (Изначальное значение 1)
        3. direction - направление движения змейки (Изначальное значение RIGHT)
        4. next_direction — следующее направление движения, которое будет применено
           после обработки нажатия клавиши
        5. body_color - цвет объекта

        """
        super().__init__()
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self) -> None:
        """ Обновляет направление движения змейки

        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """ Обновляет позицию змейки, добавляя новую
        голову в начало списка positions и удаляя последний элемент, если
        длина змейки не увеличилась.

        """
        if self.direction == UP:
            # Проверяет столкнулась ли змея с верхним барьером
            if self.get_head_position[1] <= 0:
                new_head_position = (self.get_head_position[0], 460)
            else:
                new_head_position = (self.get_head_position[0], self.get_head_position[1] - 20)
            self.positions.insert(0, new_head_position)
        elif self.direction == DOWN:
            # Проверяет столкнулась ли змея с нижним барьером
            if self.get_head_position[1] >= 460:
                new_head_position = (self.get_head_position[0], 0)
            else:
                new_head_position = (self.get_head_position[0], self.get_head_position[1] + 20)
            self.positions.insert(0, new_head_position)
        elif self.direction == LEFT:
            # Проверяет столкнулась ли змея с левым барьером
            if self.get_head_position[0] <= 0:
                new_head_position = (620, self.get_head_position[1])
            else:
                new_head_position = (self.get_head_position[0] - 20, self.get_head_position[1])
            self.positions.insert(0, new_head_position)
        elif self.direction == RIGHT:
            # Проверяет столкнулась ли змея с правым барьером
            if self.get_head_position[0] >= 620:
                new_head_position = (0, self.get_head_position[1])
            else:
                new_head_position = (self.get_head_position[0] + 20, self.get_head_position[1])
            self.positions.insert(0, new_head_position)

        # Проверяет увеличилась ли змейка или нет
        if len(self.positions) > self.length:
            del self.positions[-1]   # Удаляет 'хвост' змеи

    def draw(self) -> None:
        """ Отрисовывает змейку на экране

        """
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    @property
    def get_head_position(self) -> tuple[int, int]:
        """ Возвращает позицию головы змейки (первый элемент в списке positions)

        """
        return self.positions[0]

    def reset(self) -> None:
        """ Cбрасывает змейку в начальное состояние

        """
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object: Snake) -> None:
    """ Обрабатывает нажатия клавиш, чтобы изменить направление
    движения змейки

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


def main() -> None:
    # Инициализация PyGame:
    pygame.init()

    # Инициализация игровых классов:
    my_apple = Apple()
    my_snake = Snake()

    while True:
        # Выставляет темп игры
        clock.tick(SPEED)

        # Обработка ввода с клавиатуры
        handle_keys(game_object=my_snake)

        # Обновление направления и движение змейки
        my_snake.update_direction()
        my_snake.move()

        # Проверка на столкновение головы змейки с яблоком
        if my_snake.get_head_position == my_apple.position:
            my_snake.length += 1
            my_apple.position = my_apple.randomize_position(my_snake.positions)

        # Проверка на столкновение змейки с самой собой
        if my_snake.get_head_position in my_snake.positions[1:]:
            my_snake.reset()    # Сбрасываем состояние змейки

        # Очищает экран перед отрисовкой
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка яблока и змейки
        my_apple.draw()
        my_snake.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
