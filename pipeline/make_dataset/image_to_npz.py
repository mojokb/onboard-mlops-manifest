import argparse
from PIL import Image
import os
import numpy as np
from sklearn.model_selection import train_test_split

support_image = ['png', 'jpg']
ignore_files = ['labels.txt']


def image_label_to_npz(image_path=".",
                       label_file_path="labels.txt",
                       data_split="none",
                       save_path="."):
    array_of_images = []
    labels = []
    file_list = os.listdir(image_path)
    file_list.sort()
    filename_list = []
    for _, file in enumerate(file_list):
        if file in ignore_files:
            continue
        if not file.split(".")[-1] in support_image:  # to check if file has a certain name
            raise RuntimeError(f"not support file extension {file}")
        filename_list.append(file)
        single_array = np.array(Image.open(os.path.join(image_path, file)))
        array_of_images.append(single_array)

    label_file = open(label_file_path, 'r')
    label_dict = {}
    while True:
        line = label_file.readline()
        if not line:
            break
        label_file_name, label_label = line.split()
        label_dict[label_file_name] = label_label

    for filename in filename_list:
        if not filename in label_dict.keys():
            raise RuntimeError(f"not exists {filename} labels.txt")
        labels.append(label_dict[filename])

    if len(array_of_images) != len(labels):
        raise RuntimeError(f'이미지({len(array_of_images)})랑 라벨({len(labels)})의 수가 맞지 않음')

    if data_split == 'none':
        data_train, data_valid, labels_train, labels_valid = train_test_split(array_of_images, labels, stratify=y,
                                                                              test_size=0.10, random_state=42)
        data_train, data_test, labels_train, labels_test = train_test_split(data_train, labels_train,
                                                                            test_size=0.10, random_state=42)
        np.savez(os.path.join(save_path, "train_set.npz"), x=data_train, y=labels_train)
        np.savez(os.path.join(save_path, "valid_set.npz"), x=data_valid, y=labels_valid)
        np.savez(os.path.join(save_path, "test_set.npz"), x=data_test, y=labels_test)

    if data_split == 'train_valid':
        data_train, data_valid, labels_train, labels_valid = train_test_split(array_of_images, labels, stratify=y,
                                                                              test_size=0.10, random_state=42)
        np.savez(os.path.join(save_path, "train_set.npz"), x=data_train, y=labels_train)
        np.savez(os.path.join(save_path, "valid_set.npz"), x=data_valid, y=labels_valid)

    if data_split == 'test':
        np.savez(os.path.join(save_path, "test_set.npz"), x=array_of_images, y=labels)

    print("Success")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default="/workdir", help='--image_path=/workdir')
    parser.add_argument('--save_path', type=str, default="/workdir", help="--save_path=./workdir")
    parser.add_argument('--data_split', type=str, default="/workdir", help="--data_split=[none|train_test]")
    args = parser.parse_args()

    if args.data_split == 'none':
        image_label_to_npz(image_path=args.image_path,
                           label_file_path=args.image_path + "/labels.txt",
                           data_split='none',
                           save_path=args.save_path)

    elif args.data_split == 'train_test':
        image_label_to_npz(image_path=args.image_path + "/train",
                           label_file_path=args.image_path + "/train/labels.txt",
                           data_split='train_valid',
                           save_path=args.save_path)

        image_label_to_npz(image_path=args.image_path + "/test",
                           label_file_path=args.image_path + "/test/labels.txt",
                           data_split='test',
                           save_path=args.save_path)
    else:
        raise RuntimeError("data_split is [none|train_test]")
