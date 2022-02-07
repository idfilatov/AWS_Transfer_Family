import os

from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3_deployment as s3deployment
from aws_cdk import aws_transfer as transfer

import policy_statements
import config

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


def create_policy_body(self, policy_name_suffix: str, statements: list):
    policy_body = iam.Policy(self, f"TransferFamilyServer{policy_name_suffix}Body")
    policy_body.apply_removal_policy(core.RemovalPolicy.DESTROY)
    for statement in statements:
        policy_body.add_statements(statement)

    return policy_body


def create_managed_policy(self, policy_name_suffix: str, statements: list):
    _name = f"TransferFamilyServer{policy_name_suffix}Policy"
    _managed_policy = iam.ManagedPolicy(
        self, _name,
        managed_policy_name=_name,
        statements=statements
    )
    _managed_policy.apply_removal_policy(core.RemovalPolicy.DESTROY)

    return _managed_policy


def create_role(self, role_name_suffix: str, statements: list):
    _policy = create_managed_policy(
        self, role_name_suffix, statements
    )
    _name = f"TransferFamilyServer{role_name_suffix}Role"
    _role = iam.Role(
        self, _name,
        assumed_by=iam.ServicePrincipal("transfer.amazonaws.com"),
        role_name=_name,
        managed_policies=[_policy]
    )
    _role.apply_removal_policy(core.RemovalPolicy.DESTROY)

    return _role


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
            bucket_name=config.bucket_name,
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )




        # trtf_server_logger_policy_body = iam.Policy(self, "TransferFamilyServerLoggerPolicyBody")
        # trtf_server_logger_policy_body.apply_removal_policy(core.RemovalPolicy.DESTROY)
        # trtf_server_logger_policy_body.add_statements(policy_statements.logger_statement)

        # trtf_server_logger_policy_body = create_policy_body(
        #     self, "LoggerPolicy",
        #     [policy_statements.logger_statement]
        # )

        # trtf_server_user_policy_body = iam.Policy(self, "TransferFamilyServerUserPolicyBody")
        # trtf_server_user_policy_body.apply_removal_policy(core.RemovalPolicy.DESTROY)
        # trtf_server_user_policy_body.add_statements(policy_statements.common_bucket_access_statement)

        # trtf_server_user_policy_body = create_policy_body(
        #     self, "UserPolicy",
        #     [
        #         policy_statements.common_bucket_access_statement,
        #         policy_statements.prevent_deleting_shared_statement
        #     ]
        # )

        # trtf_server_guest_policy_body = iam.Policy(self, "TransferFamilyServerGuestPolicyBody")
        # trtf_server_guest_policy_body.apply_removal_policy(core.RemovalPolicy.DESTROY)
        # trtf_server_guest_policy_body.add_statements(policy_statements.common_bucket_access_statement)
        # trtf_server_guest_policy_body.add_statements(policy_statements.deny_write_to_shared_statement)

        # trtf_server_guest_policy_body = create_policy_body(
        #     self, "GuestPolicy",
        #     [
        #         policy_statements.common_bucket_access_statement,
        #         policy_statements.prevent_deleting_shared_statement,
        #         policy_statements.deny_write_to_shared_statement
        #     ]
        # )



        # trtf_server_logger_policy = iam.ManagedPolicy(
        #     self, "TransferFamilyServerLoggerPolicy",
        #     managed_policy_name='transfer-family-server-logging-policy',
        #     statements=[
        #         policy_statements.logger_statement
        #     ]
        # )
        # trtf_server_logger_policy.apply_removal_policy(core.RemovalPolicy.DESTROY)

        # trtf_server_logger_policy = create_managed_policy(
        #     self, "Logger",
        #     [
        #         policy_statements.logger_statement
        #     ]
        # )

        # trtf_server_user_policy = iam.ManagedPolicy(
        #     self, "TransferFamilyServerUserPolicy",
        #     managed_policy_name='transfer-family-server-user-policy',
        #     statements=[
        #         policy_statements.common_bucket_access_statement,
        #         policy_statements.prevent_deleting_shared_statement
        #     ]
        # )
        # trtf_server_user_policy.apply_removal_policy(core.RemovalPolicy.DESTROY)

        # trtf_server_user_policy = create_managed_policy(
        #     self, "User",
        #     [
        #         policy_statements.common_bucket_access_statement,
        #         policy_statements.prevent_deleting_shared_statement
        #     ]
        # )

        # trtf_server_guest_policy = iam.ManagedPolicy(
        #     self, "TransferFamilyServerGuestPolicy",
        #     managed_policy_name='transfer-family-server-guest-policy',
        #     statements=[
        #         policy_statements.common_bucket_access_statement,
        #         policy_statements.prevent_deleting_shared_statement,
        #         policy_statements.deny_write_to_shared_statement
        #     ]
        # )
        # trtf_server_guest_policy.apply_removal_policy(core.RemovalPolicy.DESTROY)

        # trtf_server_guest_policy = create_managed_policy(
        #     self, "Guest",
        #     [
        #         policy_statements.common_bucket_access_statement,
        #         policy_statements.prevent_deleting_shared_statement,
        #         policy_statements.deny_write_to_shared_statement
        #     ]
        # )



        # trtf_server_logger_role = iam.Role(
        #     self, "TransferFamilyServerLoggerRole",
        #     assumed_by=iam.ServicePrincipal("transfer.amazonaws.com"),
        #     role_name='transfer-family-server-logger-role',
        #     managed_policies=[trtf_server_logger_policy]
        # )
        # trtf_server_logger_role.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server_logger_role = create_role(
            self, "Logger",
            [
               policy_statements.logger_statement
            ]
        )

        # trtf_server_user_role = iam.Role(
        #     self, "TransferFamilyServerUserRole",
        #     assumed_by=iam.ServicePrincipal("transfer.amazonaws.com"),
        #     role_name='transfer-family-server-user-role',
        #     managed_policies=[trtf_server_user_policy]
        # )
        # trtf_server_user_role.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server_user_role = create_role(
            self, "Users",
            [
                policy_statements.common_bucket_access_statement,
                policy_statements.prevent_deleting_shared_statement
            ]
        )

        # trtf_server_guest_role = iam.Role(
        #     self, "TransferFamilyServerGuestRole",
        #     assumed_by=iam.ServicePrincipal("transfer.amazonaws.com"),
        #     role_name='transfer-family-server-guest-role',
        #     managed_policies=[trtf_server_guest_policy]
        # )
        # trtf_server_guest_role.apply_removal_policy(core.RemovalPolicy.DESTROY)

        trtf_server_guest_role = create_role(
            self, "Guests",
            [
                policy_statements.common_bucket_access_statement,
                policy_statements.prevent_deleting_shared_statement,
                policy_statements.deny_write_to_shared_statement
            ]
        )




        trtf_server = transfer.CfnServer(
            self, "CfnTransferFamilyServer",
            protocols=['SFTP'],
            identity_provider_type='SERVICE_MANAGED',
            endpoint_type='PUBLIC',
            domain='S3',
            security_policy_name='TransferSecurityPolicy-2020-06',
            logging_role=trtf_server_logger_role.role_arn
        )
        trtf_server.apply_removal_policy(core.RemovalPolicy.DESTROY)








        for member in members:
            is_user = True if member['group'] == 'users' else False
            trtf_server_user = transfer.CfnUser(
                self, f"CfnTransferFamilyServer-{member['group']}-{member['username']}",
                server_id=trtf_server.attr_server_id,
                role=trtf_server_user_role.role_arn if is_user else trtf_server_guest_role.role_arn,
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
            trtf_server_user.apply_removal_policy(core.RemovalPolicy.DESTROY)

            # eval("aws s3api put-object --bucket transfer-family-bucket-cdk --key ifilatov/")
