from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from storage import views as media_view

router = SimpleRouter()
router.register('api/v1.0/Media', media_view.MultipleFileUploadView, basename='media')
router.register('api/v1.0/Album', media_view.MultipleAlbumView, basename='album')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/auth/', include('rest_framework.urls')),
    path('api/v1.0/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1.0/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1.0/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('api/v1.0/', include('meow.urls')),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
]
