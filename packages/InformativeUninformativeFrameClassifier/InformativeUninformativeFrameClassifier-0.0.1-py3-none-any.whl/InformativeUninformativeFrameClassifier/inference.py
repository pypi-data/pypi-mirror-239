#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@brief  Test a model trained on Vit with Cholec80 and HeiCo datasets.
This has been adapted from the original code of the ViT model for CIFAR-10 classification (https://github.com/luiscarlosgph/vitcifar10)
"""

import argparse
import numpy as np
import torch
import torchvision
import sklearn
import sklearn.metrics
import os
import PIL
import shutil
from mydatasets import DatasetClass

# My imports
import src.model_functions as model_functions
from glob import glob


def help(short_option):
    """
    @returns The string with the help information for each command line option.
    """
    help_msg = {
        "--image": "Path to the image (required: True)",
        "--model": "Path to the .pt model file (required: True)",
        "--input_dir": "Path to the input directory (required: True)",
        "--output_dir": "Path to the output directory (required: True)",
    }
    return help_msg[short_option]


def parse_cmdline_params():
    """@returns The argparse args object."""
    args = argparse.ArgumentParser(
        description="PyTorch ViT for training/validation on CholecT50."
    )
    args.add_argument("--input_dir", required=True, type=str, help=help("--input_dir"))
    args.add_argument(
        "--output_dir", required=True, type=str, help=help("--output_dir")
    )
    args.add_argument("--model", required=True, type=str, help=help("--model"))

    return args.parse_args()


def test_preproc_tf(x):
    """
    @brief Preprocessing transform for test images.
    @param x Input image.
    @returns The preprocessed image.
    """
    return torchvision.transforms.Compose(
        [
            torchvision.transforms.Resize((384, 384)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(
                mean=(0.3296, 0.2224, 0.2161),  # RGB mean
                std=(0.2272, 0.1897, 0.1846),  # RGB std
            ),
        ]
    )(x)


def main():
    # Parse command line parameters
    args = parse_cmdline_params()

    # input ROOT directory
    data_dir = args.input_dir

    # output ROOT directory
    output_root = args.output_dir

    output_blurry_dir = os.path.join(output_root, "blurry")
    output_clear_dir = os.path.join(output_root, "clear")

    if not os.path.exists(output_blurry_dir):
        os.makedirs(output_blurry_dir)

    if not os.path.exists(output_clear_dir):
        os.makedirs(output_clear_dir)

    CholecT50_classes = ("bluryy", "clear")  # CholecT50 classes
    # Prepare preprocessing layers
    # _, test_preproc_tf = vitcifar10.build_preprocessing_transforms(size=(384,384))

    # Build model
    net = model_functions.build_model()

    # Enable multi-GPU support
    net = torch.nn.DataParallel(net)
    torch.backends.cudnn.benchmark = True
    # Load weights from file
    state = torch.load(args.model)
    net.load_state_dict(state["net"])

    # Load the image
    images_files = glob(os.path.join(data_dir, "*", "video*.png"))

    print("Found {} images for testing".format(len(images_files)))

    for image_file in images_files:
        # Get the filename of the image
        image_filename = os.path.basename(image_file)

        # Load the image
        im_rgb = PIL.Image.open(image_file)

        if len(im_rgb.getbands()) != 3:
            raise ValueError("[ERROR] The input image must be a colour image.")

        # Preprocess image
        im_tensor = test_preproc_tf(im_rgb)
        im_tensor.to("cuda")

        # Run inference
        output = torch.argmax(net(torch.unsqueeze(im_tensor, 0))).item()

        # Store images in the corresponding folder

        if output == 0:
            output_filename = os.path.join(output_blurry_dir, image_filename)
        else:
            output_filename = os.path.join(output_clear_dir, image_filename)

        shutil.copyfile(image_file, output_filename)

    print("==================== Done! =====================")


if __name__ == "__main__":
    main()
