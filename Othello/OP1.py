import sys
from random import choice

whiteSpots = [44, 55]
blackSpots = [45, 54]
white_token = "o"
black_token = "@"
directions = [1, -1, 11, -11, 10, -10, 9, -9]
start_board = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"
allMoves = []
global_player = ""
global_opponent = ""
corners = [11, 19, 81, 89]
badspots = [22, 72, 27, 77, 12, 21, 18, 28, 78, 87, 82, 71]
SQUARE_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 280, -40, 30, 15, 15, 30, -40, 280, 0,
    0, -20, -180, -5, -5, -5, -5, -90, -180, 0,
    0, 30, -5, 15, 3, 3, 15, -5, 30, 0,
    0, 15, -5, 3, 3, 3, 3, -5, 15, 0,
    0, 15, -5, 3, 3, 3, 3, -5, 15, 0,
    0, 30, -5, 15, 3, 3, 15, -5, 30, 0,
    0, -20, -180, -5, -5, -5, -5, -90, -180, 0,
    0, 280, -40, 30, 15, 15, 30, -40, 280, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
SQUARE_WEIGHTSe = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 500, -300, 75, 75, 75, 70, -300, 500, 0,
    0, -300, -300, -5, -5, -5, -5, -300, -300, 0,
    0, 70, -15, -15, -10, -10, -15, -15, 70, 0,
    0, 75, -15, -10, -10, -10, 10, -15, 75, 0,
    0, 75, -15, -10, -10, -10, 10, -15, 75, 0,
    0, 70, -15, -15, 10, 10, 15, -15, 70, 0,
    0, -300, -300, -5, -5, -5, -5, -300, -300, 0,
    0, 400, -30, 75, 75, 75, 30, -40, 400, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


def weighted_score3(player, board, opponent):
    opp = global_opponent
    player = global_player
    is_black = True
    count = 0
    if global_player == white_token:
        is_black = False
    for i in board:
        if i == ".":
            count += 1
    total = 0
    for sq in squares():
        if board[sq] == player:
            total += SQUARE_WEIGHTSe[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTSe[sq]
    if count >= 60:
        if is_black:
            return len(blackSpots) / len(whiteSpots) * 10 + total / 2
        else:
            return len(whiteSpots) / len(blackSpots) * 10 + total / 2
    else:
        return total


def weighted_score(player, board, opponent):
    is_black = True
    count = 0
    if global_player == white_token:
        is_black = False
    for i in board:
        if i == ".":
            count += 1
    if is_black and count > 70:
        return len(possible_moves(board, black_token)) * len(blackSpots) / len(whiteSpots) * 10
    elif count > 70:
        return len(possible_moves(board, white_token)) * len(whiteSpots) / len(blackSpots) * 10
    else:
        opp = opponent
        total = 0
        for sq in squares():
            if board[sq] == player:
                total += SQUARE_WEIGHTSe[sq]
            elif board[sq] == opp:
                total -= SQUARE_WEIGHTSe[sq]
        return total



def weighted_score2(player, board, opponent):
    #
    #
    count = 0
    for i in board:
        if i == ".":
            count += 1
    if count >= 60:
        opp = opponent
        total = 0
        for sq in squares():
            if board[sq] == player:
                total -= SQUARE_WEIGHTSe[sq]
            elif board[sq] == opp:
                total = SQUARE_WEIGHTSe[sq]
        return ((len(possible_moves(board, player)) / 1 + len(possible_moves(board, opponent))) * 20)
    #
    # # elif 50 > count >= 30:
    # #     opp = opponent
    # #     total = 0
    # #     for sq in squares():
    # #         if board[sq] == player:
    # #             total += SQUARE_WEIGHTS[sq]
    # #         elif board[sq] == opp:
    # #             total -= SQUARE_WEIGHTS[sq]
    # #     return total - len(possible_moves(board, player))
    else:
        opp = opponent
        total = 0
        for sq in squares():
            if board[sq] == player:
                total += SQUARE_WEIGHTS[sq]
            elif board[sq] == opp:
                total -= SQUARE_WEIGHTS[sq]
        return total / 4 - len(possible_moves(board, opponent))


def possible_moves(board, token):
    possible = []
    is_black = False
    if token == black_token:
        is_black = True
    if is_black:
        for i in whiteSpots:
            next_search = []
            if board[i + 1] == black_token:
                next_search.append(-1)
            if board[i - 1] == black_token:
                next_search.append(1)
            if board[i + 10] == black_token:
                next_search.append(-10)
            if board[i - 10] == black_token:
                next_search.append(10)
            if board[i + 11] == black_token:
                next_search.append(-11)
            if board[i - 11] == black_token:
                next_search.append(11)
            if board[i + 9] == black_token:
                next_search.append(-9)
            if board[i - 9] == black_token:
                next_search.append(9)
            # print(next_search)
            for z in next_search:
                current = i
                while board[current] != "?" and board[current] != "." and board[current] != "@":
                    current = current + z
                if board[current] == ("."):
                    possible.append(current)
    else:
        for i in blackSpots:
            next_search = []
            if board[i + 1] == white_token:
                next_search.append(-1)
            if board[i - 1] == white_token:
                next_search.append(1)
            if board[i + 10] == white_token:
                next_search.append(-10)
            if board[i - 10] == white_token:
                next_search.append(10)
            if board[i + 11] == white_token:
                next_search.append(-11)
            if board[i - 11] == white_token:
                next_search.append(11)
            if board[i + 9] == white_token:
                next_search.append(-9)
            if board[i - 9] == white_token:
                next_search.append(9)
            # print(next_search)
            for z in next_search:
                current = i
                while board[current] != "?" and board[current] != "." and board[current] != "o":
                    current = current + z
                if board[current] == ("."):
                    possible.append(current)
    return sorted(possible)


def print_puzzle(board_size, order):
    count = 0
    for i in range(board_size):
        for j in range(board_size):
            print(order[count], end=" ")
            count += 1
        print()
    print()


def swap(state, pos1, letter):
    return state[:pos1] + letter[0] + state[pos1 + 1:]


def move(board, token, position):
    current = swap(board, position, token)
    # print_puzzle(10,current)
    is_black = False
    if token == black_token:
        is_black = True
    if is_black:
        for i in directions:
            if position + i in whiteSpots:
                start = position + i
                while board[start] == white_token:
                    start = start + i
                if board[start] == "@":
                    end = start
                    current_board = current
                    for z in range(position + i, end, i):
                        current_board = swap(current_board, z, token)
                        # if z in whiteSpots:
                        #     whiteSpots.remove(z)
                        # blackSpots.append(z)
                    current = current_board
    else:
        for i in directions:
            if position + i in blackSpots:
                start = position + i
                while board[start] == black_token:
                    start = start + i
                if board[start] == "o":
                    end = start
                    current_board = current
                    for z in range(position + i, end, i):
                        current_board = swap(current_board, z, token)
                    current = current_board
    blackSpots.clear()
    whiteSpots.clear()
    count = 0
    for i in current:
        if i == "@":
            blackSpots.append(count)
        elif i == "o":
            whiteSpots.append(count)
        count += 1
    return current


def updatelist(board):
    blackSpots.clear()
    whiteSpots.clear()
    count = 0
    for i in board:
        if i == "@":
            blackSpots.append(count)
        elif i == "o":
            whiteSpots.append(count)
        count += 1


def goal_test(board):
    if "." not in board:
        return True
    return False


def realMove(board, token, position):
    current_board = swap(board, position, token)
    print_puzzle(10, current_board)


def maxx(player, board, depth, opponent):
    if depth == 0:
        return weighted_score(player, board, opponent)
    possible = possible_moves(board, player)
    maxValue = -1000000
    for i in possible:
        new_board = move(board, player, i)
        z = mini(opponent, new_board, depth - 1, player)
        if maxValue < z:
            maxValue = z
            position = i
    return maxValue


def mini(player, board, depth, opponent):
    if depth == 0:
        return weighted_score(player, board, opponent)
    possible = possible_moves(board, player)
    minValue = 100000
    for i in possible:
        new_board = move(board, player, i)
        z = maxx(opponent, new_board, depth - 1, player)
        if z < minValue:
            minValue = z
            position = i
    return minValue


def game(board, player):
    # print("State",allMoves)
    print_puzzle(10, board)
    if goal_test(board):
        percentW = (len(whiteSpots) / 64) * 100
        percentB = (len(blackSpots) / 64) * 100
        print("Percent White:", percentW)
        print("Percent Black", percentB)
        print("All moves", allMoves)
        return allMoves
    print("Black:", len(blackSpots))
    print("White:", len(whiteSpots))
    # print(whiteSpots)
    # print(blackSpots)
    if player == black_token:
        x = possible_moves(board, "@")
        print("Black Possible Moves", x)
        if len(x) != 0:
            random_move = choice(x)
            allMoves.append(random_move)
            # blackSpots.append(random_move)
            print("The move chosen was", random_move)
            latest_board = move(board, black_token, random_move)
            game(latest_board, white_token)

        else:
            print("Move was passed")
            allMoves.append(-1)
            game(board, white_token)
    else:
        x = possible_moves(board, "o")
        print("White Possible Moves", x)
        if len(x) != 0:
            random_move = choice(x)
            allMoves.append(random_move)
            # whiteSpots.append(random_move)
            print("The move chosen was", random_move)
            latest_board = move(board, white_token, random_move)
            game(latest_board, black_token)
        else:
            print("Move was passed")
            allMoves.append(-1)
            game(board, black_token)


def main_minimax(board, player, depth):
    bestMove = -77
    current_best = -1000
    if player == "@":
        opposite = "o"
        for i in possible_moves(board, player):
            latest_board = move(board, player, i)
            score = mini_alphabeta(opposite, latest_board, depth, player, -999999, 99999)
            if score > current_best:
                current_best = score
                bestMove = i
    else:
        opposite = "@"
        for i in possible_moves(board, player):
            latest_board = move(board, player, i)
            score = maxx_alphabeta(opposite, latest_board, depth, player, -999999, 999999)
            if score > current_best:
                current_best = score
                bestMove = i
    return bestMove


def main_minimax2(globalp, globalo, board, player, depth):
    global_player = globalp
    global_opponent = globalo
    # x = possible_moves(board,player)
    # for i in corners:
    #     for o in x:
    #         if o == x:
    #             return o
    # for i in badspots:
    #     for k in x:
    #         if i==k:
    #             x.remove(k)
    # if len(x)!=0:
    #     bestMove = choice(x)
    #     return bestMove
    # else:
    #     return choice(possible_moves(board,player))
    bestMove = -77
    current_best = -10000000
    if player == "@":
        opposite = "o"
    else:
        opposite = "@"
    for i in possible_moves(board, player):
        latest_board = move(board, player, i)
        score = maxx_alphabeta(opposite, latest_board, depth, player, -999999, 99999)
        if score > current_best:
            current_best = score
            bestMove = i
    return bestMove


def maxx_alphabeta(player, board, depth, opponent, alpha, beta):
    if len(possible_moves(board, player)) and len(possible_moves(board, opponent)) == 0:
        totaltokens = len(whiteSpots) + len(blackSpots)
        if player == "o":
            if (len(whiteSpots) > len(blackSpots)):
                return 100000 * (len(whiteSpots) / totaltokens)
            else:
                return -100000 * (len(whiteSpots) / totaltokens)
        else:
            if (len(blackSpots) > len(whiteSpots)):
                return 100000 * (len(blackSpots) / totaltokens)
            else:
                return -100000 * (len(whiteSpots) / totaltokens)
    if depth == 0:
        return weighted_score(player, board, opponent)
    possible = possible_moves(board, player)
    maxValue = alpha
    for i in possible:
        new_board = move(board, player, i)
        z = mini_alphabeta(opponent, new_board, depth - 1, player, alpha, beta)
        if z > alpha:
            alpha = z
        if maxValue < z:
            maxValue = z
        if beta <= alpha:
            return maxValue
    return maxValue


def mini_alphabeta(player, board, depth, opponent, alpha, beta):
    if len(possible_moves(board, player)) and len(possible_moves(board, opponent)) == 0:
        totaltokens = len(whiteSpots) + len(blackSpots)
        if player == "o":
            if (len(whiteSpots) > len(blackSpots)):
                return -100000 * (len(whiteSpots) / totaltokens)
            else:
                return 100000 * (len(whiteSpots) / totaltokens)
        else:
            if (len(blackSpots) > len(whiteSpots)):
                return -100000 * (len(blackSpots) / totaltokens)
            else:
                return 100000 * (len(whiteSpots) / totaltokens)
    if depth == 0:
        return weighted_score(player, board, opponent)
    possible = possible_moves(board, player)
    minValue = beta
    for i in possible:
        new_board = move(board, player, i)
        z = maxx_alphabeta(opponent, new_board, depth - 1, player, alpha, beta)
        if beta < z:
            beta = z
        if z < minValue:
            minValue = z
        if beta <= alpha:
            return minValue
    return minValue


def unusedmaxx_alphabeta(player, board, depth, opponent, alpha, beta):
    if depth == 0:
        return weighted_score(player, board, opponent)
    possible = possible_moves(board, player)
    maxValue = alpha
    for i in possible:
        new_board = move(board, player, i)
        z = mini_alphabeta(opponent, new_board, depth - 1, player, alpha, beta)
        if z > alpha:
            alpha = z
        if beta <= alpha:
            return z
        if maxValue < z:
            maxValue = z
            position = i
    return maxValue


def unusedmini_alphabeta(player, board, depth, opponent, alpha, beta):
    if depth == 0:
        return weighted_score(player, board, opponent)
    possible = possible_moves(board, player)
    minValue = beta
    for i in possible:
        new_board = move(board, player, i)
        z = maxx_alphabeta(opponent, new_board, depth - 1, player, alpha, beta)
        if beta > z:
            beta = z
        if beta <= alpha:
            return z
        if z < minValue:
            minValue = z
            position = i
    return minValue


def best_strat(board, player):
    if player == "@":
        opponent = "o"
    else:
        opponent = "@"
    value = main_minimax(player, board, 5)
    return value


#
# print(possible_moves(start_board,black_token))
# o = main_minimax(start_board,black_token,5)
# print(o)
# y = best_strat(start_board,black_token)
# print(y)
# z = move(start_board,black_token,56)
# print_puzzle(10,z)
# x = weighted_score(black_token,z,white_token)
# print(x)

import random
import time


#


class Strategy():
    # implement all the required methods on your own
    def best_strategy(self, board, player, best_move, running):
        if player == "@":
            opponent = "o"
        else:
            opponent = "@"
        gplayer = opponent
        gopponent = player
        for depth in range(3, 100):
            updatelist(board)
            best_move.value = main_minimax2(gplayer, gopponent, board, player, depth)
        # best_move.value = random.choice(self.legal_moves(board, player))

# print_puzzle(10,"???????????........??........??...@....??...@@...??...@o...??........??........??........???????????" )
# print(possible_moves("???????????........??........??...@....??...@@...??...@o...??........??........??........???????????","o"))
# new_board = move("???????????........??........??........??...o@...??...@o...??........??........??........???????????","@",34)
# print_puzzle(10,new_board)
# print_puzzle(10,(move("???????????........??..@@@...??....o...??..@@@o..??.ooo@oo.??..o.@.o.??........??........???????????",white_token,34)))
# replay = game(start_board, black_token)
