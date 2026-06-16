import pandas as pd
import streamlit as st
from pathlib import Path

# Required columns for the project
REQUIRED_COLUMNS = [
    "Student_ID",
    "Name",
    "Branch",
    "CGPA",
    "Maths",
    "DBMS",
    "OS",
    "CN",
    "Placed",
    "Company",
    "Package"
]

@st.cache_data
def load_data():
    """
    Load and preprocess student dataset.
    """

    try:
        # Get project root directory
        BASE_DIR = Path(__file__).resolve().parent
        file_path = BASE_DIR / "data" / "students.csv"

        if not file_path.exists():
            st.error(f"❌ Dataset not found:\n{file_path}")
            st.stop()

        # Read CSV
        df = pd.read_csv(file_path)

        # Remove extra spaces from column names
        df.columns = df.columns.str.strip()

        # Validate required columns
        missing_cols = [
            col for col in REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing_cols:
            st.error(
                f"❌ Missing columns in dataset:\n{', '.join(missing_cols)}"
            )
            st.stop()

        # Convert numeric columns
        numeric_cols = [
            "CGPA",
            "Maths",
            "DBMS",
            "OS",
            "CN",
            "Package"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        # Fill numeric missing values
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())

        # Fill categorical missing values
        categorical_cols = [
            "Name",
            "Branch",
            "Placed",
            "Company"
        ]

        for col in categorical_cols:
            df[col] = df[col].fillna("Unknown")

        # Remove duplicate students
        df = df.drop_duplicates(
            subset=["Student_ID"]
        )

        # Reset index
        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")
        st.stop()