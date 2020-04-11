use lifenghive;
create external table if not exists stocks 
( exchanges string,
symbol string, 
ymd string, 
price_open float, 
price_high float, 
price_low float, 
price_close float, 
volume int, 
price_adj_close float )
row format delimited fields terminated by ',' 
location '/user/lifeng/data';
