from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse
import joblib
from pydantic import BaseModel
import pandas as pd
from typing import Set
 

pipeline = joblib.load('./model/rf_pl.joblib')
pipeline_1 = joblib.load('./model/xgb_pl.joblib')
pipeline_2 = joblib.load('./model/gb_pl.joblib')
encoder = joblib.load('./model/label_encoder.joblib')


app = FastAPI(
    title="Sepsis Analysis API"
)

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

    # Define the available models
models = {
    "rf": pipeline,
    "xgb": pipeline_1,
    "gb": pipeline_2}


@app.get('/')
def home():
   return "Sepsis Anaysis"


@app.get('/info')
def appinfo():
    return 'Sepsis Analysis API: This is my interface'
 
 
# Define the prediction endpoint
@app.post('/predict_sepsis')
#def predict_sepsis(sepsis_features: SepsisFeatures):
def predict_sepsis(
    sepsis_features: SepsisFeatures,
      selected_model: str = Query("rf", description="Select the model for prediction")
):
    
    # Convert input features to a DataFrame
    df = pd.DataFrame([sepsis_features.model_dump()])
    
     # Check if the specified model is valid
    if selected_model not in models:
        return {"error": "Invalid model specified"}
 
   # Perform prediction using the selected pipeline
    selected_pipeline = models[selected_model]
    prediction = selected_pipeline.predict(df)
    encoder_prediction = encoder.inverse_transform([prediction])[0]
    
     # Get the probability scores
    try:
        probabilities = selected_pipeline.predict_proba(df)
        # Assuming binary classification, use the probability of the positive class
        probability_score = probabilities[0][1]
    except AttributeError:
        probability_score = None
    # Convert numpy.float32 to regular float
    probability_score = float(probability_score) if probability_score is not None else None

    return {"prediction": encoder_prediction, "model_used": selected_model,"probability_score": probability_score}
    
   




