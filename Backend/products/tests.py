from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .views import create_user, detail_view
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from rest_framework.test import force_authenticate

class ProductsTestCase(TestCase):

    def setUp(self):
        # Create a test user and token for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.valid_item_json_data = {
            "sku": "AAA9999",
            "name": "name1",
            "category": "Electronics",
            "tags": "gadget, tech",
            "stock_status": "in_stock",
            "available_stock": 50
            }
        
    def test_create_user_valid_data(self):
        # Test create_user with valid data
        factory = APIRequestFactory()
        data = {'username': 'user1', 'email': 'user1@example.com', 'password': 'userpassword'}
        request = factory.post('/create_user/', data, format='json')
        response = create_user(request)

        self.assertEqual(response.status_code, 201)
        self.assertIn('username', response.data)
        # Add more assertions as needed

    def test_create_user_invalid_data(self):
        # Test create_user with invalid data
        factory = APIRequestFactory()
        # Omitting required field 'password'
        data = {'username': 'user1', 'email': 'user@gmail.com'}
        request = factory.post('/create_user/', data, format='json')
        response = create_user(request)
        self.assertEqual(response.status_code, 400)
        # Add more assertions as needed

    def test_detail_view_get_item_valid_data(self):
        # Test GET request for item data with valid SKU
        factory = APIRequestFactory()
        #creating an object before fetching the details
        instance = Item.objects.create(**self.valid_item_json_data)
        request = factory.get(f'/detail_view/{instance.sku}/')
        force_authenticate(request, user=self.user)
        response = detail_view(request, sku=instance.sku, model_cls = Item, serializer_cls = ItemSerializer)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_get_items_with_category(self):
        # Test GET request for items with a specific category using query parameters
        factory = APIRequestFactory()
        # Creating objects with different categories
        Item.objects.create(sku="ABC123", name="Item1", category="Electronics", available_stock=10, stock_status = "in_stock")
        Item.objects.create(sku="XYZ456", name="Item2", category="Clothing", available_stock=20, stock_status = "in_stock")

        request = factory.get('/detail_view/', {'category': 'Clothing'})
        force_authenticate(request, user=self.user)
        response = detail_view(request, model_cls=Item, serializer_cls=ItemSerializer)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_detail_view_get_items_with_stock(self):
        # Test GET request for items with a specific category using query parameters
        factory = APIRequestFactory()
        # Creating objects with different categories
        Item.objects.create(sku="ABC123", name="Item1", tags = 't1', category="Electronics", available_stock=10, stock_status = "in_stock")
        Item.objects.create(sku="XYZ456", name="Item2", tags = 't2', category="Clothing", available_stock=20, stock_status = "out_of_stock")

        request = factory.get('/detail_view/', {'stock_status': 'in_stock'})
        force_authenticate(request, user=self.user)
        response = detail_view(request, model_cls=Item, serializer_cls=ItemSerializer)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_detail_view_get_item_invalid_sku(self):
        # Test detail_view GET request with invalid SKU
        factory = APIRequestFactory()
        request = factory.get('/detail_view/invalid_sku/')
        force_authenticate(request, user=self.user)
        response = detail_view(request, sku = 'invalid_sku', model_cls = Item, serializer_cls = ItemSerializer)
        self.assertEqual(response.status_code, 404)  # Not Found

    def test_detail_view_get_item_authentication_failure(self):
        # Test detail_view with the Authentication Failure.
        # Applies for GET, POST, PUT, DELETE Request
        factory = APIRequestFactory()
        instance = Item.objects.create(**self.valid_item_json_data)
        request = factory.get(f'/detail_view/{instance.sku}/')
        response = detail_view(request, sku=instance.sku)
        self.assertEqual(response.status_code, 401)  # Un Authorized

    def test_detail_view_post_valid_data(self):
        # Test detail_view POST request with valid data
        factory = APIRequestFactory()
        request = factory.post('/detail_view/', self.valid_item_json_data, format='json')
        force_authenticate(request, user=self.user) 
        response = detail_view(request, model_cls = Item, serializer_cls = ItemSerializer)
        self.assertEqual(response.status_code, 201)

    def test_detail_view_put_valid_data(self):
        # Test detail_view PUT request with valid data
        factory = APIRequestFactory()
        instance = Item.objects.create(**self.valid_item_json_data)
        data_new = self.valid_item_json_data
        data_new["name"] = "name2"
        request = factory.put(f'/detail_view/{instance.sku}/', data_new, format='json')
        force_authenticate(request, user=self.user)
        response = detail_view(request, sku=instance.sku, model_cls = Item, serializer_cls = ItemSerializer)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_put_invalid_sku(self):
        # Test detail_view PUT request with invalid SKU
        factory = APIRequestFactory()
        request = factory.put('/detail_view/invalid_sku/', self.valid_item_json_data, format='json')
        force_authenticate(request, user=self.user)
        response = detail_view(request, sku='invalid_sku', model_cls = Item, serializer_cls = ItemSerializer)
        self.assertEqual(response.status_code, 404)  # Not Found

    def test_detail_view_delete_valid_sku(self):
        # Test detail_view DELETE request with valid SKU
        factory = APIRequestFactory()
        instance = Item.objects.create(**self.valid_item_json_data)
        request = factory.delete(f'/detail_view/{instance.sku}/')
        force_authenticate(request, user=self.user)  # Authenticate the request
        response = detail_view(request, sku=instance.sku, model_cls = Item, serializer_cls = ItemSerializer)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Item.objects.filter(sku=instance.sku).exists())

    def test_detail_view_delete_invalid_sku(self):
        # Test detail_view DELETE request with invalid SKU
        factory = APIRequestFactory()
        request = factory.delete('/detail_view/invalid_sku/')
        force_authenticate(request, user=self.user)  
        response = detail_view(request, sku='invalid_sku', model_cls = Item, serializer_cls = ItemSerializer)
        self.assertEqual(response.status_code, 404)  # Not Found

    def test_detail_view_post_valid_category_creation(self):
        # Test detail_view POST request with valid category data
        factory = APIRequestFactory()
        category_data = {"name":"Cat1"}
        request = factory.post('/detail_view/',category_data, format='json')
        force_authenticate(request, user=self.user) 
        response = detail_view(request, model_cls = Category, serializer_cls = CategorySerializer)
        self.assertEqual(response.status_code, 201)