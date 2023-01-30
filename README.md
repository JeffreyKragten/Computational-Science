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
To run main.py, the input should take the following shape:
```
python main.py [whatever we change this to]
```
After running this, the model wil be run, and results will be saved to /[directory]/[filename].