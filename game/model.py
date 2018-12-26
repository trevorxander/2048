from random import randint
import random


class Game2048:
    DEFAULT_MATRIX_SIZE = 4

    def __init__(self, matrix_size=DEFAULT_MATRIX_SIZE):
        self._random_inserts_percent = 50
        self._matrix_size = matrix_size
        self._game_matrix = [[0] * self._matrix_size] * self._matrix_size
        self._no_random_inserts = self._matrix_size / 2
        self._random_inserts = [2, 4]
        self._newly_merged = set()
        self._empty_spots = set()

        self.restart_game()

    def restart_game(self):
        self._game_matrix = [[0 for row in self._game_matrix] for col in self._game_matrix]
        for row in range(0, self._matrix_size):
            for col in range(0, self._matrix_size):
                row_col = (row, col)
                self._empty_spots.add(row_col)
        self._rand_pop_in()

    def _print(self):
        for row in self._game_matrix:
            print(row)
        print('\n')


    def _set_new_tile(self, row, col, value):
        if (row, col) in self._empty_spots:
            self._empty_spots.remove((row, col))
        self._game_matrix[row][col] = value
        if value == 0:
            self._empty_spots.add ((row,col))


    def _move_tile(self, tile: tuple, left=0, up=0):
        new_tile_row = tile[0]
        new_tile_col = tile[1]
        tile_value = self._game_matrix[new_tile_row][new_tile_col]

        while True:
            new_tile_row = new_tile_row - up
            new_tile_col = new_tile_col - left

            #
            if new_tile_row not in range(0, self._matrix_size) or \
                    new_tile_col not in range(0, self._matrix_size):
                self._set_new_tile(new_tile_row + up, new_tile_col + left, tile_value)
                break
            if self._game_matrix[new_tile_row][new_tile_col] == 0:
                self._set_new_tile(tile[0], tile[1], 0)
                continue
            elif tile_value == self._game_matrix[new_tile_row][new_tile_col]:
                if (new_tile_row,new_tile_col) not in self._newly_merged:
                    self._game_matrix[new_tile_row][new_tile_col] *= 2
                    self._newly_merged.add((new_tile_row,new_tile_col))
                    self._set_new_tile(tile[0], tile[1], 0)
                else:
                    self._set_new_tile(new_tile_row + up, new_tile_col + left, tile_value)
                return
            else:
                self._set_new_tile(new_tile_row + up, new_tile_col + left, tile_value)
                return


    def _movement(self, left = 0, right = 0, up = 0, down = 0):
        if left:
            self._horizontal(left=1)
        if right:
            self._horizontal(right=1)
        if up:
            self._vertical(up=1)
        if down:
            self._vertical(down=1)

        self._newly_merged.clear()
        self._rand_pop_in()


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

    def left(self):
        self._movement(left=1)

    def right(self):
        self._movement(right=1)

    def up(self):
        self._movement(up=1)

    def down(self):
        self._movement(down=1)

    def get_matrix(self):
        return self._game_matrix

    def _rand_pop_in(self):
        max_random_inserts = randint(1, int(self._matrix_size / 2))
        print('')
        for rands in range(0,max_random_inserts):
            if len(self._empty_spots) == 0:
                return
            empty_spot = self._rand_empty_spot()
            self._game_matrix[empty_spot[0]][empty_spot[1]] = self._pick_random_insert()
            continue

    def _rand_empty_spot(self):
        return self._empty_spots.pop()

    def _pick_random_insert(self):
        for num in self._random_inserts:
            if num == self._random_inserts[- 1]:
                return num
            if randint(0,100) <= self._random_inserts_percent:
                return num
