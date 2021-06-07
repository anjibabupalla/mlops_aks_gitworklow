import joblib
from src.data.make_dataset import read_params
import numpy as np
import yaml
import json
import os


params_path = "config/params.yaml"
schema_path = os.path.join("config","schema_in.json")

class NotInRangeError(Exception):
    def __init__(self, message="value not in range"):
        self.message = message
        super().__init__(self.message)

class NotInColsError(Exception):
    def __init__(self, message="not in columns"):
        self.message = message
        super().__init__(self.message)

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]
    print(prediction)
    try:
        if 3 <= prediction <=8:
            return prediction
        else:
            NotInRangeError
    except NotInRangeError:
        return "unexpected result"

def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request):
    def _valid_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInColsError
    def _validate_values(col,val):
        schema = get_schema()
        if not (schema[col]['min'] <=float(dict_request[col]) <=  schema[col]['max']):
            raise NotInRangeError
        
    for col,val in dict_request.items():
        _valid_cols(col)
        _validate_values(col,val)
    return True

def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request.values()
        data = [list(map(float,data))]
        response = predict(data)
        return response

def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.values())])
            response = predict(data)
            response = {"response":response}
    except NotInRangeError as e:
        print(e)
        response = {"the_expected_range":get_schema(),"response":str(e)}        
        return response

    except NotInColsError as e:
        print(e)
        response = {"the_expected_range":get_schema().keys(),"response":str(e)}        
        return response
