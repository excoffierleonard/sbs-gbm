from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


# Function to fetch historical data and calculate mu and sigma
def calculate_parameters(ticker, start_date, end_date):
    # Fetching historical stock data
    data = yf.download(ticker, start=start_date, end=end_date)

    # Calculate daily returns
    data["Return"] = data["Adj Close"].pct_change()

    # Drop NaN values after pct_change
    returns = data["Return"].dropna()

    # Calculate the mean (mu) and standard deviation (sigma) of daily returns
    mu_daily = returns.mean()
    sigma_daily = returns.std()

    # Annualize the daily mean return and standard deviation
    trading_days = 252  # Number of trading days in a year
    mu_annual = (1 + mu_daily) ** trading_days - 1
    sigma_annual = sigma_daily * np.sqrt(trading_days)

    return mu_annual, sigma_annual, data["Adj Close"].iloc[-1]


# Function to simulate future stock prices
def simulate_stock_price(S0, mu, sigma, T, N):
    dt = T / N
    Z = np.random.standard_normal(N)  # Standard normal random variables
    S = np.zeros(N + 1)
    S[0] = S0
    for t in range(1, N + 1):
        S[t] = S[t - 1] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[t - 1]
        )
    return S


# Main function
def main():
    # User input
    ticker = input("Enter the stock ticker: ").strip()

    # Default start date (5 years ago) and end date (most recent)
    default_end_date = datetime.today().date()
    default_start_date = default_end_date - timedelta(days=5 * 365)

    start_date = input(
        f"Enter start date for historical data (YYYY-MM-DD) [default: {default_start_date}]: "
    ).strip()
    end_date = input(
        f"Enter end date for historical data (YYYY-MM-DD) [default: {default_end_date}]: "
    ).strip()

    # Use default dates if the input fields are empty
    if not start_date:
        start_date = default_start_date
    if not end_date:
        end_date = default_end_date

    # Calculate parameters
    mu, sigma, S0 = calculate_parameters(ticker, start_date, end_date)

    # Display the calculated parameters
    print(f"Annualized Mean Return (mu): {mu:.4f}")
    print(f"Annualized Volatility (sigma): {sigma:.4f}")
    print(f"Most Recent Closing Price: {S0:.2f}")

    # Prompt for the prediction period in days
    default_prediction_days = 5 * 252  # Default: 1260 days (5 years)
    prediction_days_input = input(
        f"Enter the prediction period in days [default: {default_prediction_days}]: "
    ).strip()
    prediction_days = (
        int(prediction_days_input) if prediction_days_input else default_prediction_days
    )

    # Set the time period and number of steps
    T = prediction_days / 252  # Time period in years
    N = prediction_days  # Number of steps (days to project)

    # Simulate future stock prices
    future_prices = simulate_stock_price(S0, mu, sigma, T, N)

    # Generate dates for the x-axis
    future_dates = [default_end_date + timedelta(days=i) for i in range(N + 1)]

    # Plot the stock price path
    plt.figure(figsize=(10, 6))
    plt.plot(future_dates, future_prices)
    plt.title(f"Stock Price Simulation for {ticker} using GBM")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.grid(True)
    plt.gcf().autofmt_xdate()  # Auto-format the x-axis to show dates nicely
    plt.show()


# Run the program
if __name__ == "__main__":
    main()
