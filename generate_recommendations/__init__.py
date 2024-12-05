import logging
import azure.functions as func
import pyodbc
import pandas as pd
import joblib
import datetime
import os
import json

# Load the pre-trained ML model
# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = "Random Forest Classifier";
MODEL_PATH = os.path.join(BASE_DIR, "recommendation_model.pkl")
model = joblib.load(MODEL_PATH)

# Database connection string
CONNECTION_STRING = os.getenv("SqlConnectionString")

# Recommendation mapping
recommendation_mapping = {
    0: "Send targeted notification about health resources.",
    1: "Send an email to select a primary care physician.",
    2: "Provide manual review for custom recommendation."
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing insight for generating a recommendation.")

    try:
        # Parse the request body to get insight_id
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("Invalid JSON in request body.", status_code=400)

        insight_id = req_body.get("insight_id")
        if not insight_id:
            return func.HttpResponse("Insight ID is required in the request body.", status_code=400)

        # Connect to the database
        with pyodbc.connect(CONNECTION_STRING) as conn:
            cursor = conn.cursor()

            # Fetch the insight features
            query = """
            SELECT confidence_level_id, timeliness_id, value_priority_id
            FROM Insights
            WHERE id = ?
            """
            data = pd.read_sql(query, conn, params=[insight_id])

            if data.empty:
                return func.HttpResponse("Insight not found.", status_code=404)

            # Prepare features for prediction
            features = data[['confidence_level_id', 'timeliness_id', 'value_priority_id']]

            # Predict the recommendation type
            prediction = model.predict(features)[0]
            recommendation_text = recommendation_mapping.get(prediction, "No recommendation available.")

            # Insert the recommendation into the Recommendations table
            now = datetime.datetime.utcnow()
            insert_query = """
            INSERT INTO Recommendations (insight_id, recommendation_text, confidence_level_id, delivery_channel_id, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(
                insert_query,
                insight_id, recommendation_text, int(data['confidence_level_id'].iloc[0]),
                1,  # Assuming delivery_channel_id = 1 (default notification channel)
                'Pending', now, now
            )
            conn.commit()

        return func.HttpResponse(
            json.dumps({"message": "Recommendation generated and stored successfully.", "recommendation": recommendation_text}),
            mimetype="application/json",
            status_code=200
        )

    except pyodbc.Error as db_err:
        logging.error(f"Database error: {db_err}")
        return func.HttpResponse("Internal server error: Database query failed.", status_code=500)
    except Exception as e:
        logging.error(f"Error generating recommendation: {e}")
        return func.HttpResponse("Internal server error.", status_code=500)