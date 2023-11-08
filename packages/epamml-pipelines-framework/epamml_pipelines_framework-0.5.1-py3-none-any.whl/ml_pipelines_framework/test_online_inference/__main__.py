import argparse
import requests
import time
import json

from databricks.sdk import WorkspaceClient

# Set up params
parser = argparse.ArgumentParser()

parser.add_argument("--input_data", type=str)
parser.add_argument("--depends_on_task", type=str)
parser.add_argument("--databricks_host", type=str)
parser.add_argument("--endpoint_name", type=str)
args = parser.parse_args()


def main(input_data: str = args.input_data,
         depends_on_task: str = args.depends_on_task,
         databricks_host: str = args.databricks_host,
         endpoint_name: str = args.endpoint_name
         ):

    data_json = json.loads(input_data)
    
    #generate API token
    w = WorkspaceClient()
    databricks_token = w.tokens.create(comment=f'sdk-{time.time_ns()}', lifetime_seconds=300).token_value                                             
    
    dbutils = w.dbutils
    
    # Get params from the upstream task 
    if depends_on_task:
        if not databricks_host:
            databricks_host = dbutils.jobs.taskValues.get(taskKey = depends_on_task,
                                                        key = 'databricks_host')
        if not endpoint_name:
            endpoint_name = dbutils.jobs.taskValues.get(taskKey = depends_on_task,
                                                        key = "endpoint_name")
    
    headers = {"Authorization": f"Bearer {databricks_token}",
                "Content-Type": "application/json"
                }

    url =  f"{databricks_host}/serving-endpoints/{endpoint_name}/invocations"
    response = requests.request(method="POST", headers=headers, url=url, json=data_json)
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}, {response.text}")
    predictions = response.json()
    print(predictions)

    return predictions


if __name__ == '__main__':
    main()