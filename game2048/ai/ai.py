import time
from game2048.model import Model2048
from random import randint
from anytree import AnyNode, RenderTree
from threading import Thread
import copy
import math
class AI:
    def __init__(self, interface):
        self.interface = interface
        self.all_move=['left',
                       'right',
                       'up',
                       'down']
        self._movement_args = [{'left': 1},
                               {'right': 1},
                               {'up': 1},
                               {'down': 1}]


    def make_move(self):
        game_shell = self.interface.get_result()
        if game_shell.is_game_over():
            return

        start = time.time()
        self.matrix = copy.deepcopy(game_shell.get_matrix())
        self.model = Model2048(matrix_size=len(self.matrix))
        next_move = self.get_next_move(self.matrix)
        self.interface.send_event(next_move)
        # print(time.time() - start)


    def get_next_move(self, matrix):
        root_node = self.create_node(matrix=matrix, parent=None)
        game_tree = self.create_game_tree(root_node)
        # print(RenderTree(game_tree))
        path = self.best_path(game_tree)
        return path.move

    def best_path(self, tree: AnyNode):

        def avg_score(path: AnyNode):
            if path.is_leaf:
                return path.score

            total_score = 0
            for child in path.children:
                total_score += avg_score(child)

            return total_score / 4

        best_score = 0
        best_path = 'Test'
        for child in tree.children:
            path_score = avg_score(child)
            if path_score > best_score:
                best_score = path_score
                best_path = child
        return best_path




    def create_game_tree(self, parent_node: AnyNode, max_depth = 1):
        if parent_node.depth >= max_depth:
            return
        create_tree_threads = []
        matrix = parent_node.game
        available_moves = self.model.available_moves(matrix)
        if len(available_moves) == 0:
            parent_node.score = 0

        for movement_arg in available_moves:
            for movement in movement_arg:
                moved_matrix = copy.deepcopy(matrix)
                self.model._movement(matrix=moved_matrix,**movement_arg)
                node = self.create_node(move=movement,
                                        matrix=moved_matrix,
                                        parent=parent_node)
                tree_thread = Thread(target=self.create_game_tree, args=[node])
                create_tree_threads.append(tree_thread)


        for threads in create_tree_threads:
            threads.start()
        for threads in create_tree_threads:
            threads.join()


        if parent_node.depth == 0:
            return parent_node


    def create_node(self, parent = None, matrix=None, move='start'):
        if parent is None:
            parent_score = 0
        else:
            parent_score = parent.score

        node = AnyNode(parent=parent,
                       move = move,
                       game=matrix,
                       score=self.calculate_score(matrix))
        return node

    def calculate_score(self, matrix: list):

        def find_snakes(row, col, tile, matrix):
            snakes = [0]
            if row > len(matrix) - 1:
                cell = matrix[col][row - 1]
                if (tile and tile * 2 == cell) or (tile == 0 and cell == 2):
                    snakes.append(1 + find_snakes(row - 1, col, cell, matrix))
            if row < len(matrix) - 1:
                cell = matrix[col][row + 1]
                if (tile and tile * 2 == cell) or (tile == 0 and cell == 2):
                    snakes.append(1 + find_snakes(row + 1, col, cell, matrix))
            if col > len(matrix) - 1:
                cell = matrix[col - 1][ row]
                if (tile and tile * 2 == cell) or (tile == 0 and cell == 2):
                    snakes.append(1 + find_snakes(row, col - 1, cell, matrix))
            if col < len(matrix) - 1:
                cell = matrix[col + 1][row]
                if (tile and tile * 2 == cell) or (tile == 0 and cell == 2):
                    snakes.append(1 + find_snakes(row, col + 1, cell, matrix))
            return max(snakes)

        cell_score = 0
        empty = 0
        adjacent = 0
        snakes = [1]
        for x in range(len(matrix)):
            for y in range(len(matrix)):
                cell = matrix[y][x]
                if cell > 0:
                    cell_score += (cell / 2 - 1)

                    if x > 0 and cell == matrix[y][x - 1]:
                        adjacent += 1
                    if y > 0 and cell == matrix[y - 1][x]:
                        adjacent += 1
                else:
                    empty += 1
                snakes.append(find_snakes(x, y, cell, matrix))

        monotonic_up = 0
        monotonic_down = 0
        monotonic_left = 0
        monotonic_right = 0
        for x in range(len(matrix)):
            current = 0
            next = current + 1
            while next < len(matrix):
                while next < len(matrix) - 1 and not matrix[next][x]:
                    next += 1
                current_cell = matrix[current] [x]
                current_value = math.log(current_cell, 2) if current_cell else 0
                next_cell = matrix[next][x]
                next_value = math.log(next_cell, 2) if next_cell else 0
                if current_value > next_value:
                    monotonic_up += (next_value - current_value)
                elif next_value > current_value:
                    monotonic_down += (current_value - next_value)
                current = next
                next += 1
        for y in range(len(matrix)):
            current = 0
            next = current + 1
            while next < len(matrix):
                while next < len(matrix) - 1 and not matrix[y][next]:
                    next += 1
                current_cell = matrix[y][current]
                current_value = math.log(current_cell, 2) if current_cell else 0
                next_cell = matrix[y][next]
                next_value = math.log(next_cell, 2) if next_cell else 0
                if current_value > next_value:
                    monotonic_left += (next_value - current_value)
                elif next_value > current_value:
                    monotonic_right += (current_value - next_value)
                current = next
                next += 1
                
        monotonic = max(monotonic_up, monotonic_down) + max(monotonic_left, monotonic_right)


        return cell_score + empty * 32 + adjacent * 31 + max(snakes) * 5 + monotonic * 1


    def get_adjacents(self, matrix, pos: tuple):
        pass