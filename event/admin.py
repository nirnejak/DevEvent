from django.contrib import admin

from .models import Paradigm
from .models import Language
from .models import User
from .models import Programmer
from .models import Organizer
from .models import EventType
from .models import Event

# Register your models here.

admin.site.register(Paradigm)
admin.site.register(Language)
admin.site.register(User)
admin.site.register(Programmer)
admin.site.register(Organizer)
admin.site.register(EventType)
admin.site.register(Event)