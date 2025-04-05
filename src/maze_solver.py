import random
import time

MAZE_DIMS = (20, 20)

WALL = '#'

maze = [['.'] * MAZE_DIMS[1] for _ in range(MAZE_DIMS[0])]

def print_maze():
    print("\033[H", end='')
    for row in maze:
        print(' '.join(row))
        
        
def create_border():
    for i in range(MAZE_DIMS[0]):
        for j in range(MAZE_DIMS[1]):
            if i == 0 or i == MAZE_DIMS[0] - 1 or j == 0 or j == MAZE_DIMS[1] - 1:
                maze[i][j] = '#'
                
                
def create_obstructions(factor):
    num_obs = int(factor * (MAZE_DIMS[0] - 1) * (MAZE_DIMS[1] - 1))

    x_obs = [random.randint(1, MAZE_DIMS[1] - 2) for _ in range(num_obs)]
    y_obs = [random.randint(1, MAZE_DIMS[0] - 2) for _ in range(num_obs)]
    
    for x, y in zip(x_obs, y_obs):
        maze[y][x] = WALL
        
        
def maze_solver(maze, src, sink):
    dirs = [(0, -1),
            (-1, 0),
            (0, 1),
            (1, 0)]
    
    def walk(maze, cur, sink, seen, path):
        # Base cases
        if cur in seen:
            return False
        
        seen.append(cur)
        
        if cur[0] < 0 or cur[0] > MAZE_DIMS[0] - 1 or cur[1] < 0 or cur[1] > MAZE_DIMS[1] - 1:  # Outside the borders
            return False
        
        if maze[cur[0]][cur[1]] == WALL:    # Obstructions
            return False
        
        path.append(cur)
        
        if cur == sink:
            print('Found SINK!')
            return True
        
        # Live viewer
        if cur is not src:
            maze[cur[0]][cur[1]] = 'x'
        print_maze()
        time.sleep(0.1)
        
        for d in dirs:
            if walk(maze, (cur[0] + d[0], cur[1] + d[1]), sink, seen, path):
                return True
            
        pos = path.pop()
        if pos is not src:
            maze[pos[0]][pos[1]] = '.'
        
        return False
    
    path = []
    walk(maze, src, sink, [], path)
    
    if not path:
        print('No path exists!')
    else:
        view_path(path)
        

def view_path(path):
    for i in range(1, len(path) - 1):
        pos = path[i]
        maze[pos[0]][pos[1]] = 'X'
    

if __name__ == '__main__':
    src = (MAZE_DIMS[0] - 1, 1)
    sink = (0, MAZE_DIMS[1] - 2)
    
    create_border()
    create_obstructions(factor=0.25)
    
    maze[src[0]][src[1]] = 'S'
    maze[sink[0]][sink[1]] = 'F'
    
    maze_solver(maze, src, sink)
    