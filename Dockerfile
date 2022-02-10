FROM python:3.7.12-buster
COPY api /api
COPY requirements.txt /requirements.txt
COPY TaxiFareModel /TaxiFareModel
COPY model.joblib /model.joblib
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
# write some code to build your image
