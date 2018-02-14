
import random

# this is a function to solve a 'problem' by fulfilling a 'solution'
# within a certain number of iterations by
def find_random_plan(start, problem, solution, iterations):
    random_plan = []
    situation_sequence = []
    solved = False

    current_situation = start

    for p in xrange(1, iterations):
        options = problem.get(current_situation).keys()
        random_choice = random.choice(options)
        if current_situation == solution:
            situation_sequence.append(current_situation)
            solved = True
            break
        if random_choice in problem[current_situation].keys():
            random_plan.append(random_choice)
            situation_sequence.append(current_situation)
            current_situation = problem[current_situation][random_choice]

    return random_plan, situation_sequence, solved


def find_best_plan(subject, problem, solution):

    iterations = subject["intelligence"] * 10

    current_solved_plan = []
    current_solved_situation_sequence = []
    best_plan = []
    best_situation_sequence = []
    problem_solved = False

    for i in xrange(1, iterations):

        random_plan, situation_sequence, solved = find_random_plan(start, problem, solution, iterations)

        if solved:
            current_solved_plan = random_plan
            current_solved_situation_sequence = situation_sequence
            maze_solved = True

        if len(best_plan) == 0 and solved:
            best_plan = current_solved_plan
            best_situation_sequence = current_solved_situation_sequence

        if len(current_solved_plan) < len(best_plan) and len(best_plan) != 0 and solved:
            best_plan = current_solved_plan
            best_situation_sequence = current_solved_situation_sequence

    return best_plan, best_situation_sequence, problem_solved

################ start maze_1 problem
maze = {"start of maze": {"W": "room A"},
        "room A": {"N": "room B", "E": "start of maze"},
        "room B": {"W": "room I", "E": "room C"},
        "room C": {"W": "room B", "N": "room D"},
        "room D": {"S": "room C", "N": "end of maze"},
        "room I": {"N": "room J", "E": "room B"},
        "room J": {"S": "room I"},
        "end of maze": {"S": "room D"}
        }

    #   Maze layout:
    #
    #           end
    #           |
    #   J       D
    #   |       |
    #   I---B---C
    #       |
    #       A---start
    #
    # most direct solution: [W, N, E, N, N]

start = "start of maze"
problem = maze
solution = "end of maze"
################ end maze_1 problem

mouse = {"intelligence": 20, "plan memory": {}, "plan certainty": {}}
subject = mouse

best_plan, best_situation_sequence, problem_solved = find_best_plan(subject, problem, solution)

print "The best plan for maze_1 was:", best_plan
print "It involved this sequence:", best_situation_sequence
print "Was the problem solved?", problem_solved

################ start maze_2 problem
maze = {"start of maze": {"W": "room A"},
        "room A": {"N": "room B", "E": "start of maze"},
        "room B": {"W": "room I", "E": "room C"},
        "room C": {"W": "room B", "N": "room D", "E": "room K"},
        "room D": {"S": "room C", "E": "room L"},
        "room I": {"N": "room J", "E": "room B"},
        "room J": {"S": "room I"},
        "room K": {"W": "room C", "N": "room L"},
        "room L": {"N": "end of maze", "S": "room K", "W": "room D"},
        "end of maze": {"S": "room D"}
        }

    #   Maze layout:
    #
    #               end
    #               |
    #   J       D---L
    #   |       |   |
    #   I---B---C---K
    #       |
    #       A---start
    #
    # most direct solutions: [W, N, E, E, N, N]
    #                        [W, N, E, N, E, N]

start = "start of maze"
problem = maze
solution = "end of maze"
################ end maze_2 problem

best_plan, best_situation_sequence, problem_solved = find_best_plan(subject, problem, solution)

print "The best plan for maze_2 was:", best_plan
print "It involved this sequence:", best_situation_sequence
print "Was the problem solved?", problem_solved
