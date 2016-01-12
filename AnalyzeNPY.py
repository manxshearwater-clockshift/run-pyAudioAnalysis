import argparse
import os
import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("directory", help="set the directory to analyze",
                    type=str)
parser.add_argument("model", help="the knn model to use",
                    type=str)
parser.add_argument("--features", help="fragment features used",
                    type=str)
args = parser.parse_args()

files = os.listdir(args.directory)

def load_npy_files():
    all_arrays = []
    for npyfile in files:
        nparray = np.load(args.directory + npyfile)
        all_arrays.append(nparray)
    return all_arrays

def count():
    all_arrays = load_npy_files()
    counted_arrays = []
    for array in all_arrays:
        counted_arrays.append(np.bincount(array))
    return counted_arrays

def get_elements():
    all_arrays_counted = count()
    first_elements = []
    for array in all_arrays_counted:
        first_elements.append(array[0])
    return first_elements

def plot():
    elements_list = get_elements()
    x = range(0, len(elements_list))
    y = elements_list
    print(x)
    plt.plot(x, y)
    plt.show()

if __name__ == "__main__":
    plot()