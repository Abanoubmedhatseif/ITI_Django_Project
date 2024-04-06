from django.urls import path
from .views import register, login, update_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("profile/", update_profile, name="update_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
