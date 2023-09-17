from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from .views import signup

urlpatterns = [
    path('', RedirectView.as_view(url='/polls/')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup')
]
