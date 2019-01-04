# 实例分析：Hadoop Streaming 与 Hive 交互计算实例


## 准备知识

* Hive
* Hadoop Streaming
* Python


## 数据准备
与Hadoop类似，Hive也支持使用JAVA之外的语言编写Streaming程序扩展Hive，实现Hive中的函数无法实现的功能。开发Hive的Streaming程序和开发Hadoop的Streaming程序是相同的，都是从标准输入中读取数据，将结果写出到标准输出中。
Hive中提供多个语法来使用Streaming，包括map(), reduce(), TRANSFORM( )，使用TRANSFROM()的情形较多。
例如，我们现在需要将表格中的日期字符串转换成季节字符串形式，若现在的日期形式为YYYY-MM-DD，通过变换，希望输出YYYYQ1的季节字符串形式。我们在Hive中创建表格birdata，并载入。测试数据：

	AAA    1990-02-01
	BBB	   1984-01-16
	CCC    1988-07-01

下面演示使用Hive Streaming进行字符串的转换。
首先写Python脚本进行数据的转换：

	#!/usr/bin/env python
	#-*- coding:utf-8 -*-

	import sys
	#转换函数
	def get_date_year(pdate):
	    (year_val,month_val) = (pdate[0:4],pdate[4:6])
	    quarter_index = (int(month_val)-1)/3+1
	    quarter_str = "%sQ%d" % (year_val,quarter_index)
	    return quarter_str

	for line in sys.stdin:
	    line = str(line).strip()
	    if not line: continue
	    fields = line.split("\t")
	    date_val = str(fields[-1]).replace("-","")
	    output_fields = fields[:-1]+[get_date_year(date_val)]
	    print "\t".join(output_fields)
再次，在Hive中调用上面的Streaming脚本；这个调用中包含两个步骤，第一步需要以绝对路径的方式添加脚本；第二步需要用TRANSFORM…USING…AS句式进行调用。		use test;
	add file /Users/hive/quarter.py;
	select TRANSFROM(birthday) using 'quarter.py' as (bir_quarter) from birdata;
注意，使用这种方式调用Streaming，select中除了TRANSPORM外不能有别的字段。在大数据集上使用Streaming时，一般都需要和DISTRIBUTE BY…, SORT BY句式一起使用，解决单节点负载过重问题。
