import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Placement Intelligence System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

if df is None or df.empty:
    st.error("❌ Dataset could not be loaded.")
    st.stop()

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

[data-testid="stSidebar"]{
    background-color:#111827;
}

.big-title{
    font-size:42px;
    font-weight:bold;
    text-align:center;
    color:#60A5FA;
    margin-bottom:10px;
}

.subtitle{
    text-align:center;
    color:#9CA3AF;
    font-size:18px;
}

.metric-card{
    background:#1F2937;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 4px 15px rgba(0,0,0,0.3);
}

.metric-value{
    font-size:28px;
    font-weight:bold;
    color:white;
}

.metric-label{
    color:#9CA3AF;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown(
    "<div class='big-title'>🚀 AI Placement Intelligence System</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Student Performance • Placement Analytics • AI Prediction</div>",
    unsafe_allow_html=True
)

st.write("")

# =====================================================
# SIDEBAR
# =====================================================

menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "Dashboard",
        "Result Analysis",
        "Placement Analysis",
        "AI Prediction"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    total_students = len(df)

    placed_students = len(
        df[df["Placed"] == "Yes"]
    )

    placement_rate = round(
        (placed_students / total_students) * 100,
        2
    )

    avg_cgpa = round(
        df["CGPA"].mean(),
        2
    )

    avg_package = round(
        df[df["Placed"] == "Yes"]["Package"].mean(),
        2
    )

    highest_package = round(
        df["Package"].max(),
        2
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Placed", placed_students)

    with col3:
        st.metric("Placement %", placement_rate)

    with col4:
        st.metric("Avg CGPA", avg_cgpa)

    with col5:
        st.metric("Highest Package", f"{highest_package} LPA")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            df,
            names="Placed",
            title="Placement Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        branch_data = (
            df.groupby("Branch")["CGPA"]
            .mean()
            .reset_index()
        )

        fig2 = px.bar(
            branch_data,
            x="Branch",
            y="CGPA",
            title="Average CGPA By Branch",
            text_auto=".2f"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

    st.subheader("📥 Export Dataset")

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="students.csv",
        mime="text/csv"
    )

# =====================================================
# RESULT ANALYSIS
# =====================================================

elif menu == "Result Analysis":

    st.header("📊 Student Result Analysis")

    branch = st.selectbox(
        "Select Branch",
        ["All"] + list(df["Branch"].unique())
    )

    filtered_df = df

    if branch != "All":
        filtered_df = df[
            df["Branch"] == branch
        ]

    st.subheader("Top 10 Students")

    top_students = (
        filtered_df
        .sort_values("CGPA", ascending=False)
        .head(10)
    )

    st.dataframe(
        top_students[
            ["Name", "Branch", "CGPA"]
        ],
        use_container_width=True
    )

    st.divider()

    fig = px.histogram(
        filtered_df,
        x="CGPA",
        nbins=10,
        title="CGPA Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# PLACEMENT ANALYSIS
# =====================================================

elif menu == "Placement Analysis":

    st.header("💼 Placement Analysis")

    placed_df = df[
        df["Placed"] == "Yes"
    ]

    company_count = (
        placed_df["Company"]
        .value_counts()
        .reset_index()
    )

    company_count.columns = [
        "Company",
        "Students"
    ]

    fig1 = px.bar(
        company_count,
        x="Company",
        y="Students",
        title="Company Wise Hiring"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.histogram(
        placed_df,
        x="Package",
        nbins=10,
        title="Package Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# AI PREDICTION
# =====================================================

elif menu == "AI Prediction":

    st.header("🧠 AI Placement Predictor")

    cgpa = st.slider(
        "CGPA",
        0.0,
        10.0,
        8.0
    )

    maths = st.slider(
        "Maths",
        0,
        100,
        80
    )

    dbms = st.slider(
        "DBMS",
        0,
        100,
        80
    )

    os_marks = st.slider(
        "OS",
        0,
        100,
        80
    )

    cn = st.slider(
        "CN",
        0,
        100,
        80
    )

    if st.button("Predict Placement"):

        from model import train_model

        model = train_model(df)

        prediction = model.predict(
            [[cgpa, maths, dbms, os_marks, cn]]
        )[0]

        probability = model.predict_proba(
            [[cgpa, maths, dbms, os_marks, cn]]
        )[0][1]

        if prediction == 1:

            st.success(
                f"🎉 Likely To Be Placed\n\nConfidence: {probability*100:.2f}%"
            )

        else:

            st.error(
                f"⚠ Placement Risk\n\nConfidence: {(1-probability)*100:.2f}%"
            )