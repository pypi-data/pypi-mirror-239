import numpy as np
import time

from live_plotter import FastLivePlotterGrid

N_ITERS = 100
SIMULATED_COMPUTATION_TIME_S = 0.1
OPTIMAL_TIME_S = N_ITERS * SIMULATED_COMPUTATION_TIME_S

# Slower when plotting is on same process
live_plotter = FastLivePlotterGrid.from_desired_n_plots(
    title=["sin", "cos"], desired_n_plots=2
)
x_data = []
start_time_same_process = time.time()
for i in range(N_ITERS):
    x_data.append(i)
    time.sleep(SIMULATED_COMPUTATION_TIME_S)
    live_plotter.plot_grid(
        y_data_list=[np.sin(x_data), np.cos(x_data)],
    )
time_taken_same_process = time.time() - start_time_same_process

print(f"Time taken same process: {round(time_taken_same_process, 1)} s")
print(f"OPTIMAL_TIME_S: {round(OPTIMAL_TIME_S, 1)} s")

