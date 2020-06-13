import numpy as np


class Ant:
    def __init__(self, graph, capacity, config):
        self.graph = graph
        self.ant_capacity = capacity
        self.cfg = config
        self.reset_state()

    def select_next_city(self, current_city):
        available_cities = [city for city in self.cities_left if self.capacity >= self.graph.demand_map[city]]

        if not available_cities:
            return None

        scores = [pow(self.graph.pheromone_map[current_city][city], self.cfg.ALPHA) *
                  pow(1 / (self.graph.adjacency_map[current_city][city] + 1e-10), self.cfg.BETA)
                  for city in available_cities]
        denominator = sum(scores)
        probabilities = [score / denominator for score in scores]

        next_city = np.random.choice(available_cities, p=probabilities)

        return next_city

    def move_to_city(self, current_city, next_city):
        self.routes[-1].append(next_city)
        if next_city != 1:
            self.cities_left.remove(next_city)
        self.capacity -= self.graph.demand_map[next_city]
        self.total_path_cost += self.graph.adjacency_map[current_city][next_city]

    def start_new_route(self):
        self.capacity = self.ant_capacity
        self.routes.append([1])

        first_city = np.random.choice([city for city in self.cities_left if self.capacity >= self.graph.demand_map[city]])
        self.move_to_city(1, first_city)

    def find_solution(self):
        self.start_new_route()

        while self.cities_left:
            current_city = self.routes[-1][-1]
            next_city = self.select_next_city(current_city)
            if next_city is None:
                self.move_to_city(current_city, 1)
                self.start_new_route()
            else:
                self.move_to_city(current_city, next_city)

        self.move_to_city(self.routes[-1][-1], 1)

        return self.routes, self.total_path_cost

    def reset_state(self):
        self.capacity = self.ant_capacity
        self.cities_left = set(self.graph.adjacency_map.keys())
        self.cities_left.remove(1)
        self.routes = []
        self.total_path_cost = 0