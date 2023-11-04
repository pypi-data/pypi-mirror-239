#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 绘制折线图表，指定x轴和y轴数据
# 以季度销售额为例，1-3月份销售额为257,4-6月份销售额为301,7-9月份销售额为428,10-12月份销售额为475

# 导入matplotlib中的pyplot模块
import matplotlib.pyplot as plt
# 指定x轴和y轴数据
# x轴对应月份
x=['1-3','4-6','7-9','10-12']
# y轴对应销售额
y=[257,301,428,475]
plt.plot(x,y)
# 显示图表
plt.show()


# ![image.png](attachment:image.png)
