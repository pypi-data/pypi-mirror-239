#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@brief  Module containing functions that are useful for training and testing the ViT model. 
This has been adapted from the original code of the ViT model for CIFAR-10 classification (https://github.com/luiscarlosgph/vitcifar10)

"""

import torch
import torch.utils.tensorboard
import torchvision
import timm
import tqdm

# My imports
import randomaug as raaug


def build_model(num_classes: int, pretrained: bool = True):
    """
    @brief Create Vision Transformer (ViT) model pre-trained on ImageNet-21k
           (14 million images, 21,843 classes) at resolution 224x224
           fine-tuned on ImageNet 2012 (1 million images, 1,000 classes)
           at resolution 384x384.

    @param[in]  nclasses    Number of classes, CIFAR-10 has obviously
                            10 classes.
    @param[in]  pretrained  Initialise the model with the pretrained weights
                            of ImageNet-21k and ImageNet 2012.
    """
    net = timm.create_model("vit_tiny_patch16_384", pretrained=pretrained)
    net.head = torch.nn.Linear(net.head.in_features, num_classes)
    net.cuda()

    return net


def build_preprocessing_transforms(
    size: int = 384, randaug_n: int = 2, randaug_m: int = 14
):
    """
    @brief Preprocessing and data augmentation.

    @param[in]  size  Target size of the images to be resized prior
                      processing by the network.

    @returns a tuple of two transforms, one for training and another one for testing.
    """
    # Preprocessing for training
    gaussian_blur = torchvision.transforms.GaussianBlur(
        kernel_size=(5, 5), sigma=(0.1, 5.0)
    )
    # random_crop = torchvision.transforms.RandomCrop(32, padding=4),
    train_preproc_tf = torchvision.transforms.Compose(
        [
            torchvision.transforms.RandomApply([gaussian_blur], p=0.5),
            torchvision.transforms.Resize((size, size)),
            torchvision.transforms.RandomHorizontalFlip(p=0.5),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(
                mean=(0.3543, 0.2360, 0.2374), std=(0.2576, 0.2160, 0.2180)
            ),
        ]
    )

    # Data augmentation
    # train_preproc_tf.transforms.insert(0, raaug.RandAugment(randaug_n, randaug_m))

    # Preprocessing for testing
    valid_preproc_tf = torchvision.transforms.Compose(
        [
            torchvision.transforms.Resize((size, size)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(
                mean=(0.3543, 0.2360, 0.2374), std=(0.2576, 0.2160, 0.2180)
            ),
        ]
    )

    return train_preproc_tf, valid_preproc_tf


def setup_tensorboard(log_dir) -> torch.utils.tensorboard.SummaryWriter:
    """
    @param[in]  log_dir  Path to the Tensorboard log directory.
    @returns the Tensorboard writer.
    """
    writer = torch.utils.tensorboard.SummaryWriter(log_dir=log_dir)
    return writer


def valid(net: torch.nn, valid_dl, loss_func, device="cuda"):
    """
    @param[in, out]  net        PyTorch model.
    @param[in]       valid_dl    PyTorch dataloader for the testing data.
    @param[in]       loss_func  Pointer to the loss function.
    """
    valid_loss = 0
    correct = 0
    total = 0
    y_true = []
    y_pred = []

    net.eval()
    with torch.no_grad():
        # Create progress bar
        pbar = tqdm.tqdm(enumerate(valid_dl), total=len(valid_dl))

        # Loop over testing data points
        for batch_idx, (inputs, targets) in pbar:
            # Perform inference
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = net(inputs)

            # Store top class prediction and ground truth label
            y_t = targets.tolist()
            t_p = torch.argmax(outputs, axis=1).tolist()

            y_true.extend(y_t)
            y_pred.extend(t_p)

            # Compute losses and metrics
            loss = loss_func(outputs, targets)
            valid_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

            # Display loss and top-1 accuracy on the progress bar
            display_loss = valid_loss / (batch_idx + 1)
            display_acc = 100.0 * correct / total
            pbar.set_description(
                "Validation loss: %.3f | Acc: %.3f%% (%d/%d)"
                % (display_loss, display_acc, correct, total)
            )

    return display_loss, display_acc, y_true, y_pred


if __name__ == "__main__":
    raise RuntimeError(
        "[ERROR] The module vitcifar10 is not supposed to be run as an executable."
    )
