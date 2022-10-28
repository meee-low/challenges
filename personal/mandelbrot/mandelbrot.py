import numba
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange


# Some from: https://realpython.com/mandelbrot-set-python/
# Mine is the visualization


np.warnings.filterwarnings("ignore")

def sequence(c, z=0):
    while True:
        yield z
        z = z ** 2 + c

def mandelbrot(candidate):
    return sequence(z=0, c=candidate)

def julia(candidate, parameter):
    return sequence(z=candidate, c=parameter)

def complex_matrix(xmin, xmax, ymin, ymax, pixel_density):
    re = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density))
    im = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density))
    return re[np.newaxis, :] + im[:, np.newaxis] * 1j

def is_stable(c, num_iterations=20):
    z = 0
    for _ in trange(num_iterations):
        z = z ** 2 + c
    return abs(z) <= 2

def get_members(c, num_iterations=20):
    mask = is_stable(c, num_iterations)
    return c[mask]

def iterations_til_escape(c:np.array, max_iterations=20):
    results = np.zeros(c.shape) - 1
    z = 0
    for i in trange(max_iterations):
        z = z ** 2 + c
        results[np.logical_and(results == -1, abs(z) >= 2)] = i
    results[results == -1] = max_iterations * 1.5
    return results

def main():
    c = complex_matrix(-2, 0.5, -1.5, 1.5, pixel_density=2**12)
    
    # plt.imshow(is_stable(c), cmap="binary")
    plt.imshow(iterations_til_escape(c, 100), cmap="magma")
    
    
    
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show(block=True)    
    

if __name__ == "__main__":
    main()