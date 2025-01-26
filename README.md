# polars-DeltaLake
Trying out the Dataframe Polars library with Delta Lake ... feat Python.

Comes with `docker` image.

Interesting, requires `pyarrow` to get the job done. Reading CSV files from `s3` with `pyarrow`
then pass to `Polars` after that, then you can write or read Delta Tables in `s3` with `Polars`.



#### To build and deploy the Docker image to ECR for Lambda ...
```
docker build \
  --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  --build-arg DATABRICKS_TOKEN=$DATABRICKS_TOKEN \
  --platform linux/amd64 \
  -t polarsdelta .
```

To drop into that Docker container ...
```
docker run -it polarsdelta . /bin/bash
```

To tag and push an image ...
```
docker tag polarsdelta:latest 992921014520.dkr.ecr.us-east-1.amazonaws.com/polarsdelta:latest
docker push 992921014520.dkr.ecr.us-east-1.amazonaws.com/polarsdelta:latest
```
