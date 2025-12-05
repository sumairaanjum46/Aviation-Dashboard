import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    import zipfile
    with zipfile.ZipFile("Airline_Delay_Cause.zip") as z:
        with z.open("Airline_Delay_Cause.csv") as f:
            df = pd.read_csv(f)
    return df


df = load_data()

st.title("Aviation Delay Dashboard ✈️")

st.sidebar.header("Filters")


selected_year = st.sidebar.multiselect(
    "Select Year", 
    options=df['year'].unique(), 
    default=df['year'].unique()
)

selected_airline = st.sidebar.multiselect(
    "Select Airline",
    options=df['carrier_name'].unique(),
    default=df['carrier_name'].unique()
)

filtered_df = df[
    (df['year'].isin(selected_year)) &
    (df['carrier_name'].isin(selected_airline))
]


st.subheader("Filtered Delay Data")
st.dataframe(filtered_df)


cause_cols = [
    'carrier_delay', 
    'weather_delay', 
    'nas_delay', 
    'security_delay', 
    'late_aircraft_delay'
]

cause_summary = filtered_df[cause_cols].sum().reset_index()
cause_summary.columns = ['Cause', 'Total Delay']


st.subheader("Total Delays by Cause")
fig1 = px.bar(cause_summary, x='Cause', y='Total Delay', 
              title='Delays by Cause', text='Total Delay')
fig1.update_traces(textposition='outside')
st.plotly_chart(fig1, use_container_width=True)


st.subheader("Delays Over Time")
fig2 = px.line(
    filtered_df, 
    x='year', 
    y='carrier_delay', 
    color='carrier_name',
    title='Carrier Delays Over the Years'
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Delay Proportion by Cause")
fig3 = px.pie(
    cause_summary, 
    names='Cause', 
    values='Total Delay',
    title='Delay Proportion by Cause'
)
st.plotly_chart(fig3, use_container_width=True)

st.success("Dashboard ready! Run using:  streamlit run app.py")
