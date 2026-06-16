import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_data

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Placement Analysis",
    page_icon="💼",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

st.title("💼 Placement Analytics Dashboard")

st.markdown("""
Analyze placement trends, recruiter activity,
branch performance, and salary packages.
""")

st.divider()

# ==========================================
# FILTERS
# ==========================================

branches = ["All"] + sorted(
    df["Branch"].unique().tolist()
)

selected_branch = st.selectbox(
    "Select Branch",
    branches
)

if selected_branch != "All":
    filtered_df = df[
        df["Branch"] == selected_branch
    ]
else:
    filtered_df = df

placed_df = filtered_df[
    filtered_df["Placed"] == "Yes"
]

# ==========================================
# KPI SECTION
# ==========================================

total_students = len(filtered_df)

placed_students = len(placed_df)

placement_rate = round(
    (placed_students / total_students) * 100,
    2
) if total_students > 0 else 0

avg_package = round(
    placed_df["Package"].mean(),
    2
) if len(placed_df) > 0 else 0

highest_package = round(
    placed_df["Package"].max(),
    2
) if len(placed_df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Students",
        total_students
    )

with col2:
    st.metric(
        "Placed",
        placed_students
    )

with col3:
    st.metric(
        "Placement %",
        f"{placement_rate}%"
    )

with col4:
    st.metric(
        "Highest Package",
        f"{highest_package} LPA"
    )

st.divider()

# ==========================================
# COMPANY HIRING
# ==========================================

st.subheader("🏢 Company Wise Hiring")

if len(placed_df) > 0:

    company_count = (
        placed_df["Company"]
        .value_counts()
        .reset_index()
    )

    company_count.columns = [
        "Company",
        "Students"
    ]

    fig_company = px.bar(
        company_count,
        x="Company",
        y="Students",
        text="Students",
        title="Top Recruiters"
    )

    st.plotly_chart(
        fig_company,
        use_container_width=True
    )

# ==========================================
# PACKAGE DISTRIBUTION
# ==========================================

st.subheader("💰 Package Distribution")

if len(placed_df) > 0:

    fig_package = px.histogram(
        placed_df,
        x="Package",
        nbins=10,
        title="Salary Package Distribution"
    )

    st.plotly_chart(
        fig_package,
        use_container_width=True
    )

# ==========================================
# AVERAGE PACKAGE BY BRANCH
# ==========================================

st.subheader("📊 Average Package By Branch")

branch_package = (
    df[df["Placed"] == "Yes"]
    .groupby("Branch")["Package"]
    .mean()
    .reset_index()
)

branch_package["Package"] = (
    branch_package["Package"]
    .round(2)
)

fig_branch_package = px.bar(
    branch_package,
    x="Branch",
    y="Package",
    text="Package",
    title="Average Package by Branch"
)

st.plotly_chart(
    fig_branch_package,
    use_container_width=True
)

# ==========================================
# BRANCH PLACEMENT RATE
# ==========================================

st.subheader("🏫 Branch Placement Rate")

branch_rate = (
    df.groupby("Branch")["Placed"]
    .apply(
        lambda x:
        (x == "Yes").mean() * 100
    )
    .reset_index()
)

branch_rate.columns = [
    "Branch",
    "Placement Rate"
]

branch_rate["Placement Rate"] = (
    branch_rate["Placement Rate"]
    .round(2)
)

fig_rate = px.bar(
    branch_rate,
    x="Branch",
    y="Placement Rate",
    text="Placement Rate",
    title="Placement Rate by Branch"
)

st.plotly_chart(
    fig_rate,
    use_container_width=True
)

# ==========================================
# PACKAGE VS CGPA
# ==========================================

st.subheader("📈 CGPA vs Package")

if len(placed_df) > 0:

    fig_scatter = px.scatter(
        placed_df,
        x="CGPA",
        y="Package",
        color="Branch",
        size="Package",
        hover_data=["Name", "Company"],
        title="CGPA vs Salary Package"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

# ==========================================
# TOP RECRUITERS TABLE
# ==========================================

st.subheader("🏆 Top Recruiters")

if len(placed_df) > 0:

    recruiter_table = (
        placed_df["Company"]
        .value_counts()
        .reset_index()
    )

    recruiter_table.columns = [
        "Company",
        "Students Hired"
    ]

    st.dataframe(
        recruiter_table,
        use_container_width=True
    )

# ==========================================
# PLACED STUDENTS TABLE
# ==========================================

st.subheader("📋 Placed Students")

if len(placed_df) > 0:

    display_columns = [
        "Name",
        "Branch",
        "CGPA",
        "Company",
        "Package"
    ]

    st.dataframe(
        placed_df[display_columns],
        use_container_width=True
    )

# ==========================================
# DOWNLOAD REPORT
# ==========================================

st.divider()

st.download_button(
    label="📥 Download Placement Report",
    data=placed_df.to_csv(index=False),
    file_name="placement_report.csv",
    mime="text/csv"
)