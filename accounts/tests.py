from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

class CustomUserTests(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            age='44',
            password='testing123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@test.com')
        self.assertEqual(user.age, '44')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testing123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignUpViewTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.age = 20
        self.password = 'password1234'
        self.group = 'Admin'

    def test_signup_page_url(self):
        response = self.client.get("/accounts/create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_form(self):
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'age': self.age,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
            'group': self.group
        })
        self.assertEqual(response.status_code, 200)
        #self.assertRedirects(response, '/accounts/login/')

        #users = get_user_model().objects.all()
        #self.assertEqual(users.count(), 1)
    