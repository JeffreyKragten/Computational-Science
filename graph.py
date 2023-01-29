"""
$ python graph.py
$ python graph.py [category]
$ python graph.py [category] [loadfile]
$ python graph.py [category] [loadfile] [*values]
$ python graph.py [category] [loadfile] [savefile] [*values]

- category:
    The kind of data that is represented. Categories to choose from:
        n, m, d, c, agent_count, percentage_signers, percentage_fluent_signers,
        percentage_non_fluent_signers, percentage_deaf, percentage_carry

- loadfile:
    File in from which the data is loaded to represent.
    use * to replace with different values given in the values arguments.

- savefile:
    File to store the image of the graph in. If this argument is not given the
    graph is shown.

- values:
    All the arguments after the loadfile or savefile. This values are placed on
    the position of the * in the loadfile to give differents lines for the
    different files in the same graph.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def create_graph(args=[], parameters={}):
    category = args[0] if len(args) > 0 else "percentage_non_fluent_signers"
    # category_signers = "percentage_signers"

    # Check if there is a results directory.
    results_path = f"{sys.path[0]}/results/"
    if not os.path.exists(results_path):
        print("No results directory")
        return

    # Create path for files to read data from.
    loadfile = args[1] if len(args) > 1 else "results"

    # Create the path for the savefile and get remaining arguments.
    if len(args) > 2 and not args[2].replace(".", "", 1).isdigit():
        savefile = f"{results_path}{args[2]}"
        vals = args[3:]
    else:
        savefile = None
        vals = args[2:]

    if "*" not in loadfile:
        vals = [""]

    if not vals:
        print("No values given")
        return

    for val in vals:
        # Read the data from the results file.
        path = f"{results_path}{loadfile.replace('*', val, 1)}.csv"
        try:
            with open(path) as f:
                categories = f.readline().rstrip().split(",")
            data = np.loadtxt(path, skiprows=1, delimiter=",")
        except:
            print(f"File {path.split('/')[-1]} does not exist")
            continue

        # Get the nummer of steps the model ran.
        steps = int(max(data[:,categories.index("Step")])) + 1

        # Get the data in the category and reshape to get the different runs.
        try:
            category_index = categories.index(category)
        except:
            print(f"Category {category} not in file {path.split('/')[-1]}")
            continue
        category_data = data[:,category_index].reshape((-1, steps))

        # category_data_signers = data[:,categories.index(category_signers)].reshape((-1, steps))
        # final_percentage = np.median(category_data[:,-1]) * 100
        # final_percentage_signers = np.median(category_data_signers[:,-1]) * 100
        # ratio = final_percentage / final_percentage_signers
        # print(f"Final percentage {args[1]}: {'%.2f' % final_percentage}%. Ratio {args[1]}: {'%.2f' % ratio}.")

        quartiles = np.percentile(category_data, [25, 50, 75], axis=0)
        plt.plot(quartiles[1], label=val)
        plt.fill_between(np.arange(steps), quartiles[0], quartiles[2], alpha=.2)

    plt.legend(loc="upper left")

    n = int(data[:,categories.index("n")][0])
    m = data[:,categories.index("m")][0]
    d = data[:,categories.index("d")][0]
    c = data[:,categories.index("c")][0]

    plt.title(f"n: {n}, m: {m}, d: {d}, c: {c}")

    if savefile:
        plt.savefig(savefile)
    else:
        plt.show()

if __name__ == "__main__":
    create_graph(sys.argv[1:])
