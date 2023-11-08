"""""
@breif: Custom dataset class for reading multiple datasets with one class instantiation
@author:  Hassna Irzan (rmaphir@gmail.com)
@date: 27 October 2023

""" ""
import os
import json
import model_functions
import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image



class MultiDatasetClass(Dataset):
    """
    @brief: custom dataset class for reading multiple datasets with one class instantiation
    @param: data_dirs: list of data directories
    @param: partition_files: list of partition files
    @param: labels_files: list of labels files
    @param: stage: train, validation, or test
    @param: transform: transform to apply to the data
    """

    def __init__(
        self,
        data_dirs,
        labels_files,
        stage="train",
        transform=None,
    ):
        self.stage = stage.lower()
        self.data_dirs = data_dirs
        self.labels_dict = {}

        # Load labels information from multiple files
        for labels_file in labels_files:
            self.labels_dict.update(json.load(open(labels_file))[self.stage])
        
        self.file_names = list(self.labels_dict.keys())
        self.labels = list(self.labels_dict.values())
        self.transform = transform


    def __len__(self):
        "Denotes the total number of samples"
        return len(self.file_names)

    def __getitem__(self, index):
        "Generates one sample of data"
        file_name = self.file_names[index]
        label = self.labels_dict[file_name]

        # Determine which data directory to use based on the file name
        file_found = False
        for data_dir in self.data_dirs:
            file_name_path = os.path.join(data_dir, MultiDatasetClass.LABELS_MAP[label], file_name)

            if os.path.exists(file_name_path):
                file_found = True
                break

        if not file_found:
            raise FileNotFoundError(f"File {file_name} not found in any data directory.")

        # Read the image file
        frame = Image.open(file_name_path).convert("RGB")

        # Apply the transform
        if self.transform is not None:
            frame = self.transform(frame)

        return frame, label

    LABELS_MAP = {0: "blurry", 1: "clear"}


