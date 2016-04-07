
# coding: utf-8

# # Predicting NBA championship winner
# ## Load and transform the data

# In[3]:

# import libraries
import os
import csv
import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn import linear_model


# ## Predict results

# We will use a simple linear regression model to predict the number of points scored by the two teams of each game, and hence the result of the game. We are able to predict the winner for approximately *68.2%* of the games.

# In[15]:

# read csv and create a pandas dataset
dataset = pd.read_csv(os.path.join('data', 'dataset.csv.gz'))
dataset['away_team_W%'] = dataset.apply(lambda row: float(row['away_team_W'])/float(row['away_team_GP']), axis=1)
dataset['home_team_W%'] = dataset.apply(lambda row: float(row['home_team_W'])/float(row['home_team_GP']), axis=1)

# define the features
X = dataset.as_matrix(
    [
        'away_team_PSPG',
        'away_team_PAPG',
        'home_team_PSPG',
        'home_team_PAPG',
        'home_team_W%',
        'away_team_W%', 
        'away_team_last5_W%',
        'home_team_last5_W%'
    ]
)

# define the variables to be predicted
Y = dataset.as_matrix(['home_team_points', 'away_team_points'])

# define a 10 fold cross validation procedure
k_fold = cross_validation.KFold(n = len(dataset), n_folds = 10)

# declare a classifier
clf = linear_model.LinearRegression()

accuracy = []

# for each fold...
for train_indices, test_indices in k_fold:
    
    # get training and test samples
    train_X = X[train_indices]
    train_Y = Y[train_indices]
    test_X = X[test_indices]
    test_Y = Y[test_indices]
    
    # fit the model
    model = clf.fit(train_X, train_Y)
    
    # predict the score
    predictions = model.predict(test_X)
    
    # infer the winner
    predictions_winner = [(0 if x[0]>x[1] else 1) for x in predictions]
    
    # get the real result of the game
    gt_winner = [(0 if x[0]>x[1] else 1) for x in test_Y]
    
    # check whether the prediction matches the ground truth and compute the accuracy
    prediction_matches = [predictions_winner[ind] == gt_winner[ind] for ind, _ in enumerate(predictions_winner)]
    accuracy.append(float(sum(prediction_matches))/float(len(prediction_matches)))

# overall accuracy is the mean accuracy for each fold
print 'Accuracy: %.4f +/- %.4f' % (np.mean(accuracy), np.std(accuracy))
    

