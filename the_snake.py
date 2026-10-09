import sys
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

# Цвет плохого яблока
BAD_APPLE_COLOR = (139, 0, 139)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
START_SPEED = 8
MAX_SPEED = 25
SPEED_INCREMENT = 1

TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        """Инициализирует объект с заданным цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект. Переопределяется в дочерних классах."""
        raise NotImplementedError(
            f'Метод draw не переопределён в {type(self).__name__}'
        )

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку игрового поля."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        cell_color = color
        if cell_color is None:
            cell_color = self.body_color
        pg.draw.rect(screen, cell_color, rect)
        if cell_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко - еда увеличивающая длину змейки."""

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=()):
        """Инициализирует яблоко с заданным цветом."""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=()):
        """Задаёт случайную позицию яблока, выровненную по сетке."""
        occupied_positions = set(occupied_positions)
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if position not in occupied_positions:
                self.position = position
                return

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_cell(self.position)


class BadApple(Apple):
    """Плохое яблоко - еда отнимающая длину змейки."""

    def __init__(self, body_color=BAD_APPLE_COLOR, occupied_positions=()):
        """Инициализирует плохое яблоко с заданным цветом."""
        super().__init__(
            body_color=body_color,
            occupied_positions=occupied_positions,
        )


class Snake(GameObject):
    """Змейка — управляемый игроком персонаж."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(body_color=body_color)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.removed = []

    def update_direction(self, new_direction):
        """Задаёт новое направление движения."""
        self.direction = new_direction

    def move(self):
        """Обновляет позицию змейки на один шаг."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.removed.append(self.positions.pop())

    def shrink(self):
        """Уменьшает длину змейки на один сегмент."""
        if self.length > 1:
            self.length -= 1
            self.removed.append(self.positions.pop())

    def grow(self):
        """Увеличивает длину змейки на один сегмент."""
        self.length += 1

    def draw(self):
        """Отрисовывает змейку на экране."""
        self.draw_cell(self.get_head_position())

        for position in self.removed:
            self.draw_cell(position, BOARD_BACKGROUND_COLOR)
        self.removed.clear()

    def get_head_position(self):
        """Получает позицию head Snake"""
        return self.positions[0]


def handle_keys(game_object):
    """Обрабатывает события клавиатуры."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

            turn = TURNS.get(event.key)
            if turn is not None:
                new_direction, opposite = turn
                if game_object.direction != opposite:
                    game_object.update_direction(new_direction)


def main():
    """Инициализирует Pygame и запускает игровой цикл."""
    # Инициализация PyGame:
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)
    bad_apple = BadApple(
        occupied_positions=snake.positions + [apple.position]
    )
    speed = START_SPEED
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(speed)

        handle_keys(snake)
        snake.move()

        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.grow()
            if speed < MAX_SPEED:
                speed = min(speed + SPEED_INCREMENT, MAX_SPEED)
            apple.randomize_position(
                snake.positions + [bad_apple.position]
            )

        elif head_position == bad_apple.position:
            snake.shrink()
            bad_apple.randomize_position(
                snake.positions + [apple.position]
            )

        elif head_position in snake.positions[4:]:
            snake.reset()
            speed = START_SPEED
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
            bad_apple.randomize_position(
                snake.positions + [apple.position]
            )

        snake.draw()
        apple.draw()
        bad_apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
