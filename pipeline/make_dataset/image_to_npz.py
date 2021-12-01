import argparse
from PIL import Image
import os
import numpy as np
from sklearn.model_selection import train_test_split

support_image = ['png', 'jpg']

def image_label_to_npz(image_path=".",
                       label_file_path=".labels.txt",
                       save_path="."):
    array_of_images = []
    labels = []
    file_list = os.listdir(image_path)
    file_list.sort()

    for _, file in enumerate(file_list):
        if file.split(".")[-1] in support_image:  # to check if file has a certain name
            single_im = Image.open(os.path.join(image_path, file))
            single_array = np.array(single_im)
            array_of_images.append(single_array)

    label_file = open(label_file_path, 'r')
    while True:
        line = label_file.readline()
        if not line:
            break
        labels.append(line.split()[1])

    if len(array_of_images) != len(labels):
        raise RuntimeError(f'이미지({len(array_of_images)})랑 라벨({len(labels)})의 수가 맞지 않음')

    data_train, data_valid, labels_train, labels_valid = train_test_split(array_of_images, labels,
                                                                          test_size=0.10, random_state=42)

    data_train, data_test, labels_train, labels_test = train_test_split(data_train, labels_train,
                                                                        test_size=0.10, random_state=42)

    np.savez(os.path.join(save_path, "train_set.npz"), x=data_train, y=labels_train)
    np.savez(os.path.join(save_path, "valid_set.npz"), x=data_valid, y=labels_valid)
    np.savez(os.path.join(save_path, "test_set.npz"), x=data_test, y=labels_test)
    print("Success")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default="/workdir", help='--image_path=/workdir')
    parser.add_argument('--label_file_path', type=str, default="/workdir/labels.txt",
                        help='--label_file_path=/workdir/labels.txt')
    parser.add_argument('--save_path', type=str, default="/workdir", help="--save_path=./workdir")
    args = parser.parse_args()

    image_label_to_npz(image_path=args.image_path,
                       label_file_path=args.label_file_path,
                       save_path=args.save_path)
