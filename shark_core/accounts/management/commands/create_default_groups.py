from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

GROUPS = [
    {
        'id': 1,
        'name': 'Administrators'
    },
    {
        'id': 2,
        'name': 'Moderators'
    },
    {
        'id': 3,
        'name': 'Users'
    },
    {
        'id': 4,
        'name': 'Banned'
    }
]


class Command(BaseCommand):
    help = 'Creates default groups'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(id=group['id'], name=group['name'])
            print('New group - {}. Created!.'.format(new_group.name))

        print('Successfully created groups')
