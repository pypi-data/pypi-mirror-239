"""
@brief: This script is used to visualise the data in the dataset, by reading the data from the DatasetClass and saving the images in a folder.
@author: Hassna Irzan (rmaphir@gmail.com)
@date: 29 August 2023
"""

import matplotlib.pyplot as plt
import os
import tqdm
import shutil
import numpy as np
import torch
import argparse
from train import load_dataset
from model_functions import build_preprocessing_transforms
from PIL import Image


def help(option):
    """
    @returns The string with the help information for each command line option.
    """
    help_msg = {
        "--jsdatasets": "Path to the json file containing the paths to the datasets",
        "--output_dir": "Path to the output directory",
    }
    return help_msg[option]


def parse_cmdline_params():
    """@returns The argparse args object."""
    args = argparse.ArgumentParser(
        description=" read the images and the labels from the dataset and save them in a folder"
    )
    args.add_argument(
        "--jsdatasets", required=True, type=str, help=help("--jsdatasets")
    )
    args.add_argument(
        "--output_dir", required=True, type=str, help=help("--output_dir")
    )

    return args.parse_args()


def main():
    """Main function."""

    # Parse command line
    args = parse_cmdline_params()
    jsdatasets = args.jsdatasets
    outoput_dir = args.output_dir

    batch_size = 1
    # Prepare preprocessing layers
    train_preproc_tf, valid_preproc_tf = build_preprocessing_transforms()

    train_dl, valid_dl = load_dataset(
        train_preproc_tf=train_preproc_tf,
        valid_preproc_tf=valid_preproc_tf,
        datasets_jsfile=jsdatasets,
        train_bs=batch_size,
        valid_bs=batch_size,
    )

    blurry_dir = os.path.join(outoput_dir, "blurry")
    clear_dir = os.path.join(outoput_dir, "clear")

    if os.path.exists(blurry_dir):
        shutil.rmtree(blurry_dir)
        os.makedirs(blurry_dir)

    if os.path.exists(clear_dir):
        shutil.rmtree(clear_dir)
        os.makedirs(clear_dir)

    # Create progress bar
    pbar = tqdm.tqdm(enumerate(valid_dl), total=len(valid_dl))
    means = torch.tensor([0.3543, 0.2360, 0.2374])
    stds = torch.tensor([0.2576, 0.2160, 0.2180])

    # Run forward-backward over all the samples
    for batch_idx, (inputs, targets) in pbar:
        print(
            f"batch_idx: ====================== {batch_idx} ==========================="
        )
        image_, label = inputs, targets
        print(f"image_shape: {image_.shape}")
        image = (image_ * stds.view(1, 3, 1, 1)) + means.view(1, 3, 1, 1)
        image_np = image.squeeze().permute(1, 2, 0).numpy()
        pil_image = Image.fromarray((image_np * 255).astype("uint8"))

        if label == 0:
            pil_image.save(os.path.join(blurry_dir, "blurry_{}.png".format(batch_idx)))
        else:
            pil_image.save(os.path.join(clear_dir, "clear_{}.png".format(batch_idx)))


if __name__ == "__main__":
    main()
