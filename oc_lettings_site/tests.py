from django.test import Client
from django.urls import reverse


def test_index():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    content = response.content.decode()
    assert response.status_code == 200
    assert content.find("<title>Holiday Homes</title>") != -1
