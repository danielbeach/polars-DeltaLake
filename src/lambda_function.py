import polars as pl
import os

BEARER_TOKEN = os.getenv("DATABRICKS_TOKEN")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

def handler(event, context):

       catalog = pl.Catalog("https://dbc-9a64f31c-25b9.cloud.databricks.com/", 
                            bearer_token=BEARER_TOKEN)

       df = catalog.scan_table("confessions", "default", "trip_data")
       df = df.sql("""SELECT CAST(substr(started_at, 1, 10) as DATE) as dt, rideable_type, ride_id
                     FROM self """)
       metrics = df.sql("""
              SELECT dt, rideable_type, count(*) as rides
              FROM self
              GROUP BY dt, rideable_type
              """).collect()

       metrics.write_csv("s3://confessions-of-a-data-guy/trip_data_metrics", include_header=True)