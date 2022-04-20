import os
from torchvision.io import read_image
from ..base import BaseDataset


class Dataset(BaseDataset):
    def __init__(self, data_dir, label_dir, transforms=None):
        super().__init__(data_dir=data_dir, label_dir=label_dir, transforms=transforms)

    def __getitem__(self, idx):
        img = read_image(self.data[idx])
        label = self.labels[idx]
        if self.transforms:
            img, label = self.transforms(img, label)

        return img, label

    def get_data(self, data_dir):
        self.data = sorted([path for path in os.listdir(data_dir)])

    def get_labels(self, label_dir):
        self.labels = sorted([path for path in os.listdir(label_dir)])
