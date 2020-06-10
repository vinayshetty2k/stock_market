from packages.nse import Nse
import sys

def main():
    stock = sys.argv[1]
    nse = Nse()
    try:
        stock_data = nse.get_quote(stock)
        print(stock_data)
    except:
        print("")

main()
