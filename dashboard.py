import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

# Initialize connection to MongoDB (replace 'your_connection_string' with your actual connection string)
try:
    conn = MongoClient("mongodb://monitoring:monitoring@127.0.0.1:10017/monitoring?authSource=monitoring&retryWrites=true&w=majority")
    print(conn)
except ConnectionError as e:
    print("could not connect to MongoDB")
    print(e)

db = conn.monitoring
collection = db.records

# Fetch data from MongoDB
data = list(collection.find())

# Convert the data into a Pandas DataFrame
df = pd.DataFrame(data)

# Remove the '_id' column
df.drop('_id', axis=1, inplace=True)

grouped = df.groupby('hostname')

# Iterate over each group
for name, group in grouped:
    # Plotting the chart for each server
    fig, ax = plt.subplots()
    ax.plot(group.index, group['cpu'], label='CPU Usage (%)')
    ax.plot(group.index, group['ram'], label='RAM Usage (%)')
    ax.plot(group.index, group['gpu-load'], label='GPU Load (%)')
    ax.plot(group.index, group['gpu-ram'], label='GPU RAM Usage (%)')

    # Adding labels and title
    ax.set_xlabel('Record Number')
    ax.set_ylabel('Usage')
    ax.set_title(f'Server Utilization Over Time: {name}')
    ax.legend()

    # Display the chart in Streamlit
    st.pyplot(fig)
