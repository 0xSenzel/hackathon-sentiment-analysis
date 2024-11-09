import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

def main():
    st.title("Sentiment Analysis Dashboard")
    
    # Generate Data Button
    if st.button("Generate New Data"):
        requests.post("http://localhost:8000/generate-data")
        st.success("Generating new data...")
    
    # Get Stats
    stats = requests.get("http://localhost:8000/stats").json()
    
    # Convert to DataFrame
    df = pd.DataFrame(stats['stats'])
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sentiment Distribution")
        fig = px.pie(df, values='count', names='sentiment')
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Average Scores by Sentiment")
        fig = px.bar(df, x='sentiment', y='avg_score')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main() 