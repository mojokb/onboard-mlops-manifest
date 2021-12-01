import argparse
import os
import PIL
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('spam')


class VerifyRawData:
    def __init__(self, raw_path):
        self.raw_path = raw_path
        self.total_data_size = 0
        self.total_label_size = 0
        self.match_size = 28
        self.extensions = ['.png', '.jpg']
        self.labels_file_name = 'labels.txt'
        self.labels_file_path = os.path.join(raw_path, self.labels_file_name)

    def _check_image_extension(self, filename):
        _, extension = os.path.splitext(filename)
        # labels bypass
        if filename == self.labels_file_name:
            return True
        return extension.lower() in self.extensions

    def _check_image_size(self, filename):
        image = PIL.Image.open(os.path.join(self.raw_path, filename))
        width, height = image.size
        return width == height == self.match_size

    def _check_match_label(self):
        if os.path.isfile(self.labels_file_path):
            f = open(self.labels_file_path, 'r')
            while True:
                line = f.readline()
                if not line:
                    break
                filename = line.split()[0]
                filepath = os.path.join(self.raw_path, filename)
                if not os.path.isfile(filepath):
                    raise RuntimeError(f"Missed file {filename}")
        else:
            raise RuntimeError("Cannot find labels.txt in raw_path")

    def _verify_raw_image(self):
        file_list = os.listdir(self.raw_path)
        for file_name in file_list:
            if not self._check_image_extension(file_name):
                raise RuntimeError(f"{file_name} Not Match {self.extensions}")
            if not self._check_image_size(file_name):
                raise RuntimeError(f"{file_name} image size not match {self.match_size}")

    def test(self):
        self._check_match_label()
        print("Success")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_path', type=str, default="../mnist_image_folder_0", help='--raw_path=mnist_image_folder_1')
    args = parser.parse_args()

    test_data = VerifyRawData(raw_path=args.raw_path)
    test_data.test()