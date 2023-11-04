#!/usr/bin/env python
# coding: utf-8

# ### 通过饼形图分析 2020 年 11 月 各省大米销量的占比情况</br>
# </br>
# 要求如下：</br>
# 创建绘图对象:设置画布的宽度和高度为7×5英寸</br>
# 绘制饼形图:省份作为每一块饼形图外侧显示的说明文字;销量作为每一块饼形图的数据</br>
# 设置图表标题:图表标题为'2020年11月各省大米销量占比情况分析'，字号18

# ![image-2.png](attachment:image-2.png)

# In[3]:


import pandas as pd  # 导入pandas模块
import matplotlib.pyplot as plt  # 导入matplotlib中的pyplot模块

# 导入Excel文件
df = pd.read_excel('rice.xlsx')
# 手动添加黑体字体，解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 创建绘图对象，设置画布的宽度和高度
plt.figure(figsize=(7, 5))
labels = df['省份']  # 饼形图外侧显示的说明文字
per = df['销量']  # 每一块饼形图的比例
# 设置饼形图每块的颜色
colors = ['red', 'yellow', 'green', 'blue', 'plum', 'lavender',
          'pink', 'cyan', 'teal', 'orange', 'coral']
# 绘制饼形图
plt.pie(per, labels=labels, colors=colors,  # 指定绘图数据，添加区域水平标签，自定义填充色
        autopct='%1.1f%%', startangle=90,  # 设置百分比格式为保留一位小数，从y轴正方向画起
        radius=1.1, center=(0.2, 0.2),  # 设置饼图半径为1.1，饼图的原点为(0.2, 0.2)
        textprops={'fontsize': 10, 'color': 'black'},  # 设置文本标签的属性值，大小为10，黑色
        pctdistance=0.6)  # 设置百分比标签与圆心的距离
plt.title(???)  # 设置图表标题，字体大小为18
plt.show()  # 显示图表


# In[ ]:




