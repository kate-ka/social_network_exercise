from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from api.auth.views import SignUpView, JWTObtainView, UserActivityViewSet

router = DefaultRouter()
router.register(r"users-activity", UserActivityViewSet)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", JWTObtainView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls