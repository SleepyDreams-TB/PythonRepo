# main.py
import pygame
from classes import Player, Building, NPC, Item
from sprites import load_all_images
from maps import TOWN_MAP, TAVERN_MAP

# -----------------------------
# Settings
# -----------------------------
TILE_SIZE = 32
MAP_WIDTH = 24
MAP_HEIGHT = 9
FPS = 10

# -----------------------------
# Colors
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
pygame.display.set_caption("Modular Grid Game")
clock = pygame.time.Clock()

# -----------------------------
# Load images
# -----------------------------
terrain_img, furniture_img, building_imgs, npc_imgs, player_img, item_imgs = load_all_images(TILE_SIZE)

# -----------------------------
# Game objects
# -----------------------------
player = Player("Hero", 3, 3)
player.saved_positions = {"town": (3, 3)}
player.current_map = "town"

buildings = [
    Building(
        "Tavern", 6, 1,
        interior_map=TAVERN_MAP,
        entrance=(12, 7),  # inside building spawn
        exit_spawn=(6, 2)  # outside town spawn
    ),
]

npcs = [NPC("Guide", 15, 2)]
items = [Item("Potion", 7, 4)]

current_building = None

# -----------------------------
# Functions
# -----------------------------
def draw_map(map_data):
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)

            # Terrain / furniture
            if cell == "^": screen.blit(terrain_img["Tree"], rect.topleft)
            elif cell == "#": screen.blit(terrain_img["Path"], rect.topleft)
            elif cell == ".": screen.blit(terrain_img["Grass"], rect.topleft)
            elif cell == "F": screen.blit(furniture_img["Floor"], rect.topleft)
            elif cell == "T": screen.blit(furniture_img["Table"], rect.topleft)
            elif cell == "|": screen.blit(furniture_img["WEWall"], rect.topleft)
            elif cell == "_": screen.blit(furniture_img["NSWall"], rect.topleft)
            elif cell == "D": screen.blit(furniture_img["Door"], rect.topleft)
            else: pygame.draw.rect(screen, WHITE, rect)

    # Draw town-only objects
    if player.current_map == "town":
        for b in buildings:
            rect = pygame.Rect(b.x*TILE_SIZE, b.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(building_imgs[b.name], rect.topleft)
        for npc in npcs:
            rect = pygame.Rect(npc.x*TILE_SIZE, npc.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(npc_imgs[npc.name], rect.topleft)
        for i in items:
            rect = pygame.Rect(i.x*TILE_SIZE, i.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(item_imgs[i.name], rect.topleft)

    # Draw player
    rect = pygame.Rect(player.x*TILE_SIZE, player.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_img, rect.topleft)

def enter_building(building):
    global current_building
    print(f"You entered {building.name}!")
    player.saved_positions[player.current_map] = (player.x, player.y)
    player.current_map = building.name
    player.x, player.y = building.entrance
    current_building = building

def exit_building():
    global current_building
    if current_building:
        print(f"You left {current_building.name}!")
        player.saved_positions[current_building.name] = (player.x, player.y)
        player.current_map = "town"
        player.x, player.y = current_building.exit_spawn
        current_building = None

def get_current_map():
    if player.current_map == "town":
        return TOWN_MAP
    else:
        return current_building.interior_map

# -----------------------------
# Main loop
# -----------------------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0, get_current_map())
    if keys[pygame.K_RIGHT]:
        player.move(1, 0, get_current_map())
    if keys[pygame.K_UP]:
        player.move(0, -1, get_current_map())
    if keys[pygame.K_DOWN]:
        player.move(0, 1, get_current_map())

    # Check building entry (only in town)
    if player.current_map == "town":
        for b in buildings:
            if player.x == b.x and player.y == b.y:
                enter_building(b)

    # Check building exit (inside building)
    if player.current_map != "town":
        map_data = get_current_map()
        if map_data[player.y][player.x] == "D":
            exit_building()

    # Draw
    screen.fill(WHITE)
    draw_map(get_current_map())
    pygame.display.flip()

pygame.quit()
