import os

from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_transfer as transfer

import policy_statements
import config
import utils

members = [
    {
        'group': 'users',
        'username': 'ifilatov'
    },
    {
        'group': 'users',
        'username': 'snazau'
    },
    {
        'group': 'guests',
        'username': 'person1'
    },
    {
        'group': 'guests',
        'username': 'person2'
    }
]


class AwsTransferFamilyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_id_tuple = os.environ.get("CDK_DEFAULT_ACCOUNT")
        region = os.environ.get("CDK_DEFAULT_REGION")
        print("region: ", region)
        account_id_string = ''.join(account_id_tuple)
        print("account_id: ", account_id_string)

        _bucket = s3.Bucket(
            self, "TransferFamilyBucket",
            versioned=False,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True),
            bucket_name=config.bucket_name,
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        _logger_role = utils.create_role(
            self, "Logger",
            [
               policy_statements.logger_statement
            ]
        )

        _user_role = utils.create_role(
            self, "Users",
            [
                policy_statements.common_bucket_access_statement,
                policy_statements.prevent_deleting_shared_statement
            ]
        )

        _guest_role = utils.create_role(
            self, "Guests",
            [
                policy_statements.common_bucket_access_statement,
                policy_statements.prevent_deleting_shared_statement,
                policy_statements.deny_write_to_shared_statement
            ]
        )

        _server = transfer.CfnServer(
            self, "CfnTransferFamilyServer",
            protocols=['SFTP'],
            identity_provider_type='SERVICE_MANAGED',
            endpoint_type='PUBLIC',
            domain='S3',
            security_policy_name='TransferSecurityPolicy-2020-06',
            logging_role=_logger_role.role_arn
        )
        _server.apply_removal_policy(core.RemovalPolicy.DESTROY)

        for member in members:
            is_user = True if member['group'] == 'users' else False
            _server_user = transfer.CfnUser(
                self, f"CfnTransferFamilyServer-{member['group']}-{member['username']}",
                server_id=_server.attr_server_id,
                role=_user_role.role_arn if is_user else _guest_role.role_arn,
                user_name=member['username'],
                home_directory_type='LOGICAL',
                home_directory_mappings=[
                    transfer.CfnUser.HomeDirectoryMapEntryProperty(
                        entry="/shared",
                        target=f"/{config.bucket_name}/shared"
                    ),
                    transfer.CfnUser.HomeDirectoryMapEntryProperty(
                        entry=f"/{member['username']}",
                        target=f"/{config.bucket_name}/{member['group']}/{member['username']}"
                    ),
                ],
                ssh_public_keys=[
                    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC+Ocwh4557KxPonCxC6bQRaDilzDHR+nCUGmQqtwPBqHU9Czn2znJQWBGVrJFSVMrMsteoOVVX/AnsgDq6CVy2Cwxz0pN2ruOPfRyuJ+bECeovuAX9ReX5p/adnwo4NiMiYJT3xrWkrzPIYgRcohuQTA0RJwsSVuIOj7klnRAYaMYT70mreOmA1Y9Lqm7cyqkRqUcouqSnFCz4E9ZC/r+Br4HpmzmIHW9Lxm57Sm89Qt8fIynZEMbFebHuCKVw0JaPtuVSR9yN9wRUNXtUdInw9lATMLOU0YHBncyoMc8CjgC+Yk8XkK9q1AaJekBCun1/ikXLvvrd+eff5b9PmKlJ04remTWxv8p0yYWeA2On5qFHhejZELRLvli75v6wXMBASYHmCFgvEWKroXuWNiKhG/XtvQqfQFCSMWISTa/WAiizCjHoYTZOZqCafruzSwdCfRoj1J5zsYUjqWvL8ujFOdYXSYOUFA7rCdxI+UE1JYX6RmCB8EoHroSXTr8COf0=']
            )
            _server_user.apply_removal_policy(core.RemovalPolicy.DESTROY)

            # eval("aws s3api put-object --bucket transfer-family-bucket-cdk --key ifilatov/")
