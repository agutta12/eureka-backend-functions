import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the historical dataset
data = pd.read_csv("insights_training_data.csv")

# Features and target variable
features = data[['confidence_level_id', 'timeliness_id', 'value_priority_id']]
target = data['recommendation_type']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(model, "recommendation_model.pkl")
