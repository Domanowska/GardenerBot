import aws_cdk
from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda
)
from constructs import Construct


class GardenerBotAwsEnvStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # A DynamoDB Table to store sensor data
        table = dynamodb.Table(
            self,
            "sensor_data_table",
            table_name="gardener_bot_light_sensor_data",
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
            partition_key=dynamodb.Attribute(name='timestamp', type=dynamodb.AttributeType.STRING)
        )

        # A Lambda function to pull from S3
        lambda_func = _lambda.Function(
            self,
            'LightSensorAPI',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('lambda_func'),
            handler='light_sensor_api.handler',
            environment={
                "DYNAMO_TABLE": table.table_name
            }
        )

        # AWS IAM Policy for lambda to pull from S3
        table.grant_read_data(lambda_func)

        # An API Gateway for the lambda function
        api = apigateway.LambdaRestApi(
            self,
            "light_sensor_data_api",
            handler=lambda_func,
            rest_api_name="Light Sensor Data API",
            description="Lux measurements from arduino light sensor."
        )
