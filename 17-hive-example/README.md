# 实例分析：FoodMart数据集在Hive平台的使用案例


## 准备知识

* Hive


## 数据准备

FoodMart数据库为某家大型的食品连锁店的经营业务所产生的数据，该数据涉及到了公司经营的各个方面，包括产品、库存、人事、客户和销售等。该数据库中的表包括顾客的基本信息表、货币信息表、公司部门表、职员表、消费表、地区表等。FoodMart数据库经常用于多维分析的测试数据集，同数据库部分的学习，我们选取其中一个数据库子集：sales_fact_1997、customer、product、product_class、time_by_day、store、promotion7个表导入Hive中进行测试。
在进行测试之前，我们需要在原有数据库中将所需要的数据表导出，此处，我们以文本形式为例进行。各表的维度如下表所示：


	表名	             行数	      列数
	customer	      10281	     29
	product	           1560	     15
	product_class	    110	      5
	store	             25	     25
	promotion	       1864	      7
	sales_fact_1997	 210429	      8
	time_by_day	        730	     10
## 数据迁移与导入
###创建数据库
创建名为“FoodMart”的数据库并使用：

	hive> CREATE DATABASE IF NOT EXISTS FoodMart;
	hive> USE FoodMart;
### 创建表格

store表维度最小，在此以创建store表为例，首先在FoodMart数据库下创建名为“store”的表，随后将本地数据LOAD至HIVE端即可：
创建表格：

	hive> CREATE TABLE IF NOT EXISTS store (
	store_id INT, store_type STRING,region_id INT,store_name STRING, store_number INT, store_street_address STRING,	store_city STRING,store_state STRING,	store_postal_code STRING,store_country STRING, store_manager STRING, store_phone STRING, store_fax STRING,first_opened_date STRING, last_remodel_date STRING, lease_sqft STRING,	store_sqft STRING,	grocery_sqft STRING, frozen_sqft STRING,meat_sqft STRING, coffee_bar STRING, video_store STRING, salad_bar STRING,	prepared_food STRING, florist STRING)
	ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

### 导入数据


	hive> LOAD DATA LOCAL INPATH '/home/cao.xin/FoodMart_Data/store.txt' OVERWRITE INTO TABLE store;


使用count(1)函数查看数据维度:


	hive> select count(1) from store;

由于我们所使用的数据较小，在此没有使用PARTITION对数据进行分区操作；当有数据量较大的数据进行迁移时，可使用字段中可分区的字段对数据进行分区存储，真正达到分布式数据存储效果。
通过show tables语句查看现有数据库下的表格：


	hive> show tables;



##数据查询示例
简单查询，如查询编号为1的用户在customer表中的所有信息：


	hive> select * from customer where customer_id=1;


连接查询，查询销售额最高的top3的用户是谁，基本的思路是先查询sales_fact_1997中排序前3的customer_id，再使用id与customer做连接查询出其他信息如姓名即可。
单独对销量表查询排序，代码如下：


	select customer_id, sum(store_cost) as cost_total from sales_fact_1997 group by customer_id sort by cost_total DESC limit 3;


以查询用户的姓名为例，完整的SQL语句可参考：


	hive> select b.lname,b.fname,a.cost_total from
	    > (select customer_id, sum(store_cost) as cost_total from sales_fact_1997 group by customer_id sort by cost_total DESC limit 3 ) a
	    > left outer join
	    > (select customer_id, lname,fname from customer ) b
	> on a.customer_id=b.customer_id;

返回的结果即可看到用户的lname,fname和销售额组成的3×3的数据表。

###数据导出操作

在日常的数据工作中，我们并不满足于仅在服务器端对数据进行类别的统计，很多时候，我们需要将数据下载到本地进行进一步的分析与操作。如何将Hive数据导出将是这一节介绍的内容。
整体来说，实际工作中将Hive平台的数据导出大致分为两个步骤，一为直接在Hive平台环境下将数据导出到本地文件系统、导出到HDFS中；二为切换到服务器环境，即Linux工作环境，使用Shell命令对数据进行服务器端的导出。
首先我们介绍直接在Hive平台上如何进行数据的导出。以简单查询为例，现在我们想将所有家庭拥有孩子数大于2的用户的customer信息表中的信息导出进行进一步的分析工作，若直接导出到本地文件系统：



	insert overwrite local directory '/home/cao.xin/customer_1'
	select * from customer where total_children>'2';


与数据导入不同，这里不再是insert into语句。通过insert overwrite local directory将Hive中的表导出到本地文件系统的目录下也是通过MapReduce完成的，运行完语句后，目标文件夹下将产生名为类似000000_0的文件。
将数据导出到HDFS与导出到本地文件系统类似，仅需在directory前省略local即可，这时数据存放的路径就改变了。
此外，在Linux环境下，还可通过hive调用语句将数据导出：


	hive -e "select * from foodmart.customer where total_children>'2'" >> local/customer_2.txt


如果是事先写好的SQL脚本，还可通过-f调用sql文件，如若将上述select操作写入文件customer_U.sql，则数据导出操作为：


	hive -f customer_U.sql >> customer_3.txt


按照上例的示例将数据导出到本地文件系统后，即可在Linux端使用sz操作将数据从服务器本地文件下载到个人电脑。sz的操作在Linux操作系统的课程中已做了相关介绍，在此不再做更深入的介绍。
