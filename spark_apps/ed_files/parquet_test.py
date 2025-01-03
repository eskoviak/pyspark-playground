from os import path
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ed_files/parquet_test.py").getOrCreate()


output_base = '/opt/spark/data/sparkOutput/testParquet'

spark.createDataFrame(
    [{"age": 67, "name" : "Simon Bar Sinister"}]).write.parquet(output_base, mode="overwrite")
