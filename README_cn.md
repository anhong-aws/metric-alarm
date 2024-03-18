# 介绍
当CloudFront的Request指标超过设定的阈值的时候，发送告警信息

Please run `cdk deploy --all` to deploy this stack in your AWS account.
# 部署
## 1.手动创建SNS
![SNS Infomation](docs/images/sns_detail.png)
注：
- TOPIC跟下面的配置数据要一致
- 创建订阅可以在最后步骤设置。
## 2.部署CDK应用程序
```
cdk deploy --all
```
本工程会创建
* Cloud Watch EventBridge
* Two Lambda Function
* Two DynamoDB Table
* 
## 3.在DynamoDB设置LinkedAccout的配置数据

table name: account-metric-config-items


Example Record: 
```
{
 "account_id": "11111",
 "account_name": "testaccount",
 "consecutive_points": 4,
 "linked_topic_name": "metric-alarm-topic-zhangzhongyun",
 "minutes": 30,
 "payer_topic_name": "metric-alarm-topic",
 "period": 300,
 "role": "testrole",
 "save_metric_log_flag": "open",
 "send_linked_sns_flag": "close",
 "send_sns_flag": "open",
 "status": "enable",
 "threshold": 2000
}
```
![config list](docs/images/config_list.png)
![config detail](docs/images/config_detail.png)
注：
- You can write a program to read all accounts under payer and write db them automatically
- payer_topic_name必须跟步骤1中创建的sns topic一样
- 所有LinkedAccount的告警都会发送到payer_topic_name
- 如果send_linked_sns_flag为open，则需要创建一个LinkedAccount的sns，topic必须跟linked_topic_name一样，这个只发送这个账号下的告警
# 代码
## lambda代码
```
lambda-code/
    └── metric                 采集&告警的lambda
        ├── index.py           lambda主函数
        ├── metric.py          业务逻辑主体：采集指标、告警
```
## 代码调试
建议直接运行python
```
修改入参，运行metric.py等
```
## CDK代码
```
lib
└── metric-alarm-stack.ts   读取配置、采集指标、告警
└── metric-alarm-stack.ts   写入告警日志
```