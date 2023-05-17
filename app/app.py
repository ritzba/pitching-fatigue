import pandas as pd
import numpy as np
import streamlit as st

import numpy as np
import pandas as pd
import requests
import json


from sklearn.model_selection import train_test_split,cross_val_score, GridSearchCV, RandomizedSearchCV

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from pybaseball import statcast
from statsapi import schedule, lookup_team

st.title('Pitching Fatigue Predictor')
last = st.text_input('Pitcher Last Name')
first = st.text_input('Pitcher First Name')
team = st.text_input('Team (3-letter abbreviation)')
date = st.text_input('Date (YYYY-MM-DD')

def load_pitches(last, first, team, date):
    team = lookup_team(team)[0]['id']
    game_no = schedule(date = date, team = team)[0]['game_id']
    res = requests.get(f'https://statsapi.mlb.com/api/v1.1/game/{game_no}/feed/live')
    df = res.json()
    pitches = []
    for play in df['liveData']['plays']['allPlays']:
        if play['matchup']['pitcher']['fullName'].replace(' ','').lower() == first.lower() + last.lower():
            pitcher = play['matchup']['pitcher']['fullName']
            for pitch in play['playEvents']:
                if pitch['isPitch']:
                    new_pitch = {
                    'pitcher':pitcher,
                    'pitch_type':pitch['details']['type']['code'], 
                    'release_speed':pitch['pitchData']['startSpeed'], 
                    'release_spin_rate':pitch['pitchData']['breaks']['spinRate'],
                    'vx0':pitch['pitchData']['coordinates']['vX0'],                            
                    'vy0':pitch['pitchData']['coordinates']['vY0'],
                    'vz0':pitch['pitchData']['coordinates']['vZ0'], 
                    'plate_x':pitch['pitchData']['coordinates']['pX'], 
                    'plate_z':pitch['pitchData']['coordinates']['pZ'], 
                    'release_pos_x':pitch['pitchData']['coordinates']['x0'],
                    'release_pos_y':pitch['pitchData']['coordinates']['y0'], 
                    'release_pos_z':pitch['pitchData']['coordinates']['z0'], 
                    'sz_top':pitch['pitchData']['strikeZoneTop'], 
                    'sz_bot':pitch['pitchData']['strikeZoneBottom'], 
                    'ax':pitch['pitchData']['coordinates']['aX'],
                    'ay':pitch['pitchData']['coordinates']['aY'], 
                    'az':pitch['pitchData']['coordinates']['aZ'], 
                    'pfx_x':pitch['pitchData']['coordinates']['pfxX'], 
                    'pfx_z':pitch['pitchData']['coordinates']['pfxZ'], 
                    'vz0*2':pitch['pitchData']['coordinates']['z0'] ** 2,
                    'pfx_z*2':pitch['pitchData']['coordinates']['pfxZ'] ** 2,
                    'plate_z*2':pitch['pitchData']['coordinates']['pZ'] ** 2
                    }
                    pitches.append(new_pitch)
    pitches = pd.DataFrame(pitches)
    pitches.rename(columns = {'pitcher':f'player_name_{last}, {first}'}, inplace = True)
    pitches['pitch_type_orig'] = pitches['pitch_type']
    pitches = pd.get_dummies(pitches, columns = ['pitch_type'])
    pitches['player_name_orig'] = pitches[f"player_name_{last}, {first}"]
    pitches.iloc[:,0] = 1                            
    return pitches

def transform(last,first,team,date,pitch):
    pitches = load_pitches(last,first,team,date)
    pitch_count = pitches.index + 1
    pitch_type = pitches.loc[pitches[f"pitch_type_{pitch}"] > 0,:]
    last_in_type = pd.DataFrame(pitch_type.iloc[-1,:])
    data = X_train[X_train[f"player_name_{last}, {first}"] > 0]
    data.columns = data.columns.astype('str')
    last_in_type.columns = last_in_type.columns.astype('str')
    for col in data.columns:
        if col not in last_in_type.columns:
            last_in_type[col] = data[col]
    print(enet.predict(last_in_type) ** 2)

