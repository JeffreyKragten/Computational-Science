from mesa.batchrunner import batch_run
from multiprocessing import freeze_support
import pandas as pd
from model import SignModel
import os
import sys
import itertools

def main():
    freeze_support()
    # parameters to run the model with
    parameters = {"n": 728, "m": 0.58, "d": 0.022, "c": 0.172}
    p = None
    for i, arg in enumerate(sys.argv[1:]):
        if arg.isdigit():
            arg += "."
        if arg.replace(".", "", 1).isdigit() and p:
            if type(parameters[p]) is list:
                parameters[p].append(float(arg))
            else:
                parameters[p] = [float(arg)]
        elif arg in parameters and len(sys.argv) > i + 2 and \
             sys.argv[i + 2].replace(".", "", 1).isdigit():
            p = arg
        else:
            print("Unknown parameter: {arg}")
            return

    generations = 50

    # batch runs the model
    results = batch_run(
        SignModel,
        parameters=parameters,
        iterations=100,
        max_steps=generations,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    # Create results directory if it not exsists yet.
    if not os.path.exists("results"):
        os.makedirs("results")

    # Create a file with all the collected data per.
    results_df = pd.DataFrame(results)

    pars = [p for p, v in parameters.items() if type(v) is list]
    for values in itertools.product(*(parameters[p] for p in pars)):
        res = results_df
        savefile = "results/results"
        for p, v in zip(pars, values):
            res = res[res[p] == v]
            savefile += f"_{p}_{v}"
        res.to_csv(f"{savefile}.csv")


if __name__ == "__main__":
    main()
