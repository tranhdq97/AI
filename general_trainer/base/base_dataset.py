from abc import abstractmethod
from torch.utils.data import Dataset


class BaseDataset(Dataset):
    """Base dataset module"""
    def __init__(self, data_dir, label_dir=None, transforms=None):
        self.data = None
        self.labels = None
        self.transforms = transforms
        self.get_data(data_dir)
        if label_dir:
            self.get_labels(label_dir)

    @abstractmethod
    def __getitem__(self, idx):
        pass

    def __len__(self):
        return len(self.data)

    @abstractmethod
    def get_data(self, data_dir):
        self.data = None

    @abstractmethod
    def get_labels(self, label_dir):
        self.labels = None
