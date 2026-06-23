import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("datasets/Crop_recommendation.csv")

# print(df.head(9))
# print(df.shape)
# print(df['ph'].unique())

X = df.drop("label", axis=1)    # drop the label column vertically (axis=1)
y = df["label"]     # target variable

model = RandomForestClassifier(
    n_estimators=100,   # standard number of trees
    random_state=42,    # locking in the randomness
)

model.fit(X, y)

joblib.dump(model, "ml/crop_model.pkl")

print("Model trained!")