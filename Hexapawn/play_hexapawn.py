from dlgo import minimax
from dlgo import hexapawn

from six.moves import input

COL_NAMES = '123'


def print_board(board):
    print('   1   2   3')
    for row in (1, 2, 3):
        pieces = []
        for col in (1, 2, 3):
            piece = board.get(hexapawn.Point(row, col))
            if piece == hexapawn.Player.x:
                pieces.append('X')
            elif piece == hexapawn.Player.o:
                pieces.append('O')
            else:
                pieces.append(' ')
        print('%d  %s' % (row, ' | '.join(pieces)))


def main():
    game = hexapawn.GameState.new_game()

    human_player = hexapawn.Player.x
    # bot_player = hexapawn.Player.o

    bot = minimax.MinimaxAgent()

    while not game.is_over():
        print_board(game.board)
        if game.next_player == human_player:
            # get list for starting points
            starting_pieces = game.legal_moves_hex(human_player)[1]
            # get list of move options
            options = game.legal_moves_hex(human_player)[0]
            # get the mapping of start to end points
            move_dict = game.legal_moves_hex(human_player)[2]
            # print out the move options for the player
            for i, (x, y) in enumerate(zip(starting_pieces, options)):
                print(i, (x,y))
            # get the move
            human_move = int(input('-- ').strip())
            print(options[human_move])
            # define the start point for the move
            start_point = starting_pieces[human_move]
            # define the end point for the move
            point = options[human_move]
            # convert start point to move object
            start_move = hexapawn.Move(start_point)
            # convert end point to move object
            move = hexapawn.Move(point)
            # apply the move to the game state
            game = game.apply_move(start_move, move)
        else:
            # let the bot make its choice
            move = bot.select_move(game)
            # apply the bots move with the start and end point
            game = game.apply_move(move[0],move[1])

    print_board(game.board)
    winner = game.winner()
    if winner is None:
        print("It's a draw.")
    else:
        print('Winner: ' + str(winner))


if __name__ == '__main__':
    main()
