from django.urls import include, path
from rest_framework import routers
from patients import views

router = routers.DefaultRouter()
router.register('patient', views.PatientViewSet)

urlpatterns = [
    path('', include(router.urls))
]
