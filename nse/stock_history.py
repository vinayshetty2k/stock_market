from packages.nse import Nse
import sys
import pprint

def main():
    date = sys.argv[1]
    try:
        instrument_type = sys.argv[2]
    except:
        instrument_type = None
    nse = Nse()
    try:
        stock_data = nse.download_bhavcopy(date, instrument_type)
        pprint.pprint(stock_data)
    except:
        print("")


main()
