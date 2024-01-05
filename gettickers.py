import pandas as pd
import yfinance as yf
import json
import csv
import requests
import fire
from tqdm import tqdm
from dotenv import load_dotenv
import os

# Function to check if a ticker is active
def is_ticker_active(ticker):
    ticker_obj = yf.Ticker(ticker)
    # Fetch info, if 'regularMarketPrice' isn't there, it's likely not active or delisted
    try:
        if ticker_obj.info['regularMarketOpen'] is not None:
            return True
    except KeyError:
        return False
    return False


# Function to check if a ticker is active and fetch company name
def fetch_ticker_data(ticker):
    ticker_obj = yf.Ticker(ticker)
    try:
        info = ticker_obj.info
        # print(info)
        if info.get('regularMarketOpen') is not None:
            return {
                'symbol': ticker,
                'name': info.get('longName')
            }
    except KeyError:
        return None


def to_json(data, file, ticker_only=False):
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


def to_csv(data, file, ticker_only=False):
    with open(file, 'w', newline='') as outfile:
        if ticker_only:
            csv_columns = ['symbol']
            writer = csv.writer(outfile)
            for row in data:
                writer.writerow([row['symbol']]) # writerow expects a list
        else:
            csv_columns = ['symbol', 'name']
            writer = csv.DictWriter(outfile, fieldnames=csv_columns)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        

def get_spy(format='json', file='spy_companies.json', ticker_only=False):
    # Fetch S&P 500 ticker list
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    snp500_wiki = pd.read_html(wiki_url)
    snp500_table = snp500_wiki[0]
    tickers = snp500_table['Symbol'].tolist()

    active_tickers_data = []

    if ticker_only:
        # active_tickers_data = [{"symbol": ticker} for ticker in tickers if is_ticker_active(ticker)]
        active_tickers_data = [{"symbol": ticker} for ticker in tqdm(tickers, desc="Checking Ticker active") if is_ticker_active(ticker)]
    else:
        # Filter out inactive or delisted tickers and fetch company names
        active_tickers_data = [fetch_ticker_data(ticker) for ticker in tqdm(tickers, desc="Fetching Ticker data")]
        active_tickers_data = [data for data in active_tickers_data if data is not None]

    if format == 'json':
        to_json(active_tickers_data, file, ticker_only)
    elif format == 'csv':
        to_csv(active_tickers_data, file, ticker_only)

def get_all_listings():
    
    load_dotenv()  # Load variables from .env
    api_key = os.getenv('API_KEY')

    url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'
    r = requests.get(url)

    content_type = r.headers['Content-Type']
    if 'download' in content_type:
        filename = r.headers.get('Content-Disposition').split("filename=")[-1]
        with open(filename, 'wb') as file:
            file.write(r.content)
        print(f"File saved as {filename}")
    
        # Read the CSV data
        df = pd.read_csv(filename)

        # Filter rows where status is 'Active' and assetType is 'Stock'
        stock_data = df[(df['status'] == 'Active') & (df['assetType'] == 'Stock')]

        # Select only the 'symbol' and 'name' columns
        stock_data = stock_data[['symbol', 'name']]

        # Save to 'stocks.csv'
        stock_data.to_csv('stock.csv', index=False)

        # Convert to JSON and save to 'stock.json'
        stock_json = stock_data.to_dict(orient='records')  # Convert the DataFrame to a dictionary
        with open('stock.json', 'w') as file:
            json.dump(stock_json, file)

        # Repeat the process for ETFs

        # Filter rows where status is 'Active' and assetType is 'ETF'
        etf_data = df[(df['status'] == 'Active') & (df['assetType'] == 'ETF')]

        # Select only the 'symbol' and 'name' columns
        etf_data = etf_data[['symbol', 'name']]

        # Save to 'etfs.csv'
        etf_data.to_csv('etf.csv', index=False)

        # Convert to JSON and save to 'etf.json'
        etf_json = etf_data.to_dict(orient='records')  # Convert the DataFrame to a dictionary
        with open('etf.json', 'w') as file:
            json.dump(etf_json, file)

    else:
        print("Unexpected content typen from alphavantage:", content_type)

def get_ndx(format='json', file='ndx_companies.json', ticker_only=False):

    # Fetch S&P 500 ticker list
    wiki_url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    ndx100_wiki = pd.read_html(wiki_url)
    ndx100_table = ndx100_wiki[4]
    # print(ndx100_table)
    tickers = ndx100_table['Ticker'].tolist()

    active_tickers_data = []

    if ticker_only:
        active_tickers_data = [{"symbol": ticker} for ticker in tqdm(tickers, desc="Checking Ticker active") if is_ticker_active(ticker)]
    else:
        # Filter out inactive or delisted tickers and fetch company names
        active_tickers_data = [fetch_ticker_data(ticker) for ticker in tqdm(tickers, desc="Fetching Ticker data")]
        active_tickers_data = [data for data in active_tickers_data if data is not None]

    if format == 'json':
        to_json(active_tickers_data, file, ticker_only)
    elif format == 'csv':
        to_csv(active_tickers_data, file, ticker_only)





if __name__ == '__main__':
    fire.Fire({
        'spy': get_spy,
        'ndx': get_ndx,
        'all': get_all_listings,
    })