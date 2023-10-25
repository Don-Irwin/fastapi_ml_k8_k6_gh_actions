import pickle
from operator import mod
from os import getcwd
import os
from os.path import exists, join
from xml.dom.minidom import TypeInfo
import numpy as np

import joblib
from sklearn.datasets import fetch_california_housing
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVR


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Extra
import platform
import redis
from datetime import timedelta


app = FastAPI()


redis_host = os.environ.get("REDIS_SERVER","redis")
r = redis.Redis(host=redis_host, port=6379, db=0)
model_filename = "model_pipeline.pkl"
model_path = join(getcwd(), model_filename)
loaded_model = joblib.load(model_path)


class HomeRecord(BaseModel,extra=Extra.forbid):
    MedInc: float 
    HouseAge: float 
    AveRooms: float 
    AveBedrms: float 
    Population: float 
    AveOccup: float 
    Latitude: float 
    Longitude: float 


class Item(BaseModel,extra=Extra.forbid):
    feature_a: int
    feature_b: int

class PredictionResult(BaseModel):
    prediction_result: float

class PredictionResults(BaseModel):
    prediction_results: list[PredictionResult]

class CacheHitRatioResponse(BaseModel):
    predict_calls: int
    cache_hit: int
    cache_ratio: float
    # __init__(self,m_predict_calls,m_cache_hit,m_cache_ratio):
    #     self.predict_calls=m_predict_calls
    #     cache_hit=m_cache_hit
    #     cache_ratio= m_cache_ratio


@app.get("/version/")
async def version():
    return platform.python_version()

@app.get("/")
async def not_implemented():
    raise HTTPException(status_code=404,detail="Not Implemented")

@app.get("/health")
async def not_implemented():
    return "healthy"


@app.get("/hello/")
async def read_item(name: str | None ):
    if name is None:
        raise HTTPException(status_code=422,detail="No Name Parameter Supplied")
    return_string = "hello {}".format(name)
    return return_string

    #Don Irwin:  05/17/2022  -- Leave the 422 error code.
    #  
    # Request URL: http://127.0.0.1:8000/hello/?name1=
    # Request Method: GET
    # Status Code: 422 Unprocessable Entity
    # Remote Address: 127.0.0.1:8000
    # Referrer Policy: strict-origin-when-cross-origin

@app.post("/")
async def read_item(item: Item):
    print(item.json)
    print(item.dict().keys())
    print(item.dict().keys().mapping)
    print(list(item.dict().values()))
    model_filename = "model_pipeline.pkl"
    model_path = join(getcwd(), model_filename)
    print("About to write the trained file to the following location:")
    print(model_path)
    loaded_model = joblib.load(model_path)    
    return item.dict()


@app.get("/getcacheratio", response_model=CacheHitRatioResponse)
async def getcacheratio():
    predict_calls   = int(r.get("predict_calls"))
    cache_hit       = int(r.get("cache_hit"))
    print("predict_calls",predict_calls )
    if predict_calls > 0:
        print("The Hit Ratio:",predict_calls, cache_hit, cache_hit / (predict_calls))
        my_return = CacheHitRatioResponse(predict_calls=predict_calls,cache_hit=cache_hit,cache_ratio= (cache_hit / (predict_calls)) )
        # my_return.predict_calls     = predict_calls
        # my_return.cache_hit         = cache_hit
        # my_return.cache_ratio       = 
        return my_return

def get_cache_hit_vars():
    predict_calls = None
    cache_hit = None
    if r.get("predict_calls") is not None:
        predict_calls   = int(r.get("predict_calls"))
        cache_hit       = int(r.get("cache_hit"))
    if predict_calls is None:
        r.setex("predict_calls",timedelta(minutes=10),value=0)
        r.setex("cache_hit",timedelta(minutes=10),value=0)
        predict_calls = 0 
        cache_hit = 0
    return predict_calls,cache_hit

@app.post("/predict", response_model=PredictionResults)
async def predict(HomeRecords: list[HomeRecord]):
    predict_calls,cache_hit = get_cache_hit_vars()
    predict_data_stacked = None
    my_row = 0
    predict_calls +=1

    #extract the key and prepare the matrix for input
    for hr in HomeRecords:

        predict_data = np.asarray([list(hr.dict().values())])
        my_key = " ".join(str(e) for e in list(hr.dict().values()))
        if my_row > 0:
            if my_row == 1:
                predict_data_stacked = np.concatenate((predict_data_last,predict_data), axis=0)
            else: 
                predict_data_stacked = np.concatenate((predict_data_stacked,predict_data), axis=0)
            my_key = my_last_key + my_key
           
        predict_data_last = predict_data
        my_last_key = my_key
        my_row = my_row + 1

    #print(my_row)
    #print(my_key)

    #extract single group or run against model
    predicted_value = r.get(my_key)
    if predicted_value is not None:
        predicted_value = pickle.loads(predicted_value)
        #print("***got from cache****")
        #print("predicted_value=",str(predicted_value))
        cache_hit += 1
        r.setex("predict_calls",timedelta(minutes=3),value=predict_calls)
        r.setex("cache_hit",timedelta(minutes=3),value=cache_hit)
    else:
        predicted_value = loaded_model.predict(predict_data_stacked)
        r.setex(my_key,timedelta(minutes=3),value=pickle.dumps(predicted_value))
        #print("predicted_value=",predicted_value)
        r.setex("predict_calls",timedelta(minutes=3),value=predict_calls)

    prediction_results = [PredictionResult(prediction_result=value) for value in predicted_value.tolist()]

    my_results = PredictionResults(prediction_results=prediction_results)

    return my_results



@app.post("/predictitem", response_model=PredictionResult)
async def predictitem(hr: HomeRecord):
    predict_calls, cache_hit = get_cache_hit_vars()
    predict_calls +=1
    predict_data = np.asarray([list(hr.dict().values())])
    my_key = " ".join(str(e) for e in list(hr.dict().values()))
    predicted_value = r.get(my_key)
    if predicted_value is not None:
        print("***got from cache****")
        print("predicted_value=",str(predicted_value))
        cache_hit += 1
        r.setex("predict_calls",timedelta(minutes=3),value=predict_calls)
        r.setex("cache_hit",timedelta(minutes=3),value=cache_hit)        
        return PredictionResult(prediction_result=predicted_value)
    else:
        predicted_value = loaded_model.predict(predict_data)[0]
        r.setex(my_key,timedelta(minutes=5),value=predicted_value)
        r.setex("predict_calls",timedelta(minutes=3),value=predict_calls)
        print("predicted_value=",predicted_value)
        return PredictionResult(prediction_result=predicted_value)

