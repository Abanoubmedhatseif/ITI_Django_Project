from django.urls import path
from .views import register, login, get_profile, update_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("profile/", get_profile, name="get_profile"),
    path("profile/update/", update_profile, name="update_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
