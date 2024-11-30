import logging
import os
import csv
from io import StringIO  # Required for file-like string handling
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("Processing CSV upload request.")

        # Check if a file was uploaded
        file = req.files.get('file')
        if not file:
            logging.error("No file uploaded.")
            return func.HttpResponse("No file uploaded.", status_code=400)

        logging.info(f"File received: {file.filename}")

        try:
            # Decode the file content from binary to string
            file_content = file.stream.read().decode('utf-8')
            logging.info(f"File content (first 100 chars): {file_content[:100]}")  # Log part of the content

            # Use StringIO to convert the string content to a file-like object
            csv_file = StringIO(file_content)

            # Parse CSV content
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader, None)  # Extract headers
            logging.info(f"CSV headers: {headers}")

            # Process rows
            for row in csv_reader:
                logging.info(f"Row: {row}")

            return func.HttpResponse("File uploaded and processed successfully.", status_code=200)

        except Exception as e:
            logging.error(f"Error processing CSV file: {e}")
            return func.HttpResponse(f"Error processing CSV file: {e}", status_code=400)

    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        return func.HttpResponse(f"Error processing file: {e}", status_code=500)
