import logging
import pyodbc
import os
import csv
from io import StringIO  # Required for file-like string handling
import azure.functions as func
# Database connection details (update these with your EurekaDB credentials)
DB_CONNECTION_STRING = os.getenv("SqlConnectionString")

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("Processing CSV upload request.")

        # Check if a file was uploaded
        file = req.files.get('file')
        if not file:
            logging.error("No file uploaded.")
            return func.HttpResponse("No file uploaded.", status_code=400)

        logging.info(f"File received: {file.filename}")

        # Decode and parse the file content
        file_content = file.stream.read().decode('utf-8')
        csv_reader = csv.reader(StringIO(file_content))
        headers = next(csv_reader, None)

        logging.info(f"CSV headers: {headers}")

        # Expected CSV headers
        expected_headers = [
            "content", "created_at", "insight_type", "data_source", "audience", 
            "domain", "confidence_level", "timeliness", 
            "alignment_goal", "value_priority"
        ]

        # Validate headers
        if headers != expected_headers:
            logging.error(f"Invalid CSV headers. Expected: {expected_headers}, Received: {headers}")
            return func.HttpResponse(f"Invalid CSV headers. Expected: {expected_headers}", status_code=400)

        # Connect to the database
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        logging.info("Database connection established.")

        # Process rows and insert into the database
        inserted_count = 0
        for row in csv_reader:
            logging.info(f"Processing row: {row}")
            try:
                cursor.execute("""
                    INSERT INTO Insights (
                        insight_type_id, data_source_id, audience_id, domain_id, confidence_level_id,
                        timeliness_id, alignment_goal_id, value_priority_id, created_at, content
                    )
                    VALUES (
                        (SELECT id FROM InsightTypes WHERE type_name = ?),
                        (SELECT id FROM DataSources WHERE source_name = ?),
                        (SELECT id FROM Audiences WHERE audience_name = ?),
                        (SELECT id FROM Domains WHERE domain_name = ?),
                        (SELECT id FROM ConfidenceLevels WHERE level_name = ?),
                        (SELECT id FROM Timeliness WHERE timeliness_type = ?),
                        (SELECT id FROM AlignmentGoals WHERE goal_name = ?),
                        (SELECT id FROM ValuePriorities WHERE priority_name = ?),
                        ?, ?
                    )
                """, (
                    row[1],  # insight_type
                    row[2],  # data_source
                    row[3],  # audience
                    row[4],  # domain
                    row[5],  # confidence_level
                    row[6],  # timeliness
                    
                    row[7],  # alignment_goal
                    row[8], # value_priority
                    row[9],  # created_at
                    row[10],  # content
                ))
                inserted_count += 1
                logging.info(f"Row inserted successfully: {row}")
            except Exception as e:
                logging.error(f"Failed to insert row: {row}. Error: {e}")

        # Commit the transaction
        conn.commit()
        logging.info(f"Inserted {inserted_count} rows into the database.")

        return func.HttpResponse(
            f"File uploaded successfully. {inserted_count} rows inserted.",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        return func.HttpResponse(f"Error processing file: {e}", status_code=500)

    finally:
        if 'conn' in locals():
            conn.close()
            logging.info("Database connection closed.")
