

class GridPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "GridPoint(x=%d, y=%d)" % (self.x, self.y)

    def __iter__(self):
        return (self.x, self.y).__iter__()


class GridPointRange:
    def __init__(self, x, y):
        if isinstance(x, int):
            self.start_x, self.end_x = x, x
        else:
            self.start_x, self.end_x = x

        if isinstance(y, int):
            self.start_y, self.end_y = y, y
        else:
            self.start_y, self.end_y = y
        self.diagonal = True
        self.adjacency_bounds = []
        self.calc_adjacency_bounds(True)

    def calc_adjacency_bounds(self, diagonal=False):
        # don't recalculate unless bounds haven't been calculated
        # or requested diagonal support is different from
        # existing diagonal support
        if self.adjacency_bounds and diagonal == self.diagonal:
            return
        self.diagonal = diagonal
        diagonal_int = int(diagonal)
        self.adjacency_bounds = [
            # above
            ((self.start_x-diagonal_int, self.end_x+diagonal_int),
             (self.start_y-1, self.start_y-1)),
            # below
            ((self.start_x-diagonal_int, self.end_x+diagonal_int),
             (self.end_y+1, self.end_y+1)),
            # left
            ((self.start_x-1, self.start_x-1),
             (self.start_y-diagonal_int, self.end_y+diagonal_int)),
            # right
            ((self.end_x+1, self.end_x+1),
             (self.start_y-diagonal_int, self.end_y+diagonal_int)),
        ]

    def is_adjacent(self, grid_point, diagonal=False):
        self.calc_adjacency_bounds(diagonal)
        x, y = grid_point
        for [[start_x, end_x], [start_y, end_y]] in self.adjacency_bounds:
            if start_x <= x and x <= end_x and \
                start_y <= y and y <= end_y:
                return True
        return False

    def __repr__(self):
        return "GridPointRange(%d-%d, %d-%d)" % (self.start_x,
                                              self.end_x, self.start_y,
                                                self.end_y)
