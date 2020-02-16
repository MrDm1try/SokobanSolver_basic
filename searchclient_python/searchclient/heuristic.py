from abc import ABCMeta, abstractmethod


class Heuristic(metaclass=ABCMeta):
    def __init__(self, initial_state: 'State'):
        # Here's a chance to pre-process the static parts of the level.
        pass

    def h(self, state: 'State') -> 'int':
        return self._boxes_not_in_places_h(state)

    def _boxes_not_in_places_h(self, state: 'State') -> 'int':
        boxes_todo = 0
        for row in range(state.MAX_ROW):
            for col in range(state.MAX_COL):
                if state.boxes[row][col] and state.boxes[row][col].lower() != state.goals[row][col]:
                    boxes_todo += 1
        return boxes_todo

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
        return state.g + self.h(state)

    def __repr__(self):
        return 'A* evaluation'


class WAStar(Heuristic):
    def __init__(self, initial_state: 'State', w: 'int'):
        super().__init__(initial_state)
        self.w = w

    def f(self, state: 'State') -> 'int':
        return state.g + self.w * self.h(state)

    def __repr__(self):
        return 'WA* ({}) evaluation'.format(self.w)


class Greedy(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def f(self, state: 'State') -> 'int':
        return self.h(state)

    def __repr__(self):
        return 'Greedy evaluation'
