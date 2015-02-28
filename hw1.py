from sys import argv, stdin
from copy import deepcopy
from queue import PriorityQueue

SOLUTION = ((1,2,3),(4,5,6),(7,8,0))
TILE_MAP = {
    tile: (i,j) # location of each solution tile
    for i, row in enumerate(SOLUTION)
    for j, tile in enumerate(row)
}

class NoSolution(ValueError):
    """Raise when no solution is possible."""

def main():
    input_string = stdin.read() # user must Ctrl+D to submit
    try:
        start_board = parse(input_string)
    except ValueError as e:
        print('Invalid board:', e)
        return
    try:
        path = find_path(start_board)
    except NoSolution:
        print('No possible solution.')
        return

    # THE BEST BOARD SERIALIZER EVER:
    print('\n\n'.join(
        '\n'.join(
            ' '.join(
                (str(tile) if tile != 0 else ' ')
                for tile in row)
            for row in board)
        for board in path))

def parse(input_string):
    """Returns a board object.
    
    Raises ValueError on bad input.

    """
    tokens = input_string.strip().split()
    tiles = tuple(map(int, tokens))
    if len(tiles) != 9:
        raise ValueError('should be nine tiles')
    if set(tiles) != set(range(9)):
        raise ValueError('tiles should be 0..8')
    return (tiles[:3], tiles[3:6], tiles[6:]) # this is a board

def neighbors(board):
    """Returns a list of possible boards (as neighbors)."""
    zi, zj = find_zero(board)
    neighbors = set()
    for i, j in find_adjacent(zi, zj):
        next_board = to_lists(board)
        next_board[i][j], next_board[zi][zj] = next_board[zi][zj], next_board[i][j]
        neighbors.add(to_tuples(next_board))
    return neighbors

def find_zero(board):
    """Returns coordinates of zero tile."""
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == 0:
                return (i, j)

def find_adjacent(i, j):
    """Returns list of tiles adjacent to given coordinates."""
    adjacent = [(i-1,j),(i,j-1),(i+1,j),(i,j+1)]
    return [(i,j) for (i,j) in adjacent if 0 <= i < 3 and 0 <= j < 3]

def to_lists(board):
    """Converts nested tuples to lists."""
    return [list(row) for row in board]

def to_tuples(board):
    """Converts nested lists to tuples."""
    return tuple(tuple(row) for row in board)

def distance(board):
    """Returns an int with manhattan distance to solution."""
    total = 0
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == 0:
                continue
            si, sj = TILE_MAP[tile]
            total += abs(i - si) + abs(j - sj)
    return total

def find_path(board):
    """Returns a list of boards between 'board' and SOLUTION

    Use A* algorithm to generate this list."""
    queue = PriorityQueue()
    queue.put((0, board))
    previous = {board: None}
    cost = {board: 0}
    visited = set()

    while not queue.empty():
        _, current = queue.get()
        visited.add(current)

        if current == SOLUTION:
            break

        for neighbor in neighbors(current):
            if neighbor in visited:
                # Ignore boards already tried (and hit dead end).
                continue

            new_cost = cost[current] + 1
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost + distance(neighbor)
                previous[neighbor] = current
                queue.put((priority, neighbor))

    if SOLUTION not in previous:
        raise NoSolution

    # Back up through the previous links to determine path.
    path = []
    node = SOLUTION
    while node:
        path.append(node)
        node = previous[node]

    # The path is backwards. Reverse it!
    return list(reversed(path))

if __name__ == '__main__':
    main()
