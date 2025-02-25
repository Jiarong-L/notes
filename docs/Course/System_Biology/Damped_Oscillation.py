import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, step

# 定义系统的自然频率和时间范围
omega_n = 5.0  # 自然频率
t = np.linspace(0, 5, 500)

# 定义不同阻尼比的系统
systems = {
    'Undamped (ζ=0)': lti([omega_n**2], [1, 0, omega_n**2]),
    'Underdamped (ζ=0.1)': lti([omega_n**2], [1, 2*0.1*omega_n, omega_n**2]),
    'Critically Damped (ζ=1)': lti([omega_n**2], [1, 2*1.0*omega_n, omega_n**2]),
    'Overdamped (ζ=2)': lti([omega_n**2], [1, 2*2.0*omega_n, omega_n**2])
}

color = {
    'Undamped (ζ=0)': 'gray',
    'Underdamped (ζ=0.1)': 'red',
    'Critically Damped (ζ=1)': 'blue',
    'Overdamped (ζ=2)': 'green'
}

linestyle = {
    'Undamped (ζ=0)': 'dashed',
    'Underdamped (ζ=0.1)': '-',
    'Critically Damped (ζ=1)': 'dashed',
    'Overdamped (ζ=2)': '-'
}

# 绘制每个系统的阶跃响应
plt.figure(figsize=(6, 3))
for label, system in systems.items():
    t, y = step(system, T=t)
    plt.plot(t, y, label=label,color = color[label],linestyle=linestyle[label])


plt.xlabel('Time (s)')
plt.ylabel('Response')
plt.grid(False)

num1 = 0
num2 = 1.01
num3 = 3
num4 = 0
plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4,ncol=2)

plt.show()
