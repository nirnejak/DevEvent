from django.urls import path, include
from rest_framework import routers

from . import views

router= routers.DefaultRouter()
router.register('languages',views.LanguageView)
router.register('paradigms', views.ParadigmView)
router.register('users', views.UserView)
router.register('programmers', views.ProgrammerView)
router.register('organizers', views.OrganizerView)
router.register('event_type', views.EventTypeView)
router.register('events', views.EventView, basename='events')

urlpatterns = [
       path('', include(router.urls))
]
