import argparse
import os
from minio import Minio
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('spam')


class DownloadMinio:
    def __init__(self, bucket_name, object_prefix, data_split, download_path):
        self.bucket_name = bucket_name
        self.object_prefix = object_prefix
        self.download_path = download_path
        self.data_split = data_split
        self.minio_client = None

    def _set_minio_client(self):
        """
        TODO have to move it to safety place...
        """
        self.client = Minio(
            "192.168.64.5:32008",
            access_key="aimmo_access_key",
            secret_key="aimmo_secret_key",
            region="my-region",
            secure=False
        )
        logger.info(self.client)

    def _get_list_from_minio(self, recursive):
        return self.client.list_objects(self.bucket_name, prefix=self.object_prefix, recursive=recursive)

    def _valid_data_split(self):
        if self.data_split == "train_test":
            iter = self._get_list_from_minio(recursive=False)
            # have to include /train /test
            obj_list = [obj for obj in iter]
            if 'train' not in obj_list or 'test' not in obj_list:
                raise RuntimeError("train_test type has to two dir types [train test]")

    def download(self):
        self._set_minio_client()
        self._valid_data_split()
        object_list = self._get_list_from_minio(recursive=True)
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
    parser.add_argument('--data_split', type=str, default="none", help='--data_split=[none|train_test]')
    args = parser.parse_args()

    download_minio = DownloadMinio(bucket_name=args.bucket_name,
                                   object_prefix=args.object_prefix,
                                   data_split=args.data_split,
                                   download_path=args.download_path)
    download_minio.download()