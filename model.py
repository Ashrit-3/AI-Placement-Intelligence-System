import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


def train_model(df):

    data = df.copy()

    data["Placed_Flag"] = data["Placed"].map({
        "Yes": 1,
        "No": 0
    })

    features = [
        "CGPA",
        "Maths",
        "DBMS",
        "OS",
        "CN"
    ]

    X = data[features]
    y = data["Placed_Flag"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    models = {
        "Logistic Regression":
            LogisticRegression(max_iter=1000),

        "Decision Tree":
            DecisionTreeClassifier(
                max_depth=5,
                random_state=42
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=200,
                random_state=42
            )
    }

    best_model = None
    best_model_name = ""
    best_accuracy = 0

    for name, model in models.items():

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        if accuracy > best_accuracy:

            best_accuracy = accuracy
            best_model = model
            best_model_name = name

    return (
        best_model,
        best_model_name,
        round(best_accuracy * 100, 2)
    )