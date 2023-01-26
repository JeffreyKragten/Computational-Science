import sys
import numpy as np
import matplotlib.pyplot as plt

def create_graph(args=[], parameters={}):
    # category = args[0] if len(args) > 0 else "percentage_non_fluent_signers"
    category = "percentage_non_fluent_signers"
    category_signers = "percentage_signers"
    val = args[0] if len(args) > 0 else "0.58"

    savefile = "{}/results/{}".format(sys.path[0], args[2]) if len(args) > 2 else None
    filename = "{}/results/results_d_".format(sys.path[0]) + f"{val}.csv"

    with open(filename) as f:
        categories = f.readline().rstrip().split(",")
    data = np.loadtxt(filename, skiprows=1, delimiter=",")

    steps = int(max(data[:,categories.index("Step")])) + 1
    category_data = data[:,categories.index(category)].reshape((-1, steps))
    final_percentage = np.median(category_data[:,-1]) * 100

    category_data_signers = data[:,categories.index(category_signers)].reshape((-1, steps))
    final_percentage_signers = np.median(category_data_signers[:,-1]) * 100

    ratio = final_percentage / final_percentage_signers

    plt.plot(np.median(category_data, axis=0), label=args[0])
    plt.fill_between(np.arange(steps),
                    *np.percentile(category_data, [25, 75], axis=0), alpha=.2)

    if args[1]:
        filename_2 = "{}/results/results_d_".format(sys.path[0]) + f"{args[1]}.csv"

        with open(filename_2) as f:
            categories_2 = f.readline().rstrip().split(",")
        data_2 = np.loadtxt(filename_2, skiprows=1, delimiter=",")

        category_data_2 = data_2[:,categories_2.index(category)].reshape((-1, steps))
        final_percentage_2 = np.median(category_data_2[:,-1]) * 100

        ratio_2 = final_percentage_2 / final_percentage_signers

        plt.plot(np.median(category_data_2, axis=0), label=args[1])
        plt.fill_between(np.arange(steps),
                        *np.percentile(category_data_2, [25, 75], axis=0), alpha=.2)

    plt.legend(loc="upper left")


    n = int(data[:,categories.index("n")][0])
    m = data[:,categories.index("m")][0]
    d = data[:,categories.index("d")][0]
    c = data[:,categories.index("c")][0]

    if ratio_2 and final_percentage_2:
        plt.title(f"Final percentage {args[0]}: {'%.2f' % final_percentage}%. Ratio {args[0]}: {'%.2f' % ratio}. \n \
        Final percentage {args[1]}: {'%.2f' % final_percentage_2}%. Ratio {args[1]}: {'%.2f' % ratio_2}. \nn: {n}, m: {m}, d: {d}, c: {c}")
    else:
        plt.title(f"Final percentage: {'%.2f' % final_percentage}%. Ratio: {'%.2f' % ratio}. \nn: {n}, m: {m}, d: {d}, c: {c}")

    if savefile:
        plt.savefig(savefile)
    else:
        plt.show()

if __name__ == "__main__":
    create_graph(sys.argv[1:])
