import streamlit as st
import pandas as pd

from data_loader import load_data
from model import train_model

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Placement Predictor",
    page_icon="🧠",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================

df = load_data()

# =====================================
# PAGE TITLE
# =====================================

st.title("🧠 AI Placement Prediction System")

st.markdown("""
Predict whether a student is likely to get placed based on:

- CGPA
- Maths Marks
- DBMS Marks
- Operating Systems Marks
- Computer Networks Marks

The system automatically selects the best-performing machine learning model.
""")

st.divider()

# =====================================
# TRAIN MODEL
# =====================================

try:

    model, model_name, accuracy = train_model(df)

    st.success(
        f"✅ Best Model Selected: **{model_name}** | Accuracy: **{accuracy}%**"
    )

except Exception as e:

    st.error(f"Model Training Error: {e}")
    st.stop()

# =====================================
# INPUT SECTION
# =====================================

st.subheader("🎯 Student Details")

col1, col2 = st.columns(2)

with col1:

    cgpa = st.slider(
        "CGPA",
        min_value=0.0,
        max_value=10.0,
        value=8.0,
        step=0.1
    )

    maths = st.slider(
        "Maths Marks",
        min_value=0,
        max_value=100,
        value=80
    )

    dbms = st.slider(
        "DBMS Marks",
        min_value=0,
        max_value=100,
        value=80
    )

with col2:

    os_marks = st.slider(
        "Operating Systems Marks",
        min_value=0,
        max_value=100,
        value=80
    )

    cn = st.slider(
        "Computer Networks Marks",
        min_value=0,
        max_value=100,
        value=80
    )

# =====================================
# PREDICTION BUTTON
# =====================================

st.write("")

if st.button("🚀 Predict Placement"):

    sample = pd.DataFrame(
        {
            "CGPA": [cgpa],
            "Maths": [maths],
            "DBMS": [dbms],
            "OS": [os_marks],
            "CN": [cn]
        }
    )

    try:

        prediction = model.predict(sample)[0]

        probability = model.predict_proba(sample)[0][1]

        st.divider()

        st.subheader("📈 Prediction Result")

        col1, col2 = st.columns(2)

        with col1:

            if prediction == 1:

                st.success(
                    "🎉 Likely To Be Placed"
                )

            else:

                st.error(
                    "⚠ Placement Risk"
                )

        with col2:

            st.metric(
                "Placement Probability",
                f"{probability*100:.2f}%"
            )

        # =====================================
        # PERFORMANCE SCORE
        # =====================================

        score = (
            (cgpa * 10)
            + maths
            + dbms
            + os_marks
            + cn
        ) / 5

        st.write("")

        st.progress(
            min(
                int(probability * 100),
                100
            )
        )

        st.info(
            f"Student Performance Score: {score:.2f}"
        )

        # =====================================
        # RECOMMENDATIONS
        # =====================================

        st.subheader("💡 Improvement Suggestions")

        suggestions = []

        if cgpa < 7:
            suggestions.append(
                "Improve CGPA above 7.0"
            )

        if maths < 70:
            suggestions.append(
                "Improve Maths fundamentals"
            )

        if dbms < 70:
            suggestions.append(
                "Strengthen DBMS concepts"
            )

        if os_marks < 70:
            suggestions.append(
                "Practice Operating Systems topics"
            )

        if cn < 70:
            suggestions.append(
                "Improve Computer Networks knowledge"
            )

        if len(suggestions) == 0:

            st.success(
                "Excellent Profile! Keep practicing aptitude and interviews."
            )

        else:

            for item in suggestions:
                st.warning(item)

    except Exception as e:

        st.error(
            f"Prediction Error: {e}"
        )

# =====================================
# FEATURE INFO
# =====================================

st.divider()

with st.expander("ℹ How Prediction Works"):

    st.write("""
    The AI model uses historical student records and learns patterns
    between academic performance and placement outcomes.

    Input Features:

    - CGPA
    - Maths
    - DBMS
    - Operating Systems
    - Computer Networks

    Output:

    - Placement Prediction
    - Placement Probability
    - Improvement Suggestions
    """)