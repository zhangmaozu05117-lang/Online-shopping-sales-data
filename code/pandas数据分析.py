import pandas as pd
df = pd.read_csv('D:/数据分析练手/新电商网购销售数据_5000条.csv',parse_dates = ['下单时间'])   #导入数据
print(df.info())

valid_order = df[(df['订单状态'] == '已完成') & (df['退款状态'] == '无退款')]   #有效订单

#1.2025 年一共完成了多少笔有效订单？
print('一共完成:',valid_order['订单ID'].count(),'笔订单')

#2.2025 年总销售额是多少？
print('总销售额:',valid_order['原始金额'].sum())

#3.平均每笔订单消费多少钱？
a = valid_order['原始金额'].sum() / valid_order['订单ID'].count()
print('平均消费:',round(a,2))

#4.哪个月销售额最高？
valid_order['月份'] = valid_order['下单时间'].dt.month
month_sale = valid_order.groupby('月份')['原始金额'].sum()
print('销售月份最高是:',month_sale.idxmax(),'月',month_sale.max())

#5.哪个月销售额最低？
print('销售月份最低是:',month_sale.idxmin(),'月',month_sale.min())

#6.哪个商品销量最高？
print('销量最高的商品为:',valid_order.groupby('商品名称')['购买数量'].sum().idxmax())

#7.哪个商品销售额最高？
print('销售额最高的商品为:',valid_order.groupby('商品名称')['原始金额'].sum().idxmax())

#8.哪个商品类别销售额最高？
print('销售额最高的商品为:',valid_order.groupby('商品类别')['原始金额'].sum().idxmax())

#9.哪5个商品贡献了最多销售额？（销售额前五）
product_top5 = (valid_order.groupby('商品名称').agg(销售额=('原始金额','sum'),销量=('购买数量','sum'),订单数=('订单ID','count'))
    .sort_values('销售额', ascending=False).head(5))
print(product_top5)
print('-'*30)

#10.哪个省份销售额最高？
print('销售额最高的省份为:',valid_order.groupby('省份')['原始金额'].sum().sort_values(ascending = False).idxmax())

#11.男用户和女用户谁的销售额更高？
print('销售额最高的性别为:',valid_order.groupby('用户性别')['原始金额'].sum().sort_values(ascending = False).idxmax())

#12.哪个省份订单数量最多？
print('订单最多的省份为:',valid_order.groupby('省份')['订单ID'].count().sort_values(ascending = False).idxmax())

#13.为什么这个月销售额比上个月下降？
'''
先列出12个月每月的销售额
print('每月销售额:',month_sale)
以10月与11月做比较（为什么11月销售额比10月销售额下降？）
'''
print(month_sale.index[9],'月',month_sale[10],'元')
print(month_sale.index[10],'月',month_sale[11],'元')
print('销售额下降了:',round((month_sale[10] - month_sale[11]) / month_sale[10] * 100,3),'%')
#查看原因：订单数量是否下降
print('-'*30)
month_sale_order = valid_order.groupby('月份')['订单ID'].count()
print('10月份比11月份订单多:',month_sale_order[10] - month_sale_order[11],'笔')
#具体什么商品类型销量降低
month_sale_mc = valid_order.groupby(['月份','商品类别'])['原始金额'].sum().sort_values(ascending = False)
print(month_sale_mc.loc[10])
print(month_sale_mc.loc[11])
#销售额主要差在手机和电脑办公类别