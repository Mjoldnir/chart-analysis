import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.dates import date2num

# Download historical data for S&P 500
df = yf.download("^SPX", start="1955-01-01", end="1975-01-10")

# Reset index to make the Date a regular column
df = df.reset_index()

# Gann Swing Indicator for long-term swing highs and lows, focusing on major extremes
def gann_swing_long_term(df, swing_period=150):
    """
    Identifies long-term swing highs and lows by looking at 
    price changes over a larger window defined by swing_period.
    Focuses on catching major price movements over long periods.
    """
    # Initialize SwingHigh and SwingLow columns
    df['SwingHigh'] = False
    df['SwingLow'] = False

    last_swing = None
    
    for i in range(swing_period, len(df) - swing_period):
        current_high = df['High'].iloc[i]
        current_low = df['Low'].iloc[i]
        
        # Detect major swing high (based on price extremes in the window)
        if current_high == max(df['High'].iloc[i - swing_period:i + swing_period + 1]):
            if last_swing != 'high':  # Only mark if not consecutively high
                df.at[i, 'SwingHigh'] = True
                last_swing = 'high'
        
        # Detect major swing low (based on price extremes in the window)
        if current_low == min(df['Low'].iloc[i - swing_period:i + swing_period + 1]):
            if last_swing != 'low':  # Only mark if not consecutively low
                df.at[i, 'SwingLow'] = True
                last_swing = 'low'

    return df

# Apply the Gann Swing Indicator with a longer period for long-term swings
df = gann_swing_long_term(df, swing_period=150)  # Larger swing period for long-term trends

# Filter the DataFrame to get only the points where swing highs and lows exist
swing_points = df[(df['SwingHigh']) | (df['SwingLow'])].copy()

# Define swing highs and swing lows
swing_highs = df[df['SwingHigh'] == True]
swing_lows = df[df['SwingLow'] == True]

# Plotting the price and long-term swing points
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Close'], label='Close Price', color='blue')

# Add light grey shading between 1957-10-22 and 1966-02-09
start_date = pd.to_datetime('1957-10-22')
end_date = pd.to_datetime('1966-02-09')
plt.axvspan(date2num(start_date), date2num(end_date), color='lightgrey', alpha=0.5)

# Add an arrow from 7 years before 1966-02-09 to 1966-02-09
start_arrow_date = pd.to_datetime('1966-02-09') - pd.DateOffset(years=7)
end_arrow_date = pd.to_datetime('1966-02-09')

# Adding the first arrow and label "7 years" at y-value 100
plt.annotate(
    '', xy=(date2num(end_arrow_date), 100), xytext=(date2num(start_arrow_date), 100),
    arrowprops=dict(arrowstyle='<->', color='black')
)

# Add label "7 years"
midpoint_date = start_arrow_date + (end_arrow_date - start_arrow_date) / 2
plt.text(midpoint_date, 105, '7 years', ha='center', fontsize=10)

# Add a second arrow from 1966-02-09 to 7 years into the future
start_arrow_future_date = pd.to_datetime('1966-02-09')
end_arrow_future_date = start_arrow_future_date + pd.DateOffset(years=7)

# Adding the second arrow and label "7 years" at y-value 50
plt.annotate(
    '', xy=(date2num(end_arrow_future_date), 50), xytext=(date2num(start_arrow_future_date), 50),
    arrowprops=dict(arrowstyle='<->', color='black')
)

# Add label "7 years" for the second arrow
midpoint_future_date = start_arrow_future_date + (end_arrow_future_date - start_arrow_future_date) / 2
plt.text(midpoint_future_date, 55, '7 years', ha='center', fontsize=10)

# Mark Swing Highs and Swing Lows
plt.scatter(df['Date'][df['SwingHigh']], df['High'][df['SwingHigh']], color='green', marker='^', label='Swing High', s=100)
plt.scatter(df['Date'][df['SwingLow']], df['Low'][df['SwingLow']], color='red', marker='v', label='Swing Low', s=100)

# Annotate the Swing Highs and Lows with their respective dates
for i in range(len(swing_highs)):
    plt.text(swing_highs['Date'].iloc[i], swing_highs['High'].iloc[i], swing_highs['Date'].iloc[i].strftime('%Y-%m-%d'),
             fontsize=8, color='green', rotation=45)

for i in range(len(swing_lows)):
    plt.text(swing_lows['Date'].iloc[i], swing_lows['Low'].iloc[i], swing_lows['Date'].iloc[i].strftime('%Y-%m-%d'),
             fontsize=8, color='red', rotation=45)

# Connect the Swing Highs and Lows with straight lines
for i in range(1, len(swing_points)):
    plt.plot([swing_points['Date'].iloc[i-1], swing_points['Date'].iloc[i]], 
             [swing_points['High'].iloc[i-1] if swing_points['SwingHigh'].iloc[i-1] else swing_points['Low'].iloc[i-1], 
              swing_points['High'].iloc[i] if swing_points['SwingHigh'].iloc[i] else swing_points['Low'].iloc[i]],
             color='black')

# Find the swing low on 1957-10-22 and swing high on 1966-02-09
low_point = df[df['Date'] == pd.to_datetime('1957-10-22')]['Low'].values[0]
high_point = df[df['Date'] == pd.to_datetime('1966-02-09')]['High'].values[0]

# Add a fuzzy light pink line from 1957-10-22 to 1966-02-09
line1 = Line2D(
    [date2num(start_date), date2num(end_date)], [low_point, high_point],
    color='lightpink', alpha=0.8, linewidth=10, linestyle='-', zorder=-1
)
plt.gca().add_line(line1)

# Add the second fuzzy line from 1970-05-26 to 1973-01-10
start_date_2 = pd.to_datetime('1970-05-26')
end_date_2 = pd.to_datetime('1973-01-10')

low_point_2 = df[df['Date'] == start_date_2]['Low'].values[0]
high_point_2 = df[df['Date'] == end_date_2]['High'].values[0]

# Add a second fuzzy light pink line
line2 = Line2D(
    [date2num(start_date_2), date2num(end_date_2)], [low_point_2, high_point_2],
    color='lightpink', alpha=0.8, linewidth=10, linestyle='-', zorder=-1
)
plt.gca().add_line(line2)

# Add the third fuzzy yellow line connecting 1966-02-09, 1966-10-10, 1968-12-02, and 1970-05-26
key_dates = [pd.to_datetime('1966-02-09'), pd.to_datetime('1966-10-10'), pd.to_datetime('1968-12-02'), pd.to_datetime('1970-05-26')]
key_prices = [
    df[df['Date'] == key_dates[0]]['High'].values[0],
    df[df['Date'] == key_dates[1]]['Low'].values[0],
    df[df['Date'] == key_dates[2]]['High'].values[0],
    df[df['Date'] == key_dates[3]]['Low'].values[0]
]

# Add a fuzzy yellow line connecting these key dates and prices
line3 = Line2D(
    [date2num(d) for d in key_dates], key_prices,
    color='yellow', alpha=0.8, linewidth=10, linestyle='-', zorder=-1
)
plt.gca().add_line(line3)

# Calculate midpoint for the "mid-cycle slow-down" label
midpoint_idx = len(key_dates) // 2
midpoint_date = key_dates[midpoint_idx]
midpoint_price = (key_prices[midpoint_idx] + key_prices[midpoint_idx-1]) / 2

# Add label "mid-cycle slow-down" near the midpoint of the yellow line
plt.text(midpoint_date, midpoint_price + 20, 'mid-cycle slow-down', ha='center', fontsize=12, color='yellow')

# Show the plot
plt.title('Gann Swing Indicator with Fuzzy Lines and Annotations')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.legend()
plt.show()
