from mesa.batchrunner import batch_run
from multiprocessing import freeze_support
import pandas as pd
from model import SignModel
import os
from graph import create_graph
import sys

def main():
    freeze_support()
    # parameters to run the model with
    parameters = {"n": 728, "m": [0, 0.025, 0.5, 0.075, 0.1, 0.125], "d": 0.022, "c": 0.172}
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
    for j in parameters['m']:
        results_df[results_df['m'] == j].to_csv(f'results/results_{j}.csv')

    #TODO
    create_graph()

if __name__ == "__main__":
    main()