import sys
import getpass

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.core import exceptions
from django.utils.encoding import force_str


class Command(BaseCommand):
    help = 'Used to create a user'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.UserModel = get_user_model()
        self.username_field = self.UserModel._meta.get_field(
            self.UserModel.USERNAME_FIELD
        )

    def add_arguments(self, parser):
        parser.add_argument(
            '{}'.format(self.UserModel.USERNAME_FIELD),
            help='Specifies the login for the user'
        )
        for field in self.UserModel.REQUIRED_FIELDS:
            parser.add_argument(
                '{}'.format(field),
                help='Specifies the {} for the user'.format(field)
            )

        parser.add_argument(
            '--noinput',
            action='store_true',
            help=('Tells Django not to prompt the user for password. '
                  'Users created with --noinput will not be able to '
                  'login until they\'re give a valid password.')
        )

    def handle(self, *args, **options):
        username = options.get(self.UserModel.USERNAME_FIELD)
        password = None

        database = 'default'

        user_data = {}

        verbose_field_name = self.username_field.verbose_name

        try:
            username = self.username_field.clean(username, None)

            try:
                self.UserModel._default_manager.db_manager(
                    database
                ).get_by_natural_key(username)
            except self.UserModel.DoesNotExist:
                pass
            else:
                self.stderr.write(
                    "Error: That {} is already taken.".format(
                        verbose_field_name
                    )
                )
                sys.exit(1)

            for field_name in self.UserModel.REQUIRED_FIELDS:
                if options.get(field_name):
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = field.clean(options[field_name],
                                                        None)
            if not options['noinput']:
                while password is None:
                    if not password:
                        password = getpass.getpass()
                        password2 = getpass.getpass(
                            force_str('Password (again): ')
                        )

                        if password != password2:
                            self.stderr.write(
                                "Error: Your passwords didn't match."
                            )
                            password = None
                            continue

                    if password.strip() == '':
                        self.stderr.write(
                            "Error: Blank passwords aren't allowed"
                        )
                        password = None
                        continue

        except exceptions.ValidationError as e:
            raise CommandError('; '.join(e.messages))

        except KeyboardInterrupt:
            self.stderr.write("\nOperation cancelled.")
            sys.exit(1)

        if username:
            user_data[self.UserModel.USERNAME_FIELD] = username
            user_data['password'] = password
            self.UserModel._default_manager.db_manager(
                database
            ).create_user(**user_data)

            self.stdout.write("User created successfully.")
