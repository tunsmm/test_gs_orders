FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py app.py
RUN EXPORT FLASK_APP=app.py
RUN flask run