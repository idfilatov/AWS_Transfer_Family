bucket_name = 'transfer-family-bucket-cdk'


class GroupNames:
    admins = 'admins'
    guests = 'guests'


users = [
    {
        'group': GroupNames.admins,
        'username': 'ifilatov'
    },
    {
        'group': GroupNames.admins,
        'username': 'snazau'
    },
    {
        'group': GroupNames.admins,
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

]
