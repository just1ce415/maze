"""Implemention of the Maze ADT using a 2-D array."""
from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""

    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert (
            row >= 0 and row < self.num_rows() and col >= 0 and col < self.num_cols()
        ), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def __find_helper(self, vertex_stack):
        """
        Helper for find_path
        """
        print(self, end="\n")
        if vertex_stack.is_empty():
            return False
        current_vertex = vertex_stack.peek()
        cur_ver_row = current_vertex.row
        cur_ver_col = current_vertex.col
        self._mark_path(cur_ver_row, cur_ver_col)
        if self._exit_found(cur_ver_row, cur_ver_col):
            return True
        # COLLECTING LIST OF SURROUNDING VERTEXES WITHOUT DFS-NUMBER
        surr_vertexes = []
        if (
            self._valid_move(cur_ver_row - 1, cur_ver_col)
            and not self._maze_cells[cur_ver_row - 1, cur_ver_col]
        ):
            surr_vertexes.append(_CellPosition(cur_ver_row - 1, cur_ver_col))
        if (
            self._valid_move(cur_ver_row + 1, cur_ver_col)
            and not self._maze_cells[cur_ver_row + 1, cur_ver_col]
        ):
            surr_vertexes.append(_CellPosition(cur_ver_row + 1, cur_ver_col))
        if (
            self._valid_move(cur_ver_row, cur_ver_col + 1)
            and not self._maze_cells[cur_ver_row, cur_ver_col + 1]
        ):
            surr_vertexes.append(_CellPosition(cur_ver_row, cur_ver_col + 1))
        if (
            self._valid_move(cur_ver_row, cur_ver_col - 1)
            and not self._maze_cells[cur_ver_row, cur_ver_col - 1]
        ):
            surr_vertexes.append(_CellPosition(cur_ver_row, cur_ver_col - 1))

        if not surr_vertexes:
            self._mark_tried(cur_ver_row, cur_ver_col)
            vertex_stack.pop()
            return None

        for unnumed_vertex in surr_vertexes:
            vertex_stack.push(unnumed_vertex)
            result = self.__find_helper(vertex_stack)
            if result is not None:
                return result

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        vertex_stack = Stack()
        vertex_stack.push(self._start_cell)
        return self.__find_helper(vertex_stack)

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for i in range(self._maze_cells.num_rows()):
            for j in range(self._maze_cells.num_cols()):
                if self._maze_cells[i, j] in (Maze.PATH_TOKEN, Maze.TRIED_TOKEN):
                    self._maze_cells[i, j] = None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        maze_str = ""
        for i in range(self._maze_cells.num_rows()):
            for j in range(self._maze_cells.num_cols()):
                if self._maze_cells[i, j] is None:
                    char = "_"
                else:
                    char = self._maze_cells[i, j]
                maze_str = maze_str + char + " "
            maze_str += "\n"
        return maze_str[:-1]

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return (
            row >= 0
            and row < self.num_rows()
            and col >= 0
            and col < self.num_cols()
            and self._maze_cells[row, col] is None
        )

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition:
    """Private storage class for holding a cell position."""

    def __init__(self, row, col):
        self.row = row
        self.col = col


def buildMaze(path):
    """
    Builds a maze from the file.
    """
    with open(path, "r", encoding="utf-8") as f_ptr:
        buffer_lst = []
        for line in f_ptr:
            nested = []
            for char in line:
                if char == Maze.MAZE_WALL:
                    nested.append(char)
                elif char == "_":
                    nested.append(None)
            buffer_lst.append(nested)

    i = 0
    j = 0
    if not buffer_lst:
        return None
    maze = Maze(len(buffer_lst), len(buffer_lst[0]))
    for row in buffer_lst:
        for col in row:
            if j == 0 and col is None:
                maze.set_start(i, j)
            elif j == len(buffer_lst[0]) - 1 and col is None:
                maze.set_exit(i, j)
            maze._maze_cells[i, j] = col
            j += 1
        i += 1
        j = 0
    return maze


if __name__ == "__main__":
    maze = buildMaze("mazefile.txt")
    print(maze)
    maze.find_path()
    print(maze)
    maze.reset()
    print(maze)
