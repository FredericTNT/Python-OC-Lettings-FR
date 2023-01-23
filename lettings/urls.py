from django.urls import path
from lettings.views import index, letting


def trigger_error(request):
    division_by_zero = 1 / 0

app_name = 'lettings'
urlpatterns = [
    path('', index, name='index'),
    path('<int:letting_id>/', letting, name='letting'),
    path('sentry-debug/', trigger_error),
]
