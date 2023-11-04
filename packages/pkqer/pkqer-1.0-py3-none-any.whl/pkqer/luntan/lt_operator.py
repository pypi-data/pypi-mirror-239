"""
2、论坛数据分析
第一题
mkdir discuz
粘贴Py代码
IP修改为内网IP
python *.py

第二题

create table data(
tid int,
author string,
score int,
grate string,
title string,
content string
) row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' with SERDEPROPERTIES("separatorChar"=",") STORED AS TEXTFILE;

导入数据

load data local inpath "/root/discuz/data.txt" into table data;

insert overwrite local directory '/root/discuz01'
row format delimited fields terminated by '\t'
select count(*) from data;


insert overwrite local directory '/root/discuz02'
row format delimited fields terminated by '\t'
select count(distinct author) from data;


insert overwrite local directory '/root/discuz03'
row format delimited fields terminated by '\t'
select author,count(*) as sum from data group by author order by sum desc,author asc limit 10;


insert overwrite local directory '/root/discuz04'
row format delimited fields terminated by '\t'
select a.author,a.grate from (select author,grate,count(*) as sum from data group by author,grate order by sum desc limit 1) as a;


insert overwrite local directory '/root/discuz05'
row format delimited fields terminated by '\t'
select author,score from data group by author,score order by score desc limit 5

"""