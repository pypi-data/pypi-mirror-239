"""
Batch inference module for tabular models
"""

import argparse
from datetime import datetime
import mlflow
from pyspark.sql import SparkSession
from pyspark.sql.functions import struct
from databricks.sdk import WorkspaceClient


parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str)
parser.add_argument("--model_version", type=str)
parser.add_argument("--input_table_name", type=str)
parser.add_argument("--result_type", type=str)
parser.add_argument("--output_table_path", type=str)
args = parser.parse_args()


def main(
    model_name: str = args.model_name,
    model_version: str = args.model_version,
    input_table_name: str = args.input_table_name,
    result_type: str = args.result_type,
    output_table_path: str = args.output_table_path,
):
    """
    Main batch inference function
    """
    spark = SparkSession.builder.getOrCreate()
    workspace_client = WorkspaceClient()

    # load table as a Spark DataFrame
    table = spark.table(input_table_name)

    # Load model and run inference
    predict = mlflow.pyfunc.spark_udf(
        spark=spark,
        model_uri=f"models:/{model_name}/{model_version}",
        result_type=result_type,
        )

    # Perform inference via model.transform()
    print("Starting inference...")
    output_df = table.withColumn("prediction", predict(struct(*table.columns)))
    print("Inference - DONE.")

    # Save predictions
    predictions_path = (f"{output_table_path}_{datetime.now().isoformat()}"
                        .replace(":", "."))
    print(f"Saving predictions to {predictions_path}")
    output_df.write.save(predictions_path)

    print("Sample of outputs:")
    print(output_df.limit(5).toPandas())

    workspace_client.dbutils.jobs.taskValues.set(
        key="predictions_path", value=predictions_path)


if __name__ == "__main__":
    main()
