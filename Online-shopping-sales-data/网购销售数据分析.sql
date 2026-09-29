create database Online_shopping_data;
use Online_shopping_data;

#1.2025 年一共完成了多少笔有效订单？
select
    count(订单ID) 有效订单
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款';

#2.2025 年总销售额是多少？
select
    sum(原始金额) 总销售额
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款';

#3.平均每笔订单消费多少钱？
select
    avg(原始金额) 平均消费金额
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款';

#4.哪个月销售额最高？
select
    month(下单时间) sale_month,
    sum(原始金额) month_sales
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by month(下单时间)
order by month_sales desc
limit 1;

#5.哪个月销售额最低？
select
    month(下单时间) sale_month,
    sum(原始金额) month_sales
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by month(下单时间)
order by month_sales
limit 1;
#6.哪个商品销量最高？
select
    商品名称,
    count(购买数量) sales_volume
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by 商品名称
order by sales_volume desc
limit 1;
#7.哪个商品销售额最高？
select
    商品名称,
    sum(原始金额) sales
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by 商品名称
order by sales desc
limit 1;
#8.哪个商品类别销售额最高？
select
    商品类别,
    sum(原始金额) sales
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by 商品类别
order by sales desc
limit 1;
#9.哪5个商品贡献了最多销售额？（销售额前五）
select
    商品名称,
    sum(原始金额) sales,
    sum(购买数量) amount,
    count(订单ID) order_form_amount
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by 商品名称
order by sales desc
limit 5;
#10.哪个省份销售额最高？
select
    省份,
    sum(原始金额) sales
from os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by 省份
order by sales desc
limit 1;
#11.男用户和女用户谁的销售额更高？
select
    用户性别,
    sum(原始金额) sales
from os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款' and 用户性别 != '未知'
group by 用户性别
order by sales desc;
#12.哪个省份订单数量最多？
select
    省份,
    count(订单ID) sales
from os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by 省份
order by sales desc
limit 1;

#13.每个月的销售额
select
    month(下单时间) months,
    sum(原始金额) sales
from os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by months
order by months;

#14.为什么11月销售额比10月份销售额低？
#销售额下降多少？
with month_sales as (
select
    month(下单时间) mon,
    sum(原始金额) sales
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款'
group by month(下单时间)
)
select
    (oct.sales - nov.sales)/oct.sales *100 AS 销售额下降率,
    oct.sales AS oct_sales,
    nov.sales AS nov_sales
from month_sales oct , month_sales nov
where oct.mon =10 AND nov.mon =11;

#10月与11月商品类别销售额比较
with cat_month_sale as (
select
    商品类别,
    month(下单时间) mon,
    sum(原始金额) sales
from Os_data os
where os.订单状态 = '已完成' and os.退款状态 = '无退款' and month(下单时间) in (10,11)
group by 商品类别, month(下单时间)
)
select
    商品类别,
    MAX(case when mon=10 then sales else 0 end)  oct_sales_10月,
    MAX(case when mon=11 then sales else 0 end)  nov_sales_11月
from cat_month_sale
group by 商品类别;