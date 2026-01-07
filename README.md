# Penguin Classifier

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

A platform-independent machine learning application to classify Palmer penguins, designed for non-technical field usage.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`. Contains EDA.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         penguin_classifier and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
└── src
    └── penguin_classifier <- Source code for use in this project.
        │
        ├── __init__.py             <- Makes penguin_classifier a Python module
        │
        ├── config.py               <- Store useful variables and configuration
        │
        ├── app.py               <- Entry point to the application
        │
        ├── dataset.py              <- Scripts to download or generate data
        │
        ├── features.py             <- Code to create features for modeling
        │
        ├── schema.py             
        │
        ├── modeling                
        │   ├── __init__.py 
        │   ├── predict.py          <- Code to run model inference with trained models          
        │   └── train.py            <- Code to train models
        ├── ui                
        │   ├── __init__.py 
        │   ├── layout.py           <- Code to define HTML-structure and wireframe          
        │   └── callbacks.py        <- Code to connect UI and model/data
        │
        └── plots.py                <- Code to create visualizations
```

--------

