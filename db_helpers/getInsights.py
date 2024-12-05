import pyodbc
import logging
import os

# Load database connection string from environment variable
DB_CONNECTION_STRING = os.getenv("SqlConnectionString")

def read_all_insights():
    """
    Reads all insights details from the Azure SQL database with comprehensive details.

    Returns:
        list: A list of dictionaries containing detailed insight information, or an empty list if no records are found.
    Raises:
        Exception: If there's an error connecting to the database or executing the query.
    """
    try:
        # Log the start of the process
        logging.info("Connecting to the database EurekaDB...")

        # Establish the database connection
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()

        # Comprehensive query to fetch all insights details
        query = """
        SELECT 
            i.id AS insight_id,
            i.content AS insight_content,
            i.created_at AS insight_created_at,
            it.type_name AS insight_type,
            it.description AS insight_type_description,
            ds.source_name AS data_source,
            ds.description AS data_source_description,
            a.audience_name AS audience,
            a.description AS audience_description,
            d.domain_name AS domain,
            d.description AS domain_description,
            cl.level_name AS confidence_level,
            cl.description AS confidence_level_description,
            t.timeliness_type AS timeliness,
            t.description AS timeliness_description,
            ag.goal_name AS alignment_goal,
            ag.description AS alignment_goal_description,
            vp.priority_name AS value_priority,
            vp.description AS value_priority_description
        FROM 
            Insights i
        JOIN 
            InsightTypes it ON i.insight_type_id = it.id
        JOIN 
            DataSources ds ON i.data_source_id = ds.id
        JOIN 
            Audiences a ON i.audience_id = a.id
        JOIN 
            Domains d ON i.domain_id = d.id
        JOIN 
            ConfidenceLevels cl ON i.confidence_level_id = cl.id
        JOIN 
            Timeliness t ON i.timeliness_id = t.id
        JOIN 
            AlignmentGoals ag ON i.alignment_goal_id = ag.id
        JOIN 
            ValuePriorities vp ON i.value_priority_id = vp.id;
        """

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the query result
        rows = cursor.fetchall()


        # Convert rows to a list of dictionaries
        insights = [
            {
                "insight_id": row.insight_id,
                "content": row.insight_content,
                "created_at": row.insight_created_at.strftime("%Y-%m-%d %H:%M:%S") if row.insight_created_at else None,
                "insight_type": {
                    "name": row.insight_type,
                    "description": row.insight_type_description
                },
                "data_source": {
                    "name": row.data_source,
                    "description": row.data_source_description
                },
                "audience": {
                    "name": row.audience,
                    "description": row.audience_description
                },
                "domain": {
                    "name": row.domain,
                    "description": row.domain_description
                },
                "confidence_level": {
                    "name": row.confidence_level,
                    "description": row.confidence_level_description
                },
                "timeliness": {
                    "type": row.timeliness,
                    "description": row.timeliness_description
                },
                "alignment_goal": {
                    "name": row.alignment_goal,
                    "description": row.alignment_goal_description
                },
                "value_priority": {
                    "name": row.value_priority,
                    "description": row.value_priority_description
                }
            }
            for row in rows
        ]

        # Log the number of insights fetched
        logging.info(f"Fetched {len(insights)} insights from the database.")
        return insights

    except pyodbc.Error as e:
        # Log and raise database errors
        logging.error(f"Database error: {e}")
        raise Exception("Error connecting to the database or executing the query.") from e

    finally:
        # Ensure the connection is closed
        if 'conn' in locals() and conn:
            conn.close()
            logging.info("Database connection closed.")
