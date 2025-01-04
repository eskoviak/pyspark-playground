import pyspark.sql.functions as F
from pyspark.sql import SparkSession
import re
from os import path, listdir

# get or create a spark context
spark = SparkSession.builder.appName("ed_files/read_activity_exports.py").getOrCreate()

output_base = '/opt/spark/data/sparkOutput'
data_file_base = '/opt/spark/data/HealthAll_2024-12-345_14-58-25_SimpleHealthExportCSV'
activity_base = r'^HKWorkoutActivityType'
activities = [
    'Cycling',
    'Yoga', 
    'TraditionalStrengthTraining', 
    'FunctionalStrengthTraining',
    'CrossTraining',
    'Elliptical',
    'Golf',
    'Hiking',
    'Other',
    'PaddleSports',
    'Running',
    'SnowSports',
    'Snowboarding',
#    'Swimming',
    'WaterSports',
    'Walking',
]
first = True

for activity in activities:
    print(f'++++++++++++++++++++  Processing {activity}')
    spec = re.compile(activity_base + activity)
    csv_file = [f for f in listdir(data_file_base) if path.isfile(path.join(data_file_base, f)) and f.split('.')[1] == 'csv' and spec.match(f)]
    if first:
        activity_df = spark.read.csv(path.join(data_file_base,csv_file[0]), header=True)
        first = False
    else:
        activity_df = activity_df.unionByName(spark.read.csv(path.join(data_file_base,csv_file[0]), header=True), allowMissingColumns=True)

    
activity_df.write.parquet(path.join(output_base, 'activity'), mode='overwrite')
        
    

#yoga = re.compile(activity_base + 'Yoga')
#trad_strength = re.compile(activity_base + 'TraditionalStrengthTraining')



#file = '/opt/spark/data/HealthAll_2024-12-345_14-58-25_SimpleHealthExportCSV/HKWorkoutActivityTypeYoga_2024-12-345_14-59-10_SimpleHealthExportCSV.csv'
