"""
src/factor_lib/momentum.py

Purpose: This module contains functions to calculate momentum-based factors for equities.
"""
import pandas as pd
import numpy as np
from typing import List, Optional

import sys, os 
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.backtester.engine import Backtester
def calculate_momentum(df: pd.DataFrame, window: int = 90) -> pd.Series:
    """
    Calculate the momentum factor as the percentage change over a specified window.

    Args:
        df (pd.DataFrame): DataFrame containing 'Close' prices.
        window (int): The lookback period for momentum calculation.

    Returns:
        pd.Series: Momentum values.
    """
    momentum = df['Close'].pct_change(periods=window)
    return momentum
def rank_stocks_by_momentum(df: pd.DataFrame, momentum_col: str) -> pd.Series:
    """
    Rank stocks based on their momentum values.
    Args:
        df (pd.DataFrame): DataFrame containing momentum values.
        momentum_col (str): The column name for momentum values.
    Returns:
        pd.Series: Ranks of stocks based on momentum.
    """
    ranks = df[momentum_col].rank(ascending=False)
    return ranks
def generate_momentum_signal(df: pd.DataFrame, momentum_col: str, threshold: Optional[float] = None) -> pd.Series:
    """
    Generate trading signals based on momentum ranks.

    Args:
        df (pd.DataFrame): DataFrame containing momentum ranks.
        momentum_col (str): The column name for momentum ranks.
        threshold (Optional[float]): If provided, only generate signals for ranks above this threshold.

    Returns:
        pd.Series: Trading signals (1 for buy, -1 for sell, 0 for hold).
    """
    signals = pd.Series(0, index=df.index)
    if threshold is not None:
        signals[df[momentum_col] <= threshold] = 1  # Buy signal
        signals[df[momentum_col] > threshold] = -1  # Sell signal
    else:
        median_rank = df[momentum_col].median()
        signals[df[momentum_col] < median_rank] = 1  # Buy signal
        signals[df[momentum_col] > median_rank] = -1  # Sell signal
    return signals

def apply_momentum_strategy(df: pd.DataFrame, window: int = 90, threshold: Optional[float] = None) -> pd.DataFrame:
    """
    Apply the full momentum strategy: calculate momentum, rank stocks, and generate signals.

    Args:
        df (pd.DataFrame): DataFrame containing 'Close' prices.
        window (int): The lookback period for momentum calculation.
        threshold (Optional[float]): If provided, only generate signals for ranks above this threshold.

    Returns:
        pd.DataFrame: DataFrame with added columns for momentum, ranks, and signals.
    """
    df = df.copy()
    df['Momentum'] = calculate_momentum(df, window)
    df['Momentum_Rank'] = rank_stocks_by_momentum(df, 'Momentum')
    df['Signal'] = generate_momentum_signal(df, 'Momentum_Rank', threshold)
    return df

class MomentumBacktester(Backtester):
    def __init__(self, data: pd.DataFrame, initial_balance: float = 10000):
        """
        Initializes the backtester with data and initial balance.
        Args:
            data (pd.DataFrame): DataFrame containing 'Close' prices and momentum signals.
            initial_balance (float): Starting balance for the backtest.
        """
        super().__init__(data, initial_balance)
        self.generate_signals()
        self.execute_trades()
    def generate_signals(self):
        """
        Overrides the base method to use momentum signals.
        """
        if 'Signal' not in self.data.columns:
            raise ValueError("Data must contain a 'Signal' column for momentum strategy.")
        # Signals are already generated in the data
        self.data['Signal'] = self.data['Signal'].fillna(0).astype(int)
    def execute_trades(self):
        """
        Executes trades based on momentum signals.
        """
        super().execute_trades()
        # Additional logging or metrics specific to momentum strategy can be added here
        print(f"Final Balance after Momentum Strategy: {self.balance}")
        print(f"Total Trades Executed: {len(self.trades)}")
        if self.trades:
            print(f"First Trade: {self.trades[0]}")
            print(f"Last Trade: {self.trades[-1]}")

if __name__ == "__main__":
    # Example usage
    import yfinance as yf

    # Download sample data
    ticker = "AAPL"
    df = yf.download(ticker, start="2020-01-01", end="2023-01-01")
    
    # Flatten column names if they are MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    
    # Apply momentum strategy
    processed_df = apply_momentum_strategy(df, window=90)
    
    # Initialize and run backtester
    backtester = MomentumBacktester(processed_df)
    total_return, portfolio_value = backtester.run_backtest()
    print(f"Total Return from Momentum Strategy: {total_return * 100:.2f}%")