import logging
import azure.functions as func
import pyodbc
import json
import os

# Database connection string
CONNECTION_STRING = os.getenv("SqlConnectionString")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Fetching all recommendations with insight content.")

   
