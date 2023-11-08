"""
@brief: Sampler method for upsampling the minority class
@author: Hassna Irzan (rmaphir@gmail.com)
@date: 27 October 2023
"""
import numpy as np

def get_sampling_indices(dataset):
    """
    @brief: Get the indices of the samples to be used for training. It returns the indices of the samples by upsampling the minority class
    @param: dataset: dataset object
    @return: balanced_indices: list of indices to be used for training
    """
    
    # Get the indices per class
    labels_dict = dataset.labels_dict
    indices_class0 = [i for i, label in enumerate(labels_dict.values()) if label == 0]
    indices_class1 = [i for i, label in enumerate(labels_dict.values()) if label == 1]

    # Determine the number of samples in the target class and other classes
    num_samples_class0 = len(indices_class0)
    num_samples_class1 = len(indices_class1)

    # Determine the sampling ratio for the target class to make it balanced
    sampling_ratio = int(num_samples_class1 / num_samples_class0)

    # Create a list of indices to sample from
    balanced_indices = indices_class0 * int(sampling_ratio) + indices_class1

    # Shuffle the indices
    np.random.shuffle(balanced_indices)

    return balanced_indices
