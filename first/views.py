from .serializers import VisitSerializer, ImageSerializer, ClientCreateSerializer, ProfilePicSerializer, \
    VisitDetailSerializer, ImageCreateSerializer, CalendarGooglePlan, RegistrationSerializer, \
    ClientsWithoutPhotoSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Client, Visit, ImageUrls
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from rest_framework.response import Response
from calendarApp.manual import get_event, create_event


class VisitFilter(filters.FilterSet):
    visit = filters.DateFromToRangeFilter(field_name='date_visit')

    class Meta:
        model = Visit
        fields = ['visit', 'client']


class VisitDetail(ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitDetailSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VisitFilter


class ClientListViewset(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer


class ClientsWithoutPhotoViewset(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientsWithoutPhotoSerializer


class Photo(ModelViewSet):
    serializer_class = ProfilePicSerializer
    queryset = Client.objects.all()


class VisitViewset(ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VisitFilter


class ImageListViewset(ModelViewSet):
    queryset = ImageUrls.objects.all()
    serializer_class = ImageSerializer


class ImageCreateViewset(ModelViewSet):
    queryset = ImageUrls.objects.all()
    serializer_class = ImageCreateSerializer


class CalendarViewset(ModelViewSet):
    serializer_class = CalendarGooglePlan

    def get_queryset(self):
        result = get_event()
        for i in result:
            i.setdefault('summary')
            i.setdefault('attendees', [{'email': None}])
        return result

    def create(self, request, *args, **kwargs):
        create_event(request.data)
        return Response({'name': 'hello world'})


class UserRegistrate(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    queryset = User.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
