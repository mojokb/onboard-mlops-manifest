import os
import argparse
from minio import Minio


class UploadMinio:
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

    def upload(self, dataset_path, prefix):
        for file in ['train_set.npz', 'valid_set.npz', 'test_set.npz']:
            self.client.fput_object(
                bucket_name=self.bucket_name,
                object_name=f'{prefix}{file}',
                file_path=os.path.join(dataset_path, file))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket_name', type=str, default="torch-dataset-queue")
    parser.add_argument('--dataset_path', type=str, default="/workdir")
    parser.add_argument('--prefix', type=str, default="12345/")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    onboard_minio = UploadMinio(bucket_name=args.bucket_name)
    onboard_minio.upload(args.dataset_path, args.prefix)