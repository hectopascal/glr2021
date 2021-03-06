import os
import torch
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils


class LandmarksDataset(Dataset):
    """Landmarks dataset."""

    def __init__(self, csv_file, root_dir, transform=None, train="train"):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """

        self.labels = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        self.train = train

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        label = self.labels.iloc[idx, 1]
        filename = self.labels.iloc[idx, 0]
        img_name = os.path.join(
            self.root_dir,
            self.train,
            filename[0],
            filename[1],
            filename[2],
            filename + ".jpg",
        )
        img = Image.open(img_name).convert("RGB")
        image = transforms.ToTensor()(img).unsqueeze_(0)
        if self.transform:
            image = self.transform(image)

        return image, label
