import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    category = sys.argv[1]
else:
    category = "percentage_signers"

filename = "{}/{}".format(sys.path[0], "results/results.csv")
with open(filename) as f:
    categories = f.readline().rstrip().split(",")
data = np.loadtxt(filename, skiprows=1, delimiter=",")
print(categories)

steps = int(max(data[:,categories.index("Step")])) + 1
category_data = data[:,categories.index(category)].reshape((-1, steps))

plt.plot(np.median(category_data, axis=0))
plt.fill_between(np.arange(steps),
                *np.percentile(category_data, [25, 75], axis=0), alpha=.2)

if len(sys.argv) > 3:
    plt.savefig(sys.argv[3])
else:
    plt.show()
