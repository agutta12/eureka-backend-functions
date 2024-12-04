import logging
import azure.functions as func
import pyodbc
import pandas as pd
import joblib
import datetime
import os

# Load the pre-trained ML model
MODEL_PATH = "recommendation_model.pkl"
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
        # Get the insight_id from the request
        insight_id = req.params.get('insight_id')
        if not insight_id:
            return func.HttpResponse("Insight ID is required.", status_code=400)

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
            print("Data SIze --------------------.", data.size) 
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

        return func.HttpResponse("Recommendation generated and stored successfully.", status_code=200)

    except Exception as e:
        logging.error(f"Error generating recommendation: {e}")
        return func.HttpResponse(f"Internal server error: {str(e)}", status_code=500)
