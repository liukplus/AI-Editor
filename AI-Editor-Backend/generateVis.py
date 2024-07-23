
import matplotlib.pyplot as plt
import numpy as np

# 提取数据
heights = {'小虎': 175, '小红': 166, '小东': 175 + 5}  # 小东比小虎高5cm
weights = {'小虎': 170, '小红': 100, '小东': 140}
jumps = {'小虎': 2, '小红': 1.5, '小东': 3}

# 归一化数据
min_height = min(heights.values())
max_height = max(heights.values())
min_weight = min(weights.values())
max_weight = max(weights.values())
min_jump = min(jumps.values())
max_jump = max(jumps.values())

normalized_heights = {k: (v - min_height) / (max_height - min_height) for k, v in heights.items()}
normalized_weights = {k: (v - min_weight) / (max_weight - min_weight) for k, v in weights.items()}
normalized_jumps = {k: (v - min_jump) / (max_jump - min_jump) for k, v in jumps.items()}

# 绘图
fig, ax = plt.subplots()

# 身高柱状图
ax.bar(heights.keys(), list(normalized_heights.values()), label='Height (normalized)', color='b')

# 体重柱状图
ax.bar(weights.keys(), list(normalized_weights.values()), bottom=list(normalized_heights.values()), label='Weight (normalized)', color='g')

# 跳远柱状图（堆叠在身高和体重之上）
ax.bar(jumps.keys(), list(normalized_jumps.values()), bottom=[normalized_heights[k] + normalized_weights[k] for k in jumps.keys()], label='Jump Distance (normalized)', color='r')

# 设置图例
ax.legend()

# 设置坐标轴标签
ax.set_xlabel('Person')
ax.set_ylabel('Normalized Value')

# 保存图片
plt.savefig('D:\\backend\\score-management-system-back_end\\static\\1\\imgs\\74.png', bbox_inches='tight')

# 注意：我们没有调用         ，因为您要求不要写show语句
