from graphics import Point, Line

class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = None
        self.__y1 = None
        self.__x2 = None
        self.__y2 = None
        self.__win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), "black" if self.has_left_wall else "white")
        self.__win.draw_line(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), "black" if self.has_right_wall else "white")
        self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), "black" if self.has_top_wall else "white")
        self.__win.draw_line(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), "black" if self.has_bottom_wall else "white")

    def get_top_left(self):
        return Point(self.__x1, self.__y1)
    
    def get_bottom_left(self):
        return Point(self.__x2, self.__y2)
    
    def get_center(self):
        return Point(self.__x1 + (abs(self.__x2 - self.__x1) // 2), self.__y1 + (abs(self.__y2 - self.__y1) // 2))
    
    def draw_move(self, to_cell, undo=False):
        move_line = Line(self.get_center(), to_cell.get_center())
        self.__win.draw_line(move_line, "gray" if undo else "red")