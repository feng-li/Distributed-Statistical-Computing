use lifenghive; 
insert overwrite local directory '/home/lifeng/lifenghive/result3' 
select symbol,AVG(price_close) as avg_close,AVG(price_open) as avg_open,SUM(volume) as sum_volume
from stocks
where price_open>2.6
and price_close>2.6
group by symbol
sort by sum_volume desc;

