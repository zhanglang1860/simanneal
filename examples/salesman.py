from __future__ import print_function
import math
import random
from simanneal import Annealer
import numpy as np
import matplotlib.pyplot as plt


def distance(a, b):
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    return math.acos(math.sin(lat1) * math.sin(lat2) +
                     math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * R


class TravellingSalesmanProblem(Annealer):
    """Test annealer with a travelling salesman problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, distance_matrix):
        self.distance_matrix = distance_matrix
        super(TravellingSalesmanProblem, self).__init__(state)  # important!

    def move(self):
        """Swaps two cities in the route."""
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i - 1]][self.state[i]]
        return e


if __name__ == '__main__':

    # latitude and longitude for the twenty largest U.S. cities
    cities = {
        'New York City': (40.72, 74.00),
        'Los Angeles': (34.05, 118.25),
        'Chicago': (41.88, 87.63),
        'Houston': (29.77, 95.38),
        'Phoenix': (33.45, 112.07),
        'Philadelphia': (39.95, 75.17),
        'San Antonio': (29.53, 98.47),
        'Dallas': (32.78, 96.80),
        'San Diego': (32.78, 117.15),
        'San Jose': (37.30, 121.87),
        'Detroit': (42.33, 83.05),
        'San Francisco': (37.78, 122.42),
        'Jacksonville': (30.32, 81.70),
        'Indianapolis': (39.78, 86.15),
        'Austin': (30.27, 97.77),
        'Columbus': (39.98, 82.98),
        'Fort Worth': (32.75, 97.33),
        'Charlotte': (35.23, 80.85),
        'Memphis': (35.12, 89.97),
        'Baltimore': (39.28, 76.62)
    }

    # initial state, a randomly-ordered itinerary
    init_state = list(cities.keys())
    random.shuffle(init_state)

    # create a distance matrix
    distance_matrix = {}
    for ka, va in cities.items():
        distance_matrix[ka] = {}
        for kb, vb in cities.items():
            if kb == ka:
                distance_matrix[ka][kb] = 0.0
            else:
                distance_matrix[ka][kb] = distance(va, vb)
    # print("sssssss")
    # print(distance_matrix['New York City']['Los Angeles'])  # 2448.8548064148363

    tsp = TravellingSalesmanProblem(init_state, distance_matrix)

    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    tsp.steps=10000
    # auto_schedule = tsp.auto(minutes=3, steps=5000)
    # tsp.set_schedule(auto_schedule)
    #
    # assert tsp.Tmax == auto_schedule['tmax']
    # assert tsp.Tmin == auto_schedule['tmin']
    # assert tsp.steps == auto_schedule['steps']
    # assert tsp.updates == auto_schedule['updates']

    state, e, t_list, e_list, step_list = tsp.anneal()



    while state[0] != 'New York City':
        state = state[1:] + state[:1]  # rotate NYC to start

    print()
    print("%i mile route:" % e)
    for city in state:
        print("\t", city)

    dt = 0.01
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(step_list, t_list, step_list, e_list)
    axs[0].set_xlim(0, 10000)
    axs[0].set_xlabel('step_list')
    axs[0].set_ylabel('T and E')
    axs[0].grid(True)

    cxy, f = axs[1].cohere(t_list, e_list, 256, 1. / dt)
    axs[1].set_ylabel('coherence')

    fig.tight_layout()
    plt.show()


# t = np.arange(0, 30, dt)
# nse1 = np.random.randn(len(t))                 # white noise 1
# nse2 = np.random.randn(len(t))                 # white noise 2
#
# # Two signals with a coherent part at 10Hz and a random part
# s1 = np.sin(2 * np.pi * 10 * t) + nse1
# s2 = np.sin(2 * np.pi * 10 * t) + nse2

