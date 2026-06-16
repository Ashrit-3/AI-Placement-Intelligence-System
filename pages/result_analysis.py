import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Student Result Analytics",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.title("📊 Student Result Analytics Dashboard")

st.markdown("""
Analyze student academic performance,
subject-wise scores, branch-wise rankings,
and top performers.
""")

st.divider()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🎯 Filters")

branches = ["All"] + sorted(
    df["Branch"].unique().tolist()
)

selected_branch = st.sidebar.selectbox(
    "Select Branch",
    branches
)

if selected_branch != "All":
    filtered_df = df[
        df["Branch"] == selected_branch
    ]
else:
    filtered_df = df.copy()

# =====================================================
# STUDENT SEARCH
# =====================================================

student_search = st.sidebar.text_input(
    "🔍 Search Student"
)

if student_search:

    filtered_df = filtered_df[
        filtered_df["Name"]
        .str.contains(
            student_search,
            case=False,
            na=False
        )
    ]

# =====================================================
# KPI CARDS
# =====================================================

total_students = len(filtered_df)

avg_cgpa = round(
    filtered_df["CGPA"].mean(),
    2
)

highest_cgpa = round(
    filtered_df["CGPA"].max(),
    2
)

lowest_cgpa = round(
    filtered_df["CGPA"].min(),
    2
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Students",
        total_students
    )

with col2:
    st.metric(
        "Average CGPA",
        avg_cgpa
    )

with col3:
    st.metric(
        "Highest CGPA",
        highest_cgpa
    )

with col4:
    st.metric(
        "Lowest CGPA",
        lowest_cgpa
    )

st.divider()

# =====================================================
# TOP PERFORMERS
# =====================================================

st.subheader("🏆 Top 10 Performers")

top_students = (
    filtered_df
    .sort_values(
        "CGPA",
        ascending=False
    )
    .head(10)
)

display_cols = [
    "Student_ID",
    "Name",
    "Branch",
    "CGPA"
]

st.dataframe(
    top_students[display_cols],
    use_container_width=True
)

st.divider()

# =====================================================
# SUBJECT PERFORMANCE
# =====================================================

st.subheader("📚 Subject Wise Performance")

subject_data = pd.DataFrame({
    "Subject": [
        "Maths",
        "DBMS",
        "OS",
        "CN"
    ],
    "Average Marks": [
        filtered_df["Maths"].mean(),
        filtered_df["DBMS"].mean(),
        filtered_df["OS"].mean(),
        filtered_df["CN"].mean()
    ]
})

fig_subject = px.bar(
    subject_data,
    x="Subject",
    y="Average Marks",
    text_auto=".2f",
    title="Average Marks By Subject"
)

st.plotly_chart(
    fig_subject,
    use_container_width=True
)

st.divider()

# =====================================================
# CGPA DISTRIBUTION
# =====================================================

st.subheader("📈 CGPA Distribution")

fig_cgpa = px.histogram(
    filtered_df,
    x="CGPA",
    nbins=15,
    title="CGPA Distribution"
)

st.plotly_chart(
    fig_cgpa,
    use_container_width=True
)

st.divider()

# =====================================================
# BRANCH PERFORMANCE
# =====================================================

st.subheader("🏫 Branch Performance")

branch_performance = (
    df.groupby("Branch")["CGPA"]
    .mean()
    .reset_index()
)

branch_performance["CGPA"] = (
    branch_performance["CGPA"]
    .round(2)
)

fig_branch = px.bar(
    branch_performance,
    x="Branch",
    y="CGPA",
    text="CGPA",
    title="Average CGPA By Branch"
)

st.plotly_chart(
    fig_branch,
    use_container_width=True
)

st.divider()

# =====================================================
# PERFORMANCE CATEGORY
# =====================================================

st.subheader("🎯 Student Performance Categories")

excellent = len(
    filtered_df[
        filtered_df["CGPA"] >= 9
    ]
)

good = len(
    filtered_df[
        (filtered_df["CGPA"] >= 7)
        &
        (filtered_df["CGPA"] < 9)
    ]
)

average = len(
    filtered_df[
        filtered_df["CGPA"] < 7
    ]
)

performance_df = pd.DataFrame({
    "Category": [
        "Excellent",
        "Good",
        "Average"
    ],
    "Students": [
        excellent,
        good,
        average
    ]
})

fig_perf = px.pie(
    performance_df,
    names="Category",
    values="Students",
    title="Performance Categories"
)

st.plotly_chart(
    fig_perf,
    use_container_width=True
)

st.divider()

# =====================================================
# SUBJECT CORRELATION
# =====================================================

st.subheader("📊 CGPA vs Subject Performance")

fig_scatter = px.scatter(
    filtered_df,
    x="Maths",
    y="CGPA",
    color="Branch",
    hover_data=["Name"],
    title="Maths Marks vs CGPA"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

st.divider()

# =====================================================
# STUDENT RECORDS
# =====================================================

st.subheader("📋 Student Records")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================================
# DOWNLOAD REPORT
# =====================================================

st.divider()

st.download_button(
    label="📥 Download Result Report",
    data=filtered_df.to_csv(index=False),
    file_name="student_result_report.csv",
    mime="text/csv"
)