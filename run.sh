#!/bin/bash
# This script is used to run the program

set -euo pipefail

echo "Fetch SPY tickers ..."
# python3 gettickers.py spy

# python3 gettickers.py spy --format=csv --file=spy_tickers.csv --ticker-only

echo "Fetch NDX tickers ..."
python3 gettickers.py ndx

python3 gettickers.py ndx --format=csv --file=ndx_tickers.csv --ticker-only

echo "Fetch all tickers ..."
python3 gettickers.py all