import argparse
import requests
from pyspark.sql import SparkSession
from databricks.sdk import WorkspaceClient
import os


parser = argparse.ArgumentParser()

parser.add_argument("--url", type=str)
parser.add_argument("--delta_table_path", type=str)
parser.add_argument("--dbfs_path", type=str)
parser.add_argument("--debug_main_pipeline", type=str)

args = parser.parse_args()


def main(
    url: str = args.url,
    delta_table_path: str = args.delta_table_path,
    dbfs_path: str = args.dbfs_path,
    debug_main_pipeline: str = args.debug_main_pipeline,
):
    """Main data pipeline function"""
    spark = SparkSession.builder.getOrCreate()

    # Skip all stages if debugging main pipeline
    if debug_main_pipeline.lower() == "true":
        try:
            spark.read.format("delta").load(f"/{delta_table_path}")
        except Exception as exc:
            if 'Table not found' in str(exc):
                raise ValueError(f'Tried to skip data loading from storage but table at {delta_table_path} not found') from exc
            else:
                raise Exception from exc
        else:
            print('Skipping data loading')
            return 0

    # Read CSV file
    print(f'Loading CSV file')
    response = requests.get(url)
    print(f'Loading done')
    # Get file_name from the url
    file_name = os.path.basename(url.split('?')[0])
    
    # Write file to DBFS
    print(f'Writing {file_name} to DBFS {dbfs_path}')
    full_path = os.path.join(dbfs_path, file_name)
    print(f'Full path is {full_path}')
    
    with open(full_path, "wb") as f:
        f.write(response.content)
    
    # Load the data to spark DataFrame    
    df = (spark
          .read
          .format("csv")
          .option("header", True)
          .option("inferSchema", True)
          .load(full_path))

    # Write data to Delta Table
    print(f'Writing to Delta Table {delta_table_path}')
    (df.write.format("delta")
          .mode("overwrite")
          .option("overwriteSchema", "true")
          .save(f"/{delta_table_path}"))
 
    print(f'Data successfully loaded into Delta Table {delta_table_path}')


if __name__ == "__main__":
    main()
