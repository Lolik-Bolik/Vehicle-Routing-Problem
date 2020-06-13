import sys
sys.path.append('../')
from tools.dataloader import getData
from .graph import Graph
from .ant import Ant


class Solver:
    def __init__(self):
        self.routes = []
        self.cost = 0

    @staticmethod
    def get_route_cost(route, graph):
        total_cost = 0

        for i in range(0, len(route) - 1):
            total_cost += round(graph.adjacency_map[route[i]][route[i + 1]], 5)
        return total_cost

    def get_route_cost_opt(self, route, graph):
        depot_costs = round(graph.adjacency_map[1][route[0]], 5) + round(graph.adjacency_map[route[-1]][1], 5)

        return depot_costs + self.get_route_cost(route, graph)

    @staticmethod
    def two_opt(route, i, j):
        return route[:i] + route[i:j + 1][::-1] + route[j + 1:]

    def get_better_two_opt_swap(self, route, graph):
        num_eligible_nodes_to_swap = len(route)
        route_cost = self.get_route_cost_opt(route, graph)
        for i in range(0, num_eligible_nodes_to_swap - 1):
            for k in range(i + 1, num_eligible_nodes_to_swap):
                new_route = self.two_opt(route, i, k)
                new_cost = self.get_route_cost_opt(new_route, graph)
                if new_cost < route_cost:
                    return new_route
        return None

    def get_optimal_route_intraswap(self, route, graph):
        best_route = route

        while True:
            improved_route = self.get_better_two_opt_swap(best_route, graph)
            if improved_route:
                best_route = improved_route
            else:
                break
        return best_route

    def apply_two_opt(self, initial_solution, graph):
        best_routes = [
            [1] + self.get_optimal_route_intraswap(route[1:-1], graph) + [1]
            for route in initial_solution[0]
        ]
        return best_routes, sum([self.get_route_cost(route, graph) for route in best_routes])

    def __call__(self, cfg, verbose=True):
        capacity, graph_data, demand, optimal_value, name, n_trucks = getData(cfg.FILE_NAME)
        graph = Graph(graph_data, demand, cfg)
        ants = [Ant(graph, capacity, cfg) for _ in range(0, n_trucks)]

        best_solution = None

        tolerance = 0
        for i in range(1, cfg.NUM_ITERATIONS + 1):
            for ant in ants:
                ant.reset_state()
            solutions = []
            for ant in ants:
                solutions.append(ant.find_solution())

            candidate_best_solution = min(solutions, key=lambda solution: solution[1])
            if cfg.USE_2_OPT_STRATEGY:
                candidate_best_solution = self.apply_two_opt(candidate_best_solution, graph)

            if not best_solution or candidate_best_solution[1] < best_solution[1]:
                best_solution = candidate_best_solution
                tolerance = 0
            else:
                tolerance += 1

            if verbose and i % 100 == 0:
                print("Best solution in iteration {}/{} = {}".format(i, cfg.NUM_ITERATIONS, best_solution[1]))
            if tolerance >= int(0.3 * cfg.NUM_ITERATIONS):
                if verbose:
                    print("---")
                    print("Final best solution:")
                    print(best_solution[1])
                    print(best_solution[0])
                    print("Optimal solution: ")
                    print(optimal_value)
                return best_solution, optimal_value, name, n_trucks, capacity
            graph.update_pheromone_map(solutions)
        if verbose:
            print("---")
            print("Final best solution:")
            print(best_solution[1])
            print(best_solution[0])
            print("Optimal solution: ")
            print(optimal_value)
        return best_solution, optimal_value, name, n_trucks, capacity