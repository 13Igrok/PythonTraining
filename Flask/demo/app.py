import json
import sqlite3

import pandas as pd
import plotly
import plotly.graph_objs as go
from flask import Flask, render_template, request
from flask_executor import Executor
from flask_socketio import SocketIO, emit

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()
global test_val
app = Flask(__name__)
socketio = SocketIO(app)
def create_plot(feature_importance):
    feature_importance=feature_importance.reset_index(drop=True)
    feature_importance = feature_importance.iloc[:5]
    print(feature_importance)

    data = [
        go.Bar(
            x=feature_importance['Age'], # assign x as the dataframe column 'x'
            y=feature_importance['Name'], orientation='h'
        )
    ]

    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

@socketio.on("response")
def background_task_func():
    global test_val
    global plot
    socketio.sleep(10)
    data = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18]}  
    test_val= pd.DataFrame(data)
    bar = create_plot(test_val)
    plot=bar
    if test_val.shape[0]>1:
        print(test_val)
        emit('response_output',plot ,broadcast=True)
        socketio.sleep(1)
        #return render_template('views/index_img_soc.html', plot=bar)
    
@app.route('/', methods=['GET'])
def index():
    global plot
    executor.submit(background_task_func)
    bar = create_plot(test_val)
    
    return render_template('views/index_img_soc.html', plot=bar)



if __name__ == "__main__":
    data ={'Name': [], 'Age': []}  
    test_val= pd.DataFrame(data)   
    executor = Executor(app)
    socketio.run(app) 