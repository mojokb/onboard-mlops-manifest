from __future__ import print_function
import argparse
from kubernetes import config
import kubernetes.client
from kubernetes.client.rest import ApiException

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--namespace', type=str, default="argo")
parser.add_argument('--service_name', type=str, default="onboard-mlops-model")

config.load_incluster_config()

def get_f1_scroe_from_knative(namespace="argo", name="onboard-mlops-model"):

    # Enter a context with an instance of the API kubernetes.client
    with kubernetes.client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = kubernetes.client.CustomObjectsApi(api_client)
        group = 'serving.knative.dev' # str | the custom resource's group
        version = 'v1' # str | the custom resource's version
        namespace = 'argo' # str | The custom resource's namespace
        plural = 'services' # str | the custom resource's plural name. For TPRs this would be lowercase plural kind.
        name = 'onboard-mlops-model' # str | the custom object's name
        try:
            api_response = api_instance.get_namespaced_custom_object(group, version, namespace, plural, name)
            f1_score = api_response.get('metadata').get('labels').get('f1_score')
            return float(f1_score)
        except ApiException as e:
            return 0


print(get_f1_scroe_from_knative(args.namespace, args.service_name))

