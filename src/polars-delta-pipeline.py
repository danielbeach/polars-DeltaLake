import polars as pl
import pyarrow.dataset as ds
from pyarrow import fs


def read_remote_csvs(path: str, key: str, secret: str) -> pl.DataFrame:
    s3 = fs.S3FileSystem(access_key=key, 
                         secret_key=secret, 
                         request_timeout=500, 
                         connect_timeout=500)
    dataset = ds.dataset(filesystem=s3, source=path, format="csv")
    df = pl.scan_pyarrow_dataset(dataset)
    return df


def calculate_metrics(df: pl.DataFrame) -> pl.DataFrame:
    sql = pl.SQLContext()
    sql.register("df", df)
    metrics = sql.execute("""
                      SELECT CAST(started_at as DATE) AS dt, COUNT(*) AS trips
                      FROM df
                      GROUP BY CAST(started_at as DATE)
                      """)
    return metrics.collect()


def write_delta_lake(df: pl.DataFrame, path: str, key: str, secret: str) -> None:
    storage_options = {}
    storage_options["AWS_REGION"] = "us-east-1"
    storage_options["AWS_ACCESS_KEY_ID"] = key
    storage_options["AWS_SECRET_ACCESS_KEY"] = secret
    storage_options["AWS_S3_ALLOW_UNSAFE_RENAME"] = "true"
    df.write_delta(path, 
                    mode="overwrite", 
                    overwrite_schema=True,
                    storage_options=storage_options)

def main():
    path = "confessions-of-a-data-guy/trip_data/"
    write_path = "s3://confessions-of-a-data-guy/trip_data_delta"
    key=''
    secret=''
    df = read_remote_csvs(path, key, secret)
    metrics = calculate_metrics(df)
    print(metrics)
    write_delta_lake(metrics, write_path, key, secret)


if __name__ == "__main__":
    main()