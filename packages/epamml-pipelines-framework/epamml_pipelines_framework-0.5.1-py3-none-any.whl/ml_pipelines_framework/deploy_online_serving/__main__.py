import argparse
import requests
import time
import json
import mlflow

from mlflow.tracking.client import MlflowClient
from databricks.sdk import WorkspaceClient

# Set up params
parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str)
parser.add_argument("--model_stage", type=str)
parser.add_argument("--model_version", type=str)
parser.add_argument("--endpoint_name", type=str)
parser.add_argument("--workload_size", type=str)
parser.add_argument("--scale_to_zero_enabled", type=bool)
parser.add_argument("--databricks_host", type=str)
args = parser.parse_args()

model_name = args.model_name
model_stage = args.model_stage
model_version = args.model_version
endpoint_name = args.endpoint_name
workload_size = args.workload_size
scale_to_zero_enabled = args.scale_to_zero_enabled
databricks_host = args.databricks_host

def get_latest_model_version(model_name: str, 
                             stage: str,
                             client: MlflowClient):
  '''
  Get model's version from stages by provided model name and stage.
  '''
  models = client.get_latest_versions(model_name, stages=[stage])
  for m in models:
    new_model_version = m.version
  return new_model_version


def set_model_version(model_name: str,
                      model_stage: str,
                      client: MlflowClient
                      ):
    '''
    Set the latest model version. 
    '''
    stages = ['Staging', 'Production', 'Archived', 'None']
    if model_stage in stages:
        model_version = get_latest_model_version(model_name=model_name, 
                                                 stage=model_stage, 
                                                 client=client
                                                 )
    else:
       raise ValueError(f'Model can be one of the following: {stages}.\nReceived value: {model_stage}\n') 

    return model_version


def set_headers(token: str):
    '''
    Create an authorization header for subsequent REST calls
    '''
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    return headers

def set_json_body(endpoint_name: str, 
                  model_name: str, 
                  model_version: str, 
                  workload_size: str, 
                  scale_to_zero_enabled: bool):
    json_body = {
    "name": endpoint_name,
    "config": {
    "served_models": [{
        "model_name": model_name,
        "model_version": model_version,
        "workload_size": workload_size,
        "scale_to_zero_enabled": scale_to_zero_enabled
            }]
        }
    }
    return json_body

## Model serving endpoint creation and deletion functions

def create_endpoint(endpoint_name: str,
                    databricks_host: str,
                    headers: dict,
                    json_body: dict
                    ):
  '''
  Create or update model serving endpoint.
  '''
  #get endpoint status
  endpoint_url = f"{databricks_host}/api/2.0/serving-endpoints"
  url = f"{endpoint_url}/{endpoint_name}"
  r = requests.get(url, headers=headers)
  if "RESOURCE_DOES_NOT_EXIST" in r.text:  
    print("Creating this new endpoint: ", f"{databricks_host}/serving-endpoints/{endpoint_name}/invocations")
    re = requests.post(endpoint_url, headers=headers, json=json_body)
  else:
    new_model_version = (json_body['config'])['served_models'][0]['model_version']
    print("Provided endpoint exists! Updating it to a new config with new model version: ", new_model_version)
    
    # update config
    url = f"{endpoint_url}/{endpoint_name}/config"
    re = requests.put(url, headers=headers, json=json_body['config']) 
    
    # wait till new config file in place
    #get endpoint status
    url = f"{databricks_host}/api/2.0/serving-endpoints/{endpoint_name}"
    retry = True
    total_wait = 0
    while retry:
      r = requests.get(url, headers=headers)
      assert r.status_code == 200, f"Expected an HTTP 200 response when accessing endpoint info, received {r.status_code}"
      endpoint = json.loads(r.text)
      if "pending_config" in endpoint.keys():
        seconds = 10
        print("New config still pending")
        if total_wait < 6000:
          #if less than 10 mins waiting, keep waiting
          print(f"Wait for {seconds} seconds")
          print(f"Total waiting time so far: {total_wait} seconds")
          time.sleep(10)
          total_wait += seconds
        else:
          print(f"Stopping,  waited for {total_wait} seconds")
          retry = False  
      else:
        print("New config in place now!")
        retry = False
  assert re.status_code == 200, f"Expected an HTTP 200 response, received {re.status_code}"


def delete_model_serving_endpoint(endpoint_name: str,
                                databricks_host: str,
                                headers: dict,
                                ):
  '''
  Delete model serving endpoint
  '''
  endpoint_url = f"{databricks_host}/api/2.0/serving-endpoints"
  url =  f"{endpoint_url}/{endpoint_name}" 
  response = requests.delete(url, headers=headers)
  if response.status_code != 200:
    raise Exception(f"Request failed with status {response.status_code}, {response.text}")
  else:
    print(endpoint_name, "endpoint is deleted!")
  #return response.json()

def wait_for_endpoint(endpoint_name: str,
                      databricks_host: str,
                      headers: dict,
                      ):
    '''
    Wait for endpoint to be ready
    '''
    endpoint_url = f"{databricks_host}/api/2.0/serving-endpoints"
    while True:
        url =  f"{endpoint_url}/{endpoint_name}"
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, f"Expected an HTTP 200 response, received {response.status_code}\n{response.text}"
 
        status = response.json().get("state", {}).get("ready", {})
        #print("status",status)
        if status == "READY": print(status); print("-"*80); return
        else: print(f"Endpoint not ready ({status}), waiting 10 seconds"); time.sleep(10) # Wait 10 seconds


def main(endpoint_name=endpoint_name,
         model_name=model_name,
         model_version=model_version,
         model_stage=model_stage,
         workload_size=workload_size,
         scale_to_zero_enabled=scale_to_zero_enabled,
         databricks_host=databricks_host
         ):   
    
    mlflow.set_tracking_uri("databricks")
    client = MlflowClient()

    #generate API token
    w = WorkspaceClient()
    databricks_token = w.tokens.create(comment=f'sdk-{time.time_ns()}', lifetime_seconds=600).token_value
    
    if model_version:
       pass
    elif model_stage: 
        model_version = set_model_version(model_name, model_stage, client)
    
    headers = set_headers(databricks_token)
    json_body = set_json_body(endpoint_name, model_name, model_version, 
                              workload_size, scale_to_zero_enabled)
    create_endpoint(endpoint_name, databricks_host, headers, json_body)
    wait_for_endpoint(endpoint_name, databricks_host, headers)

    ## Set up params to be passed to the scoring task
    dbutils = w.dbutils
    dbutils.jobs.taskValues.set(key='endpoint_name', value=endpoint_name)
    dbutils.jobs.taskValues.set(key='databricks_host', value=databricks_host)

if __name__ == '__main__':
    main()

