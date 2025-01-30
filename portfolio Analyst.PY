import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import minimize

# Sample bond portfolio data
bonds = pd.DataFrame({
    'Bond': ['Bond A', 'Bond B', 'Bond C'],
    'Face Value': [1000000, 500000, 750000],
    'Coupon Rate': [0.05, 0.045, 0.06],
    'Maturity (Years)': [5, 7, 10],
    'Market Price': [980000, 510000, 740000],
    'Yield to Maturity': [0.052, 0.047, 0.059]
})

# Calculate Annual Coupon Payments
bonds['Annual Coupon Payment'] = bonds['Face Value'] * bonds['Coupon Rate']

# Fixed Macaulay Duration Function
def macaulay_duration(face, coupon_rate, ytm, maturity):
    time_periods = np.arange(1, maturity + 1)  # Ensure correct length
    cash_flows = np.array([face * coupon_rate] * (maturity - 1) + [face * (1 + coupon_rate)])  # Adjusted final payment
    present_values = cash_flows / (1 + ytm) ** time_periods
    return np.sum(time_periods * present_values) / np.sum(present_values)

# Apply the function correctly
bonds['Duration'] = bonds.apply(lambda x: macaulay_duration(
    x['Face Value'], x['Coupon Rate'], x['Yield to Maturity'], int(x['Maturity (Years)'])), axis=1)

# Portfolio Duration (Weighted Average of Bond Durations)
portfolio_value = bonds['Market Price'].sum()
bonds['Weight'] = bonds['Market Price'] / portfolio_value
portfolio_duration = np.sum(bonds['Weight'] * bonds['Duration'])

# Display Portfolio Summary
print("\nBond Portfolio Summary:")
print(bonds[['Bond', 'Market Price', 'Annual Coupon Payment', 'Duration', 'Weight']])
print(f"\nTotal Portfolio Duration: {portfolio_duration:.2f} years")

# Visualizing Portfolio Composition
plt.figure(figsize=(8, 5))
plt.pie(bonds['Weight'], labels=bonds['Bond'], autopct='%1.1f%%', startangle=140)
plt.title("Portfolio Allocation by Market Value")
plt.show()

# Yield Curve Analysis (Fetching Treasury Yields)
tickers = ["^TNX", "^FVX", "^TYX"]  # 10-year, 5-year, and 30-year yields
data = yf.download(tickers, period="1y")['Adj Close']
data.plot(figsize=(10, 5), title="US Treasury Yield Curve Movements")
plt.xlabel("Date")
plt.ylabel("Yield (%)")
plt.grid()
plt.show()
