from django.test import TestCase
from .models import Role, Account, UserToken

class AccountModelTest(TestCase):
    
    def setUp(self):
        # Tạo một Role
        self.role = Role.objects.create(name="Admin")
        
        # Tạo một Account
        self.account = Account.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            phone="0123456789",
            address="123 Test Street",
            status=True,
            role=self.role
        )
        
        # Tạo UserToken
        self.user_token = UserToken.objects.create(
            user=self.account,
            refresh_token="sample_refresh_token",
            access_token="sample_access_token"
        )
    
    def test_role_creation(self):
        """Kiểm tra việc tạo đối tượng Role"""
        self.assertEqual(self.role.name, "Admin")
    
    def test_account_creation(self):
        """Kiểm tra việc tạo và lưu đối tượng Account"""
        self.assertEqual(self.account.username, "testuser")
        self.assertEqual(self.account.email, "testuser@example.com")
        self.assertEqual(self.account.role.name, "Admin")
        self.assertTrue(self.account.check_password("password123"))
    
    def test_user_token_creation(self):
        """Kiểm tra việc tạo đối tượng UserToken"""
        self.assertEqual(self.user_token.user, self.account)
        self.assertEqual(self.user_token.refresh_token, "sample_refresh_token")
        self.assertEqual(self.user_token.access_token, "sample_access_token")
    
    def test_string_representation(self):
        """Kiểm tra phương thức __str__"""
        self.assertEqual(str(self.role), "Admin")
        self.assertEqual(str(self.account), "testuser")
        self.assertIn("Token for testuser@example.com created at", str(self.user_token))
