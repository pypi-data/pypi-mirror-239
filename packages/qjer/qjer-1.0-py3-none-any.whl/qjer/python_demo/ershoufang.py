#!/usr/bin/env python
# coding: utf-8

# 现有二手房信息，要求读取数据，对数据进行清晰，并计算所有区域的二手房均价，并绘图展示。

# In[1]:


import pandas as pd  # 导入pandas模块
pd.set_option('display.unicode.east_asian_width', True) # 解决数据输出时列名不对齐的问题
# 导入csv数据文件
house = pd.read_csv('house.csv')
house.head(5) # 输出前5条数据


# In[2]:


house.drop(columns='序号', inplace=True)  # 将索引列删除
house.dropna(axis=0, how='any', inplace=True)  # 删除house数据中的所有空值
house['单价'] = house['单价'].map(lambda d: d.replace('元/平米', ''))  # 将单价“元/平米”去掉
house['单价'] = house['单价'].astype(float)  # 将房子单价转换为浮点类型
house['总价'] = house['总价'].map(lambda z: z.replace('万', ''))  # 将总价“万”去掉
house['总价'] = house['总价'].astype(float)  # 将房子总价转换为浮点类型
house['建筑面积'] = house['建筑面积'].map(lambda p: p.replace('平米', ''))  # 将建筑面价“平米”去掉
house['建筑面积'] = house['建筑面积'].astype(float)  # 将建筑面积转换为浮点类型
print(house.head())  # 输出前5条数据
house.to_csv('./house_completed.csv')  #数据导出为csv文件


# In[6]:


import pandas as pd  # 导入pandas模块
import matplotlib.pyplot as plt  # 导入matplotlib中的pyplot模块

# 解决数据输出时列名不对齐的问题
pd.set_option('display.unicode.east_asian_width', True)

# 获取各区二手房均价分析
def get_average_price():
    group = house.groupby('区域')  # 将房子区域分组
    average_price_group = group['单价'].mean()  # 计算每个区域的均价
    print(average_price_group)  # 输出各区二手房的均价信息
    region = average_price_group.index  # 区域
    average_price = average_price_group.values.astype(int)  # 区域对应的均价，转换成int类型
    return region, average_price  # 返回区域与对应的均价


# 调用函数
get_average_price()


# In[5]:


import pandas as pd  # 导入pandas模块
import matplotlib.pyplot as plt  # 导入matplotlib中的pyplot模块

# 解决数据输出时列名不对齐的问题
pd.set_option('display.unicode.east_asian_width', True)
# 手动添加黑体字体，解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 导入csv数据文件
# house = pd.read_csv('/home/qingjiao/Document/data/17_2/house_completed.csv')


# 获取各区二手房均价分析
def get_average_price():
    group = house.groupby('区域')  # 将房子区域分组
    average_price_group = group['单价'].mean()  # 计算每个区域的均价
    #    print(average_price_group)  # 输出各区二手房的均价信息
    region = average_price_group.index  # 区域
    average_price = average_price_group.values.astype(int)  # 区域对应的均价，转换成int类型
    return region, average_price  # 返回区域与对应的均价


# 绘制并显示各区二手房均价分析图
def show_average_price():
    region, average_price = ???  # 获取房子区域与均价
    # 绘制柱形图，柱子宽度0.7，居中
    plt.bar(region, average_price, width=0.7, align='center')
    plt.title('各区二手房均价分析', fontsize=18)  # 设置图表标题，大小为18
    plt.xlabel('区域')  # x轴标题
    plt.ylabel('均价（元/平米）')  # y轴标题
    # 设置每个柱子的文本标签，format(b,',')表示格式化均价为千位分隔符格式
    for a, b in zip(region, average_price):
        plt.text(a, b, format(b, ','), ha='center', va='bottom', fontsize=10, color='b')
    plt.show()  # 显示图表


# 调用函数
show_average_price()


# In[ ]:




