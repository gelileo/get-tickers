# Stock Ticker Dataset

This assumes you have python3 installed on your system.

### Install Dependenies

```
    pip3 install -r ./requirements.txt
```

### Run

##### Pull S&P 500 tickers and corresponding company names and output to `spy_companies.json`

```
 python3 gettickers.py spy
```

##### Pull S&P 500 tickers only and output to `spy_tickers.csv`

```
python3 gettickers.py spy --format=csv --file=spy_tickers.csv --ticker-only
```

##### Pull Nasdaq-100 tickers

Similary to SPY, you can use the following commands to pull NDX tickers

```
 python3 gettickers.py ndex
```

or

```
python3 gettickers.py ndx --format=csv --file=ndx_tickers.csv --ticker-only
```

##### Pull all listings on NYSE and NASDAQ

```
python3 gettickers.py all

```

This pulls creates a number of files shows ETFs and Stocks respective, in both CSV and JSON format.

Each file contains 'symbol' and 'name' columns or keys.

`listing_status.csv` is the raw file that contains all the listings with additional information like exchange and IPO date etc.

```
    .
    ├── etf.csv
    ├── etf.json
    ├── listing_status.csv
    ├── stock.csv
    └── stock.json
```
