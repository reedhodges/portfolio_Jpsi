# J/ψ Production ML Portfolio Project

## Overview
This portfolio project explores the use of machine learning in the context of particle physics, focusing on J/ψ production cross sections. It is a part of my portfolio to demonstrate skills in Python and machine learning.  It is a **work in progress**, and is intended to be an educational exercise, not a rigorous scientific one.

## File descriptions

- `constants.py`: physical constants
- `cross_sections.py`: defines the various J/ψ production cross sections
- `data_processing.py`: adds noise too and subsequently cleans the data
- `fragmentation_functions.py`: defines fragmentation functions on which the cross sections depend
- `gbm.py`: some work with gradient boosting machines
- `generate_grids.py`: generates the cross section data
- `generate_pdfs.m`: Mathematica file that fetches experimental data on the parton distribution functions
- `linear_regression.py`: some work on a linear regression model
- `pdfs.py`: functions to interpolate the parton distribution functions
- `plots.py`: produces various plots

## Project Goals
- Analyze J/ψ production cross sections using Python's ML ecosystem.
- Develop ML models for predictive analysis.
- Investigate feature importance and anomaly detection in the dataset.

## Background
J/ψ meson production in semi-inclusive deep inelastic scattering is examined, exploring various production mechanisms and their influence on the production cross section.

## Data
The dataset is derived from theoretical predictions of J/ψ production cross sections. The theoretical expressions are derived in an [academic paper](https://arxiv.org/abs/2310.13737) by me and my co-authors.

## Methodology
- Data visualization and analysis using Python libraries.
- Regression models for prediction.
- Feature importance analysis with SHAP values.
- Anomaly detection to ensure data integrity.

## Dependencies
- Python
- Scikit-learn
- Pandas

## Contact
Reed Hodges - [Email](mailto:reed.hodges@duke.edu)
