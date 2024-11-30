import json
import logging
import azure.functions as func
from db_helpers.getInsights import read_all_insights

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to fetch all insights from the database and return them as a JSON response.
    """
    logging.info("HTTP trigger function to fetch all insights invoked.")

    try:
        # Use the helper function to fetch insights
        insights = read_all_insights()

        # Handle the case where no insights are found
        if not insights:
            return func.HttpResponse(
                json.dumps({"message": "No insights found."}),
                mimetype="application/json",
                status_code=404
            )

        # Return the insights as a JSON response
        return func.HttpResponse(
            json.dumps(insights, indent=4),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error fetching insights: {e}")
        return func.HttpResponse(
            json.dumps({"error": "An error occurred while fetching insights."}),
            mimetype="application/json",
            status_code=500
        )
