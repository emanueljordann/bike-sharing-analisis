import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='darkgrid')

# Load the data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

with st.sidebar:
    st.image("bike_sharing.png")
    
    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()
    
    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
filtered_hour_df = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]

st.title('Bike Sharing Dashboard 🚲')

st.subheader('Daily Rentals Overview')

col1, col2 = st.columns(2)

with col1:
    total_daily_rentals = filtered_day_df['cnt'].sum()
    st.metric("Total Rentals (Daily)", value=total_daily_rentals)

with col2:
    average_daily_rentals = filtered_day_df['cnt'].mean()
    st.metric("Average Daily Rentals", value=round(average_daily_rentals, 2))

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(filtered_day_df['dteday'], filtered_day_df['cnt'], marker='o', linewidth=2, color="#90CAF9")
ax.set_title('Daily Bike Rentals', fontsize=20)
ax.set_xlabel('Date', fontsize=15)
ax.set_ylabel('Total Rentals', fontsize=15)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

st.pyplot(fig)

st.subheader('Hourly Rentals Overview')

average_hourly_rentals = filtered_hour_df.groupby('hr')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='hr', y='cnt', data=average_hourly_rentals, palette="Blues_d", ax=ax)
ax.set_title('Average Hourly Bike Rentals', fontsize=20)
ax.set_xlabel('Hour of the Day', fontsize=15)
ax.set_ylabel('Average Rentals', fontsize=15)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

st.pyplot(fig)

st.subheader('Impact of Weather on Rentals')

weather_rentals = filtered_day_df.groupby('weathersit')['cnt'].mean().reset_index()
weather_mapping = {1: 'Clear', 2: 'Misty', 3: 'Light Rain', 4: 'Heavy Rain'}
weather_rentals['weathersit'] = weather_rentals['weathersit'].map(weather_mapping)

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='weathersit', y='cnt', data=weather_rentals, palette="muted", ax=ax)
ax.set_title('Average Rentals by Weather Condition', fontsize=20)
ax.set_xlabel('Weather Condition', fontsize=15)
ax.set_ylabel('Average Rentals', fontsize=15)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

st.pyplot(fig)

st.caption('Bike Rental Dashboard © 2024')
