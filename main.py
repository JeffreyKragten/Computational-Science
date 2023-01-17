from mesa.batchrunner import batch_run
from multiprocessing import freeze_support
import pandas as pd
from model_file import Model


def main():
    freeze_support()
    # parameters to run the model with
    parameters = {"n": 750, "m": 0.58, "d": 0.022, "c": 0.176}
    generations = 50

    # batch runs the model
    results = batch_run(
        Model,
        parameters=parameters,
        iterations=1,
        max_steps=generations,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(f'results/results.csv')
    
if __name__ == "__main__":
    main()