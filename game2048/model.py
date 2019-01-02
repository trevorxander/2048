from random import randint
import copy
import time


class Model2048:
    DEFAULT_MATRIX_SIZE = 4

    def __init__(self, matrix_size=DEFAULT_MATRIX_SIZE):
        self._random_inserts_percent = 100
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

        self.restart_game()

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
        for row in range(0, self._matrix_size):
            for col in range(0, self._matrix_size):
                row_col = (row, col)
                self._empty_spots.add(row_col)

        self._link_game_state()
        self._rand_pop_in()


    @property
    def game_over(self):
        return self._game_over

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
        self.moved_tiles= copy.deepcopy(backup_state[2])
        self._score = copy.deepcopy(backup_state[3])
        self.pop_ins = copy.deepcopy(backup_state[4])

    def _link_game_state(self):
        self.game_state = [self._game_matrix,
                           self._empty_spots,
                           self.moved_tiles,
                           self._score,
                           self.pop_ins]


    def _move_tile(self, tile: tuple, left=0, up=0):

        def _set_new_tile(row, col, value):
            if (row, col) in self._empty_spots:
                self._empty_spots.remove((row, col))
            self._game_matrix[row][col] = value
            if value == 0:
                self._empty_spots.add((row, col))
            else:
                if tile != (row,col):
                    self.moved_tiles.append((tile, (row, col), value))

        new_tile_row = tile[0]
        new_tile_col = tile[1]
        tile_value = self._game_matrix[new_tile_row][new_tile_col]

        while True:
            new_tile_row = new_tile_row - up
            new_tile_col = new_tile_col - left

            # if tile reaches end of matrix
            if new_tile_row not in range(self._matrix_size) or \
                    new_tile_col not in range(self._matrix_size):
                _set_new_tile(new_tile_row + up, new_tile_col + left, tile_value)
                break
            # if tile moves through an empty spot
            if self._game_matrix[new_tile_row][new_tile_col] == 0:
                _set_new_tile(tile[0], tile[1], 0)
                continue
            # If the tile comes in contact with a tile of same value
            elif tile_value == self._game_matrix[new_tile_row][new_tile_col]:
                # If tile was not already merged this turn
                if (new_tile_row, new_tile_col) not in self._newly_merged:
                    #self._game_matrix[new_tile_row][new_tile_col] *= 2
                    _set_new_tile(new_tile_row,new_tile_col, self._game_matrix[new_tile_row][new_tile_col] * 2)
                    self._score[0] += self._game_matrix[new_tile_row][new_tile_col]
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

        self.moved_tiles.clear()
        self.pop_ins.clear()
        self._movement(**direction_arg)

        if self._is_game_over():
            print('GAME OVER!')

    def _movement(self, **direction_arg):
        direction = list(direction_arg.keys())[0]
        if direction == 'left' or direction == 'right':
            self._horizontal(**direction_arg)
        else:
            self._vertical(**direction_arg)
        self._newly_merged.clear()
        if self._last_game_state[0] != self._game_matrix:
            self._rand_pop_in()

    def _is_game_over(self):
        if len(self._empty_spots) > 0:
            return False

        backup = self._backup()
        current_game = backup[0]
        is_change = False
        for args in self._movement_args:
            self._movement(**args)
            if current_game != self._game_matrix:
                is_change = True
            self._restore(backup)

        self._game_over = not is_change
        return not is_change

    def _horizontal(self, left=0, right=0):
        right = -right
        check_order = range(left, len(self._game_matrix) + right)
        if right == -1:
            check_order = reversed(check_order)

        for col in check_order:
            for row in range(0, len(self._game_matrix)):
                if self._game_matrix[row][col] != 0:
                    self._move_tile((row, col), left=left + right)

    def _vertical(self, up=0, down=0):
        down = -down
        check_order = range(up, len(self._game_matrix) + down)
        if down == -1:
            check_order = reversed(check_order)

        for row in check_order:
            for col in range(0, len(self._game_matrix)):
                if self._game_matrix[row][col] != 0:
                    self._move_tile((row, col), up=up + down)

    def _rand_pop_in(self):
        max_random_inserts = randint(1, int(self._matrix_size / 2))
        for rands in range(0, max_random_inserts):
            if len(self._empty_spots) == 0:
                return
            empty_spot = self._rand_empty_spot()
            new_random_num = self._pick_random_insert()
            self._game_matrix[empty_spot[0]][empty_spot[1]] = new_random_num
            self.pop_ins.append((empty_spot,new_random_num))
            continue

    def _rand_empty_spot(self):
        return self._empty_spots.pop()

    def _pick_random_insert(self):
        for num in self._random_inserts:
            if num == self._random_inserts[- 1]:
                return num
            if randint(0, 100) <= self._random_inserts_percent:
                return num
