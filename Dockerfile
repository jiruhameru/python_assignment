FROM python:3.9-slim 
LABEL developer="zalhamer@gmail.com"
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN PYTHONPATH=/usr/bin/python3 pip3 install -r requirements.txt

COPY . .

EXPOSE 5000:5000

CMD ["python", "./financial/get_financial_data_API.py"]
