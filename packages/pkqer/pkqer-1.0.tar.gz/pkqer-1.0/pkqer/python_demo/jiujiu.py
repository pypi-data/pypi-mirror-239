#!/usr/bin/env python
# coding: utf-8

# ### 背景
# 学习编程，循环是必备能力之一，本题需要使用while循环结构编写程序打印九九乘法表（正三角），要求</br>
# 1）乘法算式按行输出，变量j是乘法的前一个数，i是后一个数；</br>
# 2）i=1，j=1都是初始参数，外层循环条件为i<10，内层循环条件为j<=i,</br>
# 3）使用运算符%对整数进行结果格式化输出，使用end关键字在每个计算结尾处添加空格；</br>
# 4）满足循环条件，则执行程序，更新变量循环参数，否则结束循环；</br>
# 请你按程序文件的注释，将Python代码补充完整，运行程序，输出的结果。输出的结果形式如下图：</br>
# ![image.png](attachment:image.png)

# In[5]:


# -*- coding:utf-8 -*-
i=1
while i<10:
    j=1
    while j<=i:
        print("%d*%d=%2d"%(j,i,j*i),end=' ')
        j+=1
    print("")
    i+=1


# In[2]:


i=1
while i<10:
    j=1
    while j<=i:
        print("%d*%d=%2d"%(j,i,j*i),end=' ')
        j+=1
    print("")
    i+=1


# In[ ]:




