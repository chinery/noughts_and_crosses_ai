import math
import numpy as np
import copy
import random
from abc import ABC, abstractmethod


class NoughtsAndCrosses:
    def __init__(self):
        self.EMPTY = ' '
        self.NOUGHT = 'O'
        self.CROSS = 'X'
        self.DRAW = 'draw'

        self.next_player = self.CROSS
        self.flip_player = {self.CROSS: self.NOUGHT, self.NOUGHT: self.CROSS}

        self.board = np.array([[self.EMPTY for _ in range(3)] for _ in range(3)])

    def valid_move(self, row, col):
        return self.board[row, col] == self.EMPTY

    def move(self, row, col):
        """Returns a *copy* of this state with the specified move"""
        if not self.valid_move(row, col):
            raise ValueError("Position not empty")

        state = copy.deepcopy(self)
        state.board[row, col] = state.next_player
        state.next_player = state.flip_player[state.next_player]
        return state

    def winner(self):
        for i in range(3):
            if np.all(self.board[i, :] == self.board[i, 0]) and self.board[i, 0] != self.EMPTY:
                return self.board[i, 0]
            if np.all(self.board[:, i] == self.board[0, i]) and self.board[0, i] != self.EMPTY:
                return self.board[0, i]
        if self.EMPTY != self.board[0, 0] and self.board[0, 0] == self.board[1, 1] and self.board[1, 1] == self.board[2, 2]:
            return self.board[1, 1]
        if self.EMPTY != self.board[2, 0] and self.board[2, 0] == self.board[1, 1] and self.board[1, 1] == self.board[0, 2]:
            return self.board[1, 1]
        if np.all(self.board != self.EMPTY):
            return self.DRAW
        return False

    def actions(self):
        row, col = np.nonzero(self.board == self.EMPTY)
        return [(r, c) for r, c in zip(row, col)]

    def __str__(self):
        grid = "  0   1   2\n"
        for i in range(3):
            line = f"{i} {self.board[i, 0]} │ {self.board[i, 1]} │ {self.board[i, 2]}\n"
            grid += line
            if i < 2:
                grid += " " + "─"*3 + "┼" + "─"*3 + "┼" + "─"*3 + "\n"
        return grid


class Agent(ABC):
    @abstractmethod
    def next_move(self, state: NoughtsAndCrosses):
        pass


class ABMinimaxAgent(Agent):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def next_move(self, state: NoughtsAndCrosses = NoughtsAndCrosses()):
        print("\nThe AI is thinking.", end="")
        player = state.next_player

        best_action = []
        best_value = -1 * math.inf
        for action in state.actions():
            new_state = state.move(action[0], action[1])
            action_value = self.get_value(new_state, player, get_min=True)
            print(".", end="", flush=True)
            if self.verbose:
                print(action_value, end=" ")
            if action_value > best_value:
                best_action = [action]
                best_value = action_value
            if action_value == best_value:
                best_action.append(action)
        if self.verbose:
            print()
        print("\n")
        return random.choice(best_action)

    def get_value(self, state, player, get_min, alpha=-math.inf, beta=math.inf):
        """If get_min is set to true, returns the minimum value, otherwise the maximum value"""
        other_player = state.flip_player[player]

        winner = state.winner()
        if winner == player:
            return 1
        elif winner == other_player:
            return -1
        elif winner == state.DRAW:
            return 0

        best_value = math.inf
        if not get_min:
            best_value *= -1

        for action in state.actions():
            new_state = state.move(action[0], action[1])
            action_value = self.get_value(new_state, player, get_min=not get_min, alpha=alpha, beta=beta)

            if not get_min:
                alpha = max(alpha, action_value)
                if action_value >= beta:
                    return action_value
            else:
                beta = min(beta, action_value)
                if action_value <= alpha:
                    return action_value

            if not get_min and action_value > best_value \
                    or get_min and action_value < best_value:
                best_value = action_value

        return best_value


class HumanAgent(Agent):
    def next_move(self, state: NoughtsAndCrosses):
        while True:
            try:
                print("What's your next move? In format row,col")
                move = input("> ").strip()
                move = move.split(',')
                move = int(move[0]), int(move[1])
                if not state.valid_move(move[0], move[1]):
                    print("Space must be empty.")
                else:
                    return move
            except ValueError:
                print("Please enter valid space as row,col between 0,0 and 2,2")


def run_game(player1: Agent = HumanAgent(), player2: Agent = ABMinimaxAgent()):
    state = NoughtsAndCrosses()
    print(state)
    while not state.winner():
        move = player1.next_move(state)
        state = state.move(move[0], move[1])
        print(state)
        if state.winner() == state.CROSS:
            print("Player one wins!")
            return
        elif state.winner() == state.DRAW:
            print("It's a draw.")
            return

        move = player2.next_move(state)
        state = state.move(move[0], move[1])
        print(state)
        if state.winner() == state.NOUGHT:
            print("Player two wins!")
            return
        elif state.winner() == state.DRAW:
            print("It's a draw.")
            return


def yes_no_input(text: str, prompt: str = "> ") -> bool:
    print(text + " (y/n)")
    response = input(prompt).strip()
    while response not in ['y', 'n']:
        print("Please enter y for yes or n for no.")
        print(text)
        response = input(prompt).strip()
    return response == "y"


def play():
    print("Let's play noughts and crosses!")
    again = True
    while again:
        response = yes_no_input("Would you like to play first?")
        if response:
            run_game(player1=HumanAgent(), player2=ABMinimaxAgent())
        else:
            run_game(player1=ABMinimaxAgent(), player2=HumanAgent())

        again = yes_no_input("Would you like to play again?")


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        pass