#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@brief  Main script to run the testing on the GoodBadframe package. This code has been adapted from https://github.com/luiscarlosgph/vitcifar10/tree/main
@author Hassna Irzan (rmaphir@gmail.com).
@date   30 August 2023
"""

import argparse
import numpy as np
import torch
import torchvision
import sklearn
import sklearn.metrics
import json
import os

# My imports
import model_functions
from mydatasets import MultiDatasetClass



def help(short_option):
    """
    @returns The string with the help information for each command line option.
    """
    help_msg = {
        "--json_datasets": "Path to the json file containing the paths to the datasets and partition files (required: True)",
        "--resume": "Path to the checkpoint file (required: True)",
        "--bs": "Batch size used for testing (required: True)",
    }
    return help_msg[short_option]


def parse_cmdline_params():
    """@returns The argparse args object."""
    args = argparse.ArgumentParser(
        description="PyTorch ViT for training/validation on CIFAR-10."
    )
    args.add_argument(
        "--json_datasets", required=True, type=str, help=help("--json_datasets")
    )
    args.add_argument("--resume", required=True, type=str, help=help("--resume"))
    args.add_argument("--bs", required=True, type=int, help=help("--bs"))

    return args.parse_args()


def readjson(datasets_json_file):
    """
    @brief Function that reads the json file with the paths to the datasets.
    @param[in]  data_js_file_path  Path to the json file that contains the paths to the datasets.
    @returns a tuple with the data directory, the labels file path and the partition file path.
    """

    with open(datasets_json_file, "r") as json_file:
        data = json.load(json_file)

    # Extract keys and lists
    data_dirs = data["data_dirs"]
    labels_files = data["labels_files"]

    return data_dirs, labels_files

def load_dataset(
    test_preproc_tf,
    data_dirs,
    labels_files,
    test_bs: int = 512,
    num_workers: int = 8,
    device="cuda",
):
    test_dataset = MultiDatasetClass(
        data_dirs,
        labels_files,
        stage="test",
        transform=test_preproc_tf,
    )

    # Create dataloaders
    test_dl = torch.utils.data.DataLoader(
        test_dataset, batch_size=test_bs, shuffle=False, num_workers=num_workers
    )
  
    return test_dl

def main():
    # Parse command line parameters
    args = parse_cmdline_params()

    # Set device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Prepare preprocessing layers
    _, test_preproc_tf = model_functions.build_preprocessing_transforms()

    # Read the json file with the paths to the datasets
    data_dirs, labels_files = readjson(
        datasets_json_file=args.json_datasets
    )

    # Get dataloaders for training and testing
    test_dl = load_dataset(test_preproc_tf=test_preproc_tf, data_dirs=data_dirs, labels_files=labels_files, test_bs=args.bs, device=device)
    print("[INFO] Number of testing images: {}".format(len(test_dl.dataset)))

    # Build model
    net = model_functions.build_model(num_classes=2, pretrained=True)

    # Enable multi-GPU support
    net = torch.nn.DataParallel(net)
    torch.backends.cudnn.benchmark = True

    # Load weights from file
    state = torch.load(args.resume)
    net.load_state_dict(state["net"])

    # Use cross-entropy loss
    loss_func = torch.nn.CrossEntropyLoss()

    # Run testing
    avg_loss, percentage_correct, y_true, y_pred = model_functions.valid(
        net, test_dl, loss_func
    )

    # Print results report
    print("[INFO] Average loss: {}".format(avg_loss))
    print(
        "[INFO] Percentage of images correctly classified: {}%".format(
            percentage_correct
        )
    )
    target_names = ["non-informative", "informative"]

    print("[INFO] Classification report:")
    print(
        sklearn.metrics.classification_report(
            y_true, y_pred, target_names=target_names, digits=4
        )
    )


if __name__ == "__main__":
    main()
