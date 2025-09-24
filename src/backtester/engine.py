"""
src/backtester/engine.py

Purpose: This module contains the backtesting engine for evaluating trading strategies.
"""
import pandas as pd
import numpy as np
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

class Backtester:
    def __init__(self, data: pd.DataFrame, initial_balance: float = 10000.0):
        """
        Initializes the backtester with financial data and initial balance.

        Args:
            data (pd.DataFrame): Financial data with technical indicators.
            initial_balance (float): Starting balance for the backtest.
        """
        self.data = data
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # 1 for long, -1 for short, 0 for no position
        self.trades = []

    def generate_signals(self):
        """
        Generates trading signals based on technical indicators.
        """
        self.data['Signal'] = 0
        # Assuming default MA columns (MA_20 for short, MA_50 for long)
        short_ma = 'MA_20'
        long_ma = 'MA_50'
        
        # Check if columns exist, otherwise use the first two MA columns found
        ma_columns = [col for col in self.data.columns if col.startswith('MA_')]
        if len(ma_columns) >= 2:
            # Sort to get consistent ordering
            ma_columns.sort(key=lambda x: int(x.split('_')[1]))
            short_ma = ma_columns[0]  # shorter period first
            long_ma = ma_columns[1]   # longer period second
            
        self.data.loc[self.data[short_ma] > self.data[long_ma], 'Signal'] = 1
        self.data.loc[self.data[short_ma] < self.data[long_ma], 'Signal'] = -1

    def execute_trades(self):
        """
        Executes trades based on generated signals.
        """
        for index, row in self.data.iterrows():
            # Ensure we have scalar values for signal
            try:
                signal = row['Signal']
                if hasattr(signal, 'iloc'):  # If it's a Series, get the first value
                    signal = signal.iloc[0] if len(signal) > 0 else 0
                
                close_price = row['Close']
                if hasattr(close_price, 'iloc'):  # If it's a Series, get the first value  
                    close_price = close_price.iloc[0] if len(close_price) > 0 else 0
                    
            except (KeyError, IndexError):
                continue
            
            # Skip if signal is NaN
            if pd.isna(signal):
                continue
                
            signal = int(signal) if not pd.isna(signal) else 0
                
            if signal == 1 and self.position <= 0:  # Buy signal
                self.trades.append((index, 'BUY', close_price))
                self.position = 1
                self.balance -= close_price
            elif signal == -1 and self.position >= 0:  # Sell signal
                if self.position == 1:
                    self.trades.append((index, 'SELL', close_price))
                    self.balance += close_price
                self.position = -1
                self.balance += close_price
                self.balance -= close_price
                self.position = -1
            elif signal == 0 and self.position != 0:  # Close position
                if self.position == 1:
                    self.trades.append((index, 'SELL', close_price))
                    self.balance += close_price
                elif self.position == -1:
                    self.trades.append((index, 'BUY', close_price))
                    self.balance -= close_price
                self.position = 0

    def calculate_performance(self):
        """
        Calculates the performance of the backtest.
        """
        self.data['Portfolio Value'] = self.initial_balance
        for trade in self.trades:
            date, action, price = trade
            if action == 'BUY':
                self.balance -= price
            elif action == 'SELL':
                self.balance += price
            self.data.loc[date:, 'Portfolio Value'] = self.balance

        total_return = (self.balance - self.initial_balance) / self.initial_balance
        return total_return, self.data['Portfolio Value']

    def monte_carlo_backtest(self, n_simulations: int = 100000):
        """
        Performs Monte Carlo simulations to evaluate strategy robustness.

        Args:
            n_simulations (int): Number of Monte Carlo simulations to run.

        Returns:
            list: List of total returns from each simulation.
        """
        returns = []
        for _ in range(n_simulations):
            shuffled_data = self.data.sample(frac=1).reset_index(drop=True)
            self.__init__(shuffled_data, self.initial_balance)
            self.generate_signals()
            self.execute_trades()
            total_return, _ = self.calculate_performance()
            returns.append(total_return)
        return returns

    def forward_test(self, new_data: pd.DataFrame):
        """
        Performs forward testing on new data.

        Args:
            new_data (pd.DataFrame): New financial data for forward testing.

        Returns:
            float: Total return from the forward test.
        """
        self.__init__(new_data, self.initial_balance)
        self.generate_signals()
        self.execute_trades()
        total_return, _ = self.calculate_performance()
        return total_return
   
    def run_backtest(self):
        """
        Runs the complete backtest process.

        Returns:
            tuple: Total return and portfolio value over time.
        """
        self.generate_signals()
        self.execute_trades()
        return self.calculate_performance()

if __name__ == "__main__":
    from src.data_processing import cleaners

    # Example usage
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2023-01-01"
    processed_df = cleaners.preprocess_data(ticker, start_date, end_date)
    if processed_df.empty:
        print("No data available for backtesting.")
    else:
        backtester = Backtester(processed_df)
        total_return, portfolio_value = backtester.run_backtest()
        print(f"Total Return: {total_return * 100:.2f}%")
    