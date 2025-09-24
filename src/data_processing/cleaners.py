"""
src/data_processing/cleaners.py

Purpose: This module contains functions for cleaning and preprocessing financial data.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def download_raw_data(ticker: str, start_date : str, end_date :str) -> pd.DataFrame:
    """
    Downloads raw financial data from Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date for data in 'YYYY-MM-DD' format.
        end_date (str): End date for data in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: Raw financial data.
    """
    df = yf.download(ticker, start=start_date, end=end_date)
    if df is not None and not df.empty:
        # Flatten multi-level columns if they exist
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Use absolute path for saving
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        raw_data_path = os.path.join(script_dir, "data", "raw", f"{ticker}_raw.csv")
        df.to_csv(raw_data_path)
        return df
    else:
     return pd.DataFrame()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the financial data by handling missing values and removing duplicates.

    Args:
        df (pd.DataFrame): Raw financial data.
    Returns:
        pd.DataFrame: Cleaned financial data.
    """
    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values by forward filling
    df = df.ffill().bfill()

    # Ensure the index is a datetime index
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index)

    return df

def add_technical_indicators(df: pd.DataFrame, long : int, short: int) -> pd.DataFrame:
    """
    Adds technical indicators to the financial data.

    Args:
        df (pd.DataFrame): Cleaned financial data.
        long (int): Long window for moving average.
        short (int): Short window for moving average.

    Returns:
        pd.DataFrame: Financial data with technical indicators.
    """
    # Calculate moving averages
    df[f'MA_{long}'] = df['Close'].rolling(window=long).mean()
    df[f'MA_{short}'] = df['Close'].rolling(window=short).mean()

    # Calculate daily returns
    df['Daily_Return'] = df['Close'].pct_change()

    # Calculate volatility (standard deviation of daily returns)
    df['Volatility'] = df['Daily_Return'].rolling(window=short).std()

    return df

def preprocess_data(ticker: str, start_date: str, end_date: str, long: int = 50, short: int = 20) -> pd.DataFrame:
    """
    Preprocesses the financial data by downloading, cleaning, and adding technical indicators.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date for data in 'YYYY-MM-DD' format.
        end_date (str): End date for data in 'YYYY-MM-DD' format.
        long (int): Long window for moving average.
        short (int): Short window for moving average.

    Returns:
        pd.DataFrame: Preprocessed financial data.
    """
    raw_data = download_raw_data(ticker, start_date, end_date)
    if raw_data.empty:
        return pd.DataFrame()
    
    cleaned_data = clean_data(raw_data)
    processed_data = add_technical_indicators(cleaned_data, long, short)
    
    # Use absolute path for saving
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    processed_data_path = os.path.join(script_dir, "data", "processed", f"{ticker}_processed.parquet")
    processed_data.to_parquet(processed_data_path)
    return processed_data

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2023-01-01"
    processed_df = preprocess_data(ticker, start_date, end_date)
    print(processed_df.head())
