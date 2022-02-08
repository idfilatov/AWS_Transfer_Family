import os

from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_transfer as transfer

import policy_statements
import config
import utils


class AwsTransferFamilyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_id_tuple = os.environ.get("CDK_DEFAULT_ACCOUNT")
        region = os.environ.get("CDK_DEFAULT_REGION")
        print("Region: ", region)
        account_id_string = ''.join(account_id_tuple)
        print("Account_id: ", account_id_string)

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

        roles_to_group_mapping = {
            config.GroupNames.users: _user_role,
            config.GroupNames.guests: _guest_role
        }

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

        for member in config.members:
            _ssh_public_key = utils.get_public_ssh_key(member['group'], member['username'])
            _server_user = transfer.CfnUser(
                self, f"CfnTransferFamilyServer-{member['group']}-{member['username']}",
                server_id=_server.attr_server_id,
                role=roles_to_group_mapping[member['group']].role_arn,
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
                ssh_public_keys=[_ssh_public_key]
            )
            _server_user.apply_removal_policy(core.RemovalPolicy.DESTROY)
