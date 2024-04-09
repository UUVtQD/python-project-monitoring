import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

try:
    conn = MongoClient("mongodb://monitoring:monitoring@127.0.0.1:10017/monitoring?authSource=monitoring&retryWrites=true&w=majority")
    print(conn)
except ConnectionError as e:
    print("could not connect to MongoDB")
    print(e)

db = conn.monitoring
collection = db.records

data = list(collection.find())

df = pd.DataFrame(data)

df.drop('_id', axis=1, inplace=True)

grouped = df.groupby('hostname')

for name, group in grouped:
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

    st.pyplot(fig)
