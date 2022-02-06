import os

from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3_deployment as s3deployment
from aws_cdk import aws_transfer as transfer

trtf_bucket_name = 'transfer-family-bucket-cdk'

allow_users_names = [
    'shared',
    'ifilatov',
    'snazarikov',
    'anaumov'
]


class AwsTransferFamilyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_id_tuple = os.environ.get("CDK_DEFAULT_ACCOUNT")
        region = os.environ.get("CDK_DEFAULT_REGION")
        print("region: ", region)
        account_id_string = ''.join(account_id_tuple)
        print("account_id: ", account_id_string)



        trtf_bucket = s3.Bucket(
            self, "TransferFamilyBucket",
            versioned=False,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True),
            bucket_name=trtf_bucket_name,
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )




        trtf_server_logger_policy_body = iam.Policy(self, "TransferFamilyServerLoggerPolicyBody")
        trtf_server_logger_policy_body.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server_logger_statement = iam.PolicyStatement(
            actions=[
                "logs:CreateLogStream",
                "logs:DescribeLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            effect=iam.Effect("ALLOW"),
            resources=["*"],
        )
        trtf_server_logger_policy_body.add_statements(trtf_server_logger_statement)

        trtf_server_logger_policy = iam.ManagedPolicy(
            self, "TransferFamilyServerLoggerPolicy",
            document=trtf_server_logger_policy_body.document,
            description="Policy that allows Transfer Family server write logs about events",
            managed_policy_name='transfer-family-server-logging-policy',
        )
        trtf_server_logger_policy.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server_logging_role = iam.Role(
            self, "TransferFamilyServerLoggerRole",
            assumed_by=iam.ServicePrincipal("transfer.amazonaws.com"),
            role_name='transfer-family-server-logger-role',
            managed_policies=[trtf_server_logger_policy]
        )
        trtf_server_logging_role.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server = transfer.CfnServer(
            self, "CfnTransferFamilyServer",
            protocols=['SFTP'],
            identity_provider_type='SERVICE_MANAGED',
            endpoint_type='PUBLIC',
            domain='S3',
            security_policy_name='TransferSecurityPolicy-2020-06',
            logging_role=trtf_server_logging_role.role_arn
        )
        trtf_server.apply_removal_policy(core.RemovalPolicy.DESTROY)



        trtf_server_user_policy_body = iam.Policy(self, "TransferFamilyServerUserPolicyBody")
        trtf_server_user_policy_body.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server_user_bucket_access_statement = iam.PolicyStatement(
            actions=[
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:PutLifecycleConfiguration",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:GetObjectTagging",
                "s3:PutObjectTagging",
                "s3:DeleteObjectVersion",
                "s3:DeleteObject",
                "s3:GetObjectVersion",
                "s3:GetBucketLocation"
            ],
            effect=iam.Effect("ALLOW"),
            resources=[
                f"arn:aws:s3:::{trtf_bucket_name}",
                f"arn:aws:s3:::{trtf_bucket_name}/*",
            ]
        )
        trtf_server_user_policy_body.add_statements(trtf_server_user_bucket_access_statement)

        trtf_server_user_policy = iam.ManagedPolicy(
            self, "TransferFamilyServerUserPolicy",
            document=trtf_server_user_policy_body.document,
            description="Policy that allows Transfer Family users to bucket",
            managed_policy_name='transfer-family-server-user-policy',
        )
        trtf_server_user_policy.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server_user_role = iam.Role(
            self, "TransferFamilyServerUserRole",
            assumed_by=iam.ServicePrincipal("transfer.amazonaws.com"),
            role_name='transfer-family-server-user-role',
            managed_policies=[trtf_server_user_policy]
        )
        # trtf_server_user_role.add_to_policy(trtf_server_user_trust_relationship_statement)
        trtf_server_user_role.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server_user = transfer.CfnUser(
            self, "CfnTransferFamilyServerUser",
            server_id=trtf_server.attr_server_id,
            role=trtf_server_user_role.role_arn,
            user_name='ifilatov',
            # home_directory=f'/{trtf_bucket_name}/',
            home_directory_type='LOGICAL',
            home_directory_mappings=[
                transfer.CfnUser.HomeDirectoryMapEntryProperty(
                    entry="/shared",
                    target=f"/{trtf_bucket_name}/shared"
                ),
                transfer.CfnUser.HomeDirectoryMapEntryProperty(
                    entry="/ifilatov",
                    target=f"/{trtf_bucket_name}/ifilatov"
                ),
            ],
            ssh_public_keys=['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC+Ocwh4557KxPonCxC6bQRaDilzDHR+nCUGmQqtwPBqHU9Czn2znJQWBGVrJFSVMrMsteoOVVX/AnsgDq6CVy2Cwxz0pN2ruOPfRyuJ+bECeovuAX9ReX5p/adnwo4NiMiYJT3xrWkrzPIYgRcohuQTA0RJwsSVuIOj7klnRAYaMYT70mreOmA1Y9Lqm7cyqkRqUcouqSnFCz4E9ZC/r+Br4HpmzmIHW9Lxm57Sm89Qt8fIynZEMbFebHuCKVw0JaPtuVSR9yN9wRUNXtUdInw9lATMLOU0YHBncyoMc8CjgC+Yk8XkK9q1AaJekBCun1/ikXLvvrd+eff5b9PmKlJ04remTWxv8p0yYWeA2On5qFHhejZELRLvli75v6wXMBASYHmCFgvEWKroXuWNiKhG/XtvQqfQFCSMWISTa/WAiizCjHoYTZOZqCafruzSwdCfRoj1J5zsYUjqWvL8ujFOdYXSYOUFA7rCdxI+UE1JYX6RmCB8EoHroSXTr8COf0=']
        )
        trtf_server_user.apply_removal_policy(core.RemovalPolicy.DESTROY)

        # for folder in allow_users_names:
        #     os.makedirs(
        #         os.path.join(
        #             os.path.dirname(os.path.abspath(__file__)),
        #             'bucket_inner_folders',
        #             folder
        #         ),
        #         exist_ok=True
        #     )
            # eval("aws s3api put-object --bucket transfer-family-bucket-cdk --key ifilatov/")
