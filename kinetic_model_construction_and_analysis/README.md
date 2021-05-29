# Increasing accoa concentration in P. putida

This repo contains all data and code used to find how to increase the accoa concentration in P. putida and to analyze omics data (metabolomics and proteomics) of P. putida with CRISPRi mediated depletion of chosen targets.

## Kinetic model 
The model ensemble of P. putida central carbon metabolism is developed with [GRASP](https://github.com/biosustain/GRASP), and performing MCA on the resulting ensemble. By looking at the Concentration Control Coefficients affecting acetyl-CoA, we find which enzyme concentrations have the most impact in acetyl-CoA's concentration.

This repo contains all the input data and code used to do the analysis, apart from the packages [GRASP](https://github.com/biosustain/GRASP) and [set_up_grasp_models](https://github.com/biosustain/set_up_grasp_models).


## Table of contents

* [Introduction](#introduction)
* [Starting up](#starting-up)
* [Project organization](#project-organization)
* [Workflow](#workflow)
* [The omics data](#the-omics-data)
* [Enzyme regulation](#enzyme-regulation)
* [Models nomenclature](#models-nomenclature)
* [Roadmap](#roadmap)


## Starting up

1. Create a new virtualenv, not super essential but recommended;
2. install the required packages with `pip install -r requirements.txt`;
3. install the package itself by going to the main folder and running `pip install -e .`.

The latter is important to use the notebooks and certain files.


## Project organization


    ├── LICENSE
    ├── README.md          <- The top-level README about the project.
    ├── data
    │   ├── omics          <- Contains all the omics data used to generate the model.
    |
    ├── matlab_scripts     <- Contains the Matlab scripts needed to build the model, do MCA and simulate the model.
    |
    ├── models             <- Both plain text lists of reactions and GRASP models produced by set_up_grasp_models.
    │
    ├── notebooks          <- Jupyter notebooks.
    │   ├── model_building      <- Notebook used to build the GRASP models
    │   ├── MCA                 <- Notebooks to visualize MCA results
    │   └── pfba                <- Notebooks to calculate flux distribution
    │
    ├── requirements.txt   <- The requirements file for reproducing the kinetic model construction analysis environment.Generated with `pip freeze > requirements.txt`
    │                         
    |
    ├── environment.yml         <- The requirements file for the conda environment for reproducing the kinetic model construction analysis environment. Produced with `conda env export > environment.yml`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    |
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py
    



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
