import pytest
from django.test import Client
from django.urls import reverse

from lettings.models import Address, Letting


@pytest.mark.django_db
class TestLettings:

    client = Client()

    def test_index(self):
        url = reverse('lettings:index')
        response = self.client.get(url)
        content = response.content.decode()
        assert response.status_code == 200
        assert content.find("<title>Lettings</title>") != -1

    def test_letting(self):
        address = Address.objects.create(
            number="74", street="Porchefontaine", city="Versailles",
            state="Yvelines", zip_code="78000", country_iso_code="033")
        letting = Letting.objects.create(
            title="Home sweet home", address=address)
        url = reverse('lettings:letting', args=[address.id])
        context = {'title': letting.title, 'address': letting.address}
        response = self.client.get(url, data=context)
        content = response.content.decode()
        assert response.status_code == 200
        assert content.find("<title>" + letting.title + "</title>") != -1
