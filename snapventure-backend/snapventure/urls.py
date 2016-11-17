from django.conf.urls import url

from . import views

from django.conf.urls import url, include
from rest_framework import routers
import api
import views



router = routers.DefaultRouter()
router.register(r'profile', api.ProfileViewSet)
router.register(r'journey', api.JourneyViewSet)
router.register(r'inscription', api.InscriptionViewSet)
router.register(r'type', api.TypeViewSet)
router.register(r'step', api.StepViewSet)
router.register(r'scan', api.ScanViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)

urlpatterns += (
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^scan/(?P<uid>\S+)', views.Scanner.as_view(), name='scan'),
)

urlpatterns += (
    # urls for Profile
    url(r'^profile/$', views.ProfileListView.as_view(), name='snapventure_profile_list'),
    url(r'^profile/create/$', views.ProfileCreateView.as_view(), name='snapventure_profile_create'),
    url(r'^profile/detail/(?P<id>\S+)/$', views.ProfileDetailView.as_view(), name='snapventure_profile_detail'),
    url(r'^profile/update/(?P<id>\S+)/$', views.ProfileUpdateView.as_view(), name='snapventure_profile_update'),
)

urlpatterns += (
    # urls for Journey
    url(r'^journey/$', views.JourneyListView.as_view(), name='snapventure_journey_list'),
    url(r'^journey/create/$', views.JourneyCreateView.as_view(), name='snapventure_journey_create'),
    url(r'^journey/detail/(?P<id>\S+)/$', views.JourneyDetailView.as_view(), name='snapventure_journey_detail'),
    url(r'^journey/update/(?P<id>\S+)/$', views.JourneyUpdateView.as_view(), name='snapventure_journey_update'),
)

urlpatterns += (
    # urls for Inscription
    url(r'^inscription/$', views.InscriptionListView.as_view(), name='snapventure_inscription_list'),
    url(r'^inscription/create/$', views.InscriptionCreateView.as_view(), name='snapventure_inscription_create'),
    url(r'^inscription/detail/(?P<id>\S+)/$', views.InscriptionDetailView.as_view(), name='snapventure_inscription_detail'),
    url(r'^inscription/update/(?P<id>\S+)/$', views.InscriptionUpdateView.as_view(), name='snapventure_inscription_update'),
)

urlpatterns += (
    # urls for Type
    url(r'^type/$', views.TypeListView.as_view(), name='snapventure_type_list'),
    url(r'^type/create/$', views.TypeCreateView.as_view(), name='snapventure_type_create'),
    url(r'^type/detail/(?P<id>\S+)/$', views.TypeDetailView.as_view(), name='snapventure_type_detail'),
    url(r'^type/update/(?P<id>\S+)/$', views.TypeUpdateView.as_view(), name='snapventure_type_update'),
)

urlpatterns += (
    # urls for Step
    url(r'^step/$', views.StepListView.as_view(), name='snapventure_step_list'),
    url(r'^step/create/$', views.StepCreateView.as_view(), name='snapventure_step_create'),
    url(r'^step/detail/(?P<id>\S+)/$', views.StepDetailView.as_view(), name='snapventure_step_detail'),
    url(r'^step/update/(?P<id>\S+)/$', views.StepUpdateView.as_view(), name='snapventure_step_update'),
)

urlpatterns += (
    # urls for Scan
    url(r'^scan/$', views.ScanListView.as_view(), name='snapventure_scan_list'),
    url(r'^scan/create/$', views.ScanCreateView.as_view(), name='snapventure_scan_create'),
    url(r'^scan/detail/(?P<id>\S+)/$', views.ScanDetailView.as_view(), name='snapventure_scan_detail'),
    url(r'^scan/update/(?P<id>\S+)/$', views.ScanUpdateView.as_view(), name='snapventure_scan_update'),
)
