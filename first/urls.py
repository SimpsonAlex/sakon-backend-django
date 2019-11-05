from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitViewset, ImageListViewset, ClientListViewset, Photo, VisitDetail, ImageCreateViewset, \
    CalendarViewset, UserRegistrate, ClientsWithoutPhotoViewset
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('visits', VisitViewset, basename='visit')
router.register('images', ImageListViewset)
router.register('list_clients', ClientListViewset, basename='listc_lients')
router.register('list_clients_without_photo', ClientsWithoutPhotoViewset, basename='list_clients_without_photo')
router.register('visit_detail', VisitDetail, basename='visit-detail')
router.register('image_create', ImageCreateViewset, basename='image_create')
router.register('photo', Photo, basename='photo')
router.register('calendar', CalendarViewset, basename='calendar')
router.register('registration', UserRegistrate)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
