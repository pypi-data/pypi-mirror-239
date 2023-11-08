#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@brief  Main script to kick off the training.
        Some of this code has been inspired by: https://github.com/kentaroy47/vision-transformers-cifar10
        and by https://github.com/luiscarlosgph/vitcifar10

@author Hassna Irzan (rmaphir@gmail.com)
@date   29 August 2023
"""

import argparse
import numpy as np
import torch
import torch.utils.data.sampler
import torch.utils.tensorboard
import tqdm
import os
import json
import time
import random
from mydataset import MultiDatasetClass
from sampler import get_sampling_indices


# My imports
import model_functions


def help(option):
    """
    @returns The string with the help information for each command line option.
    """
    help_msg = {
        "--json_datasets": "Path to the json files containing the paths to the datasets",
        "--lr": "Learning rate (required: True)",
        "--opt": "Optimizer (required: True)",
        "--nepochs": "Number of epochs (required: True)",
        "--bs": "Training batch size (required: True)",
        "--cpdir": "Path to the checkpoint directory (required: True)",
        "--logdir": "Path to the log directory (required: True)",
        "--cpint": "Checkpoint interval (required: True)",
        "--resume": "Path to the checkpoint file (required: False)",
        "--seed": "Random seed (required: False)",
        "--pretrained": "Initialise model with weights pretrained " + "on ImageNet",
    }
    return help_msg[option]


def parse_cmdline_params():
    """@returns The argparse args object."""
    args = argparse.ArgumentParser(
        description="PyTorch ViT for training/validation on CIFAR-10."
    )
    args.add_argument(
        "--json_datasets", required=True, type=str, help=help("--json_datasets")
    )
    args.add_argument("--lr", required=True, type=float, help=help("--lr"))
    args.add_argument("--opt", required=True, type=str, help=help("--opt"))
    args.add_argument("--nepochs", required=True, type=int, help=help("--nepochs"))
    args.add_argument("--bs", required=True, type=int, help=help("--bs"))
    args.add_argument("--cpdir", required=True, type=str, help=help("--cpdir"))
    args.add_argument("--logdir", required=True, type=str, help=help("--logdir"))
    args.add_argument("--cpint", required=True, type=int, help=help("--cpint"))
    args.add_argument(
        "--resume", required=False, type=str, default=None, help=help("--resume")
    )
    args.add_argument(
        "--seed", required=False, type=int, default=None, help=help("--seed")
    )
    args.add_argument(
        "--pretrained",
        required=False,
        type=bool,
        default=True,
        help=help("--pretrained"),
    )

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
    train_preproc_tf,
    valid_preproc_tf,
    data_dirs,
    labels_files,
    train_bs: int = 512,
    valid_bs: int = 100,
    num_workers: int = 8,
    device="cuda",
):
    train_dataset = MultiDatasetClass(
        data_dirs,
        labels_files,
        stage="train",
        transform=train_preproc_tf,
    )

    vald_dataset = MultiDatasetClass(
        data_dirs,
        labels_files,
        stage="validation",
        transform=valid_preproc_tf,
    )

    # Get the indices of the samples to be used for training
    train_balanced_indices = get_sampling_indices(train_dataset)
    vald_balanced_indices = get_sampling_indices(vald_dataset)

    # Create the sampler
    train_sampler = torch.utils.data.sampler.SubsetRandomSampler(train_balanced_indices)
    vald_sampler = torch.utils.data.sampler.SubsetRandomSampler(vald_balanced_indices)

    # Create dataloaders
    train_dl = torch.utils.data.DataLoader(
        train_dataset, batch_size=train_bs, sampler=train_sampler, num_workers=num_workers)

    valid_dl = torch.utils.data.DataLoader(
        vald_dataset, batch_size=valid_bs, sampler=vald_sampler, num_workers=num_workers)
    



    return train_dl, valid_dl


def build_optimizer(net, lr, opt: str = "adam"):
    """
    @brief Build the optimizer.

    @param[in]  net  Initialized PyTorch model.
    @param[in]  lr  Learning rate.
    @param[in]  opt  Optimizer to be used for training.

    @returns The optimizer.
    """

    if opt.lower() == "adam":
        optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    elif opt.lower() == "sgd":
        optimizer = torch.optim.SGD(net.parameters(), lr=lr)

    return optimizer


def resume(checkpoint_path, net, optimizer, scheduler, scaler):
    """
    @param[in]       checkpoint_path  Path to the checkpoint file (extension .pt).
    @param[in, out]  net              Initialized PyTorch model.
    @param[in, out]  optimizer        Initialized solver.
    @param[in, out]  scheduler        Initialized LR scheduler.
    @param[in, out]  scaler           Initialized gradient scaler.
    """
    print("[INFO] Resuming from checkpoint ...")

    # Check that the checkpoint directory exists
    if not os.path.isfile(checkpoint_path):
        raise FileNotFoundError(
            "[ERROR] You want to resume from the last checkpoint, "
            + 'but there is not directory called "checkpoint"'
        )

    # Load state
    state = torch.load(checkpoint_path)

    # Update model with saved weights
    net.load_state_dict(state["net"])

    # Update optimizer with saved params
    optimizer.load_state_dict(state["optimizer"])

    # Update scheduler with saved params
    scheduler.load_state_dict(state["scheduler"])

    # Update scaler with saved params
    scaler.load_state_dict(state["scaler"])

    print("[INFO] Resuming from checkpoint ...")

    return state["lowest_valid_loss"], state["epoch"] + 1


def train(
    net: torch.nn, train_dl, loss_func, optimizer, scheduler, scaler, device="cuda"
):
    """
    @brief Train the model for a single epoch.

    @param[in, out]  net       Model.
    @param[in]       train_dl  Dataloader for the trainig data.
    @param[in]       loss_func Pointer to the loss function.
    @param[in, out]  optimizer Optimizer to be used for training.
    @param[in]       scaler    Gradient scaler.
    """

    # Set network in train mode
    net.train()

    # Create progress bar
    pbar = tqdm.tqdm(enumerate(train_dl), total=len(train_dl))

    # Run forward-backward over all the samples
    train_loss = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in pbar:
        inputs, targets = inputs.to(device), targets.to(device)

        # Train with amp
        with torch.cuda.amp.autocast(enabled=True):
            outputs = net(inputs)
            loss = loss_func(outputs, targets)
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()

        train_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        # Display loss and accuracy on the progress bar
        display_loss = train_loss / (batch_idx + 1)
        display_acc = 100.0 * correct / total
        pbar.set_description(
            "Training loss: %.3f | Acc: %.3f%% (%d/%d) | LR: %.2E"
            % (display_loss, display_acc, correct, total, scheduler.get_last_lr()[0])
        )

    # Add step to the LR cosine scheduler
    # scheduler.step(epoch - 1)
    scheduler.step()

    return display_loss, display_acc


def main(args, train_dl=None, valid_dl=None):

    # Set device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Fix random seeds for reproducibility
    if args.seed is None:
        args.seed = random.SystemRandom().randrange(0, 2**32)
    torch.manual_seed(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(args.seed)

    # Prepare preprocessing layers
    (
        train_preproc_tf,
        valid_preproc_tf,
    ) = model_functions.build_preprocessing_transforms()

    # Read the json file with the paths to the datasets
    data_dirs, labels_files = readjson(
        datasets_json_file=args.json_datasets
    )

    # Get dataloaders for training and testing
    if train_dl is None and valid_dl is None:
        train_dl, valid_dl = load_dataset(
            train_preproc_tf=train_preproc_tf,
            valid_preproc_tf=valid_preproc_tf,
            data_dirs=data_dirs,
            labels_files=labels_files,
            train_bs=args.bs,
            valid_bs=100,
            device=device,
        )

    print(
        "[INFO] Number of training samples: {}".format(len(train_dl.dataset))
    )
    print("[INFO] Number of validation samples: {}".format(len(valid_dl.dataset)))

    # Build model
    net = model_functions.build_model(num_classes=2, pretrained=args.pretrained)

    # Enable multi-GPU support
    net = torch.nn.DataParallel(net)
    torch.backends.cudnn.benchmark = True
    
    # Use cross-entropy loss
    loss_func = torch.nn.CrossEntropyLoss()

    # Build optimizer
    optimizer = build_optimizer(net, args.lr, args.opt)

    # Build LR scheduler
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, args.nepochs)

    # Setup gradient scaler
    scaler = torch.cuda.amp.GradScaler(enabled=True)

    # Setup Tensorboard
    writer = model_functions.setup_tensorboard(args.logdir)

    # Resume from the last checkpoint if requested
    lowest_valid_loss = np.inf
    start_epoch = 0
    model_best = False
    if args.resume is not None:
        lowest_valid_loss, start_epoch = resume(
            args.resume, net, optimizer, scheduler, scaler
        )
        print("[INFO] Resuming from checkpoint:", start_epoch)

    # Create lists to store the losses and metrics
    train_loss_over_epochs = []
    train_acc_over_epochs = []
    valid_loss_over_epochs = []
    valid_acc_over_epochs = []

    # Training loop
    for epoch in range(start_epoch, args.nepochs):
        print("\n[INFO] Epoch: {}".format(epoch))
        start = time.time()

        # Run a training epoch
        train_loss, train_acc = train(
            net, train_dl, loss_func, optimizer, scheduler, scaler,
        )

        # Run testing
        valid_loss, valid_acc, _, _ = model_functions.valid(net, valid_dl, loss_func)

        # Update lowest validation loss
        if valid_loss < lowest_valid_loss:
            lowest_valid_loss = valid_loss
            model_best = True
        else:
            model_best = False

        # Update state
        state = {
            "net": net.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict(),
            "scaler": scaler.state_dict(),
            "lowest_valid_loss": lowest_valid_loss,
            "epoch": epoch,
        }

        # Save temporary checkpoint
        if epoch % args.cpint == 0:
            print("[INFO] Saving model for this epoch ...")
            if not os.path.isdir(args.cpdir):
                os.mkdir(args.cpdir)
            checkpoint_path = os.path.join(args.cpdir, "epoch_{}.pt".format(epoch))
            torch.save(state, checkpoint_path)
            print("[INFO] Saved.")

        # If it is the best model, let's save it too
        if model_best:
            print("[INFO] Saving best model ...")
            model_best_path = os.path.join(
                args.cpdir, "model_best_epoch_{}.pt".format(epoch)
            )
            torch.save(state, model_best_path)
            print("[INFO] Saved.")

        # Store training losses and metrics
        train_loss_over_epochs.append(train_loss)
        train_acc_over_epochs.append(train_acc)

        # Store validation losses and metrics
        valid_loss_over_epochs.append(valid_loss)
        valid_acc_over_epochs.append(valid_acc)

        # Log training losses and metrics in Tensorboard
        writer.add_scalar("Loss/train", train_loss, epoch)
        writer.add_scalar("Accuracy/train", train_acc, epoch)

        # Log validation losses and metrics in Tensorboard
        writer.add_scalar("Loss/valid", valid_loss, epoch)
        writer.add_scalar("Accuracy/valid", valid_acc, epoch)

        print("[INFO] Epoch: {} finished.".format(epoch))

    print("[INFO] Training finished.")


if __name__ == "__main__":
    # Parse command line parameters
    args = parse_cmdline_params()

    # Call main training function
    main(args)
