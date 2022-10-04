# Implement data parsing from Google Sheet using the Google Sheets API and synchronization from the database to a Postgres table

Clone this [repository](https://github.com/tunsmm/test_gs_orders.git) to your directory

## General information

My Google Sheet - [click](https://docs.google.com/spreadsheets/d/15d4M4wpqAgbVGopxPapzHu1LO3rdZacNBSgumE8XfVQ/edit#gid=0) 

To run this application you need to add your credentials file from Google API in ./gs_project as 'creds.json' (please make sure you have Google Sheets API and Google Drive API enabled), input in:

1) 'gs_project/services/helpers.py' your Telegram bot token in 'tg_token_bot' and your Telegram chat id to 'chat_id',
2) 'gs_project/services/db.py' your database URL that looks like 'dialect+driver://username:password@host:port/database'

## Project run

1. Run venv 

```bash
python -m venv venv
source venv/Scripts/activate
```

2. Run Project by Docker

```bash
docker-compose build
docker-compose up
```

3. Go to the localhost as 127.0.0.1:5000 and check the result of work
