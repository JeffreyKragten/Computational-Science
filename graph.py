import sys
import numpy as np
import matplotlib.pyplot as plt

def create_graph(args=[]):
    category = args[1] if len(args) > 1 else "percentage_signers"
    savefile = "{}/results/{}".format(sys.path[0], "results", args[2]) if len(args) > 2 else None
    filename = "{}/results/results.csv".format(sys.path[0])

    with open(filename) as f:
        categories = f.readline().rstrip().split(",")
    data = np.loadtxt(filename, skiprows=1, delimiter=",")

    steps = int(max(data[:,categories.index("Step")])) + 1
    category_data = data[:,categories.index(category)].reshape((-1, steps))

    plt.plot(np.median(category_data, axis=0))
    plt.fill_between(np.arange(steps),
                    *np.percentile(category_data, [25, 75], axis=0), alpha=.2)

    if savefile:
        plt.savefig(savefile)
    else:
        plt.show()

if __name__ == "__main__":
    create_graph(sys.argv)
