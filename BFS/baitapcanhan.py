import pygame
import sys
import time
from collections import deque
import tkinter as tk
from tkinter import messagebox
import heapq


# Khởi tạo Tkinter
root = tk.Tk()
root.withdraw()
# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8 Puzzle Game_23110340-Nguyen Thanh Tin")

# Màu sắc
BACKGROUND_COLOR = (20, 70, 100)
TILE_COLOR = (0, 122, 255)
EMPTY_TILE_COLOR = (200, 200, 200)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
DEFAULT_BUTTON_COLOR = (255, 0, 0)
SELECTED_BUTTON_COLOR = (0, 255, 0)

ALGO_NAMES = ["BFS", "DFS", "IDS","UCS","A*","Greedy","IDA*"]
algo_selected = None

INITIAL_STATE = [[2, 6, 5], [0, 8,7], [4, 3,1]]
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
current_state = [row[:] for row in INITIAL_STATE]

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 24)

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    x, y = find_blank(state)
    moves = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            moves.append(new_state)
    return moves

def bfs_solve():
    queue = deque([(INITIAL_STATE, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        if state == GOAL_STATE:
            return path
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            queue.append((neighbor, path + [neighbor]))
    return []

def dfs_solve():
    stack = [(INITIAL_STATE, [])]
    visited = set()
    while stack:
        state, path = stack.pop()
        if state == GOAL_STATE:
            return path
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            stack.append((neighbor, path + [neighbor]))
    return []

def dls(state, path, depth, visited):
    if depth == 0:
        return path if state == GOAL_STATE else None
    state_tuple = tuple(tuple(row) for row in state)
    if state_tuple in visited:
        return None
    visited.add(state_tuple)
    for neighbor in get_neighbors(state):
        result = dls(neighbor, path + [neighbor], depth - 1, visited)
        if result is not None:
            return result
    return None

def ids_solve():
    depth = 0
    while True:
        visited = set()
        result = dls(INITIAL_STATE, [], depth, visited)
        if result is not None:
            return result
        depth += 1



def ucs_solve():
    priority_queue = [(0, INITIAL_STATE, [])]  # (cost, state, path)
    visited = set()

    while priority_queue:
        cost, state, path = heapq.heappop(priority_queue)

        if state == GOAL_STATE:
            return path

        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for neighbor in get_neighbors(state):
            heapq.heappush(priority_queue, (cost + 1, neighbor, path + [neighbor]))

    return []

def heuristic(state):
    """Calculate the Manhattan distance heuristic."""
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                target_x, target_y = divmod(value - 1, 3)
                distance += abs(target_x - i) + abs(target_y - j)
    return distance

def a_star_solve():
    priority_queue = [(heuristic(INITIAL_STATE), 0, INITIAL_STATE, [])]  
    visited = set()
    while priority_queue:
        _, g, state, path = heapq.heappop(priority_queue)

        if state == GOAL_STATE:
            return path

        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for neighbor in get_neighbors(state):
            new_g = g + 1
            f = new_g + heuristic(neighbor)
            heapq.heappush(priority_queue, (f, new_g, neighbor, path + [neighbor]))

    return []
    

def greedy_solve():
    priority_queue = [(heuristic(INITIAL_STATE), INITIAL_STATE, [])]  # (h, state, path)
    visited = set()

    while priority_queue:
        _, state, path = heapq.heappop(priority_queue)

        if state == GOAL_STATE:
            return path

        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        for neighbor in get_neighbors(state):
            heapq.heappush(priority_queue, (heuristic(neighbor), neighbor, path + [neighbor]))

    return []

def ida_star_solve():
     """Giải bài toán 8-puzzle bằng thuật toán IDA*."""
     def search(state, g, threshold, path):
        f = g + heuristic(state)
        if f > threshold:
            return f, None
        if state == GOAL_STATE:
            return None, path
        min_threshold = float('inf')
        state_tuple = tuple(tuple(row) for row in state)
        visited.add(state_tuple)

        for neighbor in get_neighbors(state):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple not in visited:
                new_g = g + 1
                temp_threshold, result = search(neighbor, new_g, threshold, path + [neighbor])
                if result is not None:
                    return None, result
                min_threshold = min(min_threshold, temp_threshold)

        visited.remove(state_tuple)
        return min_threshold, None

     threshold = heuristic(INITIAL_STATE)
     path = []
     while True:
        visited = set()
        temp_threshold, result = search(INITIAL_STATE, 0, threshold, path)
        if result is not None:
            return result
        if temp_threshold == float('inf'):
            return []
        threshold = temp_threshold

def draw_elements():
    screen.fill(BACKGROUND_COLOR)
    for idx, (offset, label, state) in enumerate([(100, "Start State", INITIAL_STATE), (500, "Goal State", GOAL_STATE)]):
        screen.blit(font.render(label, True, TEXT_COLOR), (offset + 25, 50))
        for row in range(3):
            for col in range(3):
                value = state[row][col]
                tile_color = TILE_COLOR if value != 0 else EMPTY_TILE_COLOR
                pygame.draw.rect(screen, tile_color, (offset + col * 70, 80 + row * 70, 70, 70))
                pygame.draw.rect(screen, GRID_COLOR, (offset + col * 70, 80 + row * 70, 70, 70), 2)
                if value != 0:
                    screen.blit(font.render(str(value), True, TEXT_COLOR), (offset + 25 + col * 70, 95 + row * 70))

    # Trạng thái hiện tại
    screen.blit(font.render("Current State", True, TEXT_COLOR), (320, 320))
    for row in range(3):
        for col in range(3):
            value = current_state[row][col]
            tile_color = TILE_COLOR if value != 0 else EMPTY_TILE_COLOR
            pygame.draw.rect(screen, tile_color, (310 + col * 70, 350 + row * 70, 70, 70))
            pygame.draw.rect(screen, GRID_COLOR, (310 + col * 70, 350 + row * 70, 70, 70), 2)
            if value != 0:
                screen.blit(font.render(str(value), True, TEXT_COLOR), (330 + col * 70, 365 + row * 70))

    # Nút chọn thuật toán
    x_pos = 50
    for algo in ALGO_NAMES:
        button_color = SELECTED_BUTTON_COLOR if algo_selected == algo else DEFAULT_BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (x_pos, 750, 70, 30))
        screen.blit(small_font.render(algo, True, TEXT_COLOR), (x_pos + 10, 755))
        x_pos += 110

    # Nút giải
    pygame.draw.rect(screen, (0, 0, 255), (360, 600, 100, 40))
    screen.blit(font.render("Solve", True, TEXT_COLOR), (380, 610))

running = True
while running:
    draw_elements()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x_pos = 50
            for algo in ALGO_NAMES:
                if x_pos <= x <= x_pos + 70 and 750 <= y <= 780:
                    algo_selected = algo
                x_pos += 110
            if 350 <= x <= 450 and 600 <= y <= 640:
                solution_steps = []  # Initialize solution_steps to avoid NameError
                if algo_selected == "BFS":
                    solution_steps = bfs_solve()
                elif algo_selected == "DFS":
                    solution_steps = dfs_solve()
                elif algo_selected == "IDS":
                    solution_steps = ids_solve()
                elif algo_selected == "UCS":
                    solution_steps = ucs_solve()
                elif algo_selected == "A*":
                    solution_steps = a_star_solve()
                elif algo_selected == "Greedy":
                    solution_steps = greedy_solve()
                elif algo_selected == "IDA*":
                    solution_steps = ida_star_solve()
                for step in solution_steps:
                    current_state = step
                    draw_elements()
                    pygame.display.flip()
                    time.sleep(0.5)
                messagebox.showinfo("Kết quả", f"Số bước cần thực hiện: {len(solution_steps)}")
    pygame.display.flip()

pygame.quit()
sys.exit()

