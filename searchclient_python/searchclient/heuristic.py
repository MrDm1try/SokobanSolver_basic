from abc import ABCMeta, abstractmethod
from collections import deque
from state import State

heuristic = 0


class Heuristic(metaclass=ABCMeta):
    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level.
        ngoals = 0
        global heuristic
        super().__init__()
        self.goals = deque()
        for i in range(initial_state.MAX_ROW):
            for j in range(initial_state.MAX_COL):
                if initial_state.goals[i][j] is not None:
                    ngoals += 1
                    self.goals.append((i, j))

        if ngoals > 1:
            heuristic = 1

        else:
            heuristic = 0

    def h(self, state: 'State') -> 'int':
        if heuristic == 1:
            return self.h_goals(state)

        return self.h_distance_boxes(state)

    def h_goals(self, state: 'State') -> 'int':
        boxes_todo = 0
        for row in range(state.MAX_ROW):
            for col in range(state.MAX_COL):
                if state.boxes[row][col] and state.boxes[row][col].lower() != state.goals[row][col]:
                    boxes_todo += 1
        return boxes_todo


    def h_distance_agent(self, state: 'State') -> 'int':
        goals = self.goals.copy()
        price = 0
        for i in range(len(goals)):
            goal = goals.pop()
            price = price + abs(goal[0] - state.agent_row) + abs(goal[1] - state.agent_col)
            goals.append((goal[0], goal[1]))
        return price

    def h_distance_boxes(self, state: 'State') -> 'int':
        goals = self.goals.copy()
        price = 0
        for _ in range(len(goals)):
            goal = goals.popleft()
            for row in range(state.MAX_ROW):
                for col in range(state.MAX_COL):
                    if state.boxes[row][col] and state.boxes[row][col].lower() == state.goals[goal[0]][goal[1]]:
                        price = price + abs(row - goal[0]) + abs(col - goal[1])
        return price

    @abstractmethod
    def f(self, state: 'State') -> 'int':
        pass

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError


class AStar(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def f(self, state: 'State') -> 'int':
        return state.g + self.h_distance_boxes(state)


    def __repr__(self):
        return 'A* evaluation'


class WAStar(Heuristic):
    def __init__(self, initial_state: 'State', w: 'int'):
        super().__init__(initial_state)
        self.w = w

    def f(self, state: 'State') -> 'int':
        return state.g + self.w * self.h_distance_boxes(state)

    def __repr__(self):
        return 'WA* ({}) evaluation'.format(self.w)


class Greedy(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def f(self, state: 'State') -> 'int':
        return self.h_distance(state)


    def __repr__(self):
        return 'Greedy evaluation'
