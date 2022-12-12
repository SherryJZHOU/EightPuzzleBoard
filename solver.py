import puzz
import pdqpq
import sys
import random
import matplotlib
from matplotlib import pyplot as plt
import queue

def BFS(start, goal):
    if start == goal:
        return [[('start', start)], 1, 0]
    frontier = queue.Queue()
    frontier.put((start, [("start", start)], 0))
    fron = {start}
    explored = set()
    cnt = 0

    while not frontier.empty():
        node, way, cost = frontier.get()
        explored.add(node)
        cnt += 1
        if cnt > 100000:
            return [[], -1, -2, -1]
        for dir, status in node.successors().items():
            board = puzz.EightPuzzleBoard(node.__str__())
            if status is None:
                continue
            if status == goal:
                x, y = board.find('0')
                if dir == "up":
                    num = board._get_tile(x, y - 1)
                elif dir == "down":
                    num = board._get_tile(x, y + 1)
                elif dir == "left":
                    num = board._get_tile(x + 1, y)
                elif dir == "right":
                    num = board._get_tile(x - 1, y)
                return [way + [(dir, status)], len(fron), len(explored), cost+int(num) ** 2]
            if status not in fron and status not in explored:
                x, y = board.find('0')
                if dir == "up":
                    num = board._get_tile(x, y - 1)
                elif dir == "down":
                    num = board._get_tile(x, y + 1)
                elif dir == "left":
                    num = board._get_tile(x + 1, y)
                elif dir == "right":
                    num = board._get_tile(x - 1, y)
                fron.add(status)
                frontier.put((status, way + [(dir,status)], cost+int(num) ** 2))
    return [[], -1, -1, -1]

def calH(node):
    way = puzz.EightPuzzleBoard("123456780")
    cnt = 0
    for i in range(1,9):
        x1, y1 = way.find(str(i))
        x2, y2 = node.find(str(i))
        cnt += (abs(x1-x2) + abs(y1-y2)) * (i**2)
    return cnt

def print_result(path, explored, frontier, path_cost):
    for i in range(0, len(path)):
        print(i, "\t", path[len(path) - 1 - i].dir, "\t", path[len(path) - 1 - i])
    print("path cost:", path_cost)
    print("frontier:", frontier.__len__() + len(explored))
    print("expanded:", len(explored))

def astar(start, goal, type):
    sol = puzz.EightPuzzleBoard("123456780")
    game = puzz.EightPuzzleBoard(start)
    uCost = False
    greedy = False
    aStar = False
    game._set_dir("start")
    game.heuristic = calH(game)
    frontier = pdqpq.PriorityQueue()
    explored = set()
    fron = []
    path_cost = 0
    frontier.add(game)
    if start == sol.__str__():
        fron.append(game)
        print_result(fron, explored, frontier, path_cost)
        exit(1)
    halt = False
    is_BFS = False
    if type == "ucost":
        uCost = True
    elif type == "greedy":
        greedy = True
    elif type == "astar":
        aStar = True
    ready_print = False

    while not frontier.empty():
        if len(explored) == 100000:
            halt = True
            print("search halted")
            break

        temp = frontier.pop()
        if temp == sol:
            break

        explored.add(temp)
        succ = temp.successors()
        for key, value in succ.items():
            if value is not None and value not in explored:
                value._set_par(temp)
                value._set_dir(key)
                c = temp.find("0")
                if uCost:
                    if goal:
                        value.cost = 1 + temp.cost
                    else:
                        value.cost = temp.cost + int(value._get_tile(c[0], c[1])) ** 2
                elif greedy:
                    if goal:
                        value.path = 1
                        value.heuristic = calH(value)
                    else:
                        value.heuristic = calH(value)
                elif aStar:
                    if goal:
                        value.cost  = 1
                    else:
                        value.cost  = temp.cost  + int(value._get_tile(c[0], c[1])) ** 2
                    value.heuristic = calH(value) + value.cost

                if uCost:
                    frontier.add(value, value.cost)
                else:
                    frontier.add(value, value.heuristic)

    if not halt:
        if frontier.empty():
            print("no solution")
            return [path_cost, frontier.__len__() + len(explored), len(explored), temp, fron, explored, frontier,
                    ready_print]
        else:
            while temp.prev is not None:
                c = temp.find("0")
                fron.append(temp)
                temp = temp.prev
                if not noweight:
                    path_cost += int(temp._get_tile(c[0], c[1])) ** 2
                else:
                    path_cost += 1

            fron.append(temp)
            print_result(fron, explored, frontier, path_cost)

def test():
    case = []
    explored = set()
    ok = False
    for i in range (0, 20):
        sol = puzz.EightPuzzleBoard("123456780")
        explored.add(sol)
        for j in range(15):
            ran = random.randint(1, 4)
            while not ok:
                if ran == 1 and sol.success_up() is not None and sol.success_up() not in explored:
                    sol = sol.success_up()
                    explored.add(sol)
                    ok = True
                elif ran == 2 and sol.success_left() is not None and sol.success_left() not in explored:
                    sol = sol.success_left()
                    explored.add(sol)
                    ok = True
                elif ran == 3 and sol.success_right() is not None and sol.success_right() not in explored:
                    sol = sol.success_right()
                    explored.add(sol)
                    ok = True
                elif ran == 4 and sol.success_down() is not None and sol.success_down() not in explored:
                    sol = sol.success_down()
                    explored.add(sol)
                    ok = True
                else:
                    ran = random.randint(1,4)

            ok = False

        case.append(sol.__str__())
        explored.clear()
        ok = True

    return case

def Main():
    startState = puzz.EightPuzzleBoard("312450867")
    goalState = puzz.EightPuzzleBoard("012345678")
    rst = BFS(startState, goalState)
    for i in range(len(rst[0])):
        print("%i \t %s \t %s" % (i,rst[0][i][0],rst[0][i][1]))

    print()
    print("path cost:", rst[3])
    print("frontier:", rst[1])
    print("expanded:", rst[2])

Main()
