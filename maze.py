from cell import Cell
import time, random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__solving = False
        random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0,0)
        self.__reset_cells_visited()

    def __animate(self):
        self.__win.redraw()
        time.sleep(0.05 if self.__solving else 0.01)

    def get_cells(self):
        return self.__cells
    
    def __draw_cell(self, x, y):
        if self.__win is None:
            return
        x1 = self.__x1 + (x * self.__cell_size_x)
        y1 = self.__y1 + (y * self.__cell_size_y)
        y2 = y1 + self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        self.__cells[x][y].draw(x1, y1, x2, y2)
        self.__animate()


    def __create_cells(self):
        for x in range (0, self.__num_cols):
            column = []
            for y in range (0, self.__num_rows):
                column.append(Cell(self.__win))
            self.__cells.append(column)
        
        for x in range (0, self.__num_cols):
            for y in range (0, self.__num_rows):
                self.__draw_cell(x, y)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, x, y):
        self.__cells[x][y].visited = True
        while True:
            to_visit = []
            if x + 1 < self.__num_cols:
                if not self.__cells[x+1][y].visited:
                    to_visit.append((x+1, y))
            if y + 1 < self.__num_rows:
                if not self.__cells[x][y+1].visited:
                    to_visit.append((x, y+1))
            if x - 1 >= 0:
                if not self.__cells[x-1][y].visited:
                    to_visit.append((x-1, y))
            if y - 1 >= 0:
                if not self.__cells[x][y-1].visited:
                    to_visit.append((x, y-1))

            if len(to_visit) == 0:
                self.__draw_cell(x, y)
                break

            direction = random.randint(0, (len(to_visit) - 1))
            if x > to_visit[direction][0]:
                self.__cells[x][y].has_left_wall = False
                self.__cells[to_visit[direction][0]][y].has_right_wall = False
            elif y > to_visit[direction][1]:
                self.__cells[x][y].has_top_wall = False
                self.__cells[x][to_visit[direction][1]].has_bottom_wall = False
            elif x < to_visit[direction][0]:
                self.__cells[x][y].has_right_wall = False
                self.__cells[to_visit[direction][0]][y].has_left_wall = False
            elif y < to_visit[direction][1]:
                self.__cells[x][y].has_bottom_wall = False
                self.__cells[x][to_visit[direction][1]].has_top_wall = False

            self.__break_walls_r(to_visit[direction][0], to_visit[direction][1])

    def __reset_cells_visited(self):
        for x in range(0, self.__num_cols):
            for y in range(0, self.__num_rows):
                self.__cells[x][y].visited = False
            
    def solve(self):
        self.__solving = True
        return self.__solve_r(0,0)

    def __solve_r(self, x, y):
        self.__animate()
        self.__cells[x][y].visited = True

        if x == self.__num_cols - 1 and y == self.__num_rows - 1:
            return True
        
        # Check Right
        if x + 1 < self.__num_cols:
            if not self.__cells[x][y].has_right_wall and not self.__cells[x+1][y].visited:
                self.__cells[x][y].draw_move(self.__cells[x+1][y])
                check_solution = self.__solve_r(x+1, y)
                if check_solution:
                    return True
                else:
                    self.__cells[x][y].draw_move(self.__cells[x+1][y], True)

        # Check Down
        if y + 1 < self.__num_rows:
            if not self.__cells[x][y].has_bottom_wall and not self.__cells[x][y+1].visited:
                self.__cells[x][y].draw_move(self.__cells[x][y+1])
                check_solution = self.__solve_r(x, y+1)
                if check_solution:
                    return True
                else:
                    self.__cells[x][y].draw_move(self.__cells[x][y+1], True)

        # Check Left
        if x - 1 >= 0:
            if not self.__cells[x][y].has_left_wall and not self.__cells[x-1][y].visited:
                self.__cells[x][y].draw_move(self.__cells[x-1][y])
                check_solution = self.__solve_r(x-1, y)
                if check_solution:
                    return True
                else:
                    self.__cells[x][y].draw_move(self.__cells[x-1][y], True)

        # Check Up
        if y - 1 >= 0:
            if not self.__cells[x][y].has_top_wall and not self.__cells[x][y-1].visited:
                self.__cells[x][y].draw_move(self.__cells[x][y-1])
                check_solution = self.__solve_r(x, y-1)
                if check_solution:
                    return True
                else:
                    self.__cells[x][y].draw_move(self.__cells[x][y-1], True)

        # Bubkis...
        return False

