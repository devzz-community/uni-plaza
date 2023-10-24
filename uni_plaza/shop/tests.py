from rest_framework.test import APIRequestFactory, RequestsClient

factory = APIRequestFactory()
request = factory.post('/api/market/products/', {'title': 'new idea'})

client = RequestsClient()
response = client.get('http://127.0.0.1:8000/api/market/products/')
assert response.status_code == 200