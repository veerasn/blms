from django.urls import include, path, re_path
from rest_framework import routers
from patients import views

router = routers.DefaultRouter()
router.register(
    'patient/(?P<search>.+)/$', views.PatientViewSet
)


urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^patient/(?P<search>.+)/$', views.PatientViewSet.as_view({'get': 'list'}))
]
