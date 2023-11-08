import argparse
from importlib import import_module

import mlflow


parser = argparse.ArgumentParser()
parser.add_argument("--comparator_module", type=str)
parser.add_argument("--model_name", type=str)
parser.add_argument("--model_version", type=str)
args = parser.parse_args()


def main(
    model_name=args.model_name,
    model_version=args.model_version,
    comparator_module=args.comparator_module,
):
    comparator = import_module(comparator_module)
    new_model_is_better = comparator.new_model_is_better

    mlflow_client = mlflow.MlflowClient()

    model = mlflow_client.get_registered_model(name=model_name)

    last_staging_metrics = {}
    last_production_metrics = {}
    for mv in model.latest_versions:
        print(mv.version, mv.current_stage, sep='\t')
        if mv.current_stage == 'Staging':
            model_staging_id = mv.version
            print(model_staging_id)
            run_id = mv.run_id
            print(run_id)
            run = mlflow_client.get_run(run_id=run_id)
            last_staging_metrics = run.data.metrics
        elif mv.current_stage == 'Production':
            model_production_id = int(mv.version)
            print(model_production_id)
            run_id = mv.run_id
            print(run_id)
            run = mlflow_client.get_run(run_id=run_id)
            print(run.data.metrics)
            last_production_metrics = run.data.metrics

    if new_model_is_better(last_production_metrics, last_staging_metrics):
        print("Staging model better")
        mlflow_client.transition_model_version_stage(
            name=model_name,
            version=model_staging_id,
            stage="Production",
        )
        mlflow_client.transition_model_version_stage(
            name=model_name,
            version=model_production_id,
            stage="Archived",
        )
    elif last_production_metrics == {}:
        mlflow_client.transition_model_version_stage(
            name=model_name,
            version=model_staging_id,
            stage="Production",
        )


if __name__ == '__main__':
    main()
