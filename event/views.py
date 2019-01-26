from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication

from .models import (
    Paradigm,
    Language,
    User,
    Programmer,
    Organizer,
    EventType,
    Event
)
from .serializers import (
    LanguageSerializer,
    ParadigmSerializer,
    UserSerializer,
    ProgrammerSerializer,
    OrganizerSerializer,
    EventTypeSerializer,
    EventSerializer
)

from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter


class ParadigmView(viewsets.ModelViewSet):
    queryset = Paradigm.objects.all()
    serializer_class = ParadigmSerializer
    authentication_classes = [TokenAuthentication]


class LanguageView(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes = [TokenAuthentication]

    filter_fields = ('name', 'paradigm__name')
    ordering_fields = ('name', 'paradigm__name')
    search_fields = ('name', 'paradigm__name')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        try:
            # Extracting the data from request
            data = request.data
            # Creating new object
            paradigm = Paradigm.objects.get(pk=data['paradigm'])
            language = Language.objects.create(
                name=data['name'], paradigm_id=paradigm.id)
            # Commiting Changes to Database
            language.save()

            # Passing the object to serializer and generating response
            serializer = LanguageSerializer(language)
            return Response(serializer.data)
        except Paradigm.DoesNotExist as err:
            import pdb; pdb.set_trace() 
            return Response({"msg": "Paradigm Does not exists in the database"}, status = status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        language = self.get_object()
        # Extracting the data from request
        data = request.data

        # Updating the object
        language.name = data['name']
        language.paradigm = Paradigm.objects.get(pk=data['paradigm'])
        # Commiting the changes
        language.save()

        # Passing the object to serializer and generating response
        serializer = LanguageSerializer(language)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Selecting the object with the passed ID, pk in this case
        language = self.get_object()

        # Updating the object, if new data provided
        language.name = request.data.get('name', language.name)
        #language.paradigm = request.data.get('paradigm', language.paradigm)
        if 'paradigm' in request.data:
            language.paradigm = Paradigm.objects.get(
                pk=request.data['paradigm'])

        # Commiting the Changes
        language.save()

        # Passing the object to serializer and generating response
        serializer = LanguageSerializer(language)
        return Response(serializer.data)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]


class ProgrammerView(viewsets.ModelViewSet):
    queryset = Programmer.objects.all()
    serializer_class = ProgrammerSerializer
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        # Extracting the data from request
        data = request.data
        # Creating new object
        user = User.objects.get(pk=data['user'])
        programmer = Programmer.objects.create(
            company=data['company'],
            experience=data['experience'],
            user_id=user.id,
        )
        for lang_id in data['languages']:
            lang = Language.objects.get(pk=lang_id)
            programmer.languages.add(lang)

        # Commiting Changes to Database
        programmer.save()

        # Passing the object to serializer and generating response
        serializer = ProgrammerSerializer(programmer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        programmer = self.get_object()
        # Extracting the data from request
        data = request.data

        # Updating the object
        programmer.company = data['company']
        programmer.experience = data['experience']
        programmer.user = User.objects.get(pk=data['user'])

        # Remove Old Languages
        for lang in programmer.languages.all():
            programmer.languages.remove(lang)
        # Add New Languages
        for lang_id in data['languages']:
            lang = Language.objects.get(pk=lang_id)
            programmer.languages.add(lang)

        # Commiting Changes to Database
        programmer.save()

        # Passing the object to serializer and generating response
        serializer = ProgrammerSerializer(programmer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Selecting the object with the passed ID, pk in this case
        programmer = self.get_object()

        # Updating the object, if new data provided
        programmer.company = request.data.get('company', programmer.company)
        programmer.experience = request.data.get(
            'company', programmer.experience)

        if 'user' in request.data:
            programmer.user = User.objects.get(pk=request.data['user'])

        #language.paradigm = request.data.get('paradigm', language.paradigm)
        if 'languages' in request.data:
            # Remove Old Languages
            for lang in programmer.languages.all():
                programmer.languages.remove(lang)
            # Add New Languages
            for lang_id in request.data['languages']:
                lang = Language.objects.get(pk=lang_id)
                programmer.languages.add(lang)

        # Commiting Changes to Database
        programmer.save()

        # Passing the object to serializer and generating response
        serializer = ProgrammerSerializer(programmer)
        return Response(serializer.data)


class OrganizerView(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        # Extracting the data from request
        data = request.data
        # Creating new object
        user = User.objects.get(pk=data['user'])
        organizer = Organizer.objects.create(
            location=data['location'],
            user_id=user.id,
        )

        # Commiting Changes to Database
        organizer.save()

        # Passing the object to serializer and generating response
        serializer = OrganizerSerializer(organizer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        organizer = self.get_object()
        # Extracting the data from request
        data = request.data

        # Updating the object
        organizer.location = data['location']
        organizer.user = User.objects.get(pk=data['user'])

        # Commiting Changes to Database
        organizer.save()

        # Passing the object to serializer and generating response
        serializer = OrganizerSerializer(organizer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Selecting the object with the passed ID, pk in this case
        organizer = self.get_object()

        # Updating the object, if new data provided
        organizer.location = request.data.get('organizer', organizer.location)

        if 'user' in request.data:
            organizer.user = User.objects.get(pk=request.data['user'])

        # Commiting Changes to Database
        organizer.save()

        # Passing the object to serializer and generating response
        serializer = OrganizerSerializer(organizer)
        return Response(serializer.data)


class EventTypeView(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    authentication_classes = [TokenAuthentication]


class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # permission_classes = (permissions.DjangoModelPermissions)
    authentication_classes = [TokenAuthentication]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    filter_fields = ('name', 'languages__name', 'date', 'venue', 'event_type__name', 'organizer__user__username')
    ordering_fields = ('name', 'date', 'language__name')
    search_fields = ('name', 'languages__name', 'date', 'venue', 'event_type__name', 'organizer__user__username')
    # lookup_field = 'name'

    def create(self, request, *args, **kwargs):
        # Extracting the data from request
        data = request.data

        # get organizer type automatically from current user
        organizer = Organizer.objects.get(pk=data['organizer'])
        event_type = EventType.objects.get(pk=data['event_type'])

        # Creating new object
        event = Event.objects.create(
            name=data['name'],
            venue=data['venue'],
            date=data['date'],
            organizer=organizer,
            event_type=event_type
        )

        for lang_id in data['languages']:
            lang = Language.objects.get(pk=lang_id)
            event.languages.add(lang)
        
        for prog_id in data['programmers']:
            prog = Programmer.objects.get(pk=prog_id)
            event.programmers.add(prog)

        # Commiting Changes to Database
        event.save()

        # Passing the object to serializer and generating response
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        event = self.get_object()
        # Extracting the data from request
        data = request.data

        # Updating the object
        event.name = data['name']
        event.venue = data['venue']
        event.date = data['date']
        event.organizer = Organizer.objects.get(pk=data['organizer'])
        event.event_type = EventType.objects.get(pk=data['event_type'])

        # Remove Old Languages
        for lang in event.languages.all():
            event.languages.remove(lang)
        # Add New Languages
        for lang_id in data['languages']:
            lang = Language.objects.get(pk=lang_id)
            event.languages.add(lang)
        
        # Remove Old Programmers
        for prog in event.programmers.all():
            event.programmers.remove(prog)
        # Add New Programmers
        for prog_id in data['programmers']:
            prog = Programmer.objects.get(pk=prog_id)
            event.programmers.add(prog)

        # Commiting Changes to Database
        event.save()

        # Passing the object to serializer and generating response
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        # Selecting the object with the passed ID, pk in this case
        event = self.get_object()

        # Updating the object, if new data provided
        event.name = request.data.get('name', event.name)
        event.venue = request.data.get('venue', event.venue)
        event.date = request.data.get('date', event.date)

        if 'organizer' in request.data:
            event.organizer = Organizer.objects.get(pk=request.data['organizer'])

        if 'languages' in request.data:
            # Remove Old Languages
            for lang in event.languages.all():
                event.languages.remove(lang)
            # Add New Languages
            for lang_id in request.data['languages']:
                lang = Language.objects.get(pk=lang_id)
                event.languages.add(lang)
        
        if 'programmers' in request.data:
            # Remove Old Languages
            for prog in event.programmers.all():
                event.programmers.remove(prog)
            # Add New Languages
            for prog_id in request.data['programmers']:
                prog = Programmer.objects.get(pk=prog_id)
                event.programmers.add(prog)

        # Commiting Changes to Database
        event.save()

        # Passing the object to serializer and generating response
        serializer = EventSerializer(event)
        return Response(serializer.data)