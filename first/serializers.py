from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import Client, ImageUrls, Visit
from django.contrib.auth.models import User
from ast import literal_eval


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password must match.'})
        return attrs

    def save(self):
        user = User(email=self.data['email'], username=self.data['username'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class ImageSerializer(ModelSerializer):
    class Meta:
        model = ImageUrls
        fields = '__all__'
        read_only_fields = ['main_image', ]


class VisitDetailSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'


class ImageCreateSerializer(ModelSerializer):
    class Meta:
        model = ImageUrls
        fields = '__all__'
        read_only_fields = ['id', 'client', 'visit']


class ClientCreateSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['photo', ]


class ClientsWithoutPhotoSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'telephone', 'active']


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['photo']


class VisitSerializer(ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'


class CalendarGooglePlan(Serializer):
    id = serializers.CharField(read_only=True)
    status = serializers.CharField(allow_blank=True)
    htmlLink = serializers.URLField(allow_blank=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    creator = serializers.CharField(allow_blank=True)
    start = serializers.CharField()
    end = serializers.CharField(allow_blank=True)
    description = serializers.CharField(max_length=250, allow_blank=True)
    summary = serializers.CharField(max_length=250, allow_blank=True)
    attendees = serializers.CharField()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['creator'] = literal_eval(response['creator'])['email']
        response['start'] = literal_eval(response['start'])['dateTime']
        response['end'] = literal_eval(response['end'])['dateTime']
        response['attendees'] = literal_eval(response['attendees'])
        for client in range(len(response['attendees'])):
            response['attendees'][client] = response['attendees'][client]['email']
        return response
