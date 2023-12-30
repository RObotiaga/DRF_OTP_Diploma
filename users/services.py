import secrets
import string

from .models import CustomUser


def generate_unique_invite_code():
    while True:
        invite_code = ''.join(secrets.choice(
            string.ascii_letters + string.digits) for _ in range(6))
        if not CustomUser.objects.filter(invite_code=invite_code).exists():
            return invite_code
