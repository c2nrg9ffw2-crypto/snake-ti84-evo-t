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
# (the Evo gave "Height cannot be negative" for a box near the edge)
def fill_rect(x, y, w, h):
    if x < 0:
        w, x = w + x, 0
    if y < 0:
        h, y = h + y, 0
    w, h = min(w, SW - x), min(h, SH - y)
    if w > 0 and h > 0:
        try:
            ti_fill_rect(x, y, w, h)
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
GW, GH = SW // C, (SH - TOP) // C
X0 = (SW - GW * C) // 2
BLACK = (0, 0, 0)
BODY = (0, 170, 0)
HEAD = (120, 255, 120)
FOOD = (230, 0, 0)

def paint():
    if paint_buffer:
        paint_buffer()

def cell(x, y, col):
    set_color(*col)
    fill_rect(X0 + x * C, TOP + y * C, C - 1, C - 1)

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

# High score lives in the calculator list SNAKE, so it stays after quitting
def load_best():
    try:
        return int(recall_list("SNAKE")[0])
    except:
        return 0

def save_best(n):
    try:
        store_list("SNAKE", [n])
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

def start_screen(best):
    clear()
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, SH)
    x = SW // 2 - 70
    set_color(*HEAD)
    draw_text(x + 40, 20, "SNAKE")
    set_color(255, 255, 255)
    draw_text(x, 45, "Best " + str(best))
    help = ["ARROWS: turn", "Eat red food", "Don't hit walls",
            "or yourself!", "2ND: pause", "CLEAR: quit"]
    for i in range(len(help)):
        draw_text(x, 72 + i * 20, help[i])
    set_color(230, 200, 0)
    draw_text(x, 195, "ENTER: start")
    return wait_for(OK + QUIT) in OK

def game(best):
    clear()
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, SH)
    set_color(90, 90, 90)
    fill_rect(0, TOP - 2, SW, 1)
    grid = bytearray(GW * GH)              # 1 = snake is here
    snake = [(GW // 2 - 2 + i, GH // 2) for i in range(3)]   # tail ... head
    for x, y in snake:
        grid[y * GW + x] = 1
        cell(x, y, BODY)
    cell(snake[-1][0], snake[-1][1], HEAD)
    d, turns = (1, 0), []
    food = place_food(grid)
    cell(food[0], food[1], FOOD)
    score, delay, t = 0, 7, 0
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
                delay = max(2, 7 - score // 60)   # faster as you grow
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
best = load_best()
if start_screen(best):
    while True:
        score, quit = game(best)
        if score > best:
            best = score
            save_best(best)
            title = "NEW BEST!"
        else:
            title = "GAME OVER"
        if quit:
            break
        box([title, "Score " + str(score), "ENTER: again", "CLEAR: quit"])
        if wait_for(OK + QUIT) in QUIT:
            break
paint()
