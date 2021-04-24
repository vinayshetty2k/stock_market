from packages.nse import Nse
import sys
import datetime
import calendar
from packages.connect_db import ConnectMethods
import os, os.path
import glob
import pandas as pd


def main():
    try:
        nse = Nse()
        path = r'%s'%sys.argv[1].strip()  
        instrument_type = sys.argv[2].strip()
        process = sys.argv[3].strip()
        classRef = ConnectMethods()
        log_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bhavcopy_download.log'), 'w')
        if process == 'download':
            start_date = sys.argv[4].strip()
            if start_date == 'False':    start_date = False
            end_date = sys.argv[5].strip()
            if end_date == 'False':  end_date = False
            if not start_date:
                try:
                    if instrument_type == "cash":
                        query = "SELECT MAX(trd_date) FROM historical_data;"
                    else:
                        query = "SELECT MAX(trd_date) FROM future_historical_data;"
                    result = classRef.retrieve_data(query)
                    start_date = result[0][0]
                except:
                    start_date = False
                if not start_date:  start_date = datetime.date(2016, 1, 1)
            else:
                start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').date()

            if not end_date:    
                end_date = datetime.date.today()
            else:
                end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()
            delta = datetime.timedelta(days=1)
            while start_date < end_date:
                try:
                    market_open = True
                    nse.save_bhavcopy(start_date, instrument_type, path)
                except Exception as err:
                    market_open = False
                    day_name = start_date.strftime("%A")
                    if (day_name not in ['Saturday', 'Sunday']):
                        log_file.write(f'Market closed om {start_date}')
                        print(err)

########################### INDEX ######################################################
                if instrument_type == 'cash' and market_open:
                    url = f'https://www1.nseindia.com/content/indices/ind_close_all_{start_date.strftime("%d%m%Y")}.csv'
                    nse_data = nse.get_csv_data(url)
                    if nse_data:
                        df = pd.read_csv(nse_data)
                        values = ""
                        for pos in range(len(df)):
                            for i in range(2, len(df.columns)):
                                if df.iloc[pos, i] == '-' or df.iloc[pos, i] == '' or pd.isna(df.iloc[pos, i]):
                                    df.iloc[pos, i] = 'NULL'
                            value =  ', '.join(str(df.iloc[pos, i]) for i in range(2, len(df.columns)))
                            try:
                                date = datetime.datetime.strptime(df.iloc[pos, 1], '%d-%m-%Y').date()
                            except:
                                date = datetime.datetime.strptime(df.iloc[pos, 1], '%d/%m/%Y').date()
                            value =  f"('{df.iloc[pos, 0]}', to_date('{date}', 'YYYY-MM-DD'), {value})"
                                
                            if values:
                                values = values + ', ' + value 
                            else:
                                values = value
                        query = '''INSERT INTO index_data VALUES %s'''%values
                        classRef.insert_data(query)
##################################################################################            
                start_date += delta
            log_file.close()
        elif process == 'update':
            if instrument_type == "cash":
                query = '''COPY historical_data FROM '%s' DELIMITER ',' CSV HEADER;'''
            else:
                query = '''COPY future_historical_data FROM '%s' DELIMITER ',' CSV HEADER;'''

            classRef.populate_data(query, os.path.join(path, "*"))

            if instrument_type == "/DERIVATIVES/":  # removing option data
                query = '''DELETE FROM future_historical_data WHERE instrument = 'OPTIDX' OR instrument = 'OPTSTK';'''
                classRef.delete_data(query)
        elif process == 'retrieve':
            query = sys.argv[4].strip()
            filePath = sys.argv[5].strip()
            stock_list = open(filePath, "r").read()
            query = f'{query}'%(stock_list)
            db_data = classRef.retrieve_data(query)
            if path:
                df = pd.DataFrame(db_data)
                df.to_excel(path, index=False)
            else:
                print(db_data)
                return db_data
    except Exception as err:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        print(exception_traceback.tb_lineno)
main()
