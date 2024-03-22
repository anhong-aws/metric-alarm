import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as iam from 'aws-cdk-lib/aws-iam'; // 引入 IAM 相关模块
import * as ddb from 'aws-cdk-lib/aws-dynamodb';
import { CfnOutput } from 'aws-cdk-lib';

export class MetricAlarmStack extends cdk.Stack {
  public readonly AlarmLambdaArn: string;
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);


    //crate a dynamodb table
    const table = new ddb.Table(this, 'AccountMetricConfigItemsTable', {
      tableName: 'account-metric-config-items',
      partitionKey: {name: 'account_id', type: ddb.AttributeType.STRING},
      billingMode: ddb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    })

    // 创建 Lambda 执行角色并附加策略
    const lambdaExecutionRole = new iam.Role(this, 'LambdaExecutionRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'), // Lambda 服务的身份标识
    });

    // 为 Lambda 执行角色添加策略
    lambdaExecutionRole.addToPolicy(new iam.PolicyStatement({
      actions: ['logs:CreateLogGroup', 'logs:CreateLogStream', 'logs:PutLogEvents'],
      resources: ['*'], // 允许 Lambda 写入 CloudWatch Logs
    }));

    // 为 Lambda 执行角色添加 sts:AssumeRole 权限，允许切换角色
    lambdaExecutionRole.addToPolicy(new iam.PolicyStatement({
      actions: ['sts:AssumeRole'],
      resources: ['*'], // 允许扮演任何角色
    }));

    // 添加 Lambda 执行 DynamoDB 操作的权限
    table.grantReadData(lambdaExecutionRole);

    // 为 Lambda 执行角色添加所有 SNS 权限
    lambdaExecutionRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        'sns:ListTopics',
        'sns:GetTopicAttributes',
        'sns:ListSubscriptionsByTopic',
        'sns:Publish',
      ],
      resources: ['*'], // 这里资源可以根据你的实际需求进行限制
    }));

    // 创建 Python Lambda 函数
    const alarmLambda = new lambda.Function(this, 'MetricLambda', {
      runtime: lambda.Runtime.PYTHON_3_10,
      handler: 'index.handler', // 指定 Lambda 处理程序的入口函数
      code: lambda.Code.fromAsset('./lambda-code/metric'), // 替换为您的 Python Lambda 代码路径
      role: lambdaExecutionRole, // 关联 Lambda 执行角色
      memorySize: 256, // 内存128M
      timeout: cdk.Duration.minutes(3) // 设置超时时间为 3 分钟
    });

    // 创建定时触发器，每天执行一次
    // const rule = new events.Rule(this, 'MyRule', {
    //   schedule: events.Schedule.cron({ minute: '0', hour: '1' }), // 每天凌晨 1 点执行
    // });
    // 创建定时触发器，每5分钟执行一次
    const rule = new events.Rule(this, 'MyRule', {
      schedule: events.Schedule.rate(cdk.Duration.minutes(30)), // 每5分钟执行一次
    });
    rule.addTarget(new targets.LambdaFunction(alarmLambda));
    // 输出 Lambda 函数的 ARN
    new CfnOutput(this, 'AlarmLambdaArn', {
      value: alarmLambda.functionArn,
      exportName: 'AlarmLambdaArnExport'
    });

    this.AlarmLambdaArn = alarmLambda.functionArn;
  }
}
