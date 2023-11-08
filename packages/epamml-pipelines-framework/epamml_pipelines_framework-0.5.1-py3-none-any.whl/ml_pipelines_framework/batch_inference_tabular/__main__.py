"""
Batch inference module for tabular models
"""

import argparse
from datetime import datetime
import mlflow
from pyspark.sql import SparkSession
from pyspark.sql.functions import struct
from databricks.sdk import WorkspaceClient
from databricks.feature_store import FeatureStoreClient


parser = argparse.ArgumentParser()
parser.add_argument("--use_feature_store", type=str)
parser.add_argument("--model_name", type=str)
parser.add_argument("--model_version", type=str)
parser.add_argument("--input_table_path", type=str)
parser.add_argument("--result_type", type=str)
parser.add_argument("--output_table_path", type=str)
args = parser.parse_args()


def main(
    use_feature_store: str = args.use_feature_store,
    model_name: str = args.model_name,
    model_version: str = args.model_version,
    input_table_path: str = args.input_table_path,
    result_type: str = args.result_type,
    output_table_path: str = args.output_table_path,
):
    """
    Main batch inference function
    """
    spark = SparkSession.builder.getOrCreate()
    dbutils = WorkspaceClient().dbutils
    fs_client = FeatureStoreClient()

    # load table as a Spark DataFrame
    input_dataframe = spark.table(input_table_path)
    print('Sample of input dataframe:')
    print(input_dataframe.limit(5).show())

    # Load model and run inference
    print("Starting inference...")
    if use_feature_store.lower() == 'true':
        output_df = fs_client.score_batch(
            f"models:/{model_name}/{model_version}",
            input_dataframe
            )
    else:
        predict = mlflow.pyfunc.spark_udf(
            spark=spark,
            model_uri=f"models:/{model_name}/{model_version}",
            result_type=result_type,
            )
        output_df = input_dataframe.withColumn("prediction", predict(struct(*input_dataframe.columns)))

    # Save predictions
    print("Sample of outputs:")
    print(output_df.limit(5).show())

    predictions_path = f"{output_table_path}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"Saving predictions to {predictions_path}")
    output_df.write.saveAsTable(predictions_path)

    dbutils.jobs.taskValues.set(
        key="predictions_path", value=predictions_path)


if __name__ == "__main__":
    main()
