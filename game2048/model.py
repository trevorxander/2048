import copy
from random import randint


class Model2048:
    DEFAULT_MATRIX_SIZE = 4

    def __init__(self, matrix_size=DEFAULT_MATRIX_SIZE):
        self._random_inserts_percent = 90
        self._no_random_inserts_percent = 90
        self._matrix_size = matrix_size
        self._game_matrix = [[0] * self._matrix_size] * self._matrix_size
        self._no_random_inserts = self._matrix_size / 2
        self._random_inserts = [2, 4]
        self._newly_merged = set()
        self._empty_spots = set()
        self._game_over = False
        self._score = [0]
        self.moved_tiles = []
        self.pop_ins = []
        self._movement_args = [{'left': 1},
                               {'right': 1},
                               {'up': 1},
                               {'down': 1}]

        self._last_game_state = None

    def available_moves(self, matrix):
        avaliable_moves = []

        for movement_arg in self._movement_args:
            for movement in movement_arg:
                moved_matrix = copy.deepcopy(matrix)
                self._movement(matrix=moved_matrix, **movement_arg)
                if matrix != moved_matrix:
                    avaliable_moves.append(movement_arg)
        return avaliable_moves

    def undo(self):
        self._restore(self._last_game_state)

    def left(self):
        self._agent_movement(left=1)

    def right(self):
        self._agent_movement(right=1)

    def up(self):
        self._agent_movement(up=1)

    def down(self):
        self._agent_movement(down=1)

    def get_matrix(self):
        return self._game_matrix

    def get_pop_ins(self):
        return self.pop_ins

    def restart_game(self):
        self._game_matrix = [[0 for row in self._game_matrix] for col in self._game_matrix]
        for row in range(self._matrix_size):
            for col in range(self._matrix_size):
                row_col = (row, col)
                self._empty_spots.add(row_col)

        self._link_game_state()
        self._score[0] = 0
        self._rand_pop_in()

    @property
    def score(self):
        return self._score[0]

    def get_moved_tiles(self):
        return self.moved_tiles

    def _print(self):
        for row in self._game_matrix:
            print(row)
        print('\n')

    def _backup(self):
        self._link_game_state()
        backup_states = copy.deepcopy(self.game_state)
        return backup_states

    def _restore(self, backup_state):
        self._link_game_state()
        self._game_matrix = copy.deepcopy(backup_state[0])
        self._empty_spots = copy.deepcopy(backup_state[1])
        self._score = copy.deepcopy(backup_state[2])

    def _link_game_state(self):
        self.game_state = [self._game_matrix,
                           self._empty_spots,
                           self._score]

    def _move_tile(self, tile: tuple, left=0, up=0, matrix=None):
        if matrix == None:
            matrix = self._game_matrix

        def _set_new_tile(row, col, value):
            if (row, col) in self._empty_spots:
                self._empty_spots.remove((row, col))
            matrix[row][col] = value
            if value == 0:
                self._empty_spots.add((row, col))
            else:
                if tile != (row, col):
                    self.moved_tiles.append((tile, (row, col), value))

        new_tile_row = tile[0]
        new_tile_col = tile[1]
        tile_value = matrix[new_tile_row][new_tile_col]

        while True:
            new_tile_row = new_tile_row - up
            new_tile_col = new_tile_col - left

            # if tile reaches end of matrix
            if new_tile_row not in range(self._matrix_size) or \
                    new_tile_col not in range(self._matrix_size):
                _set_new_tile(new_tile_row + up, new_tile_col + left, tile_value)
                break
            # if tile moves through an empty spot
            if matrix[new_tile_row][new_tile_col] == 0:
                _set_new_tile(tile[0], tile[1], 0)
                continue
            # If the tile comes in contact with a tile of same value
            elif tile_value == matrix[new_tile_row][new_tile_col]:
                # If tile was not already merged this turn
                if (new_tile_row, new_tile_col) not in self._newly_merged:
                    # matrix[new_tile_row][new_tile_col] *= 2
                    _set_new_tile(new_tile_row, new_tile_col, matrix[new_tile_row][new_tile_col] * 2)
                    self._score[0] += matrix[new_tile_row][new_tile_col]
                    self._newly_merged.add((new_tile_row, new_tile_col))
                    _set_new_tile(tile[0], tile[1], 0)
                # If tile was merged this turn
                else:
                    _set_new_tile(new_tile_row + up, new_tile_col + left, tile_value)
                return
            else:
                _set_new_tile(new_tile_row + up, new_tile_col + left, tile_value)
                return

    def _agent_movement(self, **direction_arg):
        self._last_game_state = self._backup()

        self._movement(**direction_arg)

        if len(self.moved_tiles) != 0:
            self._rand_pop_in()

    def _movement(self, matrix=None, **direction_arg):
        self._newly_merged.clear()
        self.moved_tiles.clear()
        self.pop_ins.clear()
        if matrix == None:
            matrix = self._game_matrix
        direction = list(direction_arg.keys())[0]
        if direction == 'left' or direction == 'right':
            self._horizontal(matrix=matrix, **direction_arg)
        else:
            self._vertical(matrix=matrix, **direction_arg)

    def is_game_over(self):
        if len(self._empty_spots) > 0:
            return False

        for row in range(len(self._game_matrix)):
            for col in range(len(self._game_matrix)):
                adjacents = [(row, col - 1),
                             (row, col + 1),
                             (row - 1, col),
                             (row + 1, col)]
                for adjacent in adjacents:
                    if adjacent[0] in range(len(self._game_matrix)) and \
                            adjacent[1] in range(len(self._game_matrix)):
                        if self._game_matrix[adjacent[0]][adjacent[1]] == self._game_matrix[row][col]:
                            return False
        return True

    def _horizontal(self, matrix=None, left=0, right=0):
        if matrix == None:
            matrix = self._game_matrix
        right = -right
        check_order = range(left, len(matrix) + right)
        if right == -1:
            check_order = reversed(check_order)

        for col in check_order:
            for row in range(0, len(matrix)):
                if matrix[row][col] != 0:
                    self._move_tile((row, col), left=left + right, matrix=matrix)

    def _vertical(self, matrix=None, up=0, down=0):
        if matrix == None:
            matrix = self._game_matrix
        down = -down
        check_order = range(up, len(matrix) + down)
        if down == -1:
            check_order = reversed(check_order)

        for row in check_order:
            for col in range(0, len(matrix)):
                if matrix[row][col] != 0:
                    self._move_tile((row, col), up=up + down, matrix=matrix)

    def _rand_pop_in(self):
        max_random_inserts = int(self._matrix_size / 2)
        for num in range(1, max_random_inserts + 1):
            if randint(1, 100) <= self._no_random_inserts_percent:
                no_of_random_inserts = num
                break

        no_of_random_inserts = num
        for rands in range(no_of_random_inserts):
            if len(self._empty_spots) == 0:
                return
            empty_spot = self._pick_rand_empty_spot()
            new_random_num = self._pick_num_to_insert()
            self._game_matrix[empty_spot[0]][empty_spot[1]] = new_random_num
            self.pop_ins.append((empty_spot, new_random_num))
            continue

    def _pick_rand_empty_spot(self):
        no_of_picks = randint(1, len(self._empty_spots))
        for picks in range(no_of_picks):
            self._empty_spots.add(self._empty_spots.pop())
        return self._empty_spots.pop()

    def _pick_num_to_insert(self):
        for num in self._random_inserts:
            if num == self._random_inserts[- 1]:
                return num
            if randint(1, 100) <= self._random_inserts_percent:
                return num
