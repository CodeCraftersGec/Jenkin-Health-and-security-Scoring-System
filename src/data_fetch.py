import yfinance as yf
import os

def fetch_dogecoin_data():
    os.makedirs('data', exist_ok=True)
    data = yf.download('DOGE-USD', start='2020-01-01', end='2025-11-01')
    data.to_csv('data/dogecoin_data.csv')
    print("Data fetched and saved to data/dogecoin_data.csv")

if __name__ == "__main__":
    fetch_dogecoin_data()
