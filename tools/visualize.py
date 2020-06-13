import matplotlib.pyplot as plt


def plot_problem(graph):
    plt.figure(figsize=(7, 7))
    for i, loc in graph.items():
        xoff = 0.5 if len(str(i)) == 1 else 0.85
        yoff = 0.6 if len(str(i)) == 1 else 0.7
        plt.annotate("{}".format(i),
                     (loc[0] - xoff, loc[1] - yoff),
                     size=9,
                     color='white')
    locations = list(graph.values())
    plt.plot(locations[0][0], locations[0][1], 'ro', label='storage', markersize=13)
    plt.plot([loc[0] for loc in locations[1:]],
             [loc[1] for loc in locations[1:]], 'bo',
             label='locations',
             markersize=12)

    plt.legend()
    plt.xticks([])
    plt.yticks([])
    plt.show()