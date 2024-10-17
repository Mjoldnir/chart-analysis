import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.dates import date2num

# Download historical data for S&P 500
df = yf.download("^SPX", start="2011-01-01", end="2026-01-10")
df = df.reset_index()

# Gann Swing Indicator function
def gann_swing_long_term(df, swing_period=150):
    df['SwingHigh'] = False
    df['SwingLow'] = False
    last_swing = None
    for i in range(swing_period, len(df) - swing_period):
        current_high = df['High'].iloc[i]
        current_low = df['Low'].iloc[i]
        if current_high == max(df['High'].iloc[i - swing_period:i + swing_period + 1]):
            if last_swing != 'high':
                df.at[i, 'SwingHigh'] = True
                last_swing = 'high'
        if current_low == min(df['Low'].iloc[i - swing_period:i + swing_period + 1]):
            if last_swing != 'low':
                df.at[i, 'SwingLow'] = True
                last_swing = 'low'
    return df

# Apply Gann Swing Indicator
df = gann_swing_long_term(df, swing_period=100)

# Manually adjust swing dates
df.loc[df['Date'] == pd.to_datetime('2018-01-26'), 'SwingHigh'] = False
df.loc[df['Date'] == pd.to_datetime('2018-09-21'), 'SwingHigh'] = True

# Get swing points
swing_points = df[(df['SwingHigh']) | (df['SwingLow'])].copy()
swing_highs = df[df['SwingHigh']]
swing_lows = df[df['SwingLow']]

# Plot data
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Close'], label='Close Price', color='blue')

# Grey shading for 7 years up to September 21, 2018
end_date = pd.to_datetime('2018-09-21')
start_date = end_date - pd.DateOffset(years=7)
plt.axvspan(date2num(start_date), date2num(end_date), color='lightgrey', alpha=0.5)

# Double arrow from grey shading end date, 7 years forward, with annotation
arrow_start_date = pd.to_datetime('2018-09-21')
arrow_end_date = arrow_start_date + pd.DateOffset(years=7)
arrow_y_position = 1600 #df['Close'].max() + 100  # Position arrow above max price for visibility

plt.annotate(
    '', xy=(date2num(arrow_end_date), arrow_y_position), xytext=(date2num(arrow_start_date), arrow_y_position),
    arrowprops=dict(arrowstyle='<->', color='black')
)
midpoint_arrow_date = arrow_start_date + (arrow_end_date - arrow_start_date) / 2
plt.text(midpoint_arrow_date, arrow_y_position + 14, '7 years', ha='center', fontsize=10)


# Double arrow from grey shading end date, 7 years forward, with annotation

arrow_end_date = pd.to_datetime('2018-09-21')
arrow_start_date = arrow_end_date- pd.DateOffset(years=7)
arrow_y_position = 4000 #df['Close'].max() + 100  # Position arrow above max price for visibility

plt.annotate(
    '', xy=(date2num(arrow_end_date), arrow_y_position), xytext=(date2num(arrow_start_date), arrow_y_position),
    arrowprops=dict(arrowstyle='<->', color='black')
)
midpoint_arrow_date = arrow_start_date + (arrow_end_date - arrow_start_date) / 2
plt.text(midpoint_arrow_date, arrow_y_position + 14, '7 years', ha='center', fontsize=10)


# Adjust Y-limits to fit the annotation within the plot
plt.ylim(df['Close'].min() - 100, df['Close'].max() + 200)

# Set X-limits to extend to the end of 2026
plt.xlim([df['Date'].min(), pd.to_datetime('2026-12-31')])

# Mark Swing Highs and Swing Lows
plt.scatter(swing_highs['Date'], swing_highs['High'], color='green', marker='^', label='Swing High', s=100)
plt.scatter(swing_lows['Date'], swing_lows['Low'], color='red', marker='v', label='Swing Low', s=100)

# Annotate swing dates
for i in range(len(swing_highs)):
    plt.text(swing_highs['Date'].iloc[i], swing_highs['High'].iloc[i], swing_highs['Date'].iloc[i].strftime('%Y-%m-%d'),
             fontsize=8, color='green', rotation=45)
for i in range(len(swing_lows)):
    plt.text(swing_lows['Date'].iloc[i], swing_lows['Low'].iloc[i], swing_lows['Date'].iloc[i].strftime('%Y-%m-%d'),
             fontsize=8, color='red', rotation=45)

# Connect Swing Highs and Lows
for i in range(1, len(swing_points)):
    plt.plot([swing_points['Date'].iloc[i-1], swing_points['Date'].iloc[i]], 
             [swing_points['High'].iloc[i-1] if swing_points['SwingHigh'].iloc[i-1] else swing_points['Low'].iloc[i-1], 
              swing_points['High'].iloc[i] if swing_points['SwingHigh'].iloc[i] else swing_points['Low'].iloc[i]],
             color='black')

plt.title('Gann Swing Indicator for S&P 500 (2011-2026)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
