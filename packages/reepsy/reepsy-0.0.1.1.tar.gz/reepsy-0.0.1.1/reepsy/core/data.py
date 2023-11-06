from torch.utils.data import DataLoader

from torchvision.transforms import ToTensor

from reepsy.utils.preparing_dataset import PreparingDataset


class Data():
    def load_dataset(dataset_data_path: str, dataset_csv_path: str, transform=ToTensor(),  batch_size: int = 32) -> DataLoader:
        preparing_dataset = PreparingDataset(
            dataset_csv_path=dataset_csv_path,
            dataset_data_path=dataset_data_path,
            transform=transform
        )
        dataset = DataLoader(
            dataset=preparing_dataset,
            batch_size=batch_size,
            shuffle=True
        )
        return dataset
