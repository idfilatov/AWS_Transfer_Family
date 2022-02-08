import os

from aws_cdk import aws_iam as iam
from aws_cdk import core

import config


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


def key_pair_exists(_folder_with_keys: str, _key_name: str):
    """
    Checks if both (private and public) ssh-keys are exist
    """

    return os.path.exists(os.path.join(_folder_with_keys, _key_name)) and \
           os.path.exists(os.path.join(_folder_with_keys, _key_name + ".pub"))


def delete_extra_keys(_folder_with_keys: str):
    """
    Deletes if some extra keys exists
    (i.e. keys pair exists but there is no owner in config.members)
    """

    for file in os.listdir(_folder_with_keys):
        _file = file.replace('.pub', '')
        _group, _username = _file.split('-')[2: 4]
        if {'group': _group, 'username': _username} not in config.members:
            os.remove(os.path.join(_folder_with_keys, file))


def create_key_pair(_folder_with_keys: str, _key_name: str):
    """
    Uses shell command for creating ssh-key pair for one member
    """
    for file in os.listdir(_folder_with_keys):
        if _key_name in file:
            os.remove(os.path.join(_folder_with_keys, file))

    os.system(f'ssh-keygen -P "" -q -m PEM -f {_folder_with_keys}/{_key_name}')


def get_public_ssh_key(group: str, username: str):
    """
    Return (create if need) public part of ssh-key pair
    """
    _folder_with_keys = os.path.join(
        'aws_transfer_family' if not __name__ == "__main__" else '',
        'secret_keys',
    )
    delete_extra_keys(_folder_with_keys)

    _key_name = f"ssh-key-{group}-{username}"

    if not key_pair_exists(_folder_with_keys, _key_name):
        create_key_pair(_folder_with_keys, _key_name)

    f = open(os.path.join(_folder_with_keys, _key_name + '.pub'), "r")
    _public_ssh_key_raw = f.read()
    _public_ssh_key = "".join(_public_ssh_key_raw.split(" ")[:2])

    return _public_ssh_key


if __name__ == "__main__":
    pass
    # _public_ssh_key = get_public_ssh_key('users', 'kek123')
    # print(_public_ssh_key)
