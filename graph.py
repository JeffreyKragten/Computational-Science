import sys
import numpy as np
import matplotlib.pyplot as plt

def create_graph(args=[], parameters={}):
    # category = args[0] if len(args) > 0 else "percentage_non_fluent_signers"
    category = "percentage_non_fluent_signers"
    val = args[0] if len(args) > 0 else "0.58"

    savefile = "{}/results/{}".format(sys.path[0], args[1]) if len(args) > 1 else None
    filename = "{}/results/results_".format(sys.path[0]) + f"{val}.csv"

    with open(filename) as f:
        categories = f.readline().rstrip().split(",")
    data = np.loadtxt(filename, skiprows=1, delimiter=",")

    steps = int(max(data[:,categories.index("Step")])) + 1
    category_data = data[:,categories.index(category)].reshape((-1, steps))
    final_percentage = np.median(category_data[:,-1]) * 100

    plt.plot(np.median(category_data, axis=0))
    plt.fill_between(np.arange(steps),
                    *np.percentile(category_data, [25, 75], axis=0), alpha=.2)


    n = int(data[:,categories.index("n")][0])
    m = data[:,categories.index("m")][0]
    d = data[:,categories.index("d")][0]
    c = data[:,categories.index("c")][0]

    plt.title(f"Final percentage: {'%.2f' % final_percentage}%. n: {n}, m: {m}, d: {d}, c: {c}")

    if savefile:
        plt.savefig(savefile)
    else:
        plt.show()

if __name__ == "__main__":
    create_graph(sys.argv[1:])
