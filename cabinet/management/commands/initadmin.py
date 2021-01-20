from django.conf import settings
from django.core.management.base import BaseCommand
from cabinet.models import Account

class Command(BaseCommand):

    def handle(self, *args, **options):
        if Account.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = 'admin'
                print('Аккаунт создан для %s (%s)' % (username, email))
                admin = Account.objects.create_superuser(email=email, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Учетные записи администратора могут быть инициализированы, только если учетных записей не существует!')