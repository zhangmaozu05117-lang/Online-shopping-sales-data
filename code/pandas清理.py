import pandas as pd
from unicodedata import category

df = pd.read_csv('D:/数据分析练手/电商网购销售数据_5000条_原始脏数据.csv')   #导入数据
#print(df.head(10))                                                    #显示前十行数据
#print(df.info())                                                      #显示数据类型
#print(df.isnull().sum())                                              #缺失值统计
df.dropna(subset=['用户ID'],inplace=True)                               #用户ID缺失直接删除该数据
#print(df.duplicated().sum())                                          #显示重复值
df.drop_duplicates(inplace=True)                                       #删除重复项


#统一数据格式
df['用户性别'] = df['用户性别'].str.strip()
df['支付方式'] = df['支付方式'].str.strip().str.replace('银行卡支付','银行卡', regex=False)
df['订单状态'] = df['订单状态'].str.strip().replace('取消','已取消', regex=False).replace('完成','已完成', regex=False)
df['退款状态'] = df['退款状态'].str.strip().replace('未退款','无退款', regex=False)
df.loc[df['退款状态'] == '无','退款状态'] = '无退款'
df['商品名称'] = df['商品名称'].str.strip().str.replace(r'\s+',' ',regex=True)
df['商品类别'] = df['商品类别'].str.strip().str.replace(r'\s+',' ',regex=True)
df['商品ID'] = df['商品ID'].str.upper()                                           #全部统一成大写
df['订单ID'] = df['订单ID'].str.upper()
df['用户ID'] = df['用户ID'].str.upper()
df['省份'] = df['省份'].str.strip().replace('广东','广东省', regex=False).replace('河南','河南省', regex=False).replace('浙江','浙江省', regex=False)

df.loc[df['商品ID'] == 'P1002','商品名称'] = 'iPhone 15 Pro'
df.loc[df['商品ID'] == 'P2005','商品名称'] = '机械键盘'
df.loc[df['商品ID'] == 'P4002','商品名称'] = '阿迪达斯卫衣'
df.loc[df['商品ID'] == 'P5001','商品名称'] = '雀巢咖啡'
df.loc[df['商品名称'] == '戴尔 27英寸显示器','商品ID'] = 'P3001'
df.loc[df['商品名称'] == '华为 Mate 70','商品ID'] = 'P1003'
df.loc[df['商品名称'] == 'iPhone 15','商品ID'] = 'P1001'
df.loc[df['商品名称'] == '蒙牛纯牛奶','商品ID'] = 'P5002'
df.loc[df['商品名称'] == '罗技 MX Master 3S','商品ID'] = 'P2004'
df.loc[df['商品名称'] == '机械革命游戏本','商品ID'] = 'P3003'
df.loc[df['商品名称'] == '机械键盘','商品ID'] = 'P2005'
df.loc[df['商品名称'] == '小米手环 9','商品ID'] = 'P2003'
df.loc[df['商品名称'] == 'iPhone 15 Pro','商品ID'] = 'P1002'


#寻找缺失值
df.loc[df['用户性别'].isna(),'用户性别'] = '未知'   #用户性别为空修改为未知
df.loc[df['订单状态'].isna(),'订单状态'] = '未知'   #订单状态为空修改为未知
df.loc[df['退款状态'].isna(),'退款状态'] = '未知'   #退款状态为空修改为未知
df.loc[df['支付方式'].isna(),'支付方式'] = '未知'   #支付方式为空修改为未知
df.loc[df['城市'].isna(),'城市'] = '未知'          #城市为空修改为未知


#统一商品类别
#print(df["退款状态"].unique())                                 #查看商品类别都有什么类型数据
#print(df[["商品ID", "商品名称", "商品类别"]].drop_duplicates())  #显示这三列不同的数据
standard_map = {"P4001": "服饰鞋包","P2001": "数码配件","P2002": "数码配件","P1005": "手机"}
# 根据商品ID替换成标准类别
df["商品类别"] = df["商品ID"].map(standard_map).fillna(df["商品类别"])


#修改数据类型
df['用户性别'] = df['用户性别'].astype('category')
df['支付方式'] = df['支付方式'].astype('category')
df['订单状态'] = df['订单状态'].astype('category')
df['退款状态'] = df['退款状态'].astype('category')
df['商品类别'] = df['商品类别'].astype('category')

#修改时间格式
df['下单时间'] = df['下单时间'].str.replace('/', '-', regex=False) \
                         .str.replace('年', '-', regex=False) \
                         .str.replace('月', '-', regex=False) \
                         .str.replace('日', '', regex=False)
df['下单时间'] = pd.to_datetime(df['下单时间'], errors='coerce')     #修改日期类型为Timestamp
df = df[df['下单时间'].notna()].copy()                              #把正确的时间列复制下来再覆盖原有的df日期列（格式不对的时间会变成False,不复制）

#寻找异常值
#print(df[ (df['购买数量']<=0) & (df['商品单价']<=0) & (df['原始金额']<=0)] )    #寻找同时满足购买数量和商品单价和原始金额都小于等于0的数据

#print(df[df['商品单价'] <= 0]['商品单价'])                #寻找商品单价小于等于0或为空的数据
#修改商品单价异常的数据：商品单价 = 原始金额/购买数量
df.loc[(df['商品单价'] <= 0) | (df['商品单价'].isna()),'商品单价'] = df['原始金额']/df['购买数量']

#print(df[df['购买数量'] <= 0]['购买数量'])                #寻找购买数量小于等于0或为空的数据
#修改购买数量异常的数据：购买数量 = 原始金额/商品单价
df.loc[(df['购买数量'] <= 0) | (df['购买数量'].isna()),'购买数量'] = df['原始金额']/df['商品单价']

#print(df[df['原始金额'] <= 0]['原始金额'])                #寻找购买数量小于等于0或为空的数据
#修改购买数量异常的数据：原始金额 = 购买数量*商品单价
df.loc[(df['原始金额'] <= 0) | (df['原始金额'].isna()),'原始金额'] = df['购买数量']*df['商品单价']

df['购买数量'] = df['购买数量'].astype('int64')    #缺失值补全后修改数据类型

#print(df['购买数量'].value_counts().sort_index())  #显示购买数量各有多少条
df = df[(df['购买数量'] < 50)]    #排除购买数量过大的异常值

df.to_csv('D:/数据分析练手/新电商网购销售数据_5000条.csv', encoding='utf_8_sig',index=False)    #导出数据