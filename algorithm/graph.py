from collections import defaultdict
import numpy as np


class Graph:
    def __init__(self, graph_data, demand, config):
        self.cfg = config
        self.adjacency_map = self.create_adjacency_map(graph_data)
        self.pheromone_map = self.create_pheromone_map(graph_data.keys())

        self.demand_map = demand

    @staticmethod
    def create_adjacency_map(graph_data):
        adjacency_map = defaultdict(dict)

        nodes = list(graph_data.keys())
        for i, node_1 in enumerate(nodes):
            for node_2 in nodes[i + 1:]:
                distance = np.linalg.norm(np.asarray(graph_data[node_1]) - np.asarray(graph_data[node_2]))
                adjacency_map[node_1][node_2] = distance
                adjacency_map[node_2][node_1] = distance
        return adjacency_map

    @staticmethod
    def create_pheromone_map(nodes):
        pheromone_map = defaultdict(dict)
        nodes = list(sorted(nodes))
        for i, node_1 in enumerate(nodes):
            for node_2 in nodes[i + 1:]:
                pheromone_map[node_1][node_2] = 1
                pheromone_map[node_2][node_1] = 1
        return pheromone_map

    def global_update_pheromone_map(self, ant_solution, capacity):
        nodes = list(sorted(self.pheromone_map.keys()))
        for i, node_1 in enumerate(nodes):
            for node_2 in nodes[i + 1:]:
                new_value = max((1 - self.cfg.RHO) * self.pheromone_map[node_1][node_2], 1e-10)
                self.pheromone_map[node_1][node_2] = new_value
                self.pheromone_map[node_2][node_1] = new_value

        pheromone_increase = capacity / ant_solution[1]
        for route in ant_solution[0]:
            edges = [(route[index], route[index + 1]) for index in range(0, len(route) - 1)]
            for edge in edges:
                self.pheromone_map[edge[0]][edge[1]] += pheromone_increase
                self.pheromone_map[edge[1]][edge[0]] += pheromone_increase

    def update_pheromone_map(self, ant_solution):
        nodes = list(sorted(self.pheromone_map.keys()))
        for i, node_1 in enumerate(nodes):
            for node_2 in nodes[i + 1:]:
                new_value = max((1 - self.cfg.RHO) * self.pheromone_map[node_1][node_2], 1e-10)
                self.pheromone_map[node_1][node_2] = new_value
                self.pheromone_map[node_2][node_1] = new_value

        for route in ant_solution[0]:
            edges = [(route[index], route[index + 1]) for index in range(0, len(route) - 1)]
            for edge in edges:
                pheromone_increase = 1 / (float(self.adjacency_map[edge[0]][edge[1]]) + 1e-6)
                self.pheromone_map[edge[0]][edge[1]] += pheromone_increase
                self.pheromone_map[edge[1]][edge[0]] += pheromone_increase




