"""Игра «Змейка»."""

from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

KEY_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


def draw_cell(position, color, border_color=BORDER_COLOR):
    """Закрасить одну ячейку игрового поля и обвести её границей."""
    rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, color, rect)
    if border_color:
        pygame.draw.rect(screen, border_color, rect, 1)


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=None):
        """Создать объект в центре экрана с заданным цветом."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовать объект на игровом поле."""
        pass


class Apple(GameObject):
    """Яблоко, которое съедает змейка."""

    def __init__(self):
        """Создать яблоко в случайной ячейке."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self, occupied=()):
        """Выбрать случайную ячейку, не занятую позициями из occupied."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied:
                break

    def draw(self):
        """Отрисовать яблоко на игровом поле."""
        draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Змейка, которой управляет игрок."""

    def __init__(self):
        """Создать змейку из одной головы, движущуюся вправо."""
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Применить направление, выбранное игроком."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Сдвинуть змейку на одну ячейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовать змейку и затереть клетку, которую она покинула."""
        for position in self.positions:
            draw_cell(position, self.body_color)
        if self.last:
            draw_cell(self.last, BOARD_BACKGROUND_COLOR, None)

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Вернуть змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать нажатия клавиш и закрытие окна."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            new_direction = KEY_DIRECTIONS.get(event.key)
            dir_x, dir_y = game_object.direction
            if new_direction and new_direction != (-dir_x, -dir_y):
                game_object.next_direction = new_direction


def main():
    """Запустить основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()
        if head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif head in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
