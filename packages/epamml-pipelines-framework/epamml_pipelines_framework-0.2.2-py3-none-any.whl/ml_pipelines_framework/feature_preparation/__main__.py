import argparse
from importlib import import_module

from pyspark import pandas as pd

from databricks.sdk import WorkspaceClient
from databricks.feature_store import FeatureStoreClient


parser = argparse.ArgumentParser()

parser.add_argument("--data_loader_task", type=str)
parser.add_argument("--preprocessor_module", type=str)
parser.add_argument("--delta_table_path", type=str)
parser.add_argument("--preprocess", type=str)
parser.add_argument("--dataset_path", type=str)
parser.add_argument("--fs_table_name", type=str)
parser.add_argument("--fs_db_name", type=str)
parser.add_argument("--fs_primary_key", type=str)
parser.add_argument("--debug_main_pipeline", type=str)

args = parser.parse_args()


def fs_exists(path):
    try:
        dbutils.fs.ls(path)
    except:
        return False
    return True


def main(
    data_loader_task: str = args.data_loader_task,
    preprocessor_module: str = args.preprocessor_module,
    delta_table_path: str = args.delta_table_path,
    preprocess: str = args.preprocess,
    dataset_path: str = args.dataset_path,
    fs_table_name: str = args.fs_table_name,
    fs_db_name: str = args.fs_db_name,
    fs_primary_key: str = args.fs_primary_key,
    debug_main_pipeline: str = args.debug_main_pipeline,
):
    """Main feature preparation function"""
    fs = FeatureStoreClient()
    w = WorkspaceClient()
    dbutils = w.dbutils

    preprocessor = import_module(preprocessor_module)

    fs_path = dataset_path + fs_table_name
    fs_data_path = f"dbfs:{fs_path}"

    # If data path not provided in task parameters, try to get it from data loader task
    if not delta_table_path:
        try:
            delta_table_path = dbutils.jobs.taskValues.get(
                taskKey=data_loader_task, key="delta_table_path")
        except ValueError as exc:
            raise ValueError(f"No data path in parameters or {data_loader_task} task") from exc

    # Skip all stages if debugging main pipeline
    if debug_main_pipeline == "true" and fs_exists(fs_path):
        dbutils.jobs.taskValues.set(key="fs_data_path", value=fs_data_path)
        return 0
    
    # Read Delta Table to dataframe
    print(f'Loading raw data from Delta Table {delta_table_path}')
    raw_dataframe = pd.read_delta(f"/{delta_table_path}")
    print(f"Loaded dataframe of shape {raw_dataframe.shape}")
    print(raw_dataframe.info())

    # Preprocessing
    if preprocess:
        print('Processing dataframe')
        processed_dataframe = preprocessor.process_dataframe(raw_dataframe)
        print('Processed dataframe shape: {processed_dataframe.shape}')
    else:
        processed_dataframe = raw_dataframe

    # Write processed dataframe to Feature Store
    if not fs_exists(fs_path):
        fs.create_table(
            name=fs_table_name,
            primary_keys=[fs_primary_key],
            schema=processed_dataframe.spark.schema(),
            description="cleaned data",
        )
    print("Writing table to Feature Store")
    fs.write_table(
        df=processed_dataframe.to_spark(),
        name=f"{fs_db_name}.{fs_table_name}",
        mode="overwrite",
    )

    dbutils.jobs.taskValues.set(key="data_path", value=fs_data_path)
    dbutils.jobs.taskValues.set(key="fs_db_name", value=fs_db_name)
    dbutils.jobs.taskValues.set(key="fs_table", value=fs_table_name)


if __name__ == "__main__":
    main()
