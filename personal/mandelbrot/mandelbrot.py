from turtle import width
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

def complex_matrix(left, right, bottom, top, pixel_density=None, width=None):
    if width is None:
        width = int((right - left) * pixel_density)
    height = int(width / (right - left) * (top - bottom))
    
    
    re = np.linspace(left, right, width)
    im = np.linspace(bottom, top, height)
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

def get_boundaries(center, width, height, pos='center'):
    if pos == 'center':
        left, right = center[0] - width/2, center[0] + width/2
        bottom, top = center[1] - height/2, center[1] + height/2
    elif pos == 'top-left':
        left, right = center[0], center[0] + width
        bottom, top = center[1], center[1] + height
    return left, right, bottom, top
    

def plot_mandelbrot(left, right, bottom, top, pixel_density=None, width=None, iterations=20, save_path=None):
    c = complex_matrix(left, right, bottom, top, pixel_density=pixel_density, width=width)
    plt.imshow(iterations_til_escape(c, iterations), cmap="magma", extent=(left, right, bottom, top))
    
    plt.gca().set_aspect("equal")
    # plt.axis("off")
    if left * right < 0:
        plt.axvline()
    if top * bottom < 0:
        plt.axhline()
        
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    
    plt.show(block=True)    
    
def main():
    import os
    data_folder_path = os.path.join(os.path.realpath(__file__), os.pardir, "data")
    # plt.imshow(is_stable(c, 50), cmap="binary")
    # plot_mandelbrot(-2, 0.5, -1.5, 1.5, pixel_density=2**9, iterations=50)
    
    # c = complex_matrix(-0.4, -0.3, -0.61, -0.60, pixel_density=2**9)
    # print(c)
    # x0 = -0.34853774148008254
    # y0 = -0.6065922085831237
    # x1 = -0.34831493420245574
    # y1 = -0.606486596104741
    
    # plot_mandelbrot(x0, x1, y0, y1, width=2000, iterations=5000)
    
    save_to = os.path.join(data_folder_path, "mand 003.png")
    
    plot_mandelbrot(-2, 0.5, -1.5, 1.5, width=600, iterations=256, save_path=save_to)
       

if __name__ == "__main__":
    main()