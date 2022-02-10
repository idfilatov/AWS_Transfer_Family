from aws_cdk import aws_iam as iam
import config

'''
    Policy statement.
    Allow Transfer Family to writing logs
'''
logger_statement = iam.PolicyStatement(
    actions=[
        "logs:CreateLogStream",
        "logs:DescribeLogStream",
        "logs:CreateLogGroup",
        "logs:PutLogEvents"
    ],
    effect=iam.Effect.ALLOW,
    resources=["*"],
)

'''
    Policy statement.
    Provide common access to Read/Write/Delete files and Create/Delete folders
'''
common_bucket_access_statement = iam.PolicyStatement(
    actions=[
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
    ],
    effect=iam.Effect.ALLOW,
    resources=[
        f"arn:aws:s3:::{config.bucket_name}",
        f"arn:aws:s3:::{config.bucket_name}/*",
    ]
)

'''
    Policy statement.
    Dont allow to delete <shared> folder from S3 Bucket
'''
prevent_deleting_shared_statement = iam.PolicyStatement(
    actions=[
        "s3:DeleteObject",
    ],
    effect=iam.Effect.DENY,
    resources=[
        f"arn:aws:s3:::{config.bucket_name}/shared/",
    ]
)

'''
    Policy statement.
    Dont allow guests to Write/Delete into <shared> folder from S3 Bucket (Read-only mode)
'''
deny_write_to_shared_statement = iam.PolicyStatement(
    actions=[
        "s3:PutObject",
        "s3:DeleteObject",
    ],
    effect=iam.Effect.DENY,
    resources=[
        f"arn:aws:s3:::{config.bucket_name}/shared",
        f"arn:aws:s3:::{config.bucket_name}/shared/*",
    ]
)
