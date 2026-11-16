# Imports
# Pygame for the game code
# Random for the player shape randomization
import pygame, random

# Pygame
pygame.init()

# Screen resolution
# Width and height of the size of the window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Game window
# Uses the screen width and height to make the screen window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("QUADRIS")

# Colours
BLUE = (0, 0, 200) # For large rectangle shape
RED = (255, 0, 0) # For rectangle shape
GREEN = (0, 200, 0) # For square shape
BACK = (4, 7, 42) # For the background
YELLOW = (255, 255, 0) # For line shape
WHITE = (255, 255, 255) # For text colour
BLACK = (0, 0, 0) # For background grid

# Grid in the background
# Lines in the background to make the game more visually better
grid = [
    pygame.Rect(50, 0, 1, 800),
    pygame.Rect(100, 0, 1, 800),
    pygame.Rect(150, 0, 1, 800),
    pygame.Rect(200, 0, 1, 800),
    pygame.Rect(250, 0, 1, 800),
    pygame.Rect(300, 0, 1, 800),
    pygame.Rect(350, 0, 1, 800),
    pygame.Rect(400, 0, 1, 800),
    pygame.Rect(450, 0, 1, 800),
    pygame.Rect(500, 0, 1, 800),
    pygame.Rect(550, 0, 1, 800),
    pygame.Rect(600, 0, 1, 800),
    pygame.Rect(650, 0, 1, 800),

    pygame.Rect(0, 50, 600, 1),
    pygame.Rect(0, 100, 600, 1),
    pygame.Rect(0, 150, 600, 1),
    pygame.Rect(0, 200, 600, 1),
    pygame.Rect(0, 250, 600, 1),
    pygame.Rect(0, 300, 600, 1),
    pygame.Rect(0, 350, 600, 1),
    pygame.Rect(0, 400, 600, 1),
    pygame.Rect(0, 450, 600, 1),
    pygame.Rect(0, 500, 600, 1),
    pygame.Rect(0, 550, 600, 1),
    pygame.Rect(0, 600, 600, 1),
    pygame.Rect(0, 650, 600, 1),
    pygame.Rect(0, 700, 600, 1),
    pygame.Rect(0, 750, 600, 1)
]

# Player size defining variables
# Player x and y variables
player_size_x = 0
player_size_y = 0

# Music
# Loads the tetris music file, sets the volume and then replays it when it ends
pygame.mixer.music.load("03. A-Type Music (v1.1).mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

# Spawn player function
def spawn_player():
    
    # Randomized choise of the players shape
    shape = random.choice(["shape1", "shape2", "shape3", "shape4"])

    # Square shape
    if shape == "shape1":
        width = 100
        height = 100

    # Recangle shape
    elif shape == "shape2":
        width = 150
        height = 100

    # Large rectangle shape
    elif shape == "shape3":
        width = 200
        height = 100

    # Line shape
    else:
        width = 50
        height = 100

    # Return for the player spawn position, shape selected and the size of that shape
    return {
        "x": 300,
        "y": 0,
        "shape": shape,
        "width": width,
        "height": height,
    }

# Use the player spawn function
player = spawn_player()

# Uses the spawn position, shape selected and size of that shape from the spawn player function
player_x = player["x"]
player_y = player["y"]
player_shape = player["shape"]
player_width = player["width"]
player_height = player["height"]

# Game varibles
clock = pygame.time.Clock()
# Game use checks
running = True
loose = False
start = False
# Game speed variable
tick = 0
# Top info section
score = 0
level = 1
mode = "EASY"

# Locked shape list
locked_shapes = []

# Function for row clearing
def clear_full_rows():
    global locked_shapes, score

    # Store number of pixels in each row
    rows = {}

    # Count how many pixels are filled in each row
    for shape in locked_shapes:
        y = shape["y"]

        # If the row is not in the rows list then it will add it to the list and set the value to 0, used to count the width of the shapes in that row
        if y not in rows:
            rows[y] = 0

        # Adds the width of the shape to the row value
        rows[y] += shape["width"]

    # Find rows that are the size of the screen width
    # List of full rows that will be cleared
    full_rows = []

    # Adds up the total width of the shapes and if the width is equal to the width of the screen then the line will get cleared
    for y, width in rows.items():
        if width >= SCREEN_WIDTH:
            full_rows.append(y)

    # Remove shapes in full rows
    for row_y in full_rows:

        # Add 100 score if a line gets cleared
        score = score + 100

        # Remove shapes in the full row
        locked_shapes = [
            shape for shape in locked_shapes
            if shape["y"] != row_y
        ]

        # Make stacked shapes drop down if a line is cleared
        for shape in locked_shapes:
            if shape["y"] < row_y:
                shape["y"] += 100

# Game loop
while running:

    # Event check for if the game is still running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keybinds and key presses
    keys = pygame.key.get_pressed()

    # Title screen before the game starts
    if not start:
        # Background
        screen.fill(BACK)

        # Title
        font = pygame.font.SysFont(None, 72)
        message = font.render("QUADRIS", True, WHITE)
        screen.blit(message, (185, 200))

        # 1-3 Option
        message = font.render("PRESS 1-3", True, WHITE)
        screen.blit(message, (177, 300))

        # Option 1
        message = font.render("1. EASY", True, WHITE)
        screen.blit(message, (177, 400))

        # Option 2
        message = font.render("2. NORMAL", True, WHITE)
        screen.blit(message, (177, 450))

        # Option 3
        message = font.render("3. HARD", True, WHITE)
        screen.blit(message, (177, 500))

        # Easy mode selection
        if keys[pygame.K_1]:
            start = True
            tick = 5
            mode = "EASY"

        # Normal mode selection
        if keys[pygame.K_2]:
            start = True
            tick = 7.5
            mode = "NORMAL"

        # Hard mode selection
        if keys[pygame.K_3]:
            start = True
            tick = 10
            mode = "HARD"

        pygame.display.flip()
        clock.tick(60)

        continue
    
    # Check if player has selected a game mode
    if start == True:

        # As the player gets farther the game changes
        # Level 2
        # Easy mode becomes normal mode
        if tick == 5:
            if score >= 1000:
                tick = 7.5
                level = 2

        # Normal mode becomes hard mode
        if tick == 7.5:
            if score >= 1000:
                tick = 10
                level = 2

        # Hard mode becomes harder
        if tick == 10:
            if score >= 1000:
                tick = 12.5
                level = 2

        # Level 3
        # Easy mode becomes harder
        if tick == 5:
            if score >= 2000:
                tick = 10
                level = 3

        # Normal mode becomes harder
        if tick == 7.5:
            if score >= 2000:
                tick = 12.5
                level = 3

        # Hard mode becomes harder
        if tick == 10:
            if score >= 2000:
                tick = 15
                level = 3

        # Check if you have not lost yet
        if not loose:

            # If the player reaches the top the game ends
            for shape in locked_shapes:
                if shape["y"] == 0:
                    loose = True

            # Move left
            if keys[pygame.K_a]:
                player_x -= 50
                player = pygame.Rect(player_x, player_y, player_width, player_height)

            # Move right
            if keys[pygame.K_d]:
                player_x += 50
                player = pygame.Rect(player_x, player_y, player_width, player_height)

            # Gravity
            player_y += 50

            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

            # Locked shapes collision
            for shape in locked_shapes:
                # Collision for locked shapes
                locked_rect = pygame.Rect(
                    shape["x"],
                    shape["y"],
                    shape["width"],
                    shape["height"]
                )

                # If the player collides with a locked shape    
                if player_rect.colliderect(locked_rect):

                    # Moves player up so the shapes dont phase into each other
                    player_y -= 50

                    # Adds shape to locked shape list
                    locked_shapes.append({
                        "x": player_x,
                        "y": player_y,
                        "width": player_width,
                        "height": player_height,
                        "shape": player_shape
                    })

                    # Adds 10 score for when a shape is placed
                    score = score + 10

                    # Calls the function to clear full rows
                    clear_full_rows()

                    # Spawns a new player shape
                    player = spawn_player()
                    player_x = player["x"]
                    player_y = player["y"]
                    player_shape = player["shape"]
                    player_width = player["width"]
                    player_height = player["height"]

                # Removes shapes that are above the screen
                # Meant to fix a bug where shapes would get locked on the player spawn point
                if shape["y"] < 1:
                    locked_shapes.remove(shape)
                    

            # Borders
            # Left border
            if player_x < 0:
                player_x = 0

            # Right border
            if player_x > SCREEN_WIDTH - player_width:
                player_x = SCREEN_WIDTH - player_width

            # Top border
            if player_y < 0:
                player_y = 0

            # Bottom border if the player touches it, it adds the shape to the locked shapes list
            if player_y >= SCREEN_HEIGHT - player_height:
                locked_shapes.append({
                    "x": player_x,
                    "y": player_y,
                    "width": player_width,
                    "height": player_height,
                    "shape": player_shape
                })

                # Adds 10 score for when a shape is placed
                score = score + 10

                # Calls the function to clear full rows
                clear_full_rows()

                # Spawns a new player shape
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

    # Draw the grid
    for wall in grid:
            pygame.draw.rect(screen, BLACK, wall)

    # Colour for square shape
    if player_shape == "shape1":
        colour = GREEN

    # Colour for rectangle shape
    if player_shape == "shape2":
        colour = RED

    # Colour for large rectangle shape
    if player_shape == "shape3":
        colour = BLUE

    # Colour for line shape
    if player_shape == "shape4":
        colour = YELLOW

    # Draw locked shapes
    for shape in locked_shapes:

        # Colour for locked shapes
        if shape["shape"] == "shape1":
            shape_colour = GREEN
        elif shape["shape"] == "shape2":
            shape_colour = RED
        elif shape["shape"] == "shape3":
            shape_colour = BLUE
        else:
            shape_colour = YELLOW

        # Draw the locked shape
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

    # Loose
    if loose == True:
        font = pygame.font.SysFont(None, 72)
        message = font.render("YOU LOOSE", True, WHITE)
        screen.blit(message, (150, 350))
        pygame.mixer.music.set_volume(0)

    # Score, level and mode display
    # Score
    font = pygame.font.SysFont(None, 48)
    message = font.render(f"SCORE {score}", True, WHITE)
    screen.blit(message, (10, 10))

    # Level
    font = pygame.font.SysFont(None, 48)
    message = font.render(f"Level {level}", True, WHITE)
    screen.blit(message, (480, 10))

    # Mode
    font = pygame.font.SysFont(None, 48)
    message = font.render(f"{mode}", True, WHITE)
    screen.blit(message, (250, 10))

    # Update the display
    pygame.display.flip()

    # Limit the game to 7.5 fps
    clock.tick(tick)

# Close pygame
pygame.quit()