
#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Any, Callable, Union
from matplotlib.image import AxesImage #only for typing



def matrix_neighbors(board:np.array) -> np.array:
    # Pad and slice.
    padded = np.pad(board, (1,1))
    
    yield padded[0:-2 , 0:-2] # top-left
    yield padded[0:-2, 1:-1] # top
    yield padded[0:-2, 2:] # top-right
    yield padded[1:-1, 0:-2] # left
    yield padded[1:-1, 2:] # right
    yield padded[2:, 0:-2] # bottom-left
    yield padded[2:, 1:-1] # bottom
    yield padded[2:, 2:] # bottom-right
    
    # # Alternative:
    # x_lim, y_lim = board.shape
    # padded = np.pad(board, (1,1))
    # for x in range(2, end=True):
    #     for y in range(2, end=True):
    #         if x == 1 and y == 1:
    #             # This is the "center" cell. We want the neighbors.
    #             continue
    #         yield padded[y:y_lim-y, x:x_lim-x]
    

def next_life_generation(board:np.array, max_iterations=int):
    for _ in range(max_iterations-1):
        yield board
        neighbor_matrix = np.zeros(board.shape, dtype=np.uint8)
        for neighbor in matrix_neighbors(board):
            neighbor_matrix += neighbor
        survived = np.logical_and(board, np.logical_or(neighbor_matrix==2, neighbor_matrix==3)) # alive and 2 or 3 neighbors
        born = np.logical_and(np.logical_not(board), neighbor_matrix==3) # dead and 3 live neighbors
        board = np.logical_or(survived, born)
        # if board.sum() == 0:
        #     # all cells are dead
        #     break

def show_board(board:np.array):
    plt.imshow(board, cmap="Greys")
    
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.tight_layout()
    
    plt.show(block=True)
    
def update_board(board:np.array) -> AxesImage: 
    cur_title = plt.gca().get_title()
    plt.clf()
    ax = plt.gca()
    
    if cur_title == "":
        ax.set_title("Generation: 1")
    else:
        cur_gen = int(cur_title.split(":")[1]) 
        ax.set_title(f"Generation: {cur_gen+1}")
    ax.set_aspect("equal")
    plt.axis("off")
    plt.tight_layout()
    plot = plt.imshow(board, cmap="Greys")
    return plot


def pyplot_animation_of_life(initial_board:np.array, iterations:int, delay:Union[float, int], plotting_function:Callable[[np.array], AxesImage]) -> animation.FuncAnimation:
    fig = plt.gcf()
    anim = animation.FuncAnimation(
        fig,
        plotting_function,
        interval=delay*1000,
        repeat_delay=5*1000,
        frames=next_life_generation(initial_board, iterations)
        )
    
    return anim
    

def main():
    import os
    
    output_folder = os.path.join(os.path.realpath(__file__), os.pardir, "output")
    
    SEED = np.random.randint(1E6, 1E7)
    rng = np.random.default_rng(SEED)
    print(SEED)
    
    SIZE = (150, 150)
    CUTOFF = .5
    GENERATIONS = 200
    
    board = rng.random(SIZE) > CUTOFF
    anim = pyplot_animation_of_life(board, GENERATIONS, 0.0001, update_board)
    
    filepath = os.path.join(output_folder, f"life (seed={SEED}, size={SIZE}, cutoff={CUTOFF}, generations={GENERATIONS}).gif")
    anim.save(filepath, writer="pillow")
    # plt.show()

if __name__ == "__main__":
    main()