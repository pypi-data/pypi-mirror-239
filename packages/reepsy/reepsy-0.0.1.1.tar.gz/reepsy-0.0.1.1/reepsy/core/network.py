import torch
from torch.optim import Adam
from torch.nn import CrossEntropyLoss

from torchvision.models.googlenet import googlenet

from reepsy.utils.device import Device


class Network():
    def __init__(
        self,
        model=googlenet,
        optimizer=Adam,
        criterion=CrossEntropyLoss,
        learning_rate: float = 1e-3,
        device: Device = Device.get_device()
    ) -> None:
        self.__device = device
        self.__model = model(pretrained=True).to(device)
        self.__criterion = criterion()
        self.__optimizer = optimizer(self.__model.parameters(), learning_rate)

    def train(self, dataset, num_epochs: int = 1) -> any:
        for epoch in range(num_epochs):
            losses = []
            for _, (data, targets) in enumerate(dataset):
                data = data.to(device=self.__device)
                targets = targets.to(device=self.__device)

                scores = self.__model(data)
                loss = self.__criterion(scores, targets)

                losses.append(loss.item())

                self.__optimizer.zero_grad()
                loss.backward()

                self.__optimizer.step()
            print(f'Cost at epoch {epoch + 1} is {sum(losses)/len(losses)}')
        return self.__model

    def predict(self, dataset) -> float:
        num_correct = 0
        num_samples = 0
        self.__model.eval()

        with torch.no_grad():
            for x, y in dataset:
                x = x.to(device=self.__device)
                y = y.to(device=self.__device)

                scores = self.__model(x)
                _, predirections = scores.max(1)
                num_correct += (predirections == y).sum()
                num_samples += predirections.size(0)

        self.__model.train()
        return float(num_correct)/float(num_samples)

    def save(self, path) -> None:
        # self.__model
        pass

    def load(self, path) -> None:
        # self.__model
        pass
