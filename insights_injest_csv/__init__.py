import logging
import os
import csv
import azure.functions as func
import pyodbc
from io import StringIO  # Import StringIO for file-like string handling

# Database connection details (update these with your EurekaDB credentials)
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing CSV upload request.")

    # Check if a file was uploaded
    file = req.files.get('file')
    if not file:
        return func.HttpResponse("No file uploaded.", status_code=400)

    # Track results
    inserted_count = 0
    rejected_records = []

    try:
        # Connect to the database
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()

        # Parse the uploaded CSV
        file_content = file.stream.read().decode('utf-8')  # Decode bytes to string
        csv_reader = csv.reader(StringIO(file_content))  # Use StringIO for file-like behavior

        # Extract and validate the headers
        headers = next(csv_reader, None)
        expected_headers = [
            "insight_type", "data_source", "audience", "domain", "confidence_level", 
            "timeliness", "delivery_channel", "alignment_goal", "value_priority", "content"
        ]
        if headers != expected_headers:
            return func.HttpResponse(
                f"Invalid CSV headers. Expected: {', '.join(expected_headers)}",
                status_code=400
            )

        # Process each row in the CSV
        for row in csv_reader:
            if len(row) != len(expected_headers):
                rejected_records.append({"row": row, "reason": "Invalid number of fields"})
                continue

            (
                insight_type, data_source, audience, domain, confidence_level,
                timeliness, delivery_channel, alignment_goal, value_priority, content
            ) = row

            # Check if the record already exists (based on the `content` field)
            cursor.execute("SELECT COUNT(*) FROM Insights WHERE content = ?", (content,))
            record_exists = cursor.fetchone()[0] > 0

            if record_exists:
                rejected_records.append({"content": content, "reason": "Duplicate content"})
                continue

            try:
                # Insert the new record using subqueries to resolve foreign keys
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
                inserted_count += 1
            except Exception as e:
                rejected_records.append({"content": content, "reason": str(e)})
                continue

        # Commit the transaction
        conn.commit()

        # Construct response
        response = {
            "inserted_count": inserted_count,
            "rejected_records": rejected_records
        }

        return func.HttpResponse(
            body=str(response),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return func.HttpResponse("Error processing file. Check server logs for details.", status_code=500)

    finally:
        # Clean up the database connection
        if 'conn' in locals():
            conn.close()
