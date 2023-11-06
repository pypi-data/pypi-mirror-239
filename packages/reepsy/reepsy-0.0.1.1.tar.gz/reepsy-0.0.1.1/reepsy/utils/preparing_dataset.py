import os
import torch

import pandas as pd
from skimage import io

from torch.utils.data import Dataset


class PreparingDataset(Dataset):
    def __init__(self,  dataset_csv_path, dataset_data_path, transform=None):
        self.annotations = pd.read_csv(dataset_csv_path)
        self.root_dir = dataset_data_path
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        img_path = os.path.join(self.root_dir, self.annotations.iloc[index, 0])
        image = io.imread(img_path)
        y_label = torch.tensor(int(self.annotations.iloc[index, 1]))

        if self.transform:
            image = self.transform(image)

        return (image, y_label)
