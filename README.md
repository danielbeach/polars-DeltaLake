# polars-DeltaLake
Trying out the Dataframe Polars library with Delta Lake ... feat Python.

Comes with `docker` image.

Interesting, requires `pyarrow` to get the job done. Reading CSV files from `s3` with `pyarrow`
then pass to `Polars` after that, then you can write or read Delta Tables in `s3` with `Polars`.
