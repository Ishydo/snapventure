from .views import *

from rest_framework.authtoken import views as rviews
from django.conf.urls import url, include
from rest_framework import routers
import api
import views
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'profile', api.ProfileViewSet)
router.register(r'journey', api.JourneyViewSet)
router.register(r'inscription', api.InscriptionViewSet)
router.register(r'type', api.TypeViewSet)
router.register(r'step', api.StepViewSet)
router.register(r'scan', api.ScanViewSet)


urlpatterns = [
    # Routes for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-token-auth/', rviews.obtain_auth_token),

    # Registration related routes
    #url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),


    # Journey Useradmin Dashboard related routes
    url(r'^dashboard/journey/$', views.JourneyListView.as_view(), name='journey_list'),
    url(r'^dashboard/journey/create', views.JourneyCreateView.as_view(), name="journey_create"),
    url(r'^dashboard/journey/view/(?P<slug>\S+)/$', views.JourneyDetailView.as_view(), name='journey_detail'),
    url(r'^dashboard/journey/update/(?P<slug>\S+)/$', views.JourneyUpdateView.as_view(), name='journey_update'),
    url(r'^dashboard/journey/delete/(?P<slug>\S+)/$', views.JourneyDeleteView.as_view(), name='journey_delete'),

    url(r'^dashboard/step/create', views.StepCreateView.as_view(), name="step_create"),
    url(r'^dashboard/step/view/(?P<slug>\S+)/$', views.StepDetailView.as_view(), name="step_detail"),
    url(r'^dashboard/step/update/(?P<slug>\S+)/$', views.StepUpdateView.as_view(), name='step_update'),
    url(r'^dashboard/step/delete/(?P<slug>\S+)/$', views.StepDeleteView.as_view(), name='step_delete'),

    url(r'^dashboard/(?P<slug>\S+)/new-step/$', views.StepCreateView.as_view(), name='add_journey_step'),
    url(r'^dashboard/(?P<slug>\S+)/manage-steps/$', views.StepManageView.as_view(), name='manage_steps'),

    # Pages URLs
    url(r'^dashboard', views.Dashboard.as_view(), name="dashboard"),        # User Dashboard
    url(r'^', views.Home.as_view(), name="homepage"),                       # Default homepage
]
