import copy
import torch
import torchdrift
from torch.utils.data import DataLoader
from torchvision import transforms
from src.models.onboard_dataset import OnboardDataset


class DriftDetector:
    def __init__(self):
        self.feature_extractor = None
        self.train_dataloader = None
        self.input_dataloader = None
        self.train_path = None
        self.valid_path = None
        self.transform = None
        self.batch = 256
        self.drift_detector = torchdrift.detectors.KernelMMDDriftDetector()

    def _set_transform(self):
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])

    def set_feature_extractor(self, model_path):
        model = torch.load(model_path)
        self.feature_extractor = copy.deepcopy(model)
        self.feature_extractor.classifier = torch.nn.Identity()

    def set_dataloader(self, train_path, input_path):
        self.train_dataloader = DataLoader(OnboardDataset(path=train_path, rate=0.5, transform=self.transform),
                                           batch_size=self.batch, shuffle=True)
        self.input_dataloader = DataLoader(OnboardDataset(path=input_path, rate=0.5, transform=self.transform),
                                           batch_size=self.batch, shuffle=True)

    def fit(self):
        torchdrift.utils.fit(self.train_dataloader, self.feature_extractor, self.drift_detector)
        inputs, _ = next(iter(self.input_dataloader))
        features = self.feature_extractor(inputs)
        score = self.drift_detector(features)
        p_val = self.drift_detector.compute_p_value(features)
        print(score, p_val)
        if p_val < 0.01:
            print("Drifted Inputs")


if __name__ == "__main__":
    detector = DriftDetector()
    detector.set_feature_extractor(model_path="./model.pt")
    detector.set_dataloader(train_path="./data/processed/valid_set.npz",
                            input_path="./train_set.npz")
    detector.fit()
