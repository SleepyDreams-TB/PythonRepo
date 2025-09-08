import pygame

def load_image(path, tile_size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (tile_size, tile_size))

def get_sprite(sheet, top_left_x, top_left_y, width, height, tile_size):
    sprite = sheet.subsurface(pygame.Rect(top_left_x, top_left_y, width, height))
    return pygame.transform.scale(sprite, (tile_size, tile_size))


def load_all_images(TILE_SIZE):
    # Sprite sheet for furniture
    sprite_sheet = pygame.image.load("assets/interior.png").convert_alpha()

    # Terrain
    terrain_img = {
        "Tree": load_image("assets/tree.png", TILE_SIZE),
        "Grass": load_image("assets/grass.png", TILE_SIZE),
        "Path": load_image("assets/path.png", TILE_SIZE)
    }

    # Furniture / interior
    furniture_img = {
        "Floor": load_image("assets/floor.png", TILE_SIZE),
        "WEWall": load_image("assets/WEwall.png", TILE_SIZE),
        "NSWall": load_image("assets/NSwall.png", TILE_SIZE),
        "Door": load_image("assets/door.png", TILE_SIZE),
        "Table": get_sprite(sprite_sheet, 116, 42, 25, 31, TILE_SIZE)
    }

    # Buildings
    building_imgs = {
        "Tavern": load_image("assets/tavern.png", TILE_SIZE),
        "Shop": load_image("assets/shop.png", TILE_SIZE),
        "TownHall": load_image("assets/townhall.png", TILE_SIZE)
    }

    # NPCs
    npc_imgs = {
        "Guide": load_image("assets/npc_guide.png", TILE_SIZE)
    }

    # Player
    player_img = load_image("assets/player.png", TILE_SIZE)

    # Items
    item_imgs = {
        "Potion": load_image("assets/potion.png", TILE_SIZE)
    }

    return terrain_img, furniture_img, building_imgs, npc_imgs, player_img, item_imgs
