import logging
import azure.functions as func
import pyodbc
import json
import os

# Database connection string
CONNECTION_STRING = os.getenv("SqlConnectionString")
MODEL_NAME = "Random Forest Classifier"
MODEL_FILE_NAME = "recommendation_model.pkl"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Fetching all recommendations with insight content.")

    try:
        # Validate connection string
        if not CONNECTION_STRING:
            logging.error("Database connection string is not configured.")
            return func.HttpResponse(
                "Internal server error: Missing database connection string.",
                status_code=500
            )

        # Connect to the database
        with pyodbc.connect(CONNECTION_STRING) as conn:
            cursor = conn.cursor()

            # SQL query to fetch all recommendations with joined data
            query = """
            SELECT r.id, i.content, r.recommendation_text, 
                   cl.level_name, dc.channel_name, r.status, 
                   r.created_at, r.updated_at
            FROM Recommendations r
            JOIN Insights i ON r.insight_id = i.id
            JOIN ConfidenceLevels cl ON r.confidence_level_id = cl.id
            JOIN DeliveryChannels dc ON r.delivery_channel_id = dc.id
            """
            cursor.execute(query)

            # Fetch all results
            recommendations = cursor.fetchall()

            # Check if recommendations exist
            if not recommendations:
                return func.HttpResponse(
                    "No recommendations found.",
                    status_code=404
                )

            # Convert results to JSON
            recommendations_list = []
            for row in recommendations:
                recommendations_list.append({
                    "id": row[0],
                    "insight_content": row[1],
                    "recommendation_text": row[2],
                    "confidence_level_name": row[3],
                    "delivery_channel_name": row[4],
                    "status": row[5],
                    "created_at": row[6].strftime("%Y-%m-%d %H:%M:%S") if row[6] else None,
                    "updated_at": row[7].strftime("%Y-%m-%d %H:%M:%S") if row[7] else None
                })

        # Include model information in the response
        response = {
            "model_name": MODEL_NAME,
            "model_file_name": MODEL_FILE_NAME,
            "recommendations": recommendations_list
        }

        # Return recommendations along with model info as JSON
        return func.HttpResponse(
            json.dumps(response, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except pyodbc.Error as db_err:
        logging.error(f"Database error: {db_err}")
        return func.HttpResponse(
            "Internal server error: Database query failed.",
            status_code=500
        )
    except Exception as e:
        logging.error(f"Error fetching recommendations: {e}")
        return func.HttpResponse(
            "Internal server error.",
            status_code=500
        )
