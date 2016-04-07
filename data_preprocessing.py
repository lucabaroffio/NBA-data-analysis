
# coding: utf-8

# # NBA data analysis
# ## Preprocessing
# This script process all the base dataset, consisting of all the games from season 1989/1990 to season 2014/2015, so as to create a dataset suitable for predicting game results. In particular, for each game, the situation of the two teams is reported in terms of the number of wins and losses, the average number of points scored and allowed per game, the win percentage in the last 5 games. Given all these features, the score of the game, i.e. the number of points scored by the two teams have to be predicted.

# In[9]:

# import libraries
import os
import gzip
import csv
import Queue


# In[10]:

START_YEAR = 89
END_YEAR = 15


# In[11]:

champions = {}

with open(os.path.join('raw_data', 'champions.csv'), 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for idx, row in enumerate(csvreader):
        champions[row[0]] = row[1]

# open file and initialize the header data
out_f = gzip.open(os.path.join('data', 'dataset.csv.gz'), 'wb')
writer = csv.writer(out_f, delimiter=',')
writer.writerow([
        'away_team_GP',      # teams season history
        'away_team_W',       # until this game
        'away_team_L',       #
        'away_team_PSPG',
        'away_team_PAPG',
        'away_team_last5_W%',
        'home_team_GP',
        'home_team_W',
        'home_team_L',
        'home_team_PSPG',
        'home_team_PAPG',
        'home_team_last5_W%',
        'away_team_points',  # game result
        'home_team_points',  #
        'winning_team'
    ])

for cur_year in champions:

    f_path = cur_year + '.csv'
    team_dict = {}

    with open(os.path.join('raw_data', f_path), 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(csvreader):
            # skip header row
            if idx == 0:
                continue
            if row[3] not in team_dict:
                team_dict[row[3]] = {}
                team_dict[row[3]]['games'] = 0
                team_dict[row[3]]['W'] = 0
                team_dict[row[3]]['L'] = 0
                team_dict[row[3]]['points_for'] = 0
                team_dict[row[3]]['points_aga'] = 0
                team_dict[row[3]]['last_5_W'] = Queue.Queue(5) 
            if row[5] not in team_dict:
                team_dict[row[5]] = {}
                team_dict[row[5]]['games'] = 0
                team_dict[row[5]]['W'] = 0
                team_dict[row[5]]['L'] = 0
                team_dict[row[5]]['points_for'] = 0
                team_dict[row[5]]['points_aga'] = 0
                team_dict[row[5]]['last_5_W'] = Queue.Queue(5)
            
            # predict games only after 5 games have already been played
            if (team_dict[row[3]]['games'] >= 5 and team_dict[row[5]]['games'] >= 5):
                cur = [
                    team_dict[row[3]]['games'],
                    team_dict[row[3]]['W'],
                    team_dict[row[3]]['L'],
                    team_dict[row[3]]['points_for'],
                    team_dict[row[3]]['points_aga'],
                    float(sum(list(team_dict[row[3]]['last_5_W'].queue)))/5.0,
                    team_dict[row[5]]['games'],
                    team_dict[row[5]]['W'],
                    team_dict[row[5]]['L'],
                    team_dict[row[5]]['points_for'],
                    team_dict[row[5]]['points_aga'],
                    float(sum(list(team_dict[row[5]]['last_5_W'].queue)))/5.0,
                    float(row[4]),
                    float(row[6]),
                    1 if float(row[4])>float(row[6]) else 2,
                ]
                writer.writerow(cur)
            
            
            team_dict[row[3]]['games'] += 1
            team_dict[row[5]]['games'] += 1
            
            team_dict[row[3]]['points_for'] = (team_dict[row[3]]['points_for']*(team_dict[row[3]]['games'] - 1) +
                                               float(row[4]))/float(team_dict[row[3]]['games'])
            team_dict[row[3]]['points_aga'] = (team_dict[row[3]]['points_aga']*(team_dict[row[3]]['games'] - 1) +
                                               float(row[6]))/float(team_dict[row[3]]['games'])
            team_dict[row[5]]['points_for'] = (team_dict[row[5]]['points_for']*(team_dict[row[5]]['games'] - 1) +
                                               float(row[6]))/float(team_dict[row[5]]['games'])
            team_dict[row[5]]['points_aga'] = (team_dict[row[5]]['points_aga']*(team_dict[row[5]]['games'] - 1) +
                                               float(row[4]))/float(team_dict[row[5]]['games'])
            
            if int(row[4]) > int(row[6]):
                team_dict[row[3]]['W'] += 1
                team_dict[row[5]]['L'] += 1
                if team_dict[row[3]]['last_5_W'].full():
                    team_dict[row[3]]['last_5_W'].get()
                team_dict[row[3]]['last_5_W'].put(1)
                if team_dict[row[5]]['last_5_W'].full():
                    team_dict[row[5]]['last_5_W'].get()
                team_dict[row[5]]['last_5_W'].put(0)
            else:
                team_dict[row[3]]['L'] += 1
                team_dict[row[5]]['W'] += 1
                if team_dict[row[3]]['last_5_W'].full():
                    team_dict[row[3]]['last_5_W'].get()
                team_dict[row[3]]['last_5_W'].put(0)
                if team_dict[row[5]]['last_5_W'].full():
                    team_dict[row[5]]['last_5_W'].get()
                team_dict[row[5]]['last_5_W'].put(1)
        
out_f.close() 

