import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_excel("battery_data.xlsx")
    df['Efficiency (%)'] = 100 * df['Discharge Capacity (Ah)'] / df['Charge Capacity (Ah)']
    return df

df = load_data()

st.sidebar.title("🔍 Filter")
temp_range = st.sidebar.slider("Temperature (°C)", min_value=int(df['Temp (°C)'].min()),
                               max_value=int(df['Temp (°C)'].max()), value=(25, 40))
filtered_df = df[(df['Temp (°C)'] >= temp_range[0]) & (df['Temp (°C)'] <= temp_range[1])]

st.title("🔋 Battery Cycle Life Dashboard")

# First figure: Discharge vs Charge Capacity
fig1 = px.line(filtered_df, x='Cycle', y='Discharge Capacity (Ah)', title='Capacity vs Cycle')
fig1.add_scatter(x=filtered_df['Cycle'], y=filtered_df['Charge Capacity (Ah)'], mode='lines', name='Charge Capacity (Ah)')
st.plotly_chart(fig1)

# Second figure: Efficiency vs Cycle
fig2 = px.line(filtered_df, x='Cycle', y='Efficiency (%)', title='Coulombic Efficiency over Cycles')
st.plotly_chart(fig2)

# Summary statistics
st.subheader("📈 Summary Statistics")
st.write(filtered_df.describe())

