import numpy as np
import time

from live_plotter import FastLivePlotterGridSeparateProcess

N_ITERS = 100
SIMULATED_COMPUTATION_TIME_S = 0.1
OPTIMAL_TIME_S = N_ITERS * SIMULATED_COMPUTATION_TIME_S

live_plotter_separate_process = FastLivePlotterGridSeparateProcess(
    plot_names=["sin", "cos"]
)
live_plotter_separate_process.start()
start_time_separate_process = time.time()
for i in range(N_ITERS):
    time.sleep(SIMULATED_COMPUTATION_TIME_S)
    live_plotter_separate_process.data_dict["sin"].append(np.sin(i))
    live_plotter_separate_process.data_dict["cos"].append(np.cos(i))
    live_plotter_separate_process.update()
time_taken_separate_process = time.time() - start_time_separate_process

print(f"Time taken separate process: {round(time_taken_separate_process, 1)} s")
print(f"OPTIMAL_TIME_S: {round(OPTIMAL_TIME_S, 1)} s")
