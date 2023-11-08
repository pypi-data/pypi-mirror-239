"""
Data loader module
Read raw data file from ADLS or DBFS to delta table in Hive Metastore
TODO: add support for different formats and sources
"""

import argparse
import requests, os
from pyspark.sql import SparkSession
from databricks.sdk import WorkspaceClient

parser = argparse.ArgumentParser()

parser.add_argument("--url", type=str)
#parser.add_argument("--adls_storage_account", type=str)
#parser.add_argument("--adls_container_name", type=str)
#parser.add_argument("--adls_file_path", type=str)
#parser.add_argument("--secret_scope", type=str)
#parser.add_argument("--sas_token_key", type=str)
parser.add_argument("--dbfs_file_path", type=str)
parser.add_argument("--schema_name", type=str)
parser.add_argument("--delta_table_name", type=str)
parser.add_argument("--debug_main_pipeline", type=str)

args = parser.parse_args()


def main(
        url: str = args.url,
        #adls_storage_account: str = args.adls_storage_account,
        #adls_container_name: str = args.adls_container_name,
        #adls_file_path: str = args.adls_file_path,
        #secret_scope: str = args.secret_scope,
        #sas_token_key: str = args.sas_token_key,
        dbfs_file_path: str = args.dbfs_file_path,
        schema_name: str = args.schema_name,
        delta_table_name: str = args.delta_table_name,
        debug_main_pipeline: str = args.debug_main_pipeline,
):
    """Main data pipeline function"""
    spark = SparkSession.builder.getOrCreate()
    w = WorkspaceClient()
    dbutils = w.dbutils

    delta_table_path = f'{schema_name}.{delta_table_name}'

    # Skip all stages if debugging main pipeline
    if debug_main_pipeline.lower() == "true":
        if spark.catalog.tableExists(delta_table_path):
            print('Skipping data loading')
            print(f'Raw delta table exists at {delta_table_path}')
            dbutils.jobs.taskValues.set(
                key="raw_delta_table_path", value=delta_table_path)
            dbutils.jobs.taskValues.set(
                key="raw_delta_table_absolute_path",
                value=f'/user/hive/warehouse/{schema_name}.db/{delta_table_name}')
            return 0
        else:
            raise FileNotFoundError(f'Could not skip data loading as delta table at {delta_table_path} does not exist')

    # if data_source.lower() == 'adls':
    #     spark.conf.set(
    #         f"fs.azure.account.auth.type.{adls_storage_account}.dfs.core.windows.net",
    #         "SAS")
    #     spark.conf.set(
    #         f"fs.azure.sas.token.provider.type.{adls_storage_account}.dfs.core.windows.net",
    #         "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
    #     spark.conf.set(
    #         f"fs.azure.sas.fixed.token.{adls_storage_account}.dfs.core.windows.net",
    #         dbutils.secrets.get(scope=secret_scope, key=sas_token_key))

    #     raw_dataset_path = f"abfss://{adls_container_name}@{adls_storage_account}.dfs.core.windows.net/{adls_file_path}"

    # elif data_source.lower() == 'dbfs':
    #     if not dbfs_file_path.startswith('dbfs:'):
    #         raw_dataset_path = f'dbfs:{dbfs_file_path}'
    #     else:
    #         raw_dataset_path = dbfs_file_path
    #     # Check for file existence in DBFS path
    #     try:
    #         dbutils.fs.ls(raw_dataset_path)
    #     except Exception as exc:
    #         if 'java.io.FileNotFoundException' in str(exc):
    #             raise ValueError(f'Failed to load file from {raw_dataset_path}') from exc
    #         else:
    #             raise Exception from exc
    # else:
    #     raise NotImplementedError(f'Unknown data source: {data_source}')

    # Create schema if not exists
    if not spark.catalog.databaseExists(schema_name):
        print(f'Creating database {schema_name}')
        spark.sql(f'CREATE SCHEMA IF NOT EXISTS {schema_name}')

    # Read file from source
    print(f'Loading CSV file...')
    try: 
        response = requests.get(url)
    except:
        raise requests.exceptions.HTTPError(f"Failed to access URL {url}, status code: {response.status_code}")
    else: 
        print(f'Loading done sucessfully')
    
    # Get file_name from the url
    file_name = os.path.basename(url.split('?')[0])
    
    # Write file to DBFS
    print(f'Writing {file_name} to DBFS {dbfs_file_path}')
    full_path = os.path.join(dbfs_file_path, file_name)
    print(f'Full path is {full_path}')    
    with open(full_path, "wb") as f:
        f.write(response.content)
    
    # Read file from tmp location to Spark Dataframe
    print(f'Loading CSV file from {full_path} to dataframe')
    raw_dataframe = (spark
                     .read.format('csv')
                     .option("header", True)
                     .option("inferSchema", True)
                     .load(full_path))

    print(f'Loaded dataframe with {raw_dataframe.count()} rows')
    print(f'Dataframe columns: {raw_dataframe.columns}')

    # Write data to Delta Table
    print(f'Writing Delta Table to {delta_table_path}')

    (raw_dataframe.write
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(name=f"{delta_table_path}")
    )

    # Write delta table path to task values
    dbutils.jobs.taskValues.set(
        key="raw_delta_table_path", value=delta_table_path)

if __name__ == "__main__":
    main()
