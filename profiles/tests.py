import pytest
from django.test import Client
from django.urls import reverse

from django.contrib.auth.models import User
from profiles.models import Profile


@pytest.mark.django_db
class TestProfiles:

    client = Client()

    def test_index(self):
        url = reverse('profiles:index')
        response = self.client.get(url)
        content = response.content.decode()
        assert response.status_code == 200
        assert content.find("<title>Profiles</title>") != -1

    def test_profile(self):
        user = User.objects.create(
            username="TopUtilisateur", is_staff=True, is_superuser=True)
        profile = Profile.objects.create(
            user=user, favorite_city="New York")
        url = reverse('profiles:profile', args=[profile.user.username])
        context = {'profile': profile}
        response = self.client.get(url, data=context)
        content = response.content.decode()
        assert response.status_code == 200
        assert content.find("<title>" + profile.user.username + "</title>") != -1
