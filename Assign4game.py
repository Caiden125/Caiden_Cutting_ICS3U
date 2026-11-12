# Imports
import pygame, random

# Pygame
pygame.init()

# Screen resolution
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Maze Game")
#test
# Colours
BLUE = (0, 0, 200)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BACK = (4, 7, 32)
YELLOW = (255, 255, 0)

# Player size defining variables
player_size_x = 0
player_size_y = 0

# Spawn player function
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

# Player speed
speed = 3

# Game varibles
clock = pygame.time.Clock()
running = True
won = False

# Locked shape list
locked_shapes = []

# Function for row clearing
def clear_full_rows():
    global locked_shapes

    rows = {}

    # Count how many pixels are filled in each row
    for shape in locked_shapes:
        y = shape["y"]

        if y not in rows:
            rows[y] = 0

        rows[y] += shape["width"]

    # Find rows that span the entire screen width
    full_rows = []

    for y, width in rows.items():
        if width >= SCREEN_WIDTH:
            full_rows.append(y)

    # Remove shapes in full rows
    for row_y in full_rows:

        locked_shapes = [
            shape for shape in locked_shapes
            if shape["y"] != row_y
        ]

        # Move shapes above downward
        for shape in locked_shapes:
            if shape["y"] < row_y:
                shape["y"] += 100

# game loop
while running:

    # event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keybinds and key presses
    keys = pygame.key.get_pressed()

    # Check if player has not won
    if not won:

        # If the player reaches the top the game ends
        for shape in locked_shapes:
            if shape["y"] == 0:
                running = false
        
        # Move left
        if keys[pygame.K_a]:
            player_x -= 50
            player = pygame.Rect(player_x, player_y, player_width, player_height)

        # Move right
        if keys[pygame.K_d]:
            player_x += 50
            player = pygame.Rect(player_x, player_y, player_width, player_height)

        # Speed up moving down
        if keys[pygame.K_SPACE]:
            player_y += 50
            player = pygame.Rect(player_x, player_y, player_width, player_height)

        # Gravity
        player_y += 50

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Locked shapes collision
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

                clear_full_rows()

                player = spawn_player()
                player_x = player["x"]
                player_y = player["y"]
                player_shape = player["shape"]
                player_width = player["width"]
                player_height = player["height"]

        # Borders
        if player_x < 0:
            player_x = 0

        if player_x > SCREEN_WIDTH - player_width:
            player_x = SCREEN_WIDTH - player_width

        if player_y < 0:
            player_y = 0

        # Bottom border for if the player reaches it
        if player_y >= SCREEN_HEIGHT - player_height:
            locked_shapes.append({
                "x": player_x,
                "y": player_y,
                "width": player_width,
                "height": player_height,
                "shape": player_shape
            })

            clear_full_rows()

            player = spawn_player()
            player_x = player["x"]
            player_y = player["y"]
            player_shape = player["shape"]
            player_width = player["width"]
            player_height = player["height"]

        # Player shape update
        player = pygame.Rect(player_x, player_y, player_width, player_height)

    # Draw the background
    screen.fill(BACK)

    # Shape colours
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
        elif shape["shape"] == "shape3":
            shape_colour = BLUE
        else:
            shape_colour = YELLOW

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

    # Limit the game to 7.5 fps
    clock.tick(7.5)

# Close pygame
pygame.quit()