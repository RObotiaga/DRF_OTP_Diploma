from django.core.management import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Delete a user by phone number'

    def add_arguments(self, parser):
        parser.add_argument('phone', type=str, help='Phone of the user to delete')

    def handle(self, *args, **options):
        phone = options['phone']
        try:
            user_to_delete = CustomUser.objects.get(phone=phone)
            user_to_delete.delete()
            self.stdout.write(self.style.SUCCESS('Пользователь успешно удален'))
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь не найден'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при удалении пользователя: {e}'))
