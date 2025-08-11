from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class BugzillaTests(TestCase):

    def setUp(self):
        self.manager_group = Group.objects.create(name='Manager')
        self.qa_group = Group.objects.create(name='QA')
        self.dev_group = Group.objects.create(name='Developer')

    '''def test_user_email_cannot_be_blank(self):
        user = User(username='noemail', email='', password='pass123')
        if not user.email:
            raise ValidationError({'email': ['This field cannot be blank.']})'''


    def test_user_name_cannot_be_blank(self):
        user = User(username='', email='test@example.com', password='pass123')
        with self.assertRaises(ValidationError) as cm:
            user.full_clean()
        self.assertIn('username', cm.exception.message_dict)

        
    def test_user_group_cannot_be_blank(self):
        user = User.objects.create(username='nousergroup', email='test@example.com', password='pass123')
        self.assertEqual(user.groups.count(), 0)  # Expect no groups 
