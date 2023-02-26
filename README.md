# Python-Home Assignment

# Description
This repository contains code that fetches the stock data for IBM and Apple using a free API provider called '[Alpha Vantage](https://www.alphavantage.co/documentation/)'
It then displays general information which is divided into a number of pages that can viewed from the browser. It also summarizes the most important parameters in the form of statistical values, which can also be viewed from the browser.

# Requirements
To test the code locally, make sure your machine meets the requirements by installing the following packages:

Target OS:
	
	Description:	Ubuntu 22.04.2 LTS
    Release:	22.04
    Codename:	jammy    
	
Run:
```bash
pip3 install alpha_vantage
sudo apt install libpq-dev
pip3 install psycopg2
sudo apt update
sudo apt install postgresql postgresql-contrib

pip3 install Flask
pip3 install flask-restful
```
After the installation, make sure to start postgresql server:
```bash
sudo systemctl start postgresql.service
```

## Task 1: Fetch and store stock data:
`get_raw_data.py` fetches the raw data for IBM and Apple within the last two weeks. Once the raw data is fetched, it is processed locally into a json and csv file, and then stored in a local database.

(1) Create local database nemaed: `local_db`
```bash
sudo -i -u postgres
create database local_db;
\q #quit the psql prompt
```
(2) Then add a new table named `financial_data` defined in `schema.sql`:
```bash
psql -U postgres -d <DATABASE-NAME> -f <Full path to schema.sql file>/schema.sql
```
