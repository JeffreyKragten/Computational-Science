import sys
import numpy as np
import matplotlib.pyplot as plt

def create_graph(args=[], parameters={}):
    # category = args[0] if len(args) > 0 else "percentage_non_fluent_signers"
    category = "percentage_non_fluent_signers"
    category_signers = "percentage_signers"
    # val = args[1] if len(args) > 1 else "0.58"

    savefile = "{}/results/{}".format(sys.path[0], args[0]) if len(args) > 0 else None

    for arg in args[1:]:
        filename = "{}/results/results_d_".format(sys.path[0]) + f"{arg}.csv"
        with open(filename) as f:
            categories = f.readline().rstrip().split(",")
        data = np.loadtxt(filename, skiprows=1, delimiter=",")

        steps = int(max(data[:,categories.index("Step")])) + 1
        category_data = data[:,categories.index(category)].reshape((-1, steps))
        final_percentage = np.median(category_data[:,-1]) * 100

        category_data_signers = data[:,categories.index(category_signers)].reshape((-1, steps))
        final_percentage_signers = np.median(category_data_signers[:,-1]) * 100

        ratio = final_percentage / final_percentage_signers

        plt.plot(np.median(category_data, axis=0), label=arg)
        plt.fill_between(np.arange(steps),
                        *np.percentile(category_data, [25, 75], axis=0), alpha=.2)

        print(f"Final percentage {args[1]}: {'%.2f' % final_percentage}%. Ratio {args[1]}: {'%.2f' % ratio}.")


    plt.legend(loc="upper left")

    n = int(data[:,categories.index("n")][0])
    m = data[:,categories.index("m")][0]
    d = data[:,categories.index("d")][0]
    c = data[:,categories.index("c")][0]

    plt.title(f"n: {n}, m: {m}, d: {d}, c: {c}")

    if savefile[-1] == "-":
        plt.show()
    else:
        plt.savefig(savefile)

if __name__ == "__main__":
    create_graph(sys.argv[1:])
