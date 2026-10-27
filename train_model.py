import pandas as pd
import pickle

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data.csv")

occupation_encoder = LabelEncoder()
city_encoder = LabelEncoder()

df["Occupation"] = occupation_encoder.fit_transform(df["Occupation"])

df["City_Tier"] = city_encoder.fit_transform(df["City_Tier"])

X = df[
    [
        "Income",
        "Age",
        "Dependents",
        "Occupation",
        "City_Tier",
        "Rent",
        "Loan_Repayment",
        "Insurance",
        "Groceries",
        "Transport",
        "Eating_Out",
        "Entertainment",
        "Utilities",
        "Healthcare",
        "Education",
        "Miscellaneous"
    ]
]

y = df["Desired_Savings"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

print("Training Accuracy:",model.score(X_test, y_test))

pickle.dump(model,open("model.pkl", "wb"))
 
pickle.dump(occupation_encoder,open("occupation_encoder.pkl", "wb"))

pickle.dump(city_encoder, open("city_encoder.pkl", "wb"))

print("Model Saved Successfully")
