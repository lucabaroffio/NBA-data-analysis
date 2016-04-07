# NBA data analysis

This python repo presents a simple approach for predicting the scores and the winner of NBA games. The repo exploits some popular python modules for data analysis including pandas and scikit-learn. The model is trained and evaluated on data of NBA seasons from 1989 to 2015. The model is able to predict the correct winner for approximately 68.2% of games.

Both ipython notebooks and raw python files are available in the repo.

## Installation and requirements

```python
pip install -r requirements.txt
```
I suggest to create a virtual environment before installing the requirements

## Usage

First, preprocess raw games data to create a proper dataset and save it on file. To this end, run the script data_preprocessing.py. For the actual analysis, run the script NBA_results_analysis.py