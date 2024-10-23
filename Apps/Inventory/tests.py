# from rest_framework.test import APITestCase, APIClient
# from django.urls import reverse
# from rest_framework import status
# from Apps.Inventory.models import Items
# from django.contrib.auth.models import User

# class ItemViewTests(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client = APIClient()
#         response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
#         print(response.data)
#         self.token = response.data['access']
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         self.item = Items.objects.create(name='Test Item', description='Test Description')
    
#     def test_list_items(self):
#         """Test listing items"""
#         response = self.client.get(reverse('item-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)