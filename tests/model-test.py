from game.model import Game2048

def print_matrix (matrix):
    for row in matrix:
        print(row)

    print('\n')


if __name__ == '__main__':
    game = Game2048 (4)
    print_matrix(game.get_matrix())
    game.up()
    print_matrix(game.get_matrix())
    game.down()
    game.left()
    print_matrix(game.get_matrix())

