from aws_cdk import aws_iam as iam
from aws_cdk import core


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
