import time
import json
import argparse
from importlib import import_module

from mlflow.tracking.client import MlflowClient
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus

from databricks.sdk import WorkspaceClient
from databricks.feature_store import FeatureStoreClient


parser = argparse.ArgumentParser()

parser.add_argument("--feature_preparation_task", type=str)
parser.add_argument("--trainer_module", type=str)
parser.add_argument("--fs_db_name", type=str)
parser.add_argument("--fs_table", type=str)
parser.add_argument("--feature_cols", type=str)
parser.add_argument("--label_col", type=str)
parser.add_argument("--experiment_name", type=str)
parser.add_argument("--model_name", type=str)
parser.add_argument("--model_hyperparams", type=json.loads)

args = parser.parse_args()


def wait_until_ready(model_name: str,
                     model_version: str,
                     client: MlflowClient):
    """ Waits until model version status changes to READY """
    status = ModelVersionStatus.PENDING_REGISTRATION
    while status != ModelVersionStatus.READY:
        model_version_details = client.get_model_version(
            name=model_name, version=model_version)
        status = ModelVersionStatus.from_string(model_version_details.status)
        print(f"Model status: {ModelVersionStatus.to_string(status)}")
        time.sleep(1)


def main(feature_preparation_task=args.feature_preparation_task,
         trainer_module=args.trainer_module,
         fs_db_name=args.fs_db_name,
         fs_table=args.fs_table,
         feature_cols=args.feature_cols,
         label_col=args.label_col,
         experiment_name=args.experiment_name,
         model_name=args.model_name,
         model_hyperparams=args.model_hyperparams,
         ):
    """
    Get data path from feature preparation task
    Run model-specific `train_model` function from `trainer_module`
    Move registered model to 'Staging'
    Write model name, version and release metric to TaskValues

    """
    w = WorkspaceClient()
    dbutils = w.dbutils
    fs_client = FeatureStoreClient()

    trainer = import_module(trainer_module)

    # If Feature Store path is not provided in task parameters, try to get it from feature preparation task
    if not (fs_db_name and fs_table):
        try:
            fs_db_name = dbutils.jobs.taskValues.get(
                taskKey=feature_preparation_task, key="fs_db_name")
            fs_table = dbutils.jobs.taskValues.get(
                taskKey=feature_preparation_task, key="fs_table")
        except ValueError as exc:
            raise ValueError(f"No data path in parameters or {feature_preparation_task} task") from exc

    # Load data from Feature Store
    df = fs_client.read_table(f'{fs_db_name}.{fs_table}')

    # Train model
    model_details = trainer.train_model(
        df=df,
        feature_cols=feature_cols,
        label_col=label_col,
        experiment_name=experiment_name,
        model_name=model_name,
        model_hyperparams=model_hyperparams,
        )

    client = MlflowClient()

    # After creating a model version, it may take a short period of time to become ready
    wait_until_ready(model_details.name, model_details.version, client)

    # Move model to Staging
    client.transition_model_version_stage(
        name=model_name,
        version=model_details.version,
        stage="Staging",
    )

    # Set params to be passed to another tasks
    dbutils.jobs.taskValues.set(key="model_name", value=model_name)
    dbutils.jobs.taskValues.set(
        key="model_version", value=model_details.version)
    dbutils.jobs.taskValues.set(
        key="model_release_metric",
        value=model_details.tags['model_release_metric'])


if __name__ == "__main__":
    main()
