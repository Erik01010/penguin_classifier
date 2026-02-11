# Penguin Classifier

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

A platform-independent machine learning application to classify Palmer penguins, designed for non-technical field usage.

## Project Organization

```
├── .gitignore
├── Dockerfile
├── LICENSE
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── start_linux.sh
├── start_windows.bat
├── data
│   ├── processed
│   └── raw
├── docs
│   ├── .gitkeep
│   ├── README.md
│   ├── mkdocs.yml
│   └── docs
│       ├── getting-started.md
│       └── index.md
├── metrics
├── models
│   ├── .gitkeep
│   └── pipeline.joblib
├── notebooks
│   ├── .gitkeep
│   └── 01_initial_eda.ipynb
├── references
│   └── .gitkeep
├── reports
│   ├── .gitkeep
│   ├── metrics.json
│   ├── penguin_raw_data_profile.html
│   └── figures
│       └── .gitkeep
├── src
│   ├── __init__.py
│   └── penguin_classifier
│       ├── __init__.py
│       ├── app.py
│       ├── config.py
│       ├── dataset.py
│       ├── features.py
│       ├── plots.py
│       ├── modeling
│       │   ├── __init__.py
│       │   ├── predict.py
│       │   └── train.py
│       └── ui
│           ├── __init__.py
│           ├── callbacks.py
│           └── layout.py
└── tests
    ├── __init__.py
    ├── test_backend.py
    └── test_frontend.py
```

--------

