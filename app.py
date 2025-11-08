import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("university_student_data.csv")
    return df

df = load_data()

st.title("📊 University Data Dashboard")
st.write("Interactive analytics for applications, enrollment, retention and satisfaction.")

st.sidebar.header("🔎 Filters")

years = st.sidebar.multiselect(
    "Select Year(s)", 
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

terms = st.sidebar.multiselect(
    "Select Term(s)",
    df["Term"].unique(),
    default=df["Term"].unique()
)

departments = [
    "Engineering Enrolled", 
    "Business Enrolled", 
    "Arts Enrolled", 
    "Science Enrolled"
]

selected_depts = st.sidebar.multiselect(
    "Select Department(s)",
    departments,
    default=departments
)

filtered_df = df[
    (df["Year"].isin(years)) & 
    (df["Term"].isin(terms))
]

st.subheader("📌 Key Performance Indicators (KPIs)")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Retention Rate (%)", round(filtered_df["Retention Rate (%)"].mean(), 2))
col2.metric("Avg Satisfaction (%)", round(filtered_df["Student Satisfaction (%)"].mean(), 2))
col3.metric("Total Enrolled", int(filtered_df["Enrolled"].sum()))

st.subheader("📈 Retention Rate Over Time")

fig, ax = plt.subplots()
data = filtered_df.groupby("Year")["Retention Rate (%)"].mean()
ax.plot(data.index, data.values)
ax.set_xlabel("Year")
ax.set_ylabel("Retention Rate (%)")
ax.set_title("Retention Rate Over Time")
st.pyplot(fig)

st.subheader("😊 Student Satisfaction Over Time")

fig, ax = plt.subplots()
data = filtered_df.groupby("Year")["Student Satisfaction (%)"].mean()
ax.plot(data.index, data.values)
ax.set_xlabel("Year")
ax.set_ylabel("Satisfaction (%)")
ax.set_title("Student Satisfaction Over Time")
st.pyplot(fig)

st.subheader("🌤 Spring vs Fall Enrollment")

fig, ax = plt.subplots()
term_data = filtered_df.groupby("Term")["Enrolled"].mean()
ax.bar(term_data.index, term_data.values)
ax.set_xlabel("Term")
ax.set_ylabel("Average Enrollment")
ax.set_title("Average Enrollment: Spring vs Fall")
st.pyplot(fig)

st.subheader("🏫 Department Enrollment Over Time")

fig, ax = plt.subplots()

for dept in selected_depts:
    dept_data = filtered_df.groupby("Year")[dept].mean()
    ax.plot(dept_data.index, dept_data.values, label=dept.replace(" Enrolled", ""))

ax.set_xlabel("Year")
ax.set_ylabel("Enrollment")
ax.set_title("Department Enrollment Trends")
ax.legend()
st.pyplot(fig)

st.success("✅ Dashboard fully interactive and ready for deployment!")