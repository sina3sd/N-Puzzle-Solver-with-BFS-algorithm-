from collections import deque

def is_solvable(puzzle):
    """
    بررسی می‌کند که آیا پازل قابل حل است یا نه.
    """
    inversion_count = 0
    flat_puzzle = [num for row in puzzle for num in row if num != 0]
    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] > flat_puzzle[j]:
                inversion_count += 1
    return inversion_count % 2 == 0

def find_blank(puzzle):
    """
    پیدا کردن موقعیت خانه خالی (0) در پازل.
    """
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
                return (i, j)
    return None

def get_neighbors(position, size):
    """
    گرفتن همسایه‌های خانه خالی برای جابجا کردن کاشی‌ها.
    """
    row, col = position
    neighbors = []
    if row > 0: neighbors.append((row - 1, col))  # بالا
    if row < size - 1: neighbors.append((row + 1, col))  # پایین
    if col > 0: neighbors.append((row, col - 1))  # چپ
    if col < size - 1: neighbors.append((row, col + 1))  # راست
    return neighbors

def get_move_direction(blank_pos, neighbor_pos):
    """
    پیدا کردن جهت حرکت خانه خالی.
    """
    row_diff = blank_pos[0] - neighbor_pos[0]
    col_diff = blank_pos[1] - neighbor_pos[1]
    
    if row_diff == 1:
        return "U"  # حرکت به بالا
    elif row_diff == -1:
        return "D"  # حرکت به پایین
    elif col_diff == 1:
        return "L"  # حرکت به چپ
    elif col_diff == -1:
        return "R"  # حرکت به راست

def bfs(puzzle):
    """
    اجرای الگوریتم BFS برای حل پازل.
    """
    size = len(puzzle)
    start_state = tuple(tuple(row) for row in puzzle)  # حالت اولیه پازل به صورت یک tuple از tuple های ردیف ها.
    goal_state = tuple(tuple((i * size + j + 1) % (size * size) for j in range(size)) for i in range(size))  # حالت هدف پازل.

    # بررسی اینکه آیا پازل قابل حل است یا نه.
    if not is_solvable(puzzle):
        return None

    queue = deque([(start_state, "", 0)])  # صف برای نگهداری حالت، مسیر و تعداد حرکات.
    visited = set()
    visited.add(start_state)

    while queue:
        current_state, path, moves = queue.popleft()  # خارج کردن اولین عنصر از صف.
        if current_state == goal_state:
            return path.strip(), moves  # بازگرداندن مسیر و تعداد حرکات در صورت رسیدن به حالت هدف.

        blank_pos = find_blank(current_state)  # پیدا کردن موقعیت خالی در حالت کنونی.
        neighbors = get_neighbors(blank_pos, size)  # گرفتن همسایه‌های خالی برای جابجا کردن.

        for neighbor in neighbors:
            new_state = [list(row) for row in current_state]  # کپی کردن حالت کنونی.
            # جابجایی خانه خالی با یکی از همسایه‌ها.
            new_state[blank_pos[0]][blank_pos[1]], new_state[neighbor[0]][neighbor[1]] = \
                new_state[neighbor[0]][neighbor[1]], new_state[blank_pos[0]][blank_pos[1]]
            new_state = tuple(tuple(row) for row in new_state)  # تبدیل لیست به tuple.

            if new_state not in visited:
                visited.add(new_state)  # اضافه کردن حالت جدید به مجموعه بازدید شده.
                move_direction = get_move_direction(blank_pos, neighbor)  # یافتن جهت حرکت.
                new_path = path + move_direction + " "  # افزودن جهت حرکت به مسیر.
                new_moves = moves + 1  # افزودن یک حرکت به تعداد حرکات.
                queue.append((new_state, new_path, new_moves))  # اضافه کردن حالت جدید به صف.

    return None

# تعریف پازل اولیه.
initial_puzzle = [
    [1, 2, 0],
    [4, 5, 6],
    [7, 3, 8]
]

# اجرای الگوریتم BFS برای حل پازل.
solution = bfs(initial_puzzle)

# چاپ نتیجه.
if solution:
    path, move_count = solution  # گرفتن مسیر و تعداد حرکات از نتیجه BFS.
    print("Solution found:", path)  # چاپ مسیر حل شده.
    print("Number of moves:", move_count)  # چاپ تعداد حرکات لازم برای حل.
else:
    print("No solution exists for this puzzle.")  # در صورتی که حلی برای پازل وجود نداشته باشد.
