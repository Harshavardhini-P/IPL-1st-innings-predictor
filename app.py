# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 23:08:49 2020

@author: Admin
"""


import numpy as np
from flask import Flask,request,jsonify,render_template
import pickle


app=Flask(__name__)
model=pickle.load(open('model_lasso.pkl','rb'))

def team_encode(team,temp_array):
        if team == 'csk':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif team == 'dd':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif team == 'kxip':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif team == 'kkr':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif team == 'mi':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif team == 'rr':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif team == 'rcb':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif team == 'srh':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
        return temp_array

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict',methods=['POST'])
def predict():
    temp_array=[]
    bat_team=request.form['bat_team']
    bowl_team=request.form['bowl_team']
    temp_array=team_encode(bat_team, temp_array)
    temp_array=team_encode(bowl_team, temp_array)
    
    runs=int(request.form["Current Score"])
    wickets=int(request.form["Wickets"])
    overs=float(request.form["Overs"])
    last_5_runs=int(request.form["last_5_runs"])
    last_5_wicket=int(request.form["Last 5 Overs Wicket"])
    
    temp_array+=[runs,wickets,overs,last_5_runs,last_5_wicket]
    
    
    if bat_team=="none" :
        return render_template('index1.html',prediction_text="PLEASE!ENTER BATTING TEAM")
    elif bowl_team=="none":
        return render_template('index1.html',prediction_text="PLEASE!ENTER BOWLING TEAM")
    else:
        output=int(model.predict([temp_array])[0])
        return render_template('index1.html',prediction_text="TARGET MIGHT BE {} to {}. ".format(output-10,output+5))
        
    


if __name__=="__main__":
    app.run(debug=True)
    