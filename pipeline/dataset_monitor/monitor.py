import os
import argparse
from minio import Minio


class MonitorMinio:
    def __init__(self, bucket_name):
        self.client = None
        self.bucket_name = bucket_name
        self._set_minio_client()

    def _set_minio_client(self):
        """
        TODO replace key to env
        :return:
        """
        self.client = Minio(
            "192.168.64.5:32008",
            access_key="aimmo_access_key",
            secret_key="aimmo_secret_key",
            region="my-region",
            secure=False
        )

    def monitor(self):
        list = self.client.list_objects(bucket_name="torch-dataset")
        dataset_list = []
        if list:
            dataset_list = [x.object_name for x in list]
            if len(dataset_list) >= 3:
            # TODO have to triggering train , create branch


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket_name', type=str, default="torch-dataset-train")
    args = parser.parse_args()

    minitor = MonitorMinio(args.bucket_name)