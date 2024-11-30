import logging
import os
import csv
import azure.functions as func
import pyodbc  # Use the appropriate DB library for your database

# Database connection details (update these with your EurekaDB credentials)
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing CSV upload request.")

    # Check if a file was uploaded
    file = req.files.get('file')
    if not file:
        return func.HttpResponse("No file uploaded.", status_code=400)

    try:
        # Connect to the database
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()

        # Parse the uploaded CSV
        file_content = file.stream.read().decode('utf-8')
        csv_reader = csv.reader(file_content.splitlines())
        
        # Extract and validate the headers
        headers = next(csv_reader)
        expected_headers = [
            "insight_type", "data_source", "audience", "domain", "confidence_level", 
            "timeliness", "delivery_channel", "alignment_goal", "value_priority", "content"
        ]
        if headers != expected_headers:
            return func.HttpResponse(
                f"Invalid CSV headers. Expected: {', '.join(expected_headers)}",
                status_code=400
            )

        # Insert each row into the database
        for row in csv_reader:
            (
                insight_type, data_source, audience, domain, confidence_level,
                timeliness, delivery_channel, alignment_goal, value_priority, content
            ) = row

            # SQL query using subqueries to resolve foreign keys
            cursor.execute("""
                INSERT INTO Insights (
                    insight_type_id, data_source_id, audience_id, domain_id, confidence_level_id,
                    timeliness_id, delivery_channel_id, alignment_goal_id, value_priority_id, content
                )
                VALUES (
                    (SELECT id FROM InsightTypes WHERE type_name = ?),
                    (SELECT id FROM DataSources WHERE source_name = ?),
                    (SELECT id FROM Audiences WHERE audience_name = ?),
                    (SELECT id FROM Domains WHERE domain_name = ?),
                    (SELECT id FROM ConfidenceLevels WHERE level_name = ?),
                    (SELECT id FROM Timeliness WHERE timeliness_type = ?),
                    (SELECT id FROM DeliveryChannels WHERE channel_name = ?),
                    (SELECT id FROM AlignmentGoals WHERE goal_name = ?),
                    (SELECT id FROM ValuePriorities WHERE priority_name = ?),
                    ?
                )
            """, (
                insight_type, data_source, audience, domain, confidence_level,
                timeliness, delivery_channel, alignment_goal, value_priority, content
            ))
        
        # Commit the transaction
        conn.commit()

        return func.HttpResponse("File processed and data inserted successfully.", status_code=200)

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return func.HttpResponse("Error processing file. Check server logs for details.", status_code=500)

    finally:
        # Clean up the database connection
        if 'conn' in locals():
            conn.close()