# The Silent Minority
<b>Team members:</b> Ray Pelupessy; Luuk van der Waals; Jeffrey Kragten<br>

## Table of Contents
* [Introduction](#introduction)
* [Research Question](#research-question)
* [Results](#results)
* [Running the code](#running-the-code)

## Introduction
[explain background, sources]
This repository contains code for the course Project Computational Science at the University of Amsterdam (2022-2023).
This project focused on the persistence of sign languages under various circumstances. The basis of this model and its
input variables is taken from a paper using ABM to model exactly this, though they do not include the different levels of fluency (Mudd et al. 2020).

Mudd, K., de Vos, C., & de Boer, B. (2020). An agent-based model of sign language persistence informed by real-world data.
<i>Language Dynamics and Change</i>, 10(2), 158–187. https://doi.org/10.1163/22105832-bja10010 </br>

## Research Question
[RQ + hypothesis]
The research question answered here is “What value should the assortative marriage parameter take to maximize the percentage of non-fluent signers after 50 generations?”
Our hypothesis is as follows: A lower assortative marriage value results in a higher percentage of non-fluent signers

## Results
[our results]
[don't forget a graph or two]

## Running the code
### Necessary packages to run the code:
* Mesa
* Pandas
* Numpy
* Matplotlib
### Executing main.py
To run the model,you can simply run main.py.
```
python main.py
```
If you want to changes the parameter give the name of the parameters and the values to set the parameters to. The parameters and there standard values are:
- n: 728    The number of agents per generation.
- m: 0.58   The percantage of agent prefering assortative marriage.
- d: 0.22   The percentage of deaf in the first generation.
- c: 0.172  Percentage of agents not deaf but carrying a deaf gene in the first generation.

Example:
```
python main.py n 500 m 0.1 0.2 0.3
```
This command runs the model three times once for each value of m (0.1 0.2 and 0.3) with 500 agents per generation and the standard values for the other two parameters. The results will be saved to:

/results/results_n_500_m_0.1.csv </br>
/results/results_n_500_m_0.2.csv </br>
/results/results_n_500_m_0.3.csv

To create a graph the data use graph.py.
```
$ python graph.py [category] [loadfile] [*values]
$ python graph.py [category] [loadfile] [savefile] [*values]
```
- category: The kind of data you want to represent. The categories are n, m, d, c, agent_count, percentage_signers, percentage_fluent_signers, percentage_non_fluent_signers, percentage_deaf and percentage_carry. Standard: "percentage_non_fluent_signers"
- loadfile: The file in the results directory to get the data from to show in the graph from. If you want data from different files with different values for a certain parameter you can use "*" as a place holder for the different values and give the values as the values parameter. Standard: "results.csv"
- savefile: The file the graph is saved to. If not given the graph will be shown instead of be saved.
- values: The values that go in the place of the "*" in the filename.

Example:
```
python graph.py percentage_signers results_n_500_m_* plot 0.1 0.2 0.3
```
This command will make a plot of the percentage of people that can speak sign language from the data in the following files:

/results/results_n_500_m_0.1.csv </br>
/results/results_n_500_m_0.2.csv </br>
/results/results_n_500_m_0.3.csv

and saves the graph in the file:

/results/plot.png
