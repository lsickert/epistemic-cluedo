
from numpy import full

SPECIAL_PATHWAYS = {
    (8, -1): (15, 23),
    (15, 24): (8, 0),
    (24, 17): (0, 7),
    (-1, 7): (23, 17),
    (24, 7): (0, 19),
    (-1, 19): (23, 7)
}


STARTING_LOCATIONS = {
    "green": (10, 0),
    "peacock" : (13, 0),
    "mustard": (23, 14),
    "plum": (0, 13),
    "scarlett": (14, 23),
    "white": (9, 23)
}

DISPLAY_COLOR = {
    "green": "green",
    "peacock": "blue",
    "mustard": "yellow",
    "plum": "purple",
    "scarlett": "red",
    "white": "white"
}

ROOM_MAPPING = {0: "corridor", 
                1: "study", 
                2: "hall", 
                3: "lounge", 
                4: "library",
                5: "ballroom",
                6: "dining",
                7: "billiard",
                8: "conservatory",
                9: "kitchen",
                -1: "inaccessible"
}

ROOM_PLACEMENT = {
    # "study" : (3, 4),
    # "hall" : (11, 3),
    "lounge": (19, 4),
    "dining": (19, 10),
    "kitchen": (19, 21),
    "ballroom": (11, 21),
    "conservatory": (3, 22),
    "billiard": (4, 17),
    "library": (6, 10)
}


DOOR_LOCATIONS = {
    (3, 6): "study",
    (7, 3): "study",
    (11, 7): "hall",
    (12, 7): "hall",
    (16, 4): "lounge",
    (19, 6): "lounge",
    (7, 8): "library",
    (7, 12): "library",
    (8, 15): "billiard",
    (5, 19): "billiard",
    (2, 19): "conservatory",
    (7, 21): "conservatory",
    (15, 9): "dining",
    (17, 16): "dining",
    (21, 17): "kitchen",
    (16, 21): "kitchen",
    (11, 16): "ballroom",
    (12, 16): "ballroom",
}


def load_rooms(filename: str = "./resources/layout.csv"):
    fullmap = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        fullmap = {idx: {} for idx in range(len(lines) + 1)}
        for idx, line in enumerate(lines):
            for jdx, val in enumerate(line.split(',')):
                fullmap[jdx][idx] = ROOM_MAPPING[int(val)]
        

    return fullmap

FULLMAP = load_rooms()