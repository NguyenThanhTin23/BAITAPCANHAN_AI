import pygame
import time
import heapq
import random 
from collections import deque
import math  
import tkinter as tk  
from tkinter import ttk
import copy
import csv  
import matplotlib.pyplot as plt  
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix UI")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
PROCESS_BLUE = (0, 204, 255)
BUTTON_COLOR = (0, 0, 85)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Kích thước ô vuông
CELL_SIZE = 60
MARGIN = 10
BORDER_RADIUS = 10
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 40

# Danh sách thuật toán
algorithms = ["BFS", "DFS", "UCS", "IDS", "Greedy", "A*", "IDA*", "SHC", "S_AHC", "Stochastic", "SA", "BeamSearch", "Genetic", "AND-OR","Sensorless","Partial", "Backtracking",  "AC3", "Testing", "QLearning"]
selected_algorithm = None

# Biến toàn cục để lưu thời gian and số bước
global_elapsed_time = None
global_steps = None

# Biến toàn cục để theo dõi vị trí cuộn
scroll_offset = 0  
SCROLL_STEP = 20  

def draw_matrix(matrix, start_x, start_y, color=BLUE):
    font = pygame.font.Font(None, 36)
    for row in range(3):
        for col in range(3):
            value = matrix[row][col]
            rect_x = start_x + col * (CELL_SIZE + MARGIN)
            rect_y = start_y + row * (CELL_SIZE + MARGIN)
            pygame.draw.rect(SCREEN, color, (rect_x, rect_y, CELL_SIZE, CELL_SIZE), border_radius=BORDER_RADIUS)
            pygame.draw.rect(SCREEN, BLACK, (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 2, border_radius=BORDER_RADIUS)
            
            # Nếu value khác 0 thì vẽ số, còn 0 thì để ô rỗng
            if value != 0:
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(rect_x + CELL_SIZE//2, rect_y + CELL_SIZE//2))
                SCREEN.blit(text, text_rect)

def draw_buttons():
    """Vẽ danh sách các button thuật toán với thanh cuộn."""
    font = pygame.font.Font(None, 24)
    visible_area_height = HEIGHT - 100  # Chiều cao vùng hiển thị
    max_scroll = max(0, len(algorithms) * (BUTTON_HEIGHT + 10) - visible_area_height)  # Giới hạn cuộn

    for i, algo in enumerate(algorithms):
        button_x = 20
        button_y = 50 + i * (BUTTON_HEIGHT + 10) - scroll_offset  

        if 50 <= button_y <= HEIGHT - 50:
            button_color = BUTTON_COLOR if selected_algorithm != algo else PROCESS_BLUE
            pygame.draw.rect(SCREEN, button_color, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=5)
            pygame.draw.rect(SCREEN, BLACK, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2, border_radius=5)
            text = font.render(algo, True, BUTTON_TEXT_COLOR)
            text_rect = text.get_rect(center=(button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))
            SCREEN.blit(text, text_rect)

def handle_scroll(event):
    """Xử lý sự kiện cuộn chuột."""
    global scroll_offset
    visible_area_height = HEIGHT - 100  # Chiều cao vùng hiển thị
    max_scroll = max(0, len(algorithms) * (BUTTON_HEIGHT + 10) - visible_area_height)  # Giới hạn cuộn

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:  # Cuộn lên
            scroll_offset = max(0, scroll_offset - SCROLL_STEP)
        elif event.button == 5:  # Cuộn xuống
            scroll_offset = min(max_scroll, scroll_offset + SCROLL_STEP)

def draw_action_buttons():
    """Vẽ các nút hành động như Solve, Performance, Random and Steps."""
    font = pygame.font.Font(None, 24)
    solve_button_x, solve_button_y = 250, 280  # Vị trí nút Solve
    performance_button_x, performance_button_y = 400, 280  # Vị trí nút Performance
    random_button_x, random_button_y = 550, 280  # Vị trí nút Random
    steps_button_x, steps_button_y = 550, 500  # Vị trí nút Steps
    
    # Nút Solve
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (solve_button_x, solve_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=5)
    pygame.draw.rect(SCREEN, BLACK, (solve_button_x, solve_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2, border_radius=5)
    solve_text = font.render("Solve", True, BUTTON_TEXT_COLOR)
    solve_text_rect = solve_text.get_rect(center=(solve_button_x + BUTTON_WIDTH // 2, solve_button_y + BUTTON_HEIGHT // 2))
    SCREEN.blit(solve_text, solve_text_rect)
    
    # Nút Performance
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (performance_button_x, performance_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=5)
    pygame.draw.rect(SCREEN, BLACK, (performance_button_x, performance_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2, border_radius=5)
    performance_text = font.render("Performance", True, BUTTON_TEXT_COLOR)
    performance_text_rect = performance_text.get_rect(center=(performance_button_x + BUTTON_WIDTH // 2, performance_button_y + BUTTON_HEIGHT // 2))
    SCREEN.blit(performance_text, performance_text_rect)
    
    # Nút Random
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (random_button_x, random_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=5)
    pygame.draw.rect(SCREEN, BLACK, (random_button_x, random_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2, border_radius=5)
    random_text = font.render("Random", True, BUTTON_TEXT_COLOR)
    random_text_rect = random_text.get_rect(center=(random_button_x + BUTTON_WIDTH // 2, random_button_y + BUTTON_HEIGHT // 2))
    SCREEN.blit(random_text, random_text_rect)
    
    # Nút Steps
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (steps_button_x, steps_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=5)
    pygame.draw.rect(SCREEN, BLACK, (steps_button_x, steps_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2, border_radius=5)
    steps_text = font.render("Steps", True, BUTTON_TEXT_COLOR)
    steps_text_rect = steps_text.get_rect(center=(steps_button_x + BUTTON_WIDTH // 2, steps_button_y + BUTTON_HEIGHT // 2))
    SCREEN.blit(steps_text, steps_text_rect)

def draw_info_box(elapsed_time=None, steps=None):
    """Vẽ khung thông tin với thời gian and số bước."""
    font = pygame.font.Font(None, 24)
    info_x, info_y = 500, 350
    info_width, info_height = 200, 120
    pygame.draw.rect(SCREEN, WHITE, (info_x, info_y, info_width, info_height))
    pygame.draw.rect(SCREEN, BLACK, (info_x, info_y, info_width, info_height), 2)
    
    title_text = font.render("Information", True, BLACK)
    title_rect = title_text.get_rect(center=(info_x + info_width // 2, info_y + 20))
    SCREEN.blit(title_text, title_rect)
    
    # Hiển thị thời gian
    if elapsed_time is not None:
        time_text = font.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
    else:
        time_text = font.render("Time: --", True, BLACK)
    time_rect = time_text.get_rect(topleft=(info_x + 10, info_y + 40))
    SCREEN.blit(time_text, time_rect)
    
    # Hiển thị số bước
    if steps is not None:
        steps_text = font.render(f"Steps: {steps}", True, BLACK)
    else:
        steps_text = font.render("Steps: --", True, BLACK)
    steps_rect = steps_text.get_rect(topleft=(info_x + 10, info_y + 70))
    SCREEN.blit(steps_text, steps_rect)

# Thuật toán BFS
def bfs_solve(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        if state == goal_state:
            return path + [state] 
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            queue.append((neighbor, path + [state]))
    return []  

def get_neighbors(state):
    """Tìm các trạng thái hàng xóm của trạng thái hiện tại."""
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

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def dfs_solve(start_state, goal_state):
    stack = [(start_state, [])]
    visited = set()
    while stack:
        state, path = stack.pop()
        if state == goal_state:
            return path + [state] 
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            stack.append((neighbor, path + [state]))
    return []  

def ucs_solve(start_state, goal_state):
    priority_queue = [(0, start_state, [])] 
    visited = set()
    while priority_queue:
        cost, state, path = heapq.heappop(priority_queue)
        if state == goal_state:
            return path + [state] 
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            heapq.heappush(priority_queue, (cost + 1, neighbor, path + [state]))
    return [] 

def ids_solve(start_state, goal_state):
    def dls(state, goal, depth, path, visited):
        """Hàm tìm kiếm theo chiều sâu với giới hạn (Depth-Limited Search)."""
        if depth == 0 and state == goal:
            return path + [state]
        if depth > 0:
            state_tuple = tuple(tuple(row) for row in state)
            if state_tuple in visited:
                return None
            visited.add(state_tuple)
            for neighbor in get_neighbors(state):
                result = dls(neighbor, goal, depth - 1, path + [state], visited)
                if result:
                    return result
        return None

    for depth in range(1, 100):  
        visited = set()
        result = dls(start_state, goal_state, depth, [], visited)
        if result:
            return result
    return []  

def greedy_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    priority_queue = [(heuristic(start_state), start_state, [])]  
    visited = set()
    while priority_queue:
        _, state, path = heapq.heappop(priority_queue)
        if state == goal_state:
            return path + [state]
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            heapq.heappush(priority_queue, (heuristic(neighbor), neighbor, path + [state]))
    return [] 

def a_star_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    priority_queue = [(0 + heuristic(start_state), 0, start_state, [])] 
    visited = set()
    while priority_queue:
        f, g, state, path = heapq.heappop(priority_queue)
        if state == goal_state:
            return path + [state]
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            heapq.heappush(priority_queue, (g + 1 + heuristic(neighbor), g + 1, neighbor, path + [state]))
    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

def ida_star_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    def search(state, path, g, threshold):
        f = g + heuristic(state)
        if f > threshold:
            return f, None
        if state == goal_state:
            return f, path + [state]
        min_threshold = float('inf')
        state_tuple = tuple(tuple(row) for row in state)
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            if tuple(tuple(row) for row in neighbor) not in visited:
                t, result = search(neighbor, path + [state], g + 1, threshold)
                if result:
                    return t, result
                min_threshold = min(min_threshold, t)
        visited.remove(state_tuple)
        return min_threshold, None

    threshold = heuristic(start_state)
    while True:
        visited = set()
        t, result = search(start_state, [], 0, threshold)
        if result:
            return result
        if t == float('inf'):
            return []  # Không tìm thấy đường đi
        threshold = t

def shc_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    current_state = start_state
    path = [current_state]
    while current_state != goal_state:
        neighbors = get_neighbors(current_state)
        next_state = min(neighbors, key=heuristic, default=None)
        if next_state is None or heuristic(next_state) >= heuristic(current_state):
            break  # Không thể cải thiện thêm
        current_state = next_state
        path.append(current_state)
    return path if current_state == goal_state else []  # Trả về đường đi nếu tìm thấy

def s_ahc_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and  state[i][j] != goal_state[i][j]
        )

    current_state = start_state
    path = [current_state]
    while current_state != goal_state:
        neighbors = get_neighbors(current_state)
        next_state = min(neighbors, key=heuristic, default=None)  # Chọn trạng thái có heuristic tốt nhất
        if next_state is None or heuristic(next_state) >= heuristic(current_state):
            break  # Không thể cải thiện thêm
        current_state = next_state
        path.append(current_state)
    return path if current_state == goal_state else []  # Trả về đường đi nếu tìm thấy

def stochastic_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    current_state = start_state
    path = [current_state]
    while current_state != goal_state:
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break  # Không có hàng xóm để di chuyển
        # Chọn ngẫu nhiên một trạng thái hàng xóm
        next_state = random.choice(neighbors)
        if heuristic(next_state) < heuristic(current_state):
            current_state = next_state
            path.append(current_state)
    return path if current_state == goal_state else []  # Trả về đường đi nếu tìm thấy

def simulated_annealing_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    def probability(delta_e, temperature):
        """Tính xác suất chấp nhận trạng thái kém hơn."""
        return math.exp(-delta_e / temperature)

    current_state = start_state
    current_cost = heuristic(current_state)
    path = [current_state]
    temperature = 100  # Nhiệt độ ban đầu
    cooling_rate = 0.99  # Tỷ lệ giảm nhiệt độ

    while temperature > 0.1:
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break  # Không có hàng xóm để di chuyển

        next_state = random.choice(neighbors)
        next_cost = heuristic(next_state)
        delta_e = next_cost - current_cost

        # Chấp nhận trạng thái mới nếu tốt hơn hoặc theo xác suất
        if delta_e < 0 or random.random() < probability(delta_e, temperature):
            current_state = next_state
            current_cost = next_cost
            path.append(current_state)

        # Giảm nhiệt độ
        temperature *= cooling_rate

        # Nếu đạt trạng thái đích, dừng thuật toán
        if current_state == goal_state:
            break

    return path if current_state == goal_state else []  # Trả về đường đi nếu tìm thấy

def beam_search_solve(start_state, goal_state, beam_width=2):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    current_states = [(start_state, [])]  # Danh sách trạng thái hiện tại (state, path)
    while current_states:
        # Nếu tìm thấy trạng thái đích, trả về đường đi
        for state, path in current_states:
            if state == goal_state:
                return path + [state]

        # Tạo danh sách các trạng thái hàng xóm
        neighbors = []
        for state, path in current_states:
            for neighbor in get_neighbors(state):
                neighbors.append((neighbor, path + [state]))

        # Sắp xếp các trạng thái hàng xóm theo heuristic
        neighbors.sort(key=lambda x: heuristic(x[0]))

        # Chỉ giữ lại `beam_width` trạng thái tốt nhất
        current_states = neighbors[:beam_width]

    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

def genetic_algorithm_solve(start_state, goal_state, population_size=100, generations=100, mutation_rate=0.1):
    def fitness(state):
        """Hàm fitness tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    def initialize_population():
        """Khởi tạo quần thể ngẫu nhiên."""
        population = []
        for _ in range(population_size):
            flattened = [i for row in goal_state for i in row]
            random.shuffle(flattened)
            individual = [flattened[i:i + 3] for i in range(0, len(flattened), 3)]
            population.append(individual)
        return population

    def select_parents(population):
        """Chọn lọc cha mẹ dựa trên fitness."""
        population.sort(key=fitness)
        return population[:2]  # Chọn 2 cá thể tốt nhất

    def crossover(parent1, parent2):
        """Lai ghép hai cá thể."""
        child = [row[:] for row in parent1]
        for i in range(3):
            for j in range(3):
                if random.random() > 0.5:
                    child[i][j] = parent2[i][j]
        return child

    def mutate(individual):
        """Đột biến một cá thể."""
        if random.random() < mutation_rate:
            x1, y1 = random.randint(0, 2), random.randint(0, 2)
            x2, y2 = random.randint(0, 2), random.randint(0, 2)
            individual[x1][y1], individual[x2][y2] = individual[x2][y2], individual[x1][y1]

    # Khởi tạo quần thể
    population = initialize_population()

    for generation in range(generations):
        # Nếu tìm thấy trạng thái đích, trả về đường đi
        for individual in population:
            if individual == goal_state:
                return [start_state, individual]

        # Chọn lọc and tạo thế hệ mới
        parents = select_parents(population)
        new_population = []
        for _ in range(population_size // 2):
            child1 = crossover(parents[0], parents[1])
            child2 = crossover(parents[1], parents[0])
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        population = new_population

    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi
def and_or_search(belief_states, goal_state, get_successors, node_type='OR', visited=None):
    if visited is None:
        visited = set()

    goal_tuple = tuple(tuple(row) for row in goal_state)
    belief_signature = frozenset(tuple(tuple(row) for row in s) for s in belief_states)

    if all(tuple(tuple(s)) == goal_tuple for s in belief_states):
        return [belief_states]

    if belief_signature in visited:
        return None

    visited.add(belief_signature)

    if node_type == 'OR':
        # Từ tất cả trạng thái, thử mọi hành động and tạo hợp các trạng thái kế tiếp
        merged_successors = set()
        for state in belief_states:
            for succ in get_successors(state):
                merged_successors.add(tuple(tuple(row) for row in succ))

        if not merged_successors:
            return None

        new_belief_states = [list(map(list, s)) for s in merged_successors]
        result = and_or_search(new_belief_states, goal_state, get_successors, node_type='AND', visited=visited.copy())
        if result:
            return [belief_states] + result

    elif node_type == 'AND':
        full_plan = [belief_states]
        for state in belief_states:
            successors = get_successors(state)
            if not successors:
                return None
            result = and_or_search(successors, goal_state, get_successors, node_type='OR', visited=visited.copy())
            if not result:
                return None
            full_plan += result
        return full_plan

    return None


def sensorless_solve(goal_state, possible_states, path, visited):
    """
    Thuật toán Sensorless tìm kiếm trạng thái đích với đầu ando là tập hợp trạng thái ban đầu.
    """

    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    while possible_states:
        current_state = min(possible_states, key=heuristic)
        path.append(current_state)
        possible_states.remove(current_state)

        if current_state == tuple(tuple(row) for row in goal_state):
            return [list(map(list, state)) for state in path]  # Trả về đường đi

        neighbors = set()
        for state in get_neighbors([list(row) for row in current_state]):
            state_tuple = tuple(tuple(row) for row in state)
            if state_tuple not in visited:
                neighbors.add(state_tuple)
                visited.add(state_tuple)

        possible_states = neighbors

    return []



def partial_observation_search(initial_states, goal_state, get_successors, observe_fn=None):
    """
    Tìm kiếm trong điều kiện quan sát không đầy đủ (Partial Observable).
    """
    from collections import deque

    visited = set()
    queue = deque()
    queue.append((initial_states, []))  # (belief_state, path)

    goal_tuple = tuple(tuple(row) for row in goal_state)

    while queue:
        current_states, path = queue.popleft()

        if all(tuple(tuple(s)) == goal_tuple for s in current_states):
            return path + [goal_state]

        state_signature = frozenset(tuple(tuple(row) for row in s) for s in current_states)
        if state_signature in visited:
            continue
        visited.add(state_signature)

        next_states = set()
        for s in current_states:
            for succ in get_successors([list(row) for row in s]):
                succ_tuple = tuple(tuple(row) for row in succ)
                next_states.add(succ_tuple)

        # Áp dụng quan sát nếu có
        if observe_fn:
            next_states = {
                s for s in next_states if observe_fn([list(row) for row in s])
            }

        if next_states:
            queue.append(([list(map(list, s)) for s in next_states], path + [current_states]))

    return []


def Backtracking_solve(goal_state):
    """
    Backtracking: bắt đầu từ ma trận toàn 0, thử điền các số từ 0 đến 8
    sao cho tạo thành goal_state. Lưu tất cả trạng thái được thử ando path.
    """
    board = [[0 for _ in range(3)] for _ in range(3)]
    used = [False] * 9  # Đánh dấu các số từ 0 đến 8 đã dùng chưa
    path = []

    def draw(state):
        SCREEN.fill(WHITE)
        draw_buttons()
        draw_action_buttons()
        draw_matrix(state, 220, 50)
        draw_matrix(goal_state, 500, 50)
        draw_info_box(global_elapsed_time, global_steps)
        pygame.display.flip()
        #pygame.time.delay(1)

    def is_goal(state):
        return state == goal_state

    def dfs(pos):
        row, col = divmod(pos, 3)

        # Nếu đã gán hết 9 ô
        if pos == 9:
            path.append([r[:] for r in board])  # Lưu trạng thái cuối cùng
            draw(board)
            return is_goal(board)

        for num in range(9):
            if not used[num]:
                used[num] = True
                board[row][col] = num

                path.append([r[:] for r in board])  # Lưu mỗi bước gán
                draw(board)

                if dfs(pos + 1):
                    return True

                # Quay lui
                board[row][col] = 0
                used[num] = False

                path.append([r[:] for r in board])  # Lưu trạng thái sau khi quay lui
                draw(board)

        return False

    dfs(0)


def ac3_solve(goal_state, max_attempts=10000):
    """
    AC3 cho bài toán 3x3 với giá trị 0-8 xuất hiện đúng 1 lần.
    Tự sinh nhiều lần, chạy AC3 kiểm tra tính hợp lệ,
    nếu nghiệm trùng goal_state thì trả về path.
    """

    variables = [(i, j) for i in range(3) for j in range(3)]

    path = []

    def draw_current_domains(domains):
        board = [[next(iter(domains[(i, j)])) if len(domains[(i, j)]) == 1 else 0 for j in range(3)] for i in range(3)]
        path.append([row[:] for row in board])
        SCREEN.fill(WHITE)
        draw_buttons()
        draw_action_buttons()
        draw_matrix(board, 220, 50)
        draw_matrix(goal_state, 500, 50)
        draw_info_box(global_elapsed_time, global_steps)
        pygame.display.flip()
        #pygame.time.delay(1)

    def constraints_func(xi, vi, xj, vj):
        return vi != vj

    def revise(xi, xj, domains):
        revised = False
        to_remove = set()
        for vi in domains[xi]:
            if all(not constraints_func(xi, vi, xj, vj) for vj in domains[xj]):
                to_remove.add(vi)
        if to_remove:
            domains[xi] -= to_remove
            revised = True
        return revised

    def ac3(domains):
        queue = deque([(xi, xj) for xi in variables for xj in variables if xi != xj])
        while queue:
            xi, xj = queue.popleft()
            draw_current_domains(domains)
            if revise(xi, xj, domains):
                draw_current_domains(domains)
                if not domains[xi]:
                    return False
                for xk in variables:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True

    attempts = 0
    while attempts < max_attempts:
        # Sinh ngẫu nhiên giá trị 0-8 không trùng cho từng ô
        values = list(range(9))
        random.shuffle(values)
        domains = {var: {val} for var, val in zip(variables, values)}

        if not ac3(domains):
            attempts += 1
            continue

        # Lấy nghiệm hiện tại
        current_assignment = [[next(iter(domains[(i, j)])) for j in range(3)] for i in range(3)]

        # Nếu khớp goal_state thì trả về path
        if current_assignment == goal_state:
            path.append(current_assignment)
            return path

        attempts += 1

    # Không tìm được nghiệm khớp goal_state
    return []

def testing_solve(goal_state, max_attempts=100000):
    """
    Kiểm thử CSP 8-puzzle bằng BFS không dùng -1.
    Gán tuần tự vào các ô theo thứ tự, đảm bảo AllDifferent và có đúng 1 số 0.
    """

    variables = [(i, j) for i in range(3) for j in range(3)]
    path = []

    def draw_current(state):
        SCREEN.fill(WHITE)
        draw_buttons()
        draw_action_buttons()
        draw_matrix(state, 220, 50)
        draw_matrix(goal_state, 500, 50)
        draw_info_box(global_elapsed_time, global_steps)
        pygame.display.flip()
        #pygame.time.delay(1)
        path.append([row[:] for row in state])

    initial_state = [[0]*3 for _ in range(3)]  # Mặc định là toàn 0
    frontier = deque()
    frontier.append((initial_state, [], 0))  # state, assigned_values, index

    attempts = 0
    while frontier and attempts < max_attempts:
        state, assigned_values, index = frontier.popleft()

        draw_current(state)

        if index == len(variables):
            if state == goal_state:
                return path
            attempts += 1
            continue

        for v in range(9):
            if v not in assigned_values:
                i, j = variables[index]
                new_state = [row[:] for row in state]
                new_state[i][j] = v
                new_values = assigned_values + [v]
                frontier.append((new_state, new_values, index + 1))

    return []


def q_learning_solve(start_state, goal_state, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    """
    Giải thuật Q-Learning để tìm đường đi từ trạng thái bắt đầu đến trạng thái đích.
    """
    def state_to_tuple(state):
        """Chuyển trạng thái từ ma trận sang tuple để làm khóa trong Q-table."""
        return tuple(tuple(row) for row in state)

    def state_to_list(state_tuple):
        """Chuyển trạng thái từ tuple sang list."""
        return [list(row) for row in state_tuple]

    def choose_action(state, q_table):
        """Chọn hành động dựa trên epsilon-greedy."""
        if random.random() < epsilon:
            return random.choice(get_neighbors(state))
        else:
            state_tuple = state_to_tuple(state)
            if state_tuple in q_table:
                return state_to_list(max(q_table[state_tuple], key=q_table[state_tuple].get))
            else:
                return random.choice(get_neighbors(state))

    # Khởi tạo Q-table
    q_table = {}

    for episode in range(episodes):
        current_state = start_state
        while current_state != goal_state:
            state_tuple = state_to_tuple(current_state)
            if state_tuple not in q_table:
                q_table[state_tuple] = {state_to_tuple(neighbor): 0 for neighbor in get_neighbors(current_state)}

            # Chọn hành động
            next_state = choose_action(current_state, q_table)
            next_state_tuple = state_to_tuple(next_state)

            # Tính phần thưởng
            reward = 1 if next_state == goal_state else -0.1

            # Cập nhật Q-value
            if next_state_tuple not in q_table:
                q_table[next_state_tuple] = {state_to_tuple(neighbor): 0 for neighbor in get_neighbors(next_state)}
            max_next_q = max(q_table[next_state_tuple].values(), default=0)
            q_table[state_tuple][next_state_tuple] += alpha * (reward + gamma * max_next_q - q_table[state_tuple][next_state_tuple])

            # Chuyển sang trạng thái tiếp theo
            current_state = next_state

    # Tìm đường đi tốt nhất
    path = [start_state]
    current_state = start_state
    while current_state != goal_state:
        state_tuple = state_to_tuple(current_state)
        if state_tuple in q_table:
            next_state_tuple = max(q_table[state_tuple], key=q_table[state_tuple].get)
            next_state = state_to_list(next_state_tuple)
            path.append(next_state)
            current_state = next_state
        else:
            break

    return path if current_state == goal_state else []

def save_results_to_csv(algorithm_name, success, elapsed_time, steps):
    """Lưu kết quả ando file CSV."""
    file_path = "results.csv"
    header = ["Algorithm", "Success", "Time", "Steps"]
    data = [algorithm_name, success, elapsed_time, steps]

    try:
        # Kiểm tra nếu file chưa tồn tại, ghi header
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # File mới, ghi header
                writer.writerow(header)
            writer.writerow(data)
    except Exception as e:
        print(f"Error saving results to CSV: {e}")

def show_performance_chart():
    """Hiển thị biểu đồ hiệu suất and thông tin chi tiết."""
    # Hiển thị cửa sổ chọn thuật toán
    def on_select():
        selected_algo = algo_var.get()
        root.destroy()
        draw_performance_chart(selected_algo)

    root = tk.Tk()
    root.title("Select Algorithm for Performance")

    tk.Label(root, text="Choose an algorithm to view performance:").pack(pady=10)
    algo_var = tk.StringVar(value=algorithms[0])
    algo_dropdown = ttk.Combobox(root, textvariable=algo_var, values=algorithms, state="readonly")
    algo_dropdown.pack(pady=10)
    tk.Button(root, text="OK", command=on_select).pack(pady=10)

    root.mainloop()

def draw_performance_chart(algorithm_name):
    """Vẽ biểu đồ hiệu suất cho thuật toán đã chọn và hiển thị bảng thông tin (chỉ tính trung bình cho Success)."""
    success_count = 0
    failure_count = 0
    success_steps = 0
    success_time = 0.0

    # Đọc dữ liệu từ file CSV
    try:
        with open("results.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Algorithm"] == algorithm_name:
                    if row["Success"] == "1":
                        success_count += 1
                        success_steps += int(row["Steps"])
                        success_time += float(row["Time"])
                    else:
                        failure_count += 1
    except FileNotFoundError:
        print("No results.csv file found.")
        return

    if success_count + failure_count == 0:
        print(f"No data available for algorithm: {algorithm_name}")
        return

    # Tính toán trung bình (chỉ với Success)
    avg_steps = success_steps / success_count if success_count > 0 else 0
    avg_time = success_time / success_count if success_count > 0 else 0

    # Vẽ biểu đồ tròn
    labels = ["Success", "Failure"]
    sizes = [success_count, failure_count]
    colors = ["#4CAF50", "#F44336"]
    plt.figure(figsize=(8, 6))
    plt.subplot(121)  # Biểu đồ tròn ở bên trái
    plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    plt.title(f"Performance of {algorithm_name}")

    # Hiển thị bảng thông tin
    plt.subplot(122)  # Bảng thông tin ở bên phải
    plt.axis("off")  # Tắt trục
    table_data = [
        ["Metric", "Value"],
        ["Average Steps (Success)", f"{avg_steps:.2f}"],
        ["Average Time (s, Success)", f"{avg_time:.2f}"]
    ]
    plt.table(cellText=table_data, colLabels=None, loc="center", cellLoc="center", colWidths=[0.5, 0.5])

    # Hiển thị biểu đồ
    plt.tight_layout()
    plt.show()

    # Hiển thị thông tin chi tiết trên terminal
    print(f"Algorithm: {algorithm_name}")
    print(f"Success Cases: {success_count}")
    print(f"Failure Cases: {failure_count}")
    print(f"Average Steps (Success): {avg_steps:.2f}")
    print(f"Average Time (Success): {avg_time:.2f}s")

# Ma trận trạng thái ban đầu and trạng thái đích
original_state = [
       [1, 2, 3],
    [0, 4, 5],
    [7, 8, 6]
]

target_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

process_state = original_state

def update_process_state(path):
    """Cập nhật trạng thái process_state theo từng bước trong path."""
    global process_state
    for state in path:
        process_state = state  # Cập nhật trạng thái hiện tại
        draw_screen(color=PROCESS_BLUE)  # Vẽ lại màn hình với màu xanh dương nhạt
        pygame.time.delay(250)  # Tạm dừng 500ms để hiển thị từng bước

def draw_screen(color=BLUE):
    """Vẽ toàn bộ màn hình."""
    SCREEN.fill(WHITE)
    draw_buttons()
    draw_action_buttons()
    if selected_algorithm in ["Backtracking", "AC3", "Testing"]:
        # Nếu đã có kết quả and path không rỗng, vẽ trạng thái cuối cùng của path
        if path and len(path) > 0:
            draw_matrix(path[-1], 220, 50)
        else:
            empty_state = [[0 for _ in range(3)] for _ in range(3)]
            draw_matrix(empty_state, 220, 50)
        draw_matrix(target_state, 500, 50)
        # Không vẽ process_state (ma trận current)
    else:
        draw_matrix(original_state, 220, 50)
        draw_matrix(target_state, 500, 50)
        draw_matrix(process_state, 220, 350, color=color)
    draw_info_box(global_elapsed_time, global_steps)
    pygame.display.flip()

def print_steps_to_terminal(path):
    """In ra các ma trận trạng thái trong terminal."""
    print("Các trạng thái trong đường đi:")
    for i, state in enumerate(path):
        print(f"Step {i}:")
        for row in state:
            print(row)
        print()  # Dòng trống giữa các bước

def randomize_matrix():
    """Tạo ma trận ngẫu nhiên."""
    global original_state, process_state
    flattened = [i for row in target_state for i in row]  # Lấy tất cả các phần tử từ ma trận đích
    random.shuffle(flattened)  # Trộn ngẫu nhiên các phần tử
    original_state = [flattened[i:i + 3] for i in range(0, len(flattened), 3)]  # Chuyển về ma trận 3x3
    process_state = [row[:] for row in original_state]  # Đồng bộ process_state với original_state

# Vòng lặp chính
running = True
path = None  # Initialize path to avoid NameError
draw_screen()
while running:
    for event in pygame.event.get():
        handle_scroll(event)  # Xử lý sự kiện cuộn chuột
        draw_screen()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            # Xử lý chọn thuật toán
            for i, algo in enumerate(algorithms):
                button_x = 20
                button_y = 50 + i * (BUTTON_HEIGHT + 10) - scroll_offset  # Điều chỉnh vị trí theo scroll_offset
                if button_x <= x <= button_x + BUTTON_WIDTH and button_y <= y <= button_y + BUTTON_HEIGHT:
                    selected_algorithm = algo
                    path = None  # Reset đường đi khi chọn thuật toán mới
            
            # Xử lý nút "Performance"
            performance_button_x, performance_button_y = 400, 280
            if performance_button_x <= x <= performance_button_x + BUTTON_WIDTH and performance_button_y <= y <= performance_button_y + BUTTON_HEIGHT:
                show_performance_chart()

            # Xử lý nút "Solve"
            solve_button_x, solve_button_y = 250, 280
            if solve_button_x <= x <= solve_button_x + BUTTON_WIDTH and solve_button_y <= y <= solve_button_y + BUTTON_HEIGHT:
                if selected_algorithm == "BFS":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = bfs_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    
                    # Cập nhật giá trị toàn cục
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("BFS", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "DFS":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = dfs_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    
                    # Cập nhật giá trị toàn cục
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("DFS", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "UCS":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = ucs_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("UCS", 1 if path else 0, elapsed_time, steps)
                    
                elif selected_algorithm == "IDS":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = ids_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    # Cập nhật giá trị toàn cục
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("IDS", 1 if path else 0, elapsed_time, steps)
                elif selected_algorithm == "Greedy":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = greedy_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("Greedy", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "A*":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = a_star_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("A*", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "IDA*":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = ida_star_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("IDA*", 1 if path else 0, elapsed_time, steps)
                elif selected_algorithm == "SHC":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = shc_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("SHC", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "S_AHC":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = s_ahc_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("S_AHC", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "Stochastic":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = stochastic_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("Stochastic", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "SA":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = simulated_annealing_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("SA", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "BeamSearch":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = beam_search_solve(original_state, target_state, beam_width=2)  # Beam width mặc định là 2
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("BeamSearch", 1 if path else 0, elapsed_time, steps)
                elif selected_algorithm == "AND-OR":
                        # Tập trạng thái ban đầu (không biết chắc đang ở đâu)
                    possible_states = set()
                    for neighbor in get_neighbors(original_state):
                        possible_states.add(tuple(tuple(row) for row in neighbor))
                    possible_states.add(tuple(tuple(row) for row in original_state))

                    start_states = [list([list(row) for row in state]) for state in possible_states]

                    start_time = time.time()
                    path = and_or_search(start_states, target_state, get_neighbors)
                    elapsed_time = time.time() - start_time
                    steps = len(path) - 1 if path else 0

                    if path:
                        update_process_state(path)
                    else:
                        print("Không tìm thấy đường đi!")

                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("AND-OR", 1 if path else 0, elapsed_time, steps)
                elif selected_algorithm == "Genetic":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = genetic_algorithm_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("Genetic", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "Sensorless":
                    # Chuẩn bị dữ liệu đầu ando
                    possible_states = set()
                    for neighbor in get_neighbors(original_state):
                        possible_states.add(tuple(tuple(row) for row in neighbor))
                    possible_states.add(tuple(tuple(row) for row in original_state))  # Thêm trạng thái hiện tại
                    path = []
                    visited = set()

                    # Gọi hàm đã chỉnh sửa
                    start_time = time.time()
                    result_path = sensorless_solve(target_state, possible_states, path, visited)
                    elapsed_time = time.time() - start_time
                    steps = len(result_path) - 1 if result_path else 0

                    if result_path:
                        update_process_state(result_path)
                    else:
                        print("Không tìm thấy đường đi!")

                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("Sensorless", 1 if path else 0, elapsed_time, steps)

                elif selected_algorithm == "Partial":
                    initial_states = [tuple(tuple(row) for row in s) for s in get_neighbors(original_state)]
                    initial_states.append(tuple(tuple(row) for row in original_state))
                    
                    def observe_fn(state):
                        # Ví dụ: không có quan sát cụ thể, giữ nguyên
                        return True

                    start_time = time.time()
                    path = partial_observation_search(initial_states, target_state, get_neighbors, observe_fn)
                    elapsed_time = time.time() - start_time
                    steps = len(path) - 1 if path else 0

                    if path:
                        update_process_state(path)
                    else:
                        print("Không tìm thấy đường đi!")

                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("Partial", 1 if path else 0, elapsed_time, steps)


             
                elif selected_algorithm == "QLearning":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = q_learning_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("QLearning", 1 if path else 0, elapsed_time, steps)
                elif selected_algorithm == "Backtracking":
                    start_time = time.time()
                    path = Backtracking_solve(target_state)
                    elapsed_time = time.time() - start_time
                    steps = len(path) - 1 if path else 0
                    if path:
                        update_process_state(path)
             
                
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("Backtracking", 1 if path else 0, elapsed_time, steps)
                elif selected_algorithm == "AC3":
                    start_time = time.time()
                    path = ac3_solve(target_state)
                    elapsed_time = time.time() - start_time
                    steps = len(path) - 1 if path else 0
                    if path:
                        update_process_state(path)
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("AC3", 1 if path else 0, elapsed_time, steps)
                elif selected_algorithm == "Testing":
                    start_time = time.time()
                    path = testing_solve(target_state)
                    elapsed_time = time.time() - start_time
                    steps = len(path) - 1 if path else 0
                    if path:
                        update_process_state(path)
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
                    save_results_to_csv("Testing", 1 if path else 0, elapsed_time, steps)
            # Xử lý nút "Steps"
            steps_button_x, steps_button_y = 550, 500
            if steps_button_x <= x <= steps_button_x + BUTTON_WIDTH and  steps_button_y <= y <= steps_button_y + BUTTON_HEIGHT:
                if path:  # Kiểm tra nếu đã có đường đi
                    print_steps_to_terminal(path)  # In ra các trạng thái trên terminal
                else:
                    print("Không có đường đi để hiển thị các bước!")

            random_button_x, random_button_y = 550, 280
            if random_button_x <= x <= random_button_x + BUTTON_WIDTH and random_button_y <= y <= random_button_y + BUTTON_HEIGHT:
                randomize_matrix()  # Tạo ma trận ngẫu nhiên
                draw_screen()  # Vẽ lại màn hình với ma trận mới











