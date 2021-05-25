from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from subjects import views

router = routers.DefaultRouter()
router.register(r'person', views.PersonViewSet)
router.register(r'identification', views.IdentificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('persons/', views.PersonList.as_view()),
    path('persons/<pk>/', views.PersonDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = format_suffix_patterns(urlpatterns)
