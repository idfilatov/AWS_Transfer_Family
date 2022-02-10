import boto3

from aws_transfer_family import config


def is_it_member_folder_key(_key: str):
    """
    Checks if _key match pattern of member folder : /group/username/
    """

    split = _key.split('/')

    return len(split) == 3 and split[2] == '' and split[0] != 'shared'


def is_owner_of_folder_exists(_object_key: str):
    """
    Checks if owner of this folder is listed in config.members
    """

    _group, _username = _object_key.split('/')[:2]

    return {'group': _group, 'username': _username} in config.users


if __name__ == "__main__":
    s3_client = boto3.client('s3')
    bucket_name = config.bucket_name

    # Creates shared folder
    s3_client.put_object(Bucket=bucket_name, Key='shared/')

    current_object_keys = [key['Key'] for key in s3_client.list_objects(Bucket=bucket_name)['Contents']]

    # Creates folders for members
    for member in config.users:
        _user_folder_path = f"{member['group']}/{member['username']}/"
        if _user_folder_path in current_object_keys:
            continue
        print(f"Creating [{_user_folder_path}]")
        s3_client.put_object(Bucket=bucket_name, Key=_user_folder_path)

    # Deletes if some extra folders exists
    # (i.e. folders exists but there is no owner in config.members)
    folders_to_delete = []
    for object_key in current_object_keys:
        if not is_it_member_folder_key(object_key):
            continue
        if is_owner_of_folder_exists(object_key):
            continue
        folders_to_delete.append(object_key)
    for folder_to_delete in folders_to_delete:
        objects_to_delete = [key['Key'] for key in s3_client.list_objects(Bucket=bucket_name, Prefix=folder_to_delete)['Contents']]
        objects_to_delete.sort(reverse=True)
        for object_to_delete in objects_to_delete:
            print(f"Deleting [{object_to_delete}]")
            s3_client.delete_object(Bucket=bucket_name, Key=object_to_delete,)
