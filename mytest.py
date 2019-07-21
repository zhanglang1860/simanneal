
import numpy as np
import matplotlib.pyplot as plt

t_list, e_list, step_list, accepts_list, improves_list = [], [], [], [], []
for i in range(0,10000):
    value=round(500.39393,2)

    step_list.append(i)
    t_list.append(value)

    e_list.append(value)
print(value)
dt = 0.01
fig, axs = plt.subplots(2, 1)
axs[0].plot(step_list, t_list, step_list, e_list)
axs[0].set_ylim(499, 501)
axs[0].set_xlabel('step_list')
axs[0].set_ylabel('T and E')
axs[0].grid(True)

cxy, f = axs[1].cohere(t_list, e_list, 256, 1. / dt)
axs[1].set_ylabel('coherence')

fig.tight_layout()
plt.show()
