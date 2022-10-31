from simpleai.search import astar, SearchProblem
"""
Mateusz Miekicki s20691
Oskar Przydatek s19388
You are given a 3x3 board with numbers from 1-8 and 
one empty cell in a random position and 
you are to arrange them in ascending order starting from the top left.
We will use an A* algorithm to solve this problem.
It is an algorithm that's used to find paths to the solution in a graph.
This algorithm is a combination of Dijkstra's algorithm and a greedy best-first search.
Instead of blindly guessing where to go next,
the A* algorithm picks the one that looks the most promising.
At each node, we generate the list of all possibilities and
then pick the one with the minimal cost required to reach the goal.
"""


class PuzzleSolver(SearchProblem):
    def actions(self, cur_state):
        """Override the actions method to align it with our problem.
        Action method to get the list of the possible numbers that can be moved in to the empty space 
        Parameters:
        cur_state (string): current board arrangement
        Returns:
        list: possible transfers to empty spots
        """
        rows = string_to_list(cur_state)
        row_empty, col_empty = get_location(rows, 'e')

        actions = []
        if row_empty > 0:
            actions.append(rows[row_empty - 1][col_empty])
        if row_empty < 2:
            actions.append(rows[row_empty + 1][col_empty])
        if col_empty > 0:
            actions.append(rows[row_empty][col_empty - 1])
        if col_empty < 2:
            actions.append(rows[row_empty][col_empty + 1])
        return actions

    def result(self, state, action):
        """Override the result method. 
        Convert the string to a list and extract the location of the empty space. 
        Generate the result by updating the locations.
        Parameters:
        state (string): current board arrangement
        action (string): possibilities
        Returns:
        string: return resulting state after moving a piece to the empty space
        """
        rows = string_to_list(state)
        row_empty, col_empty = get_location(rows, 'e')
        row_new, col_new = get_location(rows, action)

        rows[row_empty][col_empty], rows[row_new][col_new] = \
            rows[row_new][col_new], rows[row_empty][col_empty]

        return list_to_string(rows)

    def is_goal(self, state):
        """
        Parameters:
        state (string): current board arrangement
        Returns:
        string: Return the resulting state after moving a piece to the empty space
        """
        return state == GOAL

    def heuristic(self, state):
        """Returns an estimate of the distance from a state to the goal using the manhattan distance 
        Parameters:
        state (string): current board arrangement
        Returns:
        int: distance
        """
        rows = string_to_list(state)

        distance = 0

        for number in '12345678e':
            row_new, col_new = get_location(rows, number)
            row_new_goal, col_new_goal = goal_positions[number]

            distance += abs(row_new - row_new_goal) + \
                abs(col_new - col_new_goal)

        return distance


def list_to_string(input_list):
    return '\n'.join(['-'.join(x) for x in input_list])


def string_to_list(input_string):
    return [x.split('-') for x in input_string.split('\n')]


def get_location(rows, input_element):
    """Find the 2D location of the input element
    input_element (string): element
    Returns:
    int: coordinate
    """
    for i, row in enumerate(rows):
        for j, item in enumerate(row):
            if item == input_element:
                return i, j


GOAL = '''1-2-3
4-5-6
7-8-e'''

INITIAL = '''e-8-7
6-5-4
3-2-1'''

goal_positions = {}
rows_goal = string_to_list(GOAL)
for number in '12345678e':
    goal_positions[number] = get_location(rows_goal, number)

result = astar(PuzzleSolver(INITIAL))

for i, (action, state) in enumerate(result.path()):
    print()
    if action == None:
        print('Initial configuration')
    elif i == len(result.path()) - 1:
        print('After moving', action, 'into the empty space. Goal achieved!')
    else:
        print('After moving', action, 'into the empty space')

    print(state)