import pyspark.sql.functions as F
from pyspark.sql import SparkSession
import re
from os import path, listdir

# get or create a spark context
spark = SparkSession.builder.appName("ed_files/read_quantity_exports.py").getOrCreate()

output_base = '/opt/spark/data/sparkOutput'
data_file_base = '/opt/spark/data/HealthAll_2024-12-345_14-58-25_SimpleHealthExportCSV'
quantity_base = r'^HKQuantityTypeIdentifier'
quantities = [
    'ActiveEnergyBurned',
    ]

for quantity in quantities:
    print(f'+++++++++++++++++++++++ Processing {quantity}')
    spec = re.compile(quantity_base + quantity)
    csv_file = [f for f in listdir(data_file_base) if path.isfile(path.join(data_file_base, f)) and f.split('.')[1] == 'csv' and spec.match(f)]
    quantity_df = spark.read.csv(path.join(data_file_base,csv_file[0]), header=True)
    
quantity_df.write.parquet(path.join(output_base, 'quantity'), mode='overwrite')