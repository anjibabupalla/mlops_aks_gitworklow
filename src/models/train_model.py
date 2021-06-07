import os
from  src.data.make_dataset import read_params
import numpy as np
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import argparse
import joblib
import json
import pandas as pd

def eval_metrics(actual,prediction):
    rmse = np.sqrt(mean_squared_error(actual, prediction))
    mae = mean_absolute_error(actual, prediction)
    r2 = r2_score(actual, prediction)
    return rmse,mae,r2
def train_and_evaluate(config_path):
    
    config = read_params(config_path)
    test_data_path = config['split_data']['test_path']
    train_data_path = config['split_data']['train_path']
    random_state = config['base']['random_state']
    model_dir = config['saved_models']['model_dir']
    alpha = config['estimators']['ElasticNet']['params']['alpha']
    l1_ratio = config['estimators']['ElasticNet']['params']['l1_ratio']
    target = config['base']['target_col'] 
    

    train = pd.read_csv(train_data_path,sep=',')
    test = pd.read_csv(test_data_path,sep=',')

    train_y = train[target]
    test_y = test[target]
    train_x = train.drop(target,axis=1)
    test_x = test.drop(target,axis=1)
    

    lr = ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=random_state)
    lr.fit(train_x,train_y)
    predicted_qualities = lr.predict(test_x)
    (rmse,mae,r2) = eval_metrics(test_y,predicted_qualities)
    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)




    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(lr, model_path)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    default_config_path = os.path.join('config','params.yaml')
    train_and_evaluate(default_config_path)