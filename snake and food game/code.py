# import libraries
import pygame
import random
import time

# size config
CELL_SIZE = 40
WIDTH = 800
HEIGHT = 600
SPEED = 0.2

# background color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#loading images
snake_img = pygame.image.load("resources/snake.png")
snake_img = pygame.transform.scale(snake_img, (CELL_SIZE, CELL_SIZE))

food_img = pygame.image.load("Resources/food.png")
food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

#block functions

def random_food_position(snake_body):
    """Generate food at a position NOT occupied by the snake"""
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake_body:
            return x, y


def check_collision(x1, y1, x2, y2):
    """Check if two grid cells overlap"""
    return x1 == x2 and y1 == y2


# game reset

def reset_game():
    snake_body = [(CELL_SIZE, CELL_SIZE)]
    direction = "RIGHT"
    food_x, food_y = random_food_position(snake_body)
    score = 0
    game_over = False
    return snake_body, direction, food_x, food_y, score, game_over


# start game
snake_body, direction, food_x, food_y, score, game_over = reset_game()

running = True
while running:

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if not game_over:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
            else:
                if event.key == pygame.K_RETURN:
                    snake_body, direction, food_x, food_y, score, game_over = reset_game()

    # update game
    if not game_over:
        head_x, head_y = snake_body[0]

        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)
        snake_body.insert(0, new_head)

        # Food collision
        if check_collision(head_x, head_y, food_x, food_y):
            score += 1
            food_x, food_y = random_food_position(snake_body)
        else:
            snake_body.pop()

        # Wall collision
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT
        ):
            game_over = True

        # Self collision
        if new_head in snake_body[1:]:
            game_over = True

    # draw
    screen.fill(BLACK)

    for x, y in snake_body:
        screen.blit(snake_img, (x, y))

    screen.blit(food_img, (food_x, food_y))

    font = pygame.font.SysFont("arial", 30)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    if game_over:
        over_text = font.render("GAME OVER - Press ENTER", True, WHITE)
        screen.blit(over_text, (200, 300))

    pygame.display.update()
    time.sleep(SPEED)

pygame.quit()