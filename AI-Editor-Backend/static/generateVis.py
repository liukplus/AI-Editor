
import matplotlib.pyplot as plt
import numpy as np

# 提取并定义数据
data = [
    {'name': '小虎', 'Height': 175, 'Weight': 170, 'LongJump': 2.0},
    {'name': '小红', 'Height': 166, 'Weight': 100, 'LongJump': 1.5},
    {'name': '小东', 'Height': 175 + 5, 'Weight': 140, 'LongJump': 3.0},
]

# 归一化处理
def normalize(data, field):
    min_val = min(item[field] for item in data)
    max_val = max(item[field] for item in data)
    normalized = [(item[field] - min_val) / (max_val - min_val) for item in data]
    return normalized

normalized_heights = normalize(data, 'Height')
normalized_weights = normalize(data, 'Weight')
normalized_long_jumps = normalize(data, 'LongJump')

# 准备绘图数据
x = np.arange(len(data))
heights_bar = plt.bar(x, normalized_heights, label='Height', color='blue')
weights_bar = plt.bar(x, normalized_weights, bottom=normalized_heights, label='Weight', color='orange')
long_jumps_bar = plt.bar(x, normalized_long_jumps, bottom=np.array(normalized_heights) + np.array(normalized_weights), label='LongJump', color='green')

# 设置图例和图标题
plt.legend()
plt.xlabel('Person')
plt.ylabel('Normalized Score')
plt.xticks(x, [item['name'] for item in data])

# 保存图片到指定路径
plt.savefig('D:\\backend\\score-management-system-back_end\\static\\1\\imgs\\108.png', bbox_inches='tight')

# 不需要调用         ，因为我们直接保存了图片
