from django.urls import path

from rest_framework import routers

from .views import MeowView, MeowTaskView

router = routers.SimpleRouter()
router.register('tasks', MeowTaskView, basename='meow-tasks')


urlpatterns = [
    path('meow', MeowView.as_view())

]

urlpatterns += router.urls