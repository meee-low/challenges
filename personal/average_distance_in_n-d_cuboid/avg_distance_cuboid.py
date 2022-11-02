import numpy as np
import matplotlib.pyplot as plt
import csv
from tqdm import tqdm
import os

REPETITIONS = 10_000_000
MAX_DIMENSIONS = 10000
GRANULARITY = 100 # Controls how many data points it tries to get. The actual number of data points will be slightly lower in almost all cases.
SEED = 30004

output_folder_path = os.path.join(os.path.realpath(__file__), os.pardir, "output")

rng = np.random.default_rng(SEED)

def simulate(dimension, repetitions=REPETITIONS):
    A = rng.random((dimension, repetitions))
    B = rng.random((dimension, repetitions))
    return np.linalg.norm(A - B, axis=0).mean()

def simulate_many(max_dim=MAX_DIMENSIONS, granularity=GRANULARITY):
    rr = np.unique(np.geomspace(1, max_dim, num=granularity).astype('int64'))
    results = []
    for dim in tqdm(rr):
        reps = REPETITIONS//dim
        results.append(simulate(dim, repetitions=reps))
    results = np.array(results)
    return rr, results

def plot_results(xx, yy, folder_path, file_name, xlabel="", ylabel="", save_figure=True):
    plt.plot(xx, yy, '-o')
    ax = plt.gca()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    file_name = f"seed_{SEED}_dim_{MAX_DIMENSIONS}_reps_{REPETITIONS}_gran_{GRANULARITY}.png"
    file_path = os.path.join(folder_path, file_name)
    plt.savefig(file_path)
    
    plt.show(block=True)
    
    
def save_results_to_csv(xx, yy, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for x, y in zip(xx, yy):
            writer.writerow([x, y])

def main():
    xx, yy = simulate_many(MAX_DIMENSIONS)
    figurefilename = f"seed_{SEED}_dim_{MAX_DIMENSIONS}_reps_{REPETITIONS}_gran_{GRANULARITY}.csv"
    plot_results(xx, yy, output_folder_path, figurefilename, "Dimensions", "Average distance")
    csvfilename = f"seed_{SEED}_dim_{MAX_DIMENSIONS}_reps_{REPETITIONS}_gran_{GRANULARITY}.csv"
    save_results_to_csv(xx, yy, output_folder_path, csvfilename)
    
if __name__ == "__main__":
    main()