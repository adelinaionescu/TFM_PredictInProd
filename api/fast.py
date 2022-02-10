from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
import pandas as pd
from google.cloud import storage
import joblib
import pandas as pd
from tempfile import TemporaryFile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(pickup_datetime
,pickup_longitude,pickup_latitude
,dropoff_longitude,dropoff_latitude,passenger_count
):
    key = "2013-07-06 17:18:00.000000119"

    BUCKET_NAME = 'wagon-data-739-ionescu'
    STORAGE_LOCATION = 'models/taxifare/v2/model.joblib'

    #convert datetime
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

    X_pred = pd.DataFrame({
        "key":[key],
        "pickup_datetime":[formatted_pickup_datetime],
        "pickup_longitude": [pickup_longitude],
        "pickup_latitude": [pickup_latitude],
        "dropoff_longitude": [dropoff_longitude],
        "dropoff_latitude": [dropoff_latitude],
        "passenger_count": [int(passenger_count)]})

    
    #storage_client = storage.Client()
    #bucket_name=BUCKET_NAME
    
    #bucket = storage_client.get_bucket(bucket_name)
    #blob = bucket.blob(STORAGE_LOCATION)
    #with TemporaryFile() as temp_file:
    #download blob into temp file
        #blob.download_to_file(temp_file)
        #temp_file.seek(0)
    #load into joblib
    pipeline =joblib.load("model.joblib")
    y_pred = pipeline.predict(X_pred)
    return{
        "fare": y_pred[0]
        #"pickup_longitude": pickup_longitude,
        #"pickup_latitude": pickup_latitude,
        #"dropoff_longitude": dropoff_longitude,
        #"dropoff_latitude": dropoff_latitude,
        #"passenger_count": passenger_count
        }


