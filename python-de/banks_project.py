from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime 

def extract(url, table_attribs, count):
    page = requests.get(url).text
    data = BeautifulSoup(page,'html.parser')
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    df = pd.DataFrame(columns=table_attribs)
    for row in rows:
        if count < 10 :
            col = row.find_all('td')
            if len(col)!=0:
                data_dict = {"Name": col[1].get_text(strip=True),
                            "MC_USD_Billion": float(col[2].contents[0])}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)
                count+=1
        else:
            break
    return df

def transform(df,exchng_path):
    dataframe = pd.read_csv(exchng_path)
    exchange_rates = dataframe.set_index('Currency').to_dict()['Rate']
    GDP_list = df["MC_USD_Billion"].tolist()
    df['MC_GBP_Billion'] = [np.round(x*exchange_rates['GBP'],2) for x in df['MC_USD_Billion']]
    df["MC_GBP_Billion"] = GDP_list
    df['MC_GBP_Billion'] = [np.round(x*exchange_rates['EUR'],2) for x in df['MC_USD_Billion']]
    df["MC_EUR_Billion"] = GDP_list
    df['MC_GBP_Billion'] = [np.round(x*exchange_rates['INR'],2) for x in df['MC_USD_Billion']]
    df["MC_INR_Billion"] = GDP_list
    return df

def load_to_csv(df, csv_path):
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'  
    now = datetime.now() 
    timestamp = now.strftime(timestamp_format) 
    with open("./code_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')    

url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ["Name", "MC_USD_Billion"]
db_name = '	Banks.db'
table_name = 'Largest_banks'
csv_path = './Largest_banks_data.csv'
df = pd.DataFrame(columns=["Name","MC_USD_Billion"])
count = 0
exchng_path = 'exchange_rate.csv'

log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url, table_attribs, count)

log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df, exchng_path)

log_progress('Data transformation complete. Initiating loading process')

load_to_csv(df, csv_path)

log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect('World_Economies.db')

log_progress('SQL Connection initiated.')

load_to_db(df, sql_connection, table_name)

log_progress('Data loaded to Database as table. Running the query')

query_statement = f"SELECT * FROM Largest_banks"
run_query(query_statement, sql_connection)

log_progress('Data loaded to Database as table. Running the second query')

query_statement = f"SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_query(query_statement, sql_connection)

log_progress('Data loaded to Database as table. Running the third query')

query_statement = f"SELECT Name from Largest_banks LIMIT 5"
run_query(query_statement, sql_connection)

log_progress('Process Complete.')

sql_connection.close()






