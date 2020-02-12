import enum
import random

from dlgo.agent import Agent
from dlgo import octopawn


__all__ = [
    'MinimaxAgent',
]


# tag::gameresult-enum[]
class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3
# end::gameresult-enum[]


def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw


# tag::minimax-signature[]
def best_result(game_state):
# end::minimax-signature[]
# tag::minimax-base-case[]
    if game_state.is_over():
        # Game is already over.
        if game_state.winner() == game_state.next_player:
            # We win!
            return GameResult.win
        elif game_state.winner() is None:
            # A draw.
            return GameResult.draw
        else:
            # Opponent won.
            return GameResult.loss
# end::minimax-base-case[]

    candidate_move_options = game_state.legal_moves_hex(octopawn.Player.o)[0]
    candidate_move_starting_pieces = game_state.legal_moves_hex(octopawn.Player.o)[1]
# tag::minimax-recursive-case[]
    best_result_so_far = GameResult.loss
    for candidate_move in candidate_move_options:
        candidate_move_start = candidate_move_starting_pieces[candidate_move_options.index(candidate_move)]
        next_state = game_state.apply_move(candidate_move_start, candidate_move)     # <1>
        opponent_best_result = best_result(next_state)         # <2>
        our_result = reverse_game_result(opponent_best_result) # <3>
        if our_result.value > best_result_so_far.value:        # <4>
            best_result_so_far = our_result
    return best_result_so_far
# end::minimax-recursive-case[]
        # See what the board would look like if we play this move.
        # Find out our opponent's best move.
        # Whatever our opponent wants, we want the opposite.
        # See if this result is better than the best we've seen so far.


# tag::minimax-agent[]
class MinimaxAgent(Agent):
    def select_move(self, game_state):
        # define lists for moves and for starting points
        win_start = []
        winning_moves = []
        draw_start = []
        draw_moves = []
        losing_start = []
        losing_moves = []
        # lists for starting points and move end points
        starting_points = game_state.legal_moves_hex(octopawn.Player.o)[1]
        options = game_state.legal_moves_hex(octopawn.Player.o)[0]
        # Loop over all legal moves.
        for possible_move in options:
            # Calculate the game state if we select this move.
            # find the corresponding starting move
            possible_move_starting_point = starting_points[options.index(possible_move)]
            next_state = game_state.apply_move(possible_move_starting_point, possible_move)
            # Since our opponent plays next, figure out their best
            # possible outcome from there.
            opponent_best_outcome = best_result(next_state)
            # Our outcome is the opposite of our opponent's outcome.
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            # Add this move to the appropriate list.
            if our_best_outcome == GameResult.win:
                # add winning move to winning move list
                winning_moves.append(possible_move)
                # add the start points to winning move start point list
                # this is necessary in order to be able to change the point on the grid
                # the place takes the start and end points and converts the start point to None and end point to player
                win_start.append(possible_move_starting_point)
            elif our_best_outcome == GameResult.draw:
                # add draw moves to list
                draw_moves.append(possible_move)
                # add corresponding start points to list
                draw_start.append(possible_move_starting_point)
            else:
                # add losing moves to list
                losing_moves.append(possible_move)
                # add corresponding start points
                losing_start.append(possible_move_starting_point)
        if winning_moves:
            #randomly pick winning move
            # return the start point and the end point (where the piece moves to)
            move = random.choice(winning_moves)
            where = winning_moves.index(move)
            start_move = starting_points[where]
            return start_move, move
        if draw_moves:
            # randomly pick drawing move
            # return the start and end points
            move = random.choice(draw_moves)
            where = draw_moves.index(move)
            start_move = starting_points[where]
            return start_move, move
        if losing_moves:
            # randomly pick a losing move
            # return start and end points
            move = random.choice(losing_moves)
            where = losing_moves.index(move)
            start_move = starting_points[where]
            return start_move, move
        #return random.choice(losing_moves)
# end::minimax-agent[]
