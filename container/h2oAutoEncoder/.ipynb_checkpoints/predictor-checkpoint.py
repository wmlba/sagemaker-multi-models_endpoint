# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os, random
import json
import pickle
import StringIO
import sys
import signal
import traceback
from sklearn.preprocessing import StandardScaler,MinMaxScaler,RobustScaler,Normalizer
import flask
import h2o
import pandas as pd
import socket
prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')
h2o.init(nthreads=-1, enable_assertions = False)
# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class ScoringService(object):
    model = None                # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls, model_name):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            files = os.listdir(model_path + "/" + str(model_name))
            model_location = os.path.join(model_path, str(model_name))
            model_location = os.path.join(model_location, str(files[0]))
            print("Loading model: " + model_location )
            cls.model = h2o.load_model(model_location)
        return cls.model

    @classmethod
    def predict(cls, input, model_name):
        """For the input, do the predictions and return them.
        print("model name is: " + str(model_name))
        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        clf = cls.get_model(model_name)
        
        return clf.anomaly(input)

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. This will select a random model from the saved ones and test loading it."""
    # Get a random model
    random_model = random.choice(os.listdir(model_path))
    health = ScoringService.get_model(random_model) is not None  # Loading one random model for the health check
    status = 200 if health else 404
    if status == 200:
        print('Model {} is healthy'.format(random_model))

    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.  """
    data = None
    model_name = flask.request.headers.get('CustomAttributes')
    if model_name == None:
        model_name = flask.request.headers.get('X-Amzn-Sagemaker-Custom-Attributes')
    print(model_name)
    # Convert from CSV to pandas
    if flask.request.content_type == 'application/python-pickle':
        data = flask.request.data
        df = pickle.loads(data)
        print('Invoked with {} records'.format(df.shape[0]))
        preds = h2o.H2OFrame(df)
        
    else:
        return flask.Response(response='This predictor only supports pickle files', status=415, mimetype='text/plain')
    
    # Do the prediction
    predictions = ScoringService.predict(preds, model_name)
    h2o.h2o.export_file(predictions,'/tmp/results.csv')
    predictions2 = pd.read_csv('/tmp/results.csv', header=None)
    os.remove("/tmp/results.csv")
    # Convert from numpy back to CSV
    out = StringIO.StringIO()
    #pd.DataFrame({'results':predictions2}).to_csv(out, header=False, index=False)
    #result = out.getvalue()
    print(socket.gethostname())
    return flask.Response(response=predictions2.to_json(orient='columns'), status=200, mimetype='text/csv')
