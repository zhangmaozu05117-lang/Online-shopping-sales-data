import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv('D:/数据分析练手/新电商网购销售数据_5000条.csv',parse_dates = ['下单时间'])   #导入数据
valid_order = df[(df['订单状态'] == '已完成') & (df['退款状态'] == '无退款')].copy()   #有效订单

#--------------------------------------------------------------------

#设置月度列
valid_order['月份'] = valid_order['下单时间'].dt.month
month_sale = valid_order.groupby('月份')['原始金额'].sum()
#设置季度列
valid_order['季度'] = valid_order['下单时间'].dt.quarter
quarter_sale = valid_order.groupby('季度')['原始金额'].sum()

#--------------------------------------------------------------------

def show_bar(title, x, y, xlabel, ylabel):                #柱状图函数
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(10,5))
    plt.title(title,color='red',fontsize=20)
    plt.bar(x, y,label=ylabel)
    plt.xticks(x)                                       # 强制 x 刻度
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for x, y in zip(x,y):
        plt.text( x,y,f'{y/10000:.1f}万',ha='center',va='bottom')
    plt.grid(axis='y', alpha=0.2)
    plt.legend(loc='upper right', fontsize=10)
    plt.tight_layout()
    plt.show()

#--------------------------------------------------------------------

def show_berh(title,x,y,xlabel,ylabel):                   #条形图函数
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体
    plt.figure(figsize=(10, 5))                   # 画布大小
    plt.title(title, color='red', fontsize=20)    # 标题设置
    plt.barh(y,x, label=xlabel, color='orange')   # 条形图
    plt.ylabel(ylabel, fontsize=15)               # y轴
    plt.xlabel(xlabel, fontsize=15)               # x轴
    plt.legend(loc='upper right', fontsize=10)    # 图例位置
    plt.grid(axis='x', alpha=0.2)                 # 网格线
    plt.tight_layout()                            # 优化排版
    plt.show()                                    # 展示图表

#--------------------------------------------------------------------

def show_pie(title,data,label,angle):                     #饼图函数
    plt.rcParams['font.sans-serif'] = ['SimHei']    # 设置字体
    plt.figure(figsize=(10, 5))                     # 画布大小
    plt.title(title, color='red', fontsize=20)      # 标题设置
    plt.pie(data,labels=label,                      # 数据及标签
            autopct='%1.1f%%',                      # 显示百分比
            startangle=angle)                       # 调整初始角度
    plt.show()                                      # 展示图表

#--------------------------------------------------------------------

def show_plot(title,x,y,xlabel,ylabel,):                   #折线图函数
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(10, 5))
    plt.title(title, color='red', fontsize=20)
    plt.plot(x,y,label=ylabel,marker = 'o')
    plt.xticks(x)                                                      # 强制 x 刻度
    plt.xlabel(xlabel, fontsize=15)                                    # x轴
    plt.ylabel(ylabel, fontsize=20)                                    # y轴
    plt.legend(loc='upper left', fontsize=10)                          # 图例位置
    plt.grid(axis='y', alpha=0.2)                                      # 网格线
    for x, y in zip(x,y):                                              # y轴上的数字
        plt.text(x, y + 15000, str(y), fontsize=11, ha='center', va='center')
    plt.tight_layout()
    plt.show()

#--------------------------------------------------------------------
plt.rcParams['font.sans-serif'] = ['SimHei']         #设置字体
plt.figure(figsize=(10,5))                           #画布大小
plt.title('2025年用户消费分布',color='red',fontsize=20)  #标题设置

a = valid_order.groupby('用户ID')['原始金额'].sum()
plt.hist(a,bins = 80,label='消费人群')                #直方图

plt.xlabel('消费金额',fontsize=15)                      #x轴
plt.ylabel('消费人数',fontsize=20)                      #y轴

plt.legend(loc='upper right',fontsize=10)            #图例位置
plt.grid(axis = 'y',alpha = 0.2)                    #网格线

plt.tight_layout()                                  #优化排版
plt.show()                                          #展示图表

#--------------------------------------------------------------------
a = valid_order.groupby('省份')['原始金额'].sum().sort_values(ascending = True).tail()
lst_index = a.index.tolist()
lst = a.tolist()
show_berh('2025年TOP5销售额省份',lst,lst_index,'销售额','省份')
#--------------------------------------------------------------------

a = valid_order.groupby('商品类别')['原始金额'].sum().sort_values(ascending = True)
lst_index = a.index.tolist()
lst = a.tolist()
show_pie('2025年各个商品类别销售额占比',lst,lst_index,301)
#--------------------------------------------------------------------
a = valid_order[valid_order['用户性别'] != '未知'].groupby('用户性别')['原始金额'].sum().sort_values(ascending = True)
lst_index = a.index.tolist()
lst = a.tolist()
show_pie('2025年男女消费比例',lst,lst_index,90)

#--------------------------------------------------------------------
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
show_plot('2025年月度销售额',months,month_sale,'月度','销售额')

#--------------------------------------------------------------------
quarters = ['1季度','2季度','3季度','4季度']
show_bar('2025年季度销售额',quarters,quarter_sale,'季度','销售额')
#--------------------------------------------------------------------
a = valid_order.groupby('商品名称')['原始金额'].sum().sort_values(ascending = False).head()
lst_index = a.index.tolist()
lst = a.tolist()
show_bar('2025年销售额TOP5商品',lst_index,lst,'商品名称','销售额')
#--------------------------------------------------------------------
a = valid_order[(valid_order['月份'] == 10) | (valid_order['月份'] == 11)].groupby('月份')['原始金额'].sum()
lst_index = a.index.tolist()
show_bar('2025年10月-11月销售额对比',lst_index,a,'月份','销售额')

#--------------------------------------------------------------------
oct_sale = (valid_order[valid_order['月份'] == 10].groupby('商品类别')['原始金额'].sum())
nov_sale = (valid_order[valid_order['月份'] == 11].groupby('商品类别')['原始金额'].sum())

plt.figure(figsize=(10, 5))                        #画布大小
plt.title('10月 vs 11月各商品类别销售额对比', fontsize=18)
x = range(len(oct_sale.index))                      #x轴坐标个数
width = 0.35                                       #柱子宽度
plt.bar([i - width/2 for i in x],oct_sale,width=width,label='10月')
plt.bar([i + width/2 for i in x],nov_sale,width=width,label='11月')
plt.xticks(x, oct_sale.index)
plt.xlabel('商品类别')
plt.ylabel('销售额（元）')
plt.legend(loc='upper right',fontsize=10)
plt.grid(axis='y', alpha=0.2)
plt.tight_layout()
plt.show()

category_compare = pd.DataFrame({'10月销售额': oct_sale,'11月销售额': nov_sale})
category_compare['销售额变化'] = (category_compare['11月销售额'] -category_compare['10月销售额'])
category_compare['变化率'] = (category_compare['销售额变化'] /category_compare['10月销售额'] * 100)
print(category_compare)