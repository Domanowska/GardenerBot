from aws_cdk import (
    Stack,
    aws_s3 as s3
)
from constructs import Construct


class GardenerBotAwsEnvStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # An S3 Bucket to store sensor data
        bucket = s3.Bucket(self, "sensor_data_bucket", bucket_name="gardener-bot-sensor-data-bucket", versioned=True)
