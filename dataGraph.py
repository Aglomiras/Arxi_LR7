import math
import matplotlib.pyplot as plt


def function_Graph(Am, time, phs):
    x = Am * math.sin(phs * math.pi / 180 + 2 * math.pi * 50 * time)
    y = Am * math.cos(phs * math.pi / 180 + 2 * math.pi * 50 * time)
    return x, y


time_list = []
for i in range(500):
    time_list.append(i / 4000)

x_list = []  # Косинусоида
y_list = []  # Синусоида
for i in range(len(time_list)):
    # xy_list = function_Graph(5, time_list[i], 30)
    if i < 200:
        xy_list = function_Graph(5, time_list[i], 30)
    else:
        xy_list = function_Graph(5, 2*time_list[i], 30)
    x_list.append(xy_list[0])
    y_list.append(xy_list[1])

plt.grid(True, color="grey", linewidth="1.4", linestyle="-.")
plt.plot(time_list, y_list)
plt.show()
