# Snake for the TI-84 Evo
# Keys: arrows = turn, 2nd or mode = pause, clear = quit
import random
from ti_draw import clear, set_color, draw_text
from ti_draw import fill_rect as ti_fill_rect
try:
    from ti_draw import get_screen_dim
    SW, SH = get_screen_dim()
except:
    SW, SH = 320, 240

# Keep every box inside the screen and never stop the game over one box
# (the Evo gave "Height cannot be negative" for a box near the edge).
# The Evo draws boxes 1 pixel too small, so we ask for 1 pixel more.
def fill_rect(x, y, w, h):
    if x < 0:
        w, x = w + x, 0
    if y < 0:
        h, y = h + y, 0
    w, h = min(w, SW - x), min(h, SH - y)
    if w > 0 and h > 0:
        try:
            ti_fill_rect(x, y, w + 1, h + 1)
        except:
            pass
# Draw in a hidden buffer and show the finished picture at once: no flicker
try:
    from ti_draw import use_buffer, paint_buffer
    use_buffer()
except:
    paint_buffer = None
try:
    from ti_system import get_key as read_key
except:
    from ti_system import getKey as read_key
# On the Evo get_key wants one number. Find out once at the start.
try:
    read_key()
    key = read_key
except TypeError:
    def key():
        return read_key(0)
try:
    from ti_system import store_list, recall_list
except:
    store_list = recall_list = None
try:
    from time import sleep
except:
    from ti_system import sleep
try:
    import gc
except:
    gc = None

# Key numbers (the Evo uses the second number in each pair)
LEFT = (2, 24)
RIGHT = (1, 26)
UP = (3, 25)
DOWN = (4, 34)
OK = (5, 105)                 # enter
PAUSE = (21, 22)              # 2nd, mode
QUIT = (9, 45)                # clear

C = 10                        # cell size in pixels
TOP = 30                      # height of the score bar
WALL = 3                      # thickness of the blue wall
GW, GH = (SW - 2 * WALL) // C, (SH - TOP - 2 * WALL) // C
X0 = (SW - GW * C) // 2
Y0 = TOP + (SH - TOP - GH * C) // 2
BLACK = (0, 0, 0)
BODY = (0, 170, 0)
HEAD = (120, 255, 120)
FOOD = (230, 0, 0)

def paint():
    if paint_buffer:
        paint_buffer()

def cell(x, y, col):
    set_color(*col)
    fill_rect(X0 + x * C, Y0 + y * C, C - 1, C - 1)

# Wipe the whole bar (tall letters leave nothing behind), then write
def bar(s):
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, TOP - 2)
    set_color(255, 255, 255)
    draw_text(4, 20, s)

def box(lines):
    set_color(0, 0, 0)
    fill_rect(SW // 2 - 90, SH // 2 - 50, 180, 100)
    set_color(255, 255, 255)
    for i in range(len(lines)):
        draw_text(SW // 2 - 80, SH // 2 - 26 + i * 20, lines[i])

def wait_for(keys):
    paint()
    while True:
        k = key()
        if k in keys:
            return k
        sleep(0.05)

# Speeds: name, steps per move at the start, fewest steps per move (fastest)
SPEEDS = [("Slow", 7, 2), ("Normal", 5, 2), ("Fast", 3, 1)]

# High scores live in the calculator list SNAKE: [slow, normal, fast].
# (An old list with 1 number becomes the Slow high score.)
def load_best():
    try:
        l = [int(v) for v in recall_list("SNAKE")]
    except:
        l = []
    return (l + [0, 0, 0])[:3]

def save_best(bests):
    try:
        store_list("SNAKE", bests)
    except:
        pass

def direction(k):
    if k in LEFT:
        return (-1, 0)
    if k in RIGHT:
        return (1, 0)
    if k in UP:
        return (0, -1)
    if k in DOWN:
        return (0, 1)
    return None

def place_food(grid):
    for i in range(200):
        x, y = random.randrange(GW), random.randrange(GH)
        if not grid[y * GW + x]:
            return (x, y)
    for y in range(GH):                    # board almost full: search
        for x in range(GW):
            if not grid[y * GW + x]:
                return (x, y)
    return None

# Returns the chosen speed (0 slow, 1 normal, 2 fast), or -1 to quit
def start_screen(bests):
    clear()
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, SH)
    x = SW // 2 - 80
    set_color(*HEAD)
    draw_text(x + 50, 20, "SNAKE")
    set_color(255, 255, 255)
    draw_text(x, 45, "Eat food, avoid walls")
    draw_text(x, 202, "UP/DOWN + ENTER")
    choice = 0
    while True:
        for i in range(3):
            set_color(0, 0, 0)
            fill_rect(x - 20, 64 + i * 28, 220, 27)
            set_color(*((230, 200, 0) if i == choice else (150, 150, 150)))
            draw_text(x, 90 + i * 28, ("> " if i == choice else "  ") + SPEEDS[i][0]
                      + "   best " + str(bests[i]))
        k = wait_for(UP + DOWN + OK + QUIT)
        if k in QUIT:
            return -1
        if k in OK:
            return choice
        if k in UP:
            choice = (choice - 1) % 3
        if k in DOWN:
            choice = (choice + 1) % 3

def game(best, speed):
    clear()
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, SH)
    set_color(40, 90, 230)                 # blue wall: the real edge of the map
    fill_rect(X0 - WALL, Y0 - WALL, GW * C + 2 * WALL, WALL)
    fill_rect(X0 - WALL, Y0 + GH * C, GW * C + 2 * WALL, WALL)
    fill_rect(X0 - WALL, Y0, WALL, GH * C)
    fill_rect(X0 + GW * C, Y0, WALL, GH * C)
    grid = bytearray(GW * GH)              # 1 = snake is here
    snake = [(GW // 2 - 2 + i, GH // 2) for i in range(3)]   # tail ... head
    for x, y in snake:
        grid[y * GW + x] = 1
        cell(x, y, BODY)
    cell(snake[-1][0], snake[-1][1], HEAD)
    d, turns = (1, 0), []
    food = place_food(grid)
    cell(food[0], food[1], FOOD)
    name, slowest, fastest = SPEEDS[speed]
    score, delay, t = 0, slowest, 0
    bar("Score 0    Best " + str(best))
    paint()
    while True:
        k = key()
        if not k:
            pass
        elif k in QUIT:
            return score, True
        elif k in PAUSE:
            bar("PAUSED    2ND: go on")
            if wait_for(PAUSE + OK + QUIT) in QUIT:
                return score, True
            bar("Score " + str(score) + "    Best " + str(best))
            paint()
        else:
            nd = direction(k)
            # remember up to 2 quick turns; no turning straight back
            last = turns[-1] if turns else d
            if nd and len(turns) < 2 and nd != last and nd != (-last[0], -last[1]):
                turns.append(nd)
        t += 1
        if t >= delay:                     # time to move
            t = 0
            if turns:
                d = turns.pop(0)
            hx, hy = snake[-1]
            nx, ny = hx + d[0], hy + d[1]
            if nx < 0 or nx >= GW or ny < 0 or ny >= GH:
                break                      # hit the wall
            eat = (nx, ny) == food
            if not eat:                    # tail moves on
                tx, ty = snake.pop(0)
                grid[ty * GW + tx] = 0
                cell(tx, ty, BLACK)
            if grid[ny * GW + nx]:
                break                      # hit yourself
            grid[ny * GW + nx] = 1
            snake.append((nx, ny))
            cell(hx, hy, BODY)
            cell(nx, ny, HEAD)
            if eat:
                score += 10
                delay = max(fastest, slowest - score // 60)   # faster as you grow
                food = place_food(grid)
                if food is None:
                    break                  # board full: you win!
                cell(food[0], food[1], FOOD)
                bar("Score " + str(score) + "    Best " + str(best))
                if gc:
                    gc.collect()
            paint()
        sleep(0.03)
    return score, False

# --- start ---
bests = load_best()
speed = start_screen(bests)
while speed >= 0:
    score, quit = game(bests[speed], speed)
    if score > bests[speed]:
        bests[speed] = score
        save_best(bests)
        title = "NEW BEST!"
    else:
        title = "GAME OVER"
    if quit:
        break
    box([title, "Score " + str(score), "ENTER: again", "CLEAR: quit"])
    if wait_for(OK + QUIT) in QUIT:
        break
paint()
