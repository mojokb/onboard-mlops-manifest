import argparse
import os
from minio import Minio
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('spam')


class DownloadMinio:
    def __init__(self, bucket_name, object_prefix, download_path):
        self.bucket_name = bucket_name
        self.object_prefix = object_prefix
        self.download_path = download_path
        self.minio_client = None
        self._set_minio_client()

    def _set_minio_client(self):
        self.client = Minio(
            "192.168.64.5:32008",
            access_key="aimmo_access_key",
            secret_key="aimmo_secret_key",
            region="my-region",
            secure=False
        )
        logger.info(self.client)

    def download(self):
        object_list = self.client.list_objects(self.bucket_name, prefix=self.object_prefix, recursive=True)
        total = 0
        for obj in object_list:
            self.client.fget_object(self.bucket_name, obj.object_name,
                                    os.path.join(self.download_path, obj.object_name))
            total += 1
        logger.info(f"{total} download")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket_name', type=str, default="torch-raw-images", help='--bucket_name=torch-raw-images')
    parser.add_argument('--object_prefix', type=str, default="20211128-163614/", help='--object_prefix=20211128-163614/')
    parser.add_argument('--download_path', type=str, default="./workdir", help='--download_path=./workdir')
    args = parser.parse_args()

    download_minio = DownloadMinio(bucket_name=args.bucket_name,
                                   object_prefix=args.object_prefix,
                                   download_path=args.download_path)
    download_minio.download()