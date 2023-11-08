import argparse
import json
from importlib import import_module

from pyspark.pandas import DataFrame as PandasAPIonSparkDataFrame
from pandas import DataFrame as PandasDataframe
from pyspark.sql import SparkSession

from databricks.sdk import WorkspaceClient
from databricks.feature_store import FeatureStoreClient

parser = argparse.ArgumentParser()

parser.add_argument("--data_loader_task", type=str)
parser.add_argument("--preprocessor_module", type=str)
parser.add_argument("--raw_delta_table_path", type=str)
parser.add_argument("--train_dataset_path", type=str)
parser.add_argument("--use_feature_store", type=str)
parser.add_argument("--fs_table_path", type=str)
parser.add_argument("--fs_primary_key", type=str)
parser.add_argument("--label_col", type=str)

args = parser.parse_args()


def main(
    data_loader_task: str = args.data_loader_task,
    preprocessor_module: str = args.preprocessor_module,
    raw_delta_table_path: str = args.raw_delta_table_path,
    train_dataset_path: str = args.train_dataset_path,
    use_feature_store: str = args.use_feature_store,
    fs_table_path: str = args.fs_table_path,
    fs_primary_key: str = args.fs_primary_key,
    label_col: str = args.label_col,
):
    """
    Main feature preparation function
    """

    fs_client = FeatureStoreClient()
    dbutils = WorkspaceClient().dbutils
    spark = SparkSession.builder.getOrCreate()

    preprocessor = import_module(preprocessor_module)

    # If raw Delta Table path is not provided in task parameters, try to get it from data loader task
    if not raw_delta_table_path:
        try:
            raw_delta_table_path = dbutils.jobs.taskValues.get(
                taskKey=data_loader_task, key="raw_delta_table_path"
            )
        except ValueError as exc:
            raise ValueError(
                f"No data path in parameters or {data_loader_task} task"
            ) from exc

    if not spark.catalog.tableExists(raw_delta_table_path):
        raise FileNotFoundError(f"Raw dataset at {raw_delta_table_path} does not exist")

    # Read Delta Table to dataframe
    print(f"Loading raw data from Delta Table {raw_delta_table_path}")
    raw_dataframe = spark.read.table(raw_delta_table_path)
    print(f"Raw dataframe shape: {raw_dataframe.count()}, {len(raw_dataframe.columns)}")
    print(raw_dataframe.columns)

    # Clean data and compute features
    print("Processing dataframe")
    processed_dataframe = preprocessor.process_dataframe(raw_dataframe)

    # Check the return type from preprocessor and convert to Spark DataFrame is applicable
    if isinstance(processed_dataframe, PandasAPIonSparkDataFrame):
        processed_dataframe = processed_dataframe.to_spark()
    elif isinstance(processed_dataframe, PandasDataframe):
        processed_dataframe = spark.createDataFrame(processed_dataframe)
    
    print(f"Processed dataframe shape: {processed_dataframe.count()}, {len(processed_dataframe.columns)}")
    print(processed_dataframe.columns)

    if use_feature_store.lower() == "true":
        # Write computed features to Feature Store
        if not spark.catalog.tableExists(fs_table_path):
            print(f"Feature table {fs_table_path} does not exist. Creating table")
            fs_client.create_table(
                name=fs_table_path,
                primary_keys=[fs_primary_key],
                schema=processed_dataframe.drop(label_col).schema,
                description=f"Features computed by {preprocessor_module}",
            )
        print("Updating feature table in Feature Store")
        fs_client.write_table(
            df=processed_dataframe.drop(label_col),
            name=fs_table_path,
            mode="overwrite",
        )
        feature_cols = [col for col in processed_dataframe.columns 
                        if col not in (fs_primary_key, label_col)]
        
        dbutils.jobs.taskValues.set(key="fs_table_path", value=fs_table_path)
        dbutils.jobs.taskValues.set(key="features", value=json.dumps(feature_cols))

        processed_dataframe = processed_dataframe.select(fs_primary_key, label_col)

    (
        processed_dataframe.write.mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(name=train_dataset_path)
    )
    dbutils.jobs.taskValues.set(key="train_dataset_path", value=train_dataset_path)


if __name__ == "__main__":
    main()
