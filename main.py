from tqdm import tqdm
import csv
import glob
import os
from tools.config import Config
from algorithm.ant_colony import Solver

from time import time


if __name__ == '__main__':
    make_csv = True
    config = Config()
    files = glob.glob('./data/*/*.vrp')
    for file in tqdm(files):
        if make_csv:
            statistic = open('statistic.csv', 'w')
            columns_names = ['File name', 'Number of Locations', 'Number of trucks', 'Capacity', 'Optimal', 'Achieved', '2-opt', 'Routes', 'Work time']
            writer = csv.DictWriter(statistic, fieldnames=columns_names)
            writer.writeheader()
        config.FILE_NAME = file
        tic = time()
        ant_colony = Solver()
        best_solution, optimal_value, name, n_trucks, capacity = ant_colony(config, verbose=False)
        n_locations = int(name.split('-')[1][1:])
        if make_csv:
            writer.writerow({'File name': name,
                             'Number of Locations': n_locations,
                             'Number of trucks': n_trucks,
                             'Capacity': capacity,
                             'Optimal': optimal_value,
                             'Achieved': round(best_solution[1], 3),
                             '2-opt': config.USE_2_OPT_STRATEGY,
                             'Routes': best_solution[0],
                             'Work time': round(time() - tic, 3)})
        os.makedirs('solutions', exist_ok=True)
        with open(f'solutions/{name}.sol', 'w') as sol_fp:
            for i, route in enumerate(best_solution[0], 1):
                sol_fp.write(f'Route #{i}: {route}\n')
            sol_fp.write(f'cost: {round(best_solution[1], 3)}\n')
    if make_csv:
        statistic.close()


