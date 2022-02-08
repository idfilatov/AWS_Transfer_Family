bucket_name = 'transfer-family-bucket-cdk'


class GroupNames:
    users = 'users'
    guests = 'guests'


members = [
    {
        'group': GroupNames.users,
        'username': 'ifilatov'
    },
    {
        'group': GroupNames.users,
        'username': 'snazau'
    },
    {
        'group': GroupNames.users,
        'username': 'anaumov'
    },
    {
        'group': GroupNames.guests,
        'username': 'person1'
    },
    {
        'group': GroupNames.guests,
        'username': 'person2'
    },
    {
        'group': GroupNames.guests,
        'username': 'person3'
    },
]
