from queue import Queue


from gui.load_rooms import DOOR_LOCATIONS, ROOM_MAPPING, ROOM_PLACEMENT, SPECIAL_PATHWAYS, load_rooms

class Node:
    INSTANCES = {}
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        if x not in Node.INSTANCES:
            Node.INSTANCES[x] = {}
        Node.INSTANCES[x][y] = self
    
    def get_path(self):
        path = [ROOM_PLACEMENT[DOOR_LOCATIONS[(self.x, self.y)]]]
        current = self
        while current:
            path.append((current.x, current.y))
            current = current.parent
        return path[::-1]
    
    @staticmethod
    def clear_instances():
        Node.INSTANCES = {}


def get_neighbors(node, fullmap):
    x = node.x
    y = node.y
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for k,v in ROOM_PLACEMENT.items():
        if v == (x,y) or v == (x+1, y):
            neighbors = [K for K, V in DOOR_LOCATIONS.items() if V == k]

    to_return = []
    for X, Y in neighbors:
        if X in Node.INSTANCES and Y in Node.INSTANCES[X]:
            continue
        if X in fullmap and Y in fullmap[X]:
            if fullmap[X][Y] == "corridor":
                to_return.append(Node(X, Y, node))
        elif (X,Y) in SPECIAL_PATHWAYS:
            new_x, new_y = SPECIAL_PATHWAYS[(X,Y)]
            to_return.append(Node(new_x, new_y, node))
    return to_return



def find_paths(x, y):
    """
    Uses a breadth first search to find the shortest paths to each room
    """
    Node.clear_instances()
    fullmap = load_rooms()
    goal_rooms = list(ROOM_PLACEMENT.keys())
    paths = {}
    queue = Queue()
    queue.put(Node(x, y))

    idx = 0
    while len(goal_rooms) > 0 and queue._qsize() > 0:
        idx += 1
        current = queue.get()
        if (current.x, current.y) in DOOR_LOCATIONS:
            reached_goal = DOOR_LOCATIONS[(current.x, current.y)]
            if reached_goal in goal_rooms:
                goal_rooms.remove(reached_goal)
                paths[reached_goal] = current.get_path()
        # If we haven't reached the goal, add all the neighbors to the queue
        for neighbor in get_neighbors(current, fullmap):
            queue.put(neighbor)
    
    return paths

