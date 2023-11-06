import torch


class Device():
    def get_device() -> type[torch.device]:
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
