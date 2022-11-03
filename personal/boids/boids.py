import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.animation import PillowWriter
from typing import Optional, Union, Literal

class Boid:
    top_speed = 0.2
    r1_weight = 1 # Separation
    r2_weight = 0.3 # Alignment
    r3_weight = 1.2 # Cohesion
    r4_weight = 2 # Avoid other colors
    r5_weight = 0.05 # Individualism
    flock_threshhold = 1.5
    too_close_threshhold = 0.5
    color_options = ["blue", "red"]
    
    def __init__(self, position:np.array, heading:np.array, color=str):
        self.position:np.array = position 
        self.heading:np.array = heading
        self.next_heading:Optional[np.array] = None
        self.color=color
        
    @property
    def weights(self) -> np.array:
        return np.array([self.r1_weight,
                         self.r2_weight,
                         self.r3_weight,
                         self.r4_weight,
                         self.r5_weight,
                         ])
        
    @classmethod
    def random(cls, boundaries:np.array, rng=np.random) -> 'Boid':
        position:np.array = rng.random(size=2) * boundaries
        angle = rng.uniform(0, 2*math.pi)
        color = rng.choice(cls.color_options)
        heading:np.array = np.array([math.cos(angle), math.sin(angle)])
        
        return cls(position, heading, color)
    
    def distance(self, other:'Boid') -> float:
        return np.linalg.norm(self.position - other.position)
    
    def can_see(self, other='Boid') -> bool:
        return self.distance(other) <= self.flock_threshhold and self != other
    
    def calculate_next_heading(self, flock:list['Boid'], rng=np.random) -> np.array:
        if len(flock) == 0:
            next_heading = self.heading
            self.prepare_next_heading(next_heading)
            return next_heading
        
        flock_relative_positions = np.array([b.position for b in flock]) - self.position
        flock_headings = np.array([b.heading for b in flock])
        flock_color = [b.color for b in flock]
        same_color_mask = np.array(flock_color) == self.color
        
        # Rule 1: Separation (try to stay apart):
        too_close_mask = np.linalg.norm(flock_relative_positions, axis=1) <= self.too_close_threshhold
        r1 = -1 * (flock_relative_positions[too_close_mask].sum(axis=0))
        # Rule 2: Alignment (try to head in the same direction as the flock):
        if same_color_mask.sum() == 0:
            r2 = np.zeros(2)
        else:
            r2 = flock_headings[same_color_mask].mean(axis=0)
        # Rule 3: Cohesion (try to head towards the centre of mass of the flock):
        if same_color_mask.sum() == 0:
            r3 = np.zeros(2)
        else:
            r3 = flock_relative_positions[same_color_mask].mean(axis=0)
        # Rule 4: Avoid other colors (try to stay very far from other colors):
        too_close_and_other_color = np.logical_and(too_close_mask, np.logical_not(same_color_mask))
        if too_close_and_other_color.sum() == 0:
            r4 = np.zeros(2)
        else:
            r4 = -1 * (flock_relative_positions[too_close_and_other_color].sum(axis=0))
        # Rule 5: Individualism (random variance):
        r5 = rng.normal(size=2)
        
        influence = (np.array([r1, r2, r3, r4, r5]).T * self.weights).sum(axis=1)
        # influence /= np.linalg.norm(influence)
        # influence *= 100
                
        next_heading = self.heading + influence
        # next_heading /= np.linalg.norm(next_heading)
        
        self.prepare_next_heading(next_heading)
        return next_heading
        
    def prepare_next_heading(self, next_heading:np.array) -> None:
        if self.next_heading is not None:
            print("You probably don't want to update the heading. Updating anyway.")
        self.next_heading = next_heading
        
    def update_heading(self) -> None:
        if self.next_heading is None:
            raise ValueError("Can't update headings if there is no new heading loaded.")
        self.heading, self.next_heading = self.next_heading, None
        
    def advance(self, wrap) -> None:
        delta = self.heading
        size_delta = np.linalg.norm(delta)
        if size_delta > self.top_speed:
            delta = delta / size_delta * self.top_speed
        new_position = self.position + delta
        
        # Wrap
        while new_position[0] > wrap[0]: # Right edge
            new_position[0] -= wrap[0]
        while new_position[0] < 0: # Left edge
            new_position[0] += wrap[0]
        while new_position[1] > wrap[1]: # Top edge
            new_position[1] -= wrap[1]
        while new_position[1] < 0: # Bottom edge
            new_position[1] += wrap[1]    
                
        self.position = new_position
        
    def __hash__(self):
        return hash(tuple(self.position, self.heading, self.color))
            
        
class World:
    def __init__(self, boundaries, boids=None, rng=np.random):
        self.boundaries = boundaries
        self.boids = boids 
        self.rng = rng
        
    def create_boids(self, number_of_boids:int):
        self.boids = [Boid.random(self.boundaries, self.rng) for _ in range(number_of_boids)]
        
    def advance(self):
        # Prepare
        for b1 in self.boids:
            flock = [b2 for b2 in self.boids if b1.can_see(b2)]
            b1.calculate_next_heading(flock, self.rng)
        
        # Execute
        for b1 in self.boids:
            b1.update_heading()
            b1.advance(wrap=self.boundaries)
        
    def draw(self):
        xx, yy, c = [], [], []
        for b in self.boids:
            xx.append(b.position[0])
            yy.append(b.position[1])
            c.append(b.color)
        
        plt.xlim([0, self.boundaries[0]])
        plt.ylim([0, self.boundaries[1]])
        plt.tight_layout()
        plt.axis("off")
        plt.gca().set_aspect("equal")
        
        plt.scatter(xx, yy, c=c, s=2)
        return plt.gcf()
            
    def animate(self, iterations:Union[Literal[False], int]):
        turn = 0
        while not iterations or turn <= iterations:
            plt.clf()
            self.draw()
            plt.show(block=True)
            self.advance()
            turn += 1
            
    def gen_frames(self):
        while True:
            yield self.draw()
            self.advance()
        
        
def main():
    SEED = np.random.randint(1E6, 1E7)
    rng = np.random.default_rng()
    print(f"Seed: {SEED}")  
    
    world = World((10, 10), rng)
    world.create_boids(130)
    

    
    import os
    import pathlib
    from tqdm import tqdm, trange
    
    output_folder = os.path.join(os.path.realpath(__file__), os.pardir, "output")
    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True) # create the folder if it doesn't exist
    filename = os.path.join(output_folder, f"boids demo.gif")
        
    gen = world.gen_frames()
    
    pw = PillowWriter(60)
    pw.setup(next(gen), filename, dpi=None)
    for _ in trange(200):
        plt.clf()
        next(gen)
        pw.grab_frame()
        plt.draw()
        plt.pause(1/60)
        
    pw.finish()
    
    
    

if __name__ == "__main__":
    main()