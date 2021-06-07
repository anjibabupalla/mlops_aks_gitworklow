import os
import argparse
import yaml
import logging
import pandas as pd
import glob

def read_all_csv(path):
    all_files = glob.glob(path + "/*.csv")
    list_of_dfs = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0,sep=',')
        list_of_dfs.append(df)
    return pd.concat(list_of_dfs, axis=0, ignore_index=True)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def load_and_save(config_path):   
    config = read_params(config_path)
    df = get_data(config_path)
    df.columns = [cols.replace(' ','_') for cols in df.columns]
    write_path = config['load_data']['processed_data_set']
    df.to_csv(write_path,sep=',',index=False,header=True)

def get_data(config_path):
    config = read_params(config_path)
    print('displaying config values',config)
    data_path = config['data_source']['raw_data_set']
    df = pd.read_csv(data_path)
    print(df.columns)
    return df


if __name__=="__main__":
    parser =  argparse.ArgumentParser()
    parser.add_argument('--config',default='config/params.yaml')
    args = parser.parse_args()
    load_and_save(config_path=args.config)