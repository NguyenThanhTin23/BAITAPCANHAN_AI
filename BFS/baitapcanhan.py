import pygame
import time
import heapq
import random  # Thêm thư viện random để tạo ma trận ngẫu nhiên
from collections import deque
import math  # Thêm import math nếu chưa có

# Khởi tạo pygame
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
algorithms = ["BFS", "DFS", "UCS", "IDS", "Greedy", "A*", "IDA*", "SHC", "S_AHC", "Stochastic", "SA", "BeamSearch", "AND-OR", "Genetic"]
selected_algorithm = None

# Biến toàn cục để lưu thời gian và số bước
global_elapsed_time = None
global_steps = None

# Biến toàn cục để theo dõi vị trí cuộn
scroll_offset = 0  # Giá trị cuộn ban đầu
SCROLL_STEP = 20  # Bước cuộn mỗi lần

def draw_matrix(matrix, start_x, start_y, color=BLUE):
    font = pygame.font.Font(None, 36)
    for row in range(3):
        for col in range(3):
            value = matrix[row][col]
            rect_x = start_x + col * (CELL_SIZE + MARGIN)
            rect_y = start_y + row * (CELL_SIZE + MARGIN)
            pygame.draw.rect(SCREEN, color, (rect_x, rect_y, CELL_SIZE, CELL_SIZE), border_radius=BORDER_RADIUS)
            pygame.draw.rect(SCREEN, BLACK, (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 2, border_radius=BORDER_RADIUS)
            
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
        button_y = 50 + i * (BUTTON_HEIGHT + 10) - scroll_offset  # Điều chỉnh vị trí theo scroll_offset

        # Chỉ vẽ các button nằm trong vùng hiển thị
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
    """Vẽ các nút hành động như Solve, Random và Steps."""
    font = pygame.font.Font(None, 24)
    solve_button_x, solve_button_y = 250, 280  # Vị trí nút Solve
    random_button_x, random_button_y = 550, 280  # Vị trí nút Random
    steps_button_x, steps_button_y = 550, 500  # Vị trí nút Steps
    
    # Nút Solve
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (solve_button_x, solve_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=5)
    pygame.draw.rect(SCREEN, BLACK, (solve_button_x, solve_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2, border_radius=5)
    solve_text = font.render("Solve", True, BUTTON_TEXT_COLOR)
    solve_text_rect = solve_text.get_rect(center=(solve_button_x + BUTTON_WIDTH // 2, solve_button_y + BUTTON_HEIGHT // 2))
    SCREEN.blit(solve_text, solve_text_rect)
    
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
    """Vẽ khung thông tin với thời gian và số bước."""
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
            return path + [state]  # Trả về đường đi bao gồm trạng thái cuối cùng
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            queue.append((neighbor, path + [state]))
    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

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
            return path + [state]  # Trả về đường đi bao gồm trạng thái cuối cùng
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            stack.append((neighbor, path + [state]))
    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

def ucs_solve(start_state, goal_state):
    priority_queue = [(0, start_state, [])]  # (cost, state, path)
    visited = set()
    while priority_queue:
        cost, state, path = heapq.heappop(priority_queue)
        if state == goal_state:
            return path + [state]  # Trả về đường đi bao gồm trạng thái cuối cùng
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        for neighbor in get_neighbors(state):
            heapq.heappush(priority_queue, (cost + 1, neighbor, path + [state]))
    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

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

    # Lặp qua các giới hạn độ sâu
    for depth in range(1, 100):  # Giới hạn độ sâu tối đa là 100
        visited = set()
        result = dls(start_state, goal_state, depth, [], visited)
        if result:
            return result
    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

def greedy_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    priority_queue = [(heuristic(start_state), start_state, [])]  # (heuristic, state, path)
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
    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

def a_star_solve(start_state, goal_state):
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    priority_queue = [(0 + heuristic(start_state), 0, start_state, [])]  # (f, g, state, path)
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
def or_and_search(state, goal_state, get_successors, node_type='OR', visited=None):
    if visited is None:
        visited = set()

    state_tuple = tuple(tuple(row) for row in state)
    if state == goal_state:
        return [state]
    if state_tuple in visited:
        return None

    visited.add(state_tuple)

    if node_type == 'OR':
        for next_state in get_successors(state):
            result = or_and_search(next_state, goal_state, get_successors, node_type='AND', visited=visited.copy())
            if result:
                return [state] + result
    else:  # AND node
        all_results = [state]
        for next_state in get_successors(state):
            result = or_and_search(next_state, goal_state, get_successors, node_type='OR', visited=visited.copy())
            if not result:
                return None
            all_results += result
        return all_results

    return None

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

        # Chọn lọc và tạo thế hệ mới
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

def sensorless_solve(start_state, goal_state):
    """
    Thuật toán Sensorless tìm kiếm trạng thái đích mà không biết vị trí chính xác của các ô.
    """
    def heuristic(state):
        """Hàm heuristic tính số ô sai vị trí."""
        return sum(
            1 for i in range(3) for j in range(3) if state[i][j] != 0 and state[i][j] != goal_state[i][j]
        )

    # Khởi tạo tập hợp các trạng thái có thể
    possible_states = {tuple(tuple(row) for row in start_state)}
    path = []

    while possible_states:
        # Chọn trạng thái có heuristic tốt nhất
        current_state = min(possible_states, key=heuristic)
        path.append(current_state)
        possible_states.remove(current_state)

        if current_state == tuple(tuple(row) for row in goal_state):
            return [list(map(list, state)) for state in path]  # Trả về đường đi

        # Sinh các trạng thái hàng xóm
        neighbors = set()
        for state in possible_states:
            for neighbor in get_neighbors([list(row) for row in state]):
                neighbors.add(tuple(tuple(row) for row in neighbor))
        possible_states = neighbors

    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

# Ma trận trạng thái ban đầu và trạng thái đích
original_state = [
     [1, 2, 3],
    [4, 5, 6],
    [7,0,8]
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
        pygame.time.delay(500)  # Tạm dừng 500ms để hiển thị từng bước

def draw_screen(color=BLUE):
    """Vẽ toàn bộ màn hình."""
    SCREEN.fill(WHITE)
    draw_buttons()
    draw_action_buttons()
    draw_matrix(original_state, 220, 50)
    draw_matrix(target_state, 500, 50)
    draw_matrix(process_state, 220, 350, color=color)  # Vẽ ma trận process_state với màu được chỉ định
    draw_info_box(global_elapsed_time, global_steps)  # Truyền thời gian và số bước vào khung thông tin
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
  
# Thêm "Sensorless" vào danh sách thuật toán
algorithms.append("Sensorless")

# Vòng lặp chính
running = True
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
                elif selected_algorithm == "AND-OR":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = or_and_search(original_state, target_state, get_neighbors)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
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
                elif selected_algorithm == "Sensorless":
                    start_time = time.time()  # Bắt đầu đo thời gian
                    path = sensorless_solve(original_state, target_state)
                    elapsed_time = time.time() - start_time  # Tính thời gian thực thi
                    steps = len(path) - 1 if path else 0  # Tính số bước
                    if path:
                        update_process_state(path)  # Cập nhật trạng thái theo từng bước
                    else:
                        print("Không tìm thấy đường đi!")
                    global_elapsed_time = elapsed_time
                    global_steps = steps
            
            # Xử lý nút "Steps"
            steps_button_x, steps_button_y = 550, 500
            if steps_button_x <= x <= steps_button_x + BUTTON_WIDTH and  steps_button_y <= y <= steps_button_y + BUTTON_HEIGHT:
                if path:  # Kiểm tra nếu đã có đường đi
                    print_steps_to_terminal(path)  # In ra các trạng thái trên terminal
                else:
                    print("Không có đường đi để hiển thị các bước!")
            
            # Xử lý nút "Random"
            random_button_x, random_button_y = 550, 280
            if random_button_x <= x <= random_button_x + BUTTON_WIDTH and random_button_y <= y <= random_button_y + BUTTON_HEIGHT:
                randomize_matrix()  # Tạo ma trận ngẫu nhiên
                draw_screen()  # Vẽ lại màn hình với ma trận mới

        handle_scroll(event)

pygame.quit()
