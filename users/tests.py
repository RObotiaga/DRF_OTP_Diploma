from rest_framework.test import APITestCase
from rest_framework import status

from users.models import CustomUser

User = CustomUser


class AuthenticationTests(APITestCase):
    def test_user_creation_with_phone_number(self):
        # Test creating a user with phone number
        data = {'phone': '79638551644'}
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_activation_with_code(self):
        # Test user activation with OTP code
        User.objects.create(phone='1234567890',
                            one_time_password='1234',
                            is_active=False)
        data = {'phone': '1234567890', 'one_time_password': '1234'}
        response = self.client.post('/code/', data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_invite_code_activation(self):
        # Login user
        user = User.objects.create(phone='1234567890')
        self.client.force_authenticate(user=user)
        # Create test user
        invite_code = 'testte'
        User.objects.create(phone='1233211233',
                            invite_code=invite_code)

        data = {'activated_invite_code': invite_code}
        response = self.client.patch('/invite/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_own_user_data(self):
        # Login user
        user = User.objects.create(phone='1234567890',
                                   invite_code='testte')
        self.client.force_authenticate(user=user)

        response = self.client.get(f'/user/{user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '1234567890')
        self.assertEqual(response.data['invite_code'], 'testte')

    def test_retrieve_other_user_data(self):
        # Login user
        user = User.objects.create(phone='1234567890')
        self.client.force_authenticate(user=user)
        # Create test user
        other_user = User.objects.create(phone='1233211233',
                                         invite_code='testte')

        response = self.client.get(f'/user/{other_user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '1233211233')
        self.assertEqual(response.data['invite_code'], 'testte')

    def test_change_password(self):
        user = User.objects.create(phone='1234567890', password='qwerty123')
        self.client.force_authenticate(user=user)

        data = {'password': 'newpassword123'}
        response = self.client.put(f'/edit/{user.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password('newpassword123'))

    def test_delete_user(self):
        user = User.objects.create(phone='1234567890', password='qwerty123')
        self.client.force_authenticate(user=user)

        data = {'password': 'qwerty123'}
        response = self.client.delete(f'/delete/{user.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
