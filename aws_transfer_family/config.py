bucket_name = 'transfer-family-bucket-cdk'


class GroupNames:
    admins = 'admins'
    guests = 'guests'


users = [
    {
        'group': GroupNames.admins,
        'username': 'user1'
    },
    {
        'group': GroupNames.admins,
        'username': 'user2'
    },
    {
        'group': GroupNames.admins,
        'username': 'user3'
    },
    {
        'group': GroupNames.guests,
        'username': 'person1'
    },
    {
        'group': GroupNames.guests,
        'username': 'person2'
    },

]
