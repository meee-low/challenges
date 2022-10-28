import numpy as np
import matplotlib.pyplot as plt
import numba

SEED = np.random.randint(10**6, 10**7-1)
rng  = np.random.default_rng(SEED)

def integrate_function_using_rule(function, start_x, end_x, num_points, plot=True):
    f = np.vectorize(function)
    xx = np.arange(start_x, end_x, (end_x-start_x)/num_points)
    f_x = f(xx)
    min_y = min(f_x.min(), 0)
    max_y = max(f_x.max(), 0)
    
    
    def rule(x, y):
        if 0 < y < function(x):
            # Positive under the curve
            return 1
        if 0 > y > function(x):
            # Negative under the curve
            return -1
        return 0
    
    area_under_curve = integrate_rule(rule, start_x, end_x, min_y, max_y, num_points, plot=plot)
    
    return area_under_curve

def integrate(function, start_x, end_x, num_points, plot=True):
    f = numba.vectorize([numba.float64(numba.float64)], target='parallel')(function)
    xx = np.linspace(start_x, end_x, num_points)
    f_x = f(xx)
    min_y = min(f_x.min(), 0)
    max_y = max(f_x.max(), 0)
    yy = rng.uniform(min_y, max_y, num_points)
    
    total_area = (max_y - min_y) * (end_x - start_x)
    
    pos_under_curve = np.logical_and(0 < yy, yy < f_x)
    neg_above_curve = np.logical_and(0 > yy, yy > f_x)
    
    if plot:
        sample_filter = rng.choice(num_points, min(num_points, 100_000)) # don't plot too many points
        values = np.zeros(sample_filter.shape[0])
        values[pos_under_curve[sample_filter]] = 1
        values[neg_above_curve[sample_filter]] = -1
        
        plt.scatter(xx[sample_filter], yy[sample_filter], c=values, s=1)
        plt.plot(xx, f_x, color="orange")
        
        plt.axhline()
        plt.axvline()
        
        plt.show(block=True)
    
    return (pos_under_curve.sum() - neg_above_curve.sum()) * total_area / num_points

    
def integrate_rule(rule, min_x=None, max_x=None, min_y=None, max_y=None, num_points=None, xxyy=None, plot=True):
    """
    A rule takes a 2-d point and outputs a boolean or a weight.
    """
    if xxyy is not None:
        xx = xxyy[0]
        yy = xxyy[1]
    else:
        xx = rng.uniform(min_x, max_x, num_points)
        yy = rng.uniform(min_y, max_y, num_points)
    
    rule = numba.vectorize([numba.float64(numba.float64, numba.float64)], target='parallel')(rule)
    points_ruled = rule(xx, yy)
    total_area = (max_y - min_y) * (max_x - min_x)
    
    if plot:
        points_sample = rng.choice(np.array((xx, yy, points_ruled)).T,
                                   size=min(100000, num_points))\
                            .T
        plt.scatter(points_sample[0], points_sample[1], c=points_sample[2], s=1)
        plt.axhline()
        plt.axvline()
        plt.show(block=True)
    
    return points_ruled.sum() / num_points * total_area

def main():
    print(f"SEED: {SEED}")
    N = 100_000_000
    plot = False
    
    
    f = lambda x: x * x - 1
    print(integrate(f, start_x=0, end_x=2, num_points=N, plot=plot))
    
    f = lambda x: x
    print(integrate(f, start_x=0, end_x=2, num_points=N, plot=plot))
    
    circle = lambda x, y: x ** 2 + y ** 2 < 1
    print(integrate_rule(circle, -1, 1, -1, 1, N, plot=plot))
    
    import math
    non_integratable_f = lambda x: math.sin(x ** 2)
    print(integrate(non_integratable_f, start_x=0, end_x=math.pi * 4, num_points=N, plot=plot))
    
if __name__ == "__main__":
    main()  
    