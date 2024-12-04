import logging
import azure.functions as func
import pyodbc
import json
import os

# Database connection string
CONNECTION_STRING = os.getenv("SqlConnectionString")

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

            # SQL query to fetch all recommendations
            query = """
            SELECT r.id, r.insight_id, i.content, r.recommendation_text, r.confidence_level_id, 
                   r.delivery_channel_id, r.status, r.created_at, r.updated_at
            FROM Recommendations r
            JOIN Insights i ON r.insight_id = i.id
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
                    "insight_id": row[1],
                    "insight_content": row[2],
                    "recommendation_text": row[3],
                    "confidence_level_id": row[4],
                    "delivery_channel_id": row[5],
                    "status": row[6],
                    "created_at": row[7].strftime("%Y-%m-%d %H:%M:%S") if row[7] else None,
                    "updated_at": row[8].strftime("%Y-%m-%d %H:%M:%S") if row[8] else None
                })

        # Return recommendations as JSON
        return func.HttpResponse(
            json.dumps(recommendations_list, indent=2),
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