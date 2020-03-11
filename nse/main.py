from packages.nse import Nse
import pandas as pd
from datetime import datetime

log = open("log.txt", "a+")
log.write("Log as on %s\n"%datetime.now())
nse = Nse()


def all_stock_details():
    stock_list = nse.get_stock_codes()
    stock_list_data = []
    for index, stock in enumerate(stock_list):
        if index:
            try:
                stock_data = nse.get_quote(stock)
                stock_list_data.append(stock_data)
            except Exception as error:
                log.write("Couldn't fetch stock details for %s\n" % stock)

    df = pd.DataFrame(stock_list_data)
    df.to_excel('stocks_price.xlsx')
    log.write("\n")
    log.close()


def fno_details():
    fno_list = nse.get_fno_lot_sizes()
    df = pd.Series(fno_list, name ='Lot')
    df.index.name = "Company Name"
    df.to_excel('fno_lot.xlsx')


fno_details()