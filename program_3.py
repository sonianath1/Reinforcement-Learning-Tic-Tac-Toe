"""
⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹ ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹
CS441 - Sonia Nath - Programming 3 - Problem 2: tic tac toe
⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹ ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹
"""

import random
import matplotlib.pyplot as plt
import sys

# GLOABL VARIABLES
AGENT = 'X'
OPPONENT= 'O'
# rewards based on outcome
win= 1.0
draw= 0.5
loss = -1.0


# creating a 3x3 board
def new_board():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


# checking for whicjh actioas are legal
def available_actions(board):
    actions = []

    for row in range(3):
        for col in range(3):

            if board[row][col] == 0:
                actions.append((row, col))

    return actions


# applying the move thst the player wants
def apply_move(board, action, player):

    row, col = action

    new_board = []

    for r in board:
        new_board.append(r.copy())

    new_board[row][col] = player

    return new_board



# checking through all winning boards and seeing
# if they match. if so, it is a win.
def check_winner(board):
 
    '''
    ROWS / COLUMNS
    '''
    for row in board:
        if row[0] != 0:
            if row[0] == row[1] == row[2]:
                return row[0]

    for col in range(3):
        if board[0][col] != 0:
            if board[0][col] == board[1][col] == board[2][col]:
                return board[0][col]

    '''
    DIAGNOALS
    '''
    #(top left to bottom right)
    if board[0][0] != 0: 
        if board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
    # (top rihgt to bottom left)
    if board[0][2] != 0: 
        if board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]

    '''
    DRAW
    '''
    if not available_actions(board):
        return "draw"

    '''
    GAME IS STILL GOING
    '''
    return None

#printing the board for visual player purposes
def render(board):

    print("---------|")

    for row in board:
        row_string = ""

        for i in range(len(row)):
            # convert to string
            row_string += str(row[i])

            # seperators
            if i != len(row) - 1:
                row_string += " | "

        print(row_string)
        print("---------|")

#    print("---------")


#turning winner into reward. 
def reward_for(winner):
    if winner == AGENT:
        return win
    elif winner == OPPONENT:
        return loss
    elif winner == 'draw':
        return draw
    return 0.0


# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 
#               Q-learning agent
# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\


#evaluations with tuple represerntation
def board_to_tuple(board):
    rows = []

    for row in board:
        rows.append(tuple(row))

    return tuple(rows)


# get dict key for Q table
def q_key(state, action):
    return (board_to_tuple(state), action)


# return the Q-value for a state and action
# if not seen before, 0.0 is Q value
def get_q(Q, state, action):
    return Q.get(q_key(state, action), 0.0)


# bext move using greedy 
def epsilon_greedy(Q, state, actions, epsilon):
    if random.random() < epsilon:
        return random.choice(actions)

    q_values = []
    best_actions = []
 
    max_q, q_values = find_max_q(Q, state, actions)

    for i in range(len(actions)):
        if q_values[i] == max_q:
            best_actions.append(actions[i])

    return random.choice(best_actions)


#used in function to calulate
def max_q_next(Q, state):
    if state is None:
        return 0.0
    actions = available_actions(state)
    if not actions:
        return 0.0
    
    max_q, _ = find_max_q(Q, state, actions)

    return max_q


# finding max q value
def find_max_q(Q, state, actions):
    q_values = []
    
    for action in actions:
        q = get_q(Q, state, action)
        q_values.append(q)

    max_q = max(q_values)

    return max_q, q_values



# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 
#                 Evaluation 
# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 


# agent plays with random, 
def play_eval_game(Q, epsilon):
    state = new_board()
    while True:
        actions = available_actions(state)
        a = epsilon_greedy(Q, state, actions, epsilon)
        state = apply_move(state, a, AGENT)
        winner = check_winner(state)
        if winner is not None:
            break

        opp_a = random_opponent_move(state)
        state = apply_move(state, opp_a, OPPONENT)
        winner = check_winner(state)
        if winner is not None:
            break

    if winner == AGENT:
        return 'win'
    elif winner == OPPONENT:
        return 'loss'
    return 'draw'


# evaluate a game 
def evaluate(Q, epsilon):
    score = 0.0
    num_games = 10

    results = {'win': 0, 'loss': 0, 'draw': 0}

    for _ in range(num_games):
        outcome = play_eval_game(Q, epsilon)
        results[outcome] += 1
        
        if outcome == 'win':
            score += 1.0
        elif outcome == 'draw':
            score += 0.5
    return score, results


# random oppentent movements
def random_opponent_move(board):
    return random.choice(available_actions(board))



# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 
#                Training loop
# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 

# training
def play_training(Q, epsilon, lr, gamma):

    state = new_board()

    while True:
        # agent goes first 
        actions = available_actions(state)
        a = epsilon_greedy(Q, state, actions, epsilon)
        state_after_agent = apply_move(state, a, AGENT)
        winner = check_winner(state_after_agent)

        if winner is not None:
            # if game ended on the agent's move
            target = reward_for(winner)
          #  target = r
            update_q(Q, state, a, target, lr)
            break

        # Opponents responce
        opp_a = random_opponent_move(state_after_agent)
        state_after_opp = apply_move(state_after_agent, opp_a, OPPONENT)
        winner = check_winner(state_after_opp)

        if winner is not None:
            target = reward_for(winner)
#            targ0iet = r
            update_q(Q, state, a, target, lr)
            break
        else:
            # r is 0.0 since no winner yet 
            target = 0.0 + gamma * max_q_next(Q, state_after_opp)
            update_q(Q, state, a, target, lr)
            state = state_after_opp  # continue the game


# updating new q state
def update_q(Q, state, action, target, lr):

    old_q = get_q(Q, state, action)
    new_q = old_q + lr * (target - old_q)
    Q[q_key(state, action)] = new_q


def train(num_training, lr, gamma, epsilon_0, e_decay, decay_timing,
          evaluations, evaluations_e):
    Q = {}
    epsilon = epsilon_0

    epochs, scores = [], []

    for training in range(1, num_training + 1):
        play_training(Q, epsilon, lr, gamma)

        # decaying epsilon every decay_timing trainings
        if training % decay_timing == 0:
            epsilon = max(0.0, epsilon - e_decay)

        # periodic evaluations
        if training % evaluations == 0:
            score, _ = evaluate(Q, evaluations_e)
            epochs.append(training)
            scores.append(score / 10)

            print(f"Episode {training:6d} ✶ eval score: score={score/10:.2f}/1.0") 

    return Q, epochs, scores



# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 
#              human based game
# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 


# getting human players move
def get_human_move(board):
    legal = available_actions(board)
    while True:
        try:
            choice = int(input("Choose a square (1-9): ")) - 1
        except ValueError:
            print("Please enter a number from 1 to 9.")
            continue

        if choice not in range(9):
            print("num must be between 1 and 9.")
            continue

        row = choice // 3
        col = choice % 3
        action = (row, col)

        if action not in legal:
            print("NOT A LEGAL TURN. CHOOSE A LEGAL SQUARE")
        else:
            return action


# let the human play one or more games against the agent
def play_against_agent(Q):
    answer = input("\nWould you like to play 10 games? (y/n): ").strip().lower()
    if answer != 'y':
        print("\nExiting now...")
        sys.exit(0)
    
    agent_wins = 0
    human_wins = 0
    draws = 0

    for i in range(10):
        print("\n⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\n")
        print(f"\nThis is game {i}")
        state = new_board()
        print("\nYou are playing as O.\n")

        # game starts
        while True:
            # agents turn first
            print("\nAgent's turn")
            agent_action = epsilon_greedy(Q,state, available_actions(state), epsilon=0.0)
            state = apply_move(state, agent_action, AGENT)
#            print("\n")
            render(state)
            

            winner = check_winner(state)
            if winner is not None:
                break

            # humans turn if agent not won
            human_action = get_human_move(state)
            state = apply_move(state, human_action, OPPONENT)

            print("\nYour move:")
            render(state)

            winner = check_winner(state)
            if winner is not None:
                break
        
        # checking who won or if draw
        if winner == AGENT:
            print("The agent wins!")
            agent_wins += 1
        elif winner == OPPONENT:
            print("You win!")
            human_wins += 1
        else:
            print("It's a draw!")
            draws += 1

    return agent_wins, human_wins, draws

'''
        # if player wants to go again
        again = input("\nPlay again? (y/n): ").lower()
        if again != 'y':
            print("\n⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\n")
            print("Thanks for playing!")
            break
'''

# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 
#                  Plotting
# ⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\ 
def plot_progress(epochs, scores):
    plt.plot(epochs, scores)
    plt.xlabel("Epoch #")
    plt.ylabel("(Total score) / 10")
    plt.title("Tic tac toe with Q learning agent")
    plt.savefig("tic-tac-toe-training.png")


if __name__ == "__main__":
    #    random.seed(0)

    # Training
    num_training  = 30000
    lr = 0.3 # leanring rate
    gamma = 0.95



    # epsilon-greedy 
    epsilon_0  = 0.3 # initial exploration rate
    e_decay = 0.02 # amount to subtract from epsilon
    decay_timing = 500 # subtract every this many trainings



    # Evaluation during training
    evaluations = 500 # run an eval against random every N trainings
    evaluations_e = 0.0# greedy (no exploration) when evaluating


    print("TRAINING STARTS")
    Q, epochs, scores = train(num_training, lr, gamma, epsilon_0, 
                              e_decay, decay_timing, evaluations,
                              evaluations_e)

    plot_progress(epochs, scores)

    print("\nDONE!!!!!i\n")
    print("\n10 games vs. random opponent (greedy policy)")
    final_score, final_results = evaluate(Q, epsilon=0.0)
    print(f"Score: {final_score}/10  "
          f"(wins={final_results['win']}, "
          f"losses={final_results['loss']}, "
          f"draws={final_results['draw']})")

    print("\n⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\n")
    agent_w, human_w, draws = play_against_agent(Q)
    print("\n⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹⊹₊˚‧︵‿₊⊱·✶·⊰₊‿︵‧˚₊⊹\n")
    print("\nResults of human v agent game")
    print(f"Agent wins: {agent_w} ·✶· Human wins: {human_w} ·✶· Draws: {draws}")
