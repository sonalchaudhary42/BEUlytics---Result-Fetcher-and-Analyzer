import pandas as pd
import streamlit as st
import plotly.express as px

def show_analytics(df):
    st.markdown("## 📊 Analytics Summary")

    # Ensure SGPA column is numeric
    df["Current SGPA"] = pd.to_numeric(df["Current SGPA"], errors="coerce")

    # === 1. Metric Cards ===
    st.subheader("📌 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average SGPA", round(df["Current SGPA"].mean(), 2))
    col2.metric("Highest SGPA", df["Current SGPA"].max())
    col3.metric("Lowest SGPA", df["Current SGPA"].min())

    # === 2. Histogram ===
    st.subheader("📈 SGPA Distribution")
    fig1 = px.histogram(
        df,
        x="Current SGPA",
        nbins=10,
        title="SGPA Distribution"
    )
    fig1.update_layout(bargap=0.1)  # 10% space between bars
    st.plotly_chart(fig1, use_container_width=True)

    # === 3. Top Performers ===
    st.subheader("🏅 Top 10 Students")
    top_df = df.sort_values(by="Current SGPA", ascending=False).head(10)
    fig2 = px.bar(top_df, x="Student Name", y="Current SGPA", title="Top 10 Performers")
    st.plotly_chart(fig2, use_container_width=True)

    # === 4. Semester Trend ===
    sem_cols = [col for col in df.columns if col.startswith("Sem ")]
    if sem_cols:
        st.subheader("📉 Semester-wise Average Grades")
        sem_df = df[sem_cols].apply(pd.to_numeric, errors="coerce")
        avg_sem = sem_df.mean().reset_index()
        avg_sem.columns = ["Semester", "Average Grade"]
        fig3 = px.line(avg_sem, x="Semester", y="Average Grade", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    # === 5. Result Category ===
    st.subheader("📊 Performance Categories")
    def grade_bucket(sgpa):
        if sgpa >= 9: return "Excellent"
        elif sgpa >= 8: return "Very Good"
        elif sgpa >= 7: return "Good"
        elif sgpa >= 6: return "Average"
        else: return "Needs Improvement"

    df["SGPA Category"] = df["Current SGPA"].apply(grade_bucket)
    fig4 = px.pie(df, names="SGPA Category", title="Result Distribution")
    st.plotly_chart(fig4, use_container_width=True)

    # st.subheader("📈 SGPA Distribution")
    # fig1 = px.histogram(df, x="Current SGPA", nbins=10, title="SGPA Distribution")
    # st.plotly_chart(fig1, use_container_width=True)