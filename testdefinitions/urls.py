from django.urls import path
from testdefinitions import views

urlpatterns = [
    path('testdefinitions/', views.TestCompositionViewSet.as_view({'get': 'list'})),
]

