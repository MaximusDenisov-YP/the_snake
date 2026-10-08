from random import choice, randint

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

# Цвет плохого яблока
BAD_APPLE_COLOR = (139, 0, 139)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
START_SPEED = 8
MAX_SPEED = 25
SPEED_INCREMENT = 1


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализирует объект с заданным цветом."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект. Переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Яблоко - еда увеличивающая длину змейки."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализирует яблоко с заданным цветом."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт случайную позицию яблока, выровненную по сетке."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class BadApple(GameObject):
    """Плохое яблоко - еда отнимающая длину змейки."""

    def __init__(self, body_color=BAD_APPLE_COLOR):
        """Инициализирует плохое яблоко с заданным цветом."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт случайную позицию плохого яблока, выровненную по сетке."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает плохое яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка — управляемый игроком персонаж."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(body_color)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.speed = START_SPEED
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.removed = []

    def update_direction(self):
        """Применяет отложенное направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

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

    def draw(self):
        """Отрисовывает змейку на экране."""
        for positions in self.positions[:-1]:
            rect = (pygame.Rect(positions, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        for position in self.removed:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.removed.clear()

    def get_head_position(self):
        """Получает позицию head Snake"""
        return self.positions[0]


def handle_keys(game_object):
    """Обрабатывает события клавиатуры."""
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


def main():
    """Инициализирует Pygame и запускает игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    bad_apple = BadApple()

    while True:
        clock.tick(snake.speed)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.length += 1
            if snake.speed < MAX_SPEED:
                snake.speed = min(snake.speed + SPEED_INCREMENT, MAX_SPEED)
            apple.randomize_position()

        elif head_position == bad_apple.position:
            if snake.length > 1:
                snake.length -= 1
                snake.removed.append(snake.positions.pop())
            bad_apple.randomize_position()

        if head_position in snake.positions[1:]:
            snake.reset()

        apple.draw()
        bad_apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
