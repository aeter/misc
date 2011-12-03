'''
A prototype of simulated annealing.

Copyright 2011 Adrian Nackov
Released under BSD Licence (3 clause):
http://www.opensource.org/licenses/bsd-license.php
'''

import math
import random


TEMPERATURE = 20000.0
COOLING_RATE = 0.9


class Optimization(object):

    @classmethod
    def anneal(cls, toy_problem,
               temperature=TEMPERATURE, cooling_rate=COOLING_RATE):
        '''
        Implements simulated annealing. Returns some optimized solution.
        '''
        solution = toy_problem.example_solution()
        while temperature > 0.1:
            _next = toy_problem.modify(solution)
            delta = toy_problem.cost(_next) - toy_problem.cost(solution)
            if delta < 0:
                solution = _next
            # accept a worse solution with some probability dependent
            # on the temperature:
            elif math.exp(-delta/temperature) > random.random():
                solution = _next
            temperature *= cooling_rate
        return solution, toy_problem.cost(solution)


class BaseToyProblem(object):
    '''
    A base class representing optimization problems
    '''

    def example_solution(self):
        raise NotImplemented

    def cost(self, solution):
        '''
        The cost function of a given solution
        '''
        raise NotImplemented

    def modify(self, solution):
        '''
        A function describing how the next optimization solution
        should be constructed from the current one.
        '''
        raise NotImplemented

class TravellingSalesman(BaseToyProblem):

    CITIES = {
        "Sofia" : {
            "Bucharest" : 100,
            "Dresden" : 500,
            "Paris" : 1000,
            "Istanbul" : 200,
        },
        "Bucharest" : {
            "Sofia" : 150,
            "Dresden" : 300,
            "Paris" : 800,
            "Istanbul" : 400,
        },
        "Dresden" : {
            "Paris" : 300,
            "Sofia" : 600,
            "Bucharest" : 400,
            "Istanbul" : 600,
        },
        "Paris" : {
            "Dresden" : 350,
            "Sofia" : 950,
            "Bucharest" : 750,
            "Istanbul" : 800,
        },
        "Istanbul" : {
            "Dresden": 600,
            "Sofia" : 200,
            "Bucharest": 400,
            "Paris" : 800,
        },
    }

    def __init__(self, data):
        '''
        Input:
            data has format like TravellingSalesman.CITIES is a list of items
        '''
        self._data = data
        self._example_solution = data.keys()

    def example_solution(self):
        return self._example_solution

    def cost(self, solution):
        """
        Calculates the overall distance starting from the first element and
        proceeding towards the last.
        Input:
            solution is a list of items, such as ["a", "b", "c", "d"]
        """
        cities = self._data
        cities_by_two = zip(solution, solution[1:])
        distances = [cities[first][second] for first, second in cities_by_two]
        return sum(distances)

    def modify(self, solution):
        '''
        Swap the places of 2 data items
        '''
        result = solution[:]
        i1, i2 = [result.index(_) for _ in random.sample(result, 2)]
        result[i1], result[i2] = result[i2], result[i1]
        return result

if __name__ == '__main__':
    t = TravellingSalesman(TravellingSalesman.CITIES)
    print Optimization.anneal(t)

