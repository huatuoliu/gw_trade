# 长城交易下单脚本使用说明
## 简介
本脚本提供了以下功能:

1. 长城证券下单相关的功能。包括：自动登录、查询持仓、查询订单、查询余额、下单、撤单，通过http请求实现。
2. 条件单功能。条件单采用mysql存储触发下单的相关指令，服务进程读取命令后，定期检查价格，判断是否触发，满足触发条件则通过下单接口下单。

## 安装
1. 安装python2.7，并且把python的安装路径加入系统的环境变量PATH
2. 安装需要的库，建议采用pycharm工具搞定这些缺少的库
	1.	大部分库都可以用pycharm自动帮忙安装，除了pillow。
	2.	pillow:pycharm中安装PIL失败。PIL只有32位的库，有人写了64位的PILLOW来替代，安装这个即可。调用还是用from PIL import *。详情请见[http://www.itnose.net/detail/6190636.html]
3. 安装mysql，创建用户，执行代码目录里的create_table.sql.txt里的语句。
4. 进入gw_trade目录，添加配置文件，config.ini。内容如下：
    
	[common]
	
	\#长城证券的资金账号
	
	account = 
	
	\#加密过的密码，可以用chrome的F12监控长城证券登录页面post的字段，其中有一个是password字段
	
	passwd_encrypted = 
	
	\#上海的股东代码
	
	secuids_sh = 
	
	\#深圳的股东代码
	secuids_sz =  

	[mysql]
	user = root
	password = root123

5. 启动pyro的名字服务。python -m Pyro4.naming
6. 启动rmi_server.py。该脚本用于接受rmi_client.py发来的条件单请求
7. 启动process_cond_order.py。该脚本用于检查是否提交条件单到长城证券。

## 使用说明
主要功能通过两个脚本实现。main.py和rmi_client.py。请执行-h可以看到使用说明。

1. python main.py -h 
2. python rmi_client.py -h 。 其中


8. 进入gw_trade目录， 执行python main.py –h ，可以看到使用说明。其中要说明的是begin_in_day和end_in_day的格式，例如：9点30，用整数930表示，14点30用1430表示。


