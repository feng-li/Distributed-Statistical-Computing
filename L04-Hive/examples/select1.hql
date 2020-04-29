use lifenghive;
insert overwrite local directory '/home/lifeng/lifenghive/result' 
select AVG(price_close),AVG(price_open),AVG(price_high),AVG(price_low), exchanges
from stocks
where symbol = 'AAPL'
group by exchanges;
