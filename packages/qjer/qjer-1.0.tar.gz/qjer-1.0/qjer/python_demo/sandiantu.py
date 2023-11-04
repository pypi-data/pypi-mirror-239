#!/usr/bin/env python
# coding: utf-8

# 绘制简单的散点图

# In[1]:


import numpy as np  # 导入numpy模块
import matplotlib.pyplot as plt  # 导入matplotlib中的pyplot模块
x = np.random.randint(0,10,8)  # 随机生成8个[0,10)之间的整数
y = np.random.randint(0,10,8)  # 随机生成8个[0,10)之间的整数
plt.scatter(x, y)  # 绘制散点图
plt.show()  # 显示图表


# In[ ]:




