from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch



def sample_user(email='test@londonappdev.com',password='testpass'):
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""
        email='test@hyderabad.com'
        password='testpass123'
        user=get_user_model().objects.create_user(
        email=email,
        password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email='test@Hyderabad.com'
        user=get_user_model().objects.create_user(email,'test123')
        self.assertEqual(user.email,email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')

    def test_create_new_superuser(self):
        """Test create super user"""
        user=get_user_model().objects.create_superuser(
        'test@hyderabad.com',
        'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag=models.Tag.objects.create(user=sample_user(),
        name='Vegan')
        self.assertEqual(str(tag),tag.name)

    def test_ingredient_str(self):
        ingredient=models.Ingredient.objects.create(user=sample_user(),
        name='cucumber')
        self.assertEqual(str(ingredient),ingredient.name)

    def test_recipe_str(self):
        recipe=models.Recipe.objects.create(user=sample_user(),title='Steak',time_minutes=6,price=5.00)
        self.assertEqual(str(recipe),recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuif(self,mock_uuid):
        uuid='test-uuid'
        mock_uuid.return_value=uuid
        file_path=models.recipe_image_file_path(None,'myimage.jpg')

        exp_path=f'upload/recipe/{uuid}.jpg'
        self.assertEqual(file_path,exp_path)
