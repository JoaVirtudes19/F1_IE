import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import joblib

model = tf.keras.models.load_model('web/models/IE_F1_model.h5')
scaler = joblib.load('web/models/IE_F1_minmaxscaler.mod')

def predict(driver,
            grid_pos,
            year,
            constructor,
            circuit,
            year_round,
            weather={'weather_warm':0,
                     'weather_cold':0,
                     'weather_dry':0,
                     'weather_wet':0,
                     'weather_cloudy':0}
            ):

    
    # Crear nueva instancia para predecir
    instance = pd.DataFrame()
    instance['driverId'] = driver
    instance['constructorId'] = constructor
    instance['grid'] = grid_pos
    instance['year'] = year
    instance['round'] = year_round
    instance['circuitId'] = circuit
    instance['weather_warm'] = weather['weather_warm']
    instance['weather_cold'] = weather['weather_cold']
    instance['weather_dry'] = weather['weather_dry']
    instance['weather_wet'] = weather['weather_wet']
    instance['weather_cloudy'] = weather['weather_cloudy']


    instance['grid'] = instance['grid'].clip(upper=20)
    instance['position'] = instance['position'].clip(upper=20)
    columns_to_scale = ['year']
    instance[columns_to_scale] = scaler.transform(instance[columns_to_scale])
    columns_to_replace = ['weather_warm', 'weather_cold', 'weather_dry', 'weather_wet', 'weather_cloudy']
    instance[columns_to_replace] = instance[columns_to_replace].replace(1,20)   
    drivers = instance['driverId']
    constructors = instance['constructorId']
    circuits = instance['circuitId']
    X = instance.drop(['driverId', 'constructorId', 'circuitId', 'position'], axis=1) 

    prediction = model.predict([drivers, constructors, circuits, X], verbose=0)

    pred_df = pd.DataFrame()
    pred_df['driverId'] = drivers
    pred_df['predictions'] = prediction
    pred_df['predictions'] = pred_df['predictions'].round(0)
    pred_df['predictions'] = pred_df['predictions'].clip(lower=1, upper=20)
    return pred_df



