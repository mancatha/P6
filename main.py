from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd

pipeline = joblib.load('./model/rf_pl.joblib')
encoder = joblib.load('./model/label_encoder.joblib')


app = FastAPI()

class SepsisFeatures(BaseModel):
    PRG: int
    PL: int
    PR:int
    SK :int
    TS :int
    M11:float
    BD2:float
    Age:int
    Insurance:int

@app.get('/')
def home():
    return "Hello world"

@app.get('/info')
def appinfo():
    return 'This is the info page of this app'
 
 
# Define the prediction endpoint
@app.post('/predict_sepsis')
def predict_sepsis(sepsis_features: SepsisFeatures):
    # Convert input features to a DataFrame
    df = pd.DataFrame([sepsis_features.model_dump()])

    # Perform prediction using the pre-trained pipeline
    prediction = pipeline.predict(df)

    encoder_prediction = encoder.inverse_transform([prediction])[0]
    

    return {'prediction' : encoder_prediction}






    
#return response