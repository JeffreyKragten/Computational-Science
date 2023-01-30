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
    Use [category1]/[category2] to get the ratio between the two categories.

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


def create_graph(category="percentage_non_fluent_signers",
                 category2=None,
                 end=False,
                 loadfile="results",
                 savefile=None,
                 values=[]):
    # category_signers = "percentage_signers"

    # Check if there is a results directory.
    results_path = f"{sys.path[0]}/results/"
    if not os.path.exists(results_path):
        print("No results directory")
        return

    if "*" not in loadfile:
        values = [""]

    if not values:
        print("No values given")
        return

    data = None
    for val in values:
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

        if category2 is None:
            quartiles = np.percentile(category_data, [25, 50, 75], axis=0)
            if end:
                plt.plot(val, quartiles[1,-1], marker="o", color="k")
                plt.vlines(val, quartiles[0,-1], quartiles[2,-1], "k")
            else:
                plt.plot(quartiles[1], label=val)
                plt.fill_between(np.arange(steps), quartiles[0], quartiles[2], alpha=.2)
        else:
            try:
                category2_index = categories.index(category2)
            except:
                print(f"Category {category2} not in file {path.split('/')[-1]}")
                continue
            category2_data = data[:,category2_index].reshape((-1, steps))
            plt.plot(np.median(category_data, axis=0) / np.median(category2_data, axis=0), label=val)


    plt.legend(loc="upper left")

    if data is None:
        return

    n = int(data[:,categories.index("n")][0])
    m = data[:,categories.index("m")][0]
    d = data[:,categories.index("d")][0]
    c = data[:,categories.index("c")][0]

    plt.title(f"n: {n}, m: {m}, d: {d}, c: {c}")

    if savefile:
        plt.savefig(f"{results_path}{savefile}")
    else:
        plt.show()


def __read_args__(args):
    if len(args) == 0:
        category = "percentage_non_fluent_signers"
        category2 = None
    elif "/" in args[0]:
        category, category2 = args[0].split("/", 1)
    else:
        category = args[0]
        category2 = None

    end = False
    if len(args) > 1 and args[1] in ["True", "False"]:
        end = args[1] == "True"
        args = args[1:]

    loadfile = args[1] if len(args) > 1 else "results"

    if len(args) > 2 and not args[2].replace(".", "", 1).isdigit():
        savefile = args[2]
        values = args[3:]
    else:
        savefile = None
        values = args[2:]

    return category, category2, end, loadfile, savefile, values


if __name__ == "__main__":
    create_graph(*__read_args__(sys.argv[1:]))
