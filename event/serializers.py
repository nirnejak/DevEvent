from rest_framework import serializers

from .models import (
    Paradigm,
    Language,
    User,
    Programmer,
    Organizer,
    EventType,
    Event
)

class ParadigmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paradigm
        fields = ('id', 'name')


class LanguageSerializer(serializers.ModelSerializer):
    paradigm = serializers.StringRelatedField()
    class Meta:
        model = Language
        fields = ('id', 'name', 'paradigm')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProgrammerSerializer(serializers.ModelSerializer):
    languages = serializers.StringRelatedField(many=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Programmer
        fields = '__all__'


class OrganizerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Organizer
        fields = '__all__'


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ('id','name',)


class EventSerializer(serializers.ModelSerializer):
    languages = serializers.StringRelatedField(many=True)
    programmers = serializers.StringRelatedField(many=True)
    event_type = serializers.StringRelatedField()
    organizer = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = '__all__'