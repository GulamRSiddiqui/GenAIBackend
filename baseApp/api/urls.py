from django.urls import path, include
from .views import MyTokenObtainPairView, view, CustomTokenVerifyView, upload_image
from django.views.decorators.csrf import csrf_exempt


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', view.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('Places', csrf_exempt(upload_image), name='upload_image'),
    
    
]
