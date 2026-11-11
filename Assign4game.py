import pygame, random

pygame.init()

# Set screen resolution
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Maze Game")

# Set up colours
WHITE = (255, 255, 255)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
BACK = (4, 7, 32)
YELLOW = (255, 255, 0)

player_size_x = 0
player_size_y = 0

def spawn_player():
    shape = random.choice(["shape1", "shape2", "shape3", "shape4"])

    if shape == "shape1":
        width = 100
        height = 100

    elif shape == "shape2":
        width = 150
        height = 100

    elif shape == "shape3":
        width = 200
        height = 100

    else:
        width = 50
        height = 100

    return {
        "x": 300,
        "y": 0,
        "shape": shape,
        "width": width,
        "height": height,
    }

player = spawn_player()

player_x = player["x"]
player_y = player["y"]
player_shape = player["shape"]
player_width = player["width"]
player_height = player["height"]

# Set up the player
speed = 3

# Set up the game
clock = pygame.time.Clock()
running = True
won = False

locked_shapes = []

# Main game loop
while running:

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys being pressed
    keys = pygame.key.get_pressed()

    if not won:

        # Move left
        if keys[pygame.K_a]:
            player_x -= 50
            player = pygame.Rect(player_x, player_y, player_width, player_height)

        # Move right
        if keys[pygame.K_d]:
            player_x += 50
            player = pygame.Rect(player_x, player_y, player_width, player_height)

        # Move down
        if keys[pygame.K_SPACE]:
            player_y += 50
            player = pygame.Rect(player_x, player_y, player_width, player_height)

        player_y += 50

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        for shape in locked_shapes:
            locked_rect = pygame.Rect(
                shape["x"],
                shape["y"],
                shape["width"],
                shape["height"]
            )

            if player_rect.colliderect(locked_rect):

                player_y -= 50

                locked_shapes.append({
                    "x": player_x,
                    "y": player_y,
                    "width": player_width,
                    "height": player_height,
                    "shape": player_shape
                })

                player = spawn_player()
                player_x = player["x"]
                player_y = player["y"]
                player_shape = player["shape"]
                player_width = player["width"]
                player_height = player["height"]

        # Keep the player inside the screen
        if player_x < 0:
            player_x = 0

        if player_x > SCREEN_WIDTH - player_width:
            player_x = SCREEN_WIDTH - player_width

        if player_y < 0:
            player_y = 0

        if player_y >= SCREEN_HEIGHT - player_height:
            locked_shapes.append({
                "x": player_x,
                "y": player_y,
                "width": player_width,
                "height": player_height,
                "shape": player_shape
            })

            player = spawn_player()
            player_x = player["x"]
            player_y = player["y"]
            player_shape = player["shape"]
            player_width = player["width"]
            player_height = player["height"]

        # Update the player rectangle
        player = pygame.Rect(player_x, player_y, player_width, player_height)

    # Draw the background
    screen.fill(BACK)

    if player_shape == "shape1":
        colour = GREEN

    if player_shape == "shape2":
        colour = RED

    if player_shape == "shape3":
        colour = BLUE

    if player_shape == "shape4":
        colour = YELLOW
    # Draw locked shapes
    for shape in locked_shapes:

        if shape["shape"] == "shape1":
            shape_colour = GREEN
        elif shape["shape"] == "shape2":
            shape_colour = RED
        elif shape
            shape_colour = BLUE

        pygame.draw.rect(
            screen,
            shape_colour,
            pygame.Rect(
                shape["x"],
                shape["y"],
                shape["width"],
                shape["height"]
            )
        )
    
    # Draw the player
    player = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, colour, player)

    # Update the display
    pygame.display.flip()

    # Limit the game to 60 FPS
    clock.tick(7.5)

# Close Pygame
pygame.quit()