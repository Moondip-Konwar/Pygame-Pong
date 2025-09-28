import time
from random import uniform
from typing import Literal

import pygame

# Pygame initial Setup
_ = pygame.init()
running: bool = True
screen: pygame.Surface = pygame.display.set_mode((1280, 620))
clock: pygame.time.Clock = pygame.time.Clock()


# Classes
class Paddle(pygame.Rect):
    init_speed: float = 10
    speed: float = init_speed

    def __init__(self, side: Literal["left", "right"]):
        width: int = 20
        height: int = 80

        x_offset: int = 10
        left: int = (
            0 + x_offset if side == "left" else screen.get_width() - x_offset - width
        )
        top: int = (screen.get_height() - height) // 2
        super().__init__(left, top, width, height)


class Ball(pygame.Rect):
    def __init__(self):
        self.radius: int = 8
        self.init_speed: float = 10
        self.speed: float = self.init_speed
        self.direction: pygame.Vector2 = pygame.Vector2(-1, 0)
        super().__init__(
            screen.get_width() // 2,
            screen.get_height() // 2,
            self.radius * 2,
            self.radius * 2,
        )


# Game objects
player: Paddle = Paddle("left")
computer: Paddle = Paddle("right")
ball: Ball = Ball()
speed_increase = 1
color: pygame.Color = pygame.Color(255, 255, 255)


# Functions
def check_quit() -> bool:  # Checks quitting events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False


def increase_difficulty() -> None:
    global color
    speed_increase = int(uniform(-2, 1)) + 1
    ball.speed += speed_increase
    Paddle.speed += speed_increase
    color -= pygame.Color(0, 5, 10)


def reset() -> None:
    global player, computer, ball, color

    color = pygame.Color(255, 255, 255)
    ball.left = screen.get_width() // 2
    ball.top = screen.get_height() // 2
    ball.direction.y = 0
    ball.speed = ball.init_speed

    Paddle.speed = Paddle.init_speed
    player = Paddle("left")
    computer = Paddle("right")

    time.sleep(0.5)


def render() -> None:  # Handles drawing and rendering
    _ = screen.fill("black")

    # Paddles
    _ = pygame.draw.rect(screen, "white", player)
    _ = pygame.draw.rect(screen, "white", computer)

    # Ball
    _ = pygame.draw.circle(screen, color, (ball.left, ball.top), ball.radius)

    # Lines
    line_color = pygame.Color(100, 100, 100)
    _ = pygame.draw.line(
        screen,
        line_color,
        (player.x, player.y + player.height / 2),
        (ball.x, ball.y),
    )
    _ = pygame.draw.line(
        screen,
        line_color,
        (computer.x, computer.y + computer.height / 2),
        (ball.x, ball.y),
    )
    _ = pygame.draw.line(
        screen, line_color, (ball.x, ball.y), (screen.get_width() / 2, 0)
    )
    _ = pygame.draw.line(
        screen,
        line_color,
        (ball.x, ball.y),
        (screen.get_width() / 2, screen.get_height()),
    )
    # _ = pygame.draw.line(
    #    screen,
    #    "red",
    #    (ball.x, ball.y),
    #    (
    #        ball.left * ball.speed * ball.direction.x,
    #        ball.top * ball.speed * ball.direction.y,
    #    ),
    # )
    pygame.display.flip()


def update() -> None:  # Handles game object states and motion
    global ball

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.top -= int(Paddle.speed)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.top += int(Paddle.speed)

    # Ball collision
    if ball.colliderect(player) or ball.colliderect(computer):
        ball.direction.x *= -1
        ball.direction.y = uniform(-1.0, 1.0)

        increase_difficulty()
    if ball.top <= 0 or ball.bottom >= screen.get_height():
        ball.direction.y = (
            abs(ball.direction.y) * -1
            if ball.bottom >= screen.get_height()
            else abs(ball.direction.y)
        )
    if ball.left <= 0 or ball.right >= screen.get_width():
        reset()

    # Ball Movement
    ball.left += int(ball.direction.x * ball.speed)
    ball.top += int(ball.direction.y * ball.speed)

    # Computer Movement
    computer_dir_y = 0
    if (
        abs(computer.top - ball.top) < Paddle.speed
        or ball.left < screen.get_width() / 2
    ):
        computer_dir_y = 0
    elif computer.top > ball.top:
        computer_dir_y = -1
    else:
        computer_dir_y = 1
    computer.top += int(computer_dir_y * Paddle.speed)

    # Paddle Limiters
    player.top = player.top if player.top >= 0 else 0
    player.bottom = (
        player.bottom if player.bottom <= screen.get_height() else screen.get_height()
    )
    computer.top = computer.top if computer.top >= 0 else 0
    computer.bottom = (
        computer.bottom
        if computer.bottom <= screen.get_height()
        else screen.get_height()
    )


# Main loop
while running:
    running = not check_quit()
    update()
    render()
    _ = clock.tick(60)

pygame.quit()
