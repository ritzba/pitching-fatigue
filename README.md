# Modeling Pitcher Fatigue

## Introduction

MLB has provided live, pitch-by-pitch data online for every pitch in every game since 2015.  This data goes far beyond pitch speed - it includes everything from velocity and acceleration on all 3 axes to release spin rate to identification of the pitch type based on prior information about the pitcher's arsenal.

Managers and pitching coaches should be able to harness this data during the course of games to evaluate their pitcher's performance as the game progresses.  This could improve decision-making with respect to pitch choice, as well as decisions about when to substitute a fatigued pitcher for someone (or someone else) in the bullpen.


## Problem Statement

Develop a machine learning model which can assess pitcher fatigue using live, in-game mechanical measurements such as velocity and release point.  The strategy chosen for this model is to use this data in light of league averages and the pitcher's own history to predict the pitcher's "pitch number equivalent."

##  The Data

MLB releases its data publicly through an API.  I have used two Python wrappers (pybaseball for past pitches and MLB-StatsApi for live pitches) to simplify the process of data retrieval.  The relevant data includes the following (all dtypes are Float64 unless specified otherwise):

Directions:  
x = lateral (positive numbers are to catcher's right/pitcher's left)
<p>
y = forward (toward home plate)
<p>
z = vertical
<p>pitch_type - type of pitch, as evaluated by MLB's modeling, including stored data regarding the pitcher's repertoire
<p>player_name - pitcher's first and last name 
<p>release_speed - initial pitch speed in mph
<p>release_spin_rate - initial spin rate in rpm
<p>release_pos_x, release_pos_y, release_pos_z - release position in x, y, z directions
<p>distances measured from center of pitcher's mound
<p><p>x and z directions measured in feet, y direction measured in inches
<p>vx0, vy0, vz0 - initial velocity in x, y, z directions (feet/sec)
<p><p>ax, ay, az - acceleration in x, y, z directions (feet/sec ^ 2)
    
##  Conclusions
    
Ultimately, after trying several different types of models, an ElasticNet model was fit to the data which performed marginally better than the baseline.  With greater processing power, more data could be used and the model complexity could be increased.
