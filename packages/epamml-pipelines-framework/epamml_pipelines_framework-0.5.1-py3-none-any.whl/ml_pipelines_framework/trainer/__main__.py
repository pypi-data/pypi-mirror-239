"""
Wrapper module for model-specific trainer
"""
import time
import json
import argparse
from importlib import import_module

import mlflow
from mlflow.tracking.client import MlflowClient
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus
from mlflow.models import infer_signature, set_signature

from databricks.sdk import WorkspaceClient
from databricks.feature_store import FeatureStoreClient, FeatureLookup

from pyspark.sql import SparkSession


parser = argparse.ArgumentParser()

parser.add_argument("--feature_preparation_task", type=str)
parser.add_argument("--use_feature_store", type=str)
parser.add_argument("--trainer_module", type=str)
parser.add_argument("--train_dataset_path", type=str)
parser.add_argument("--fs_table_path", type=str)
parser.add_argument("--feature_cols", type=str)
parser.add_argument("--label_col", type=str)
parser.add_argument("--primary_key", type=str)
parser.add_argument("--experiment_name", type=str)
parser.add_argument("--model_name", type=str)
parser.add_argument("--model_flavor", type=str)
parser.add_argument("--model_hyperparams", type=json.loads)
parser.add_argument("--model_release_metric", type=str)
parser.add_argument("--use_autolog", type=str)

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
         use_feature_store=args.use_feature_store,
         trainer_module=args.trainer_module,
         train_dataset_path=args.train_dataset_path,
         fs_table_path=args.fs_table_path,
         feature_cols=args.feature_cols,
         label_col=args.label_col,
         primary_key=args.primary_key,
         experiment_name=args.experiment_name,
         model_name=args.model_name,
         model_flavor=args.model_flavor,
         model_hyperparams=args.model_hyperparams,
         model_release_metric=args.model_release_metric,
         use_autolog=args.use_autolog,
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
    mlflow_client = MlflowClient()
    spark = SparkSession.builder.getOrCreate()

    trainer = import_module(trainer_module)

    use_feature_store = (use_feature_store.lower() == 'true')
    # If Feature Store path is not provided in task parameters, try to get it from feature preparation task
    if use_feature_store and not fs_table_path:
        try:
            fs_table_path = dbutils.jobs.taskValues.get(
                taskKey=feature_preparation_task, key="fs_table_path")
        except ValueError as exc:
            raise ValueError(f"No feature table path in parameters or {feature_preparation_task} task") from exc
    if not train_dataset_path:
        try:
            train_dataset_path = dbutils.jobs.taskValues.get(
                taskKey=feature_preparation_task, key="train_dataset_path")
        except ValueError as exc:
            raise ValueError(f"No train_dataset_path in parameters or {feature_preparation_task} task") from exc

    # Read feature column list from args or upstream task
    if feature_preparation_task and not feature_cols:
        feature_cols = json.loads(
            dbutils.jobs.taskValues.get(
                taskKey=feature_preparation_task, key='features'))
        print(f'Using feature columns from upstream feature preparation task: {feature_cols}')
    elif feature_cols:
        print(f'Using feature columns from Train task parameters: {feature_cols}')
        feature_cols = json.loads(feature_cols)
    else:
        raise NotImplementedError('No feature columns')

    # Read training dataset and optionally join features from Feature Store
    if not spark.catalog.tableExists(train_dataset_path):
        raise FileNotFoundError(f'Train dataset not found at {train_dataset_path}')
    train_df = spark.read.table(train_dataset_path)

    if use_feature_store:
        # TODO: implement multiple feature lookups
        feature_lookups = [
            FeatureLookup(
                table_name=fs_table_path,
                feature_names=feature_cols,
                lookup_key=primary_key,
            ),
        ]
        training_set = fs_client.create_training_set(
            df=train_df,
            feature_lookups=feature_lookups,
            label=label_col,
            exclude_columns=primary_key,
        )
        train_df = training_set.load_df()


    # Set experiment or create new if not exists
    experiment = mlflow.set_experiment(experiment_name)
    print(f'Experiment: {experiment_name}')
    
    # Train model
    mlflow.autolog(
        # Disable autologging, if `use_autolog` param is `true`
        # In this case, all logging should be handled by `train_model` function
        disable=(use_autolog.lower() == 'false'),
        log_input_examples=True,
        )
    with mlflow.start_run(experiment_id=experiment.experiment_id):
        run_id = mlflow.active_run().info.run_id
        print(f'Started run {run_id} ({mlflow.active_run().info.run_name})')
        train_results = trainer.train_model(
            df=train_df,
            feature_cols=feature_cols,
            label_col=label_col,
            model_hyperparams=model_hyperparams,
            model_name=model_name,
            experiment_name=experiment_name,
            )
        if train_results and (metrics := train_results.get('metrics')):
            # TODO: handle some other metadata possibly returned by train_model
            print(metrics)
            mlflow.log_metrics(metrics)
    
        mlflow_flavor = import_module(f'mlflow.{model_flavor}')
        model_uri = f'runs:/{run_id}/model'
        if use_feature_store:
            # Log and register model with Feature Store metadata
            print('Logging model with Feature Store client')
            fs_client.log_model(
                model=mlflow_flavor.load_model(model_uri),
                artifact_path='fs_model',
                flavor=mlflow_flavor,
                training_set=training_set,
                registered_model_name=model_name,
            )
            model_uri = f'runs:/{run_id}/fs_model'
        else:
            # Register autologged (or logged inside train_model) model
            model_details = mlflow.register_model(
                model_uri=model_uri,
                name=model_name,
                tags={'model_release_metric': model_release_metric}
            )
        signature = infer_signature(
            model_input=train_df.select(feature_cols).limit(5).toPandas(),
            model_output=train_df.select(label_col).limit(5).toPandas())
        set_signature(model_uri, signature)

    # After creating a model version, it may take a short period of time to become ready
    model_version = mlflow_client.get_latest_versions(
        model_name, stages=['None'])[0].version
    wait_until_ready(
        model_name=model_name,
        model_version=model_version,
        client=mlflow_client
        )

    # Move model to Staging
    mlflow_client.transition_model_version_stage(
        name=model_name,
        version=model_version,
        stage="Staging",
    )

    # Set params to be passed to another tasks
    dbutils.jobs.taskValues.set(key="model_name", value=model_name)
    dbutils.jobs.taskValues.set(key="model_version", value=model_version)
    dbutils.jobs.taskValues.set(
        key="model_release_metric", value=model_release_metric)


if __name__ == "__main__":
    main()
