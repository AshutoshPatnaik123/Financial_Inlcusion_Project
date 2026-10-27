from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

from utils import (
    calculate_expenses,
    calculate_credit_score,
    risk_level
)

app = Flask(__name__)

# Allow Vue frontend
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://localhost:4173"
            ]
        }
    }
)

# ==============================
# Load model and encoders
# ==============================
model = pickle.load(open("model.pkl", "rb"))

occupation_encoder = pickle.load(
    open("occupation_encoder.pkl", "rb")
)

city_encoder = pickle.load(
    open("city_encoder.pkl", "rb")
)

# ==============================
# Health Route
# ==============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "FinTrust API Running"
    })

# ==============================
# Prediction Route
# ==============================
@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        age = int(data["age"])
        occupation = data["occupation"]
        city_tier = data["city_tier"]

        income = float(data["income"])
        dependents = int(data["dependents"])

        rent = float(data["rent"])
        loan = float(data["loan"])
        insurance = float(data["insurance"])
        groceries = float(data["groceries"])
        transport = float(data["transport"])
        eating_out = float(data["eating_out"])
        entertainment = float(data["entertainment"])
        utilities = float(data["utilities"])
        healthcare = float(data["healthcare"])
        education = float(data["education"])
        miscellaneous = float(data["miscellaneous"])

        # Encode categorical values
        occupation_encoded = (
            occupation_encoder
            .transform([occupation])[0]
        )

        city_encoded = (
            city_encoder
            .transform([city_tier])[0]
        )

        # Model Input
        input_data = np.array([[
            income,
            age,
            dependents,
            occupation_encoded,
            city_encoded,
            rent,
            loan,
            insurance,
            groceries,
            transport,
            eating_out,
            entertainment,
            utilities,
            healthcare,
            education,
            miscellaneous
        ]])

        # Predict savings
        predicted_savings = float(
            model.predict(input_data)[0]
        )

        # Expense calculation
        total_expenses = calculate_expenses(
            rent,
            loan,
            insurance,
            groceries,
            transport,
            eating_out,
            entertainment,
            utilities,
            healthcare,
            education,
            miscellaneous
        )

        # Credit score calculation
        score = calculate_credit_score(
            income,
            total_expenses,
            loan,
            predicted_savings
        )

        future_savings = predicted_savings * 6

        risk = risk_level(score)

        recommendations = []

        if eating_out > 5000:
            recommendations.append(
                "Reduce eating-out expenses"
            )

        if entertainment > 5000:
            recommendations.append(
                "Reduce entertainment spending"
            )

        if loan > income * 0.30:
            recommendations.append(
                "Loan burden is high"
            )

        if predicted_savings < income * 0.10:
            recommendations.append(
                "Increase monthly savings"
            )

        if len(recommendations) == 0:
            recommendations.append(
                "Financial profile looks healthy"
            )

        return jsonify({
            "status": "success",

            "input_summary": {
                "age": age,
                "occupation": occupation,
                "city_tier": city_tier,
                "income": income,
                "dependents": dependents
            },

            "financial_metrics": {
                "total_expenses": round(
                    total_expenses, 2
                ),
                "monthly_savings": round(
                    predicted_savings, 2
                ),
                "future_savings_6_months": round(
                    future_savings, 2
                )
            },

            "credit_assessment": {
                "credit_score": round(
                    score, 2
                ),
                "risk_level": risk
            },

            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )