class Player:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.inventory = []
        self.current_map = "town"       # "town" or building name
        self.current_building = None
        self.previous_x = None          # Position to return to after leaving a building
        self.previous_y = None
        self.interacted_building = None
        self.interacted_npc = None

    def move(self, dx, dy, map_data):
        """
        Moves the player in the given direction if the target tile is walkable.
        """
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_y < len(map_data) and 0 <= new_x < len(map_data[0]):
            if map_data[new_y][new_x] in ['#', 'B', 'N', '.', 'F', 'D', 'T']:
                self.x = new_x
                self.y = new_y


class Building:
    def __init__(self, name, x, y, interior_map, entrance=(1, 1), exit_spawn=(0,0), symbol='B'):
        self.name = name
        self.x = x
        self.y = y
        self.symbol = symbol
        self.interior_map = interior_map
        self.entrance = entrance      # spawn inside
        self.exit_spawn = exit_spawn  # spawn outside when leaving



class Item:
    def __init__(self, name, x, y, symbol='I'):
        self.name = name
        self.x = x
        self.y = y
        self.symbol = symbol

    def pick_up(self, player):
        player.inventory.append(self.name)
        print(f"{self.name} added to inventory!")


class NPC:
    def __init__(self, name, x, y, symbol='N', dialogue=None):
        self.name = name
        self.x = x
        self.y = y
        self.symbol = symbol
        self.dialogue = dialogue if dialogue else [f"{self.name} says hello!"]

    def talk(self):
        """Return the first line of dialogue."""
        return self.dialogue[0]
