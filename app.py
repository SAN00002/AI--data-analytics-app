import streamlit as st
from agent import DataAgent
import os

st.title("📊 Data Analytics AI Agent")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    agent = DataAgent("temp.csv")
    
    
    st.subheader("🎛️ Data Filters")

df = agent.df.copy()

for col in df.select_dtypes(include="object").columns:
    selected = st.multiselect(f"Filter {col}", df[col].unique())
    if selected:
        df = df[df[col].isin(selected)]

    st.write("Filtered Data Preview")
    st.dataframe(df.head())


    st.subheader("📌 Dataset Overview")
    st.write(agent.get_overview())

    st.subheader("⚠️ Missing Values")
    st.text(agent.get_missing())

    st.subheader("💡 Key Insights")
    insights = agent.generate_insights()
    for i in insights:
        st.write("•", i)
        
    st.subheader("📊 Correlation Heatmap")
    agent.correlation_heatmap()
    st.image("heatmap.png")

    st.subheader("📈 Automatic Charts")
    cols = agent.plot_all_numeric()
    for col in cols:
       st.image(f"{col}.png", caption=col)
       
    st.subheader("🚨 Outlier Detection")

    outliers = agent.detect_outliers()

    for col, count in outliers.items():
       st.write(f"{col}: {count} outliers")

    st.subheader("📦 Outlier Visualization")
    cols = agent.plot_outliers()

    for col in cols:
      st.image(f"{col}_outliers.png", caption=f"{col} Outliers")

    


    question = st.text_input("Ask about your data")

    if question:
        response = agent.ask(question)
        st.write(response)

        if os.path.exists("chart.png"):
            st.image("chart.png")
            
    st.subheader("💬 Chat with your data")

    user_q = st.text_input("Ask a question")

    if user_q:
       st.write(agent.chat(user_q))

