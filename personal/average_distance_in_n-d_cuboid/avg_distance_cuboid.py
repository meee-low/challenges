import numpy as np
import matplotlib.pyplot as plt
import os
import csv


REPETITIONS = 1_000_000
MAX_DIMENSIONS = 1000
GRANULARITY = 50 # Controls how many data points it tries to get. The actual number of data points will be slightly lower in almost all cases.
SEED = 30004

data_folder_path = os.path.join(os.path.realpath(__file__), os.pardir, "data")

rng = np.random.default_rng(SEED)

def simulate(dimension, repetitions=REPETITIONS):
    A = rng.random((dimension, repetitions))
    B = rng.random((dimension, repetitions))
    return np.linalg.norm(A - B, axis=0).mean()

def simulate_many(max_dim, granularity=GRANULARITY):
    rr = np.unique(np.geomspace(1, 1000, num=GRANULARITY).astype('int64'))
    results = []
    for dim in rr:
        reps = REPETITIONS//dim
        results.append(simulate(dim, repetitions=reps))
    results = np.array(results)
    return rr, results

def plot_results(xx, yy):
    plt.plot(xx, yy, '-o')
    ax = plt.gca()
    ax.set_xlabel("Dimensions")
    ax.set_ylabel("Average distance")
    
    file_name = f"seed_{SEED}_dim_{MAX_DIMENSIONS}_reps_{REPETITIONS}_gran_{GRANULARITY}.png"
    file_path = os.path.join(data_folder_path, file_name)
    plt.savefig(file_path)
    
    plt.show(block=True)
    
    
def save_results_to_csv(xx, yy):
    file_name = f"seed_{SEED}_dim_{MAX_DIMENSIONS}_reps_{REPETITIONS}_gran_{GRANULARITY}.csv"
    file_path = os.path.join(data_folder_path, file_name)
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for x, y in zip(xx, yy):
            writer.writerow([x, y])

def main():
    xx, yy = simulate_many(MAX_DIMENSIONS)
    plot_results(xx, yy)
    save_results_to_csv(xx, yy)    
    
if __name__ == "__main__":
    main()