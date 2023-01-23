import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) > 2:
    filename = sys.argv[2]
else:
    filename = "{}/{}".format(sys.path[0], "results/results.csv")

if len(sys.argv) > 1:
    category = sys.argv[1]
else:
    category = "percentage_signers"

with open(filename) as f:
    categories = f.readline().rstrip().split(",")
data = np.loadtxt(filename, skiprows=1, delimiter=",")
print(categories)

plt.plot(data[:,categories.index(category)])

if len(sys.argv) > 3:
    plt.savefig(sys.argv[3])
else:
    plt.show()
