 
use lifenghive;
insert overwrite local directory '/home/lifeng/lifenghive/result2'
select AVG(price_close),AVG(price_open),SUM(volume),symbol
from stocks
where exchanges='NASDAQ'
group by symbol
order by symbol;

