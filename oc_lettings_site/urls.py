from django.contrib import admin
from django.urls import path, include

from oc_lettings_site.views import index


urlpatterns = [
    path('', index, name='index'),
    path('lettings/', include('lettings.urls', namespace='lettings')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('admin/', admin.site.urls),
]
