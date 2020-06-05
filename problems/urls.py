from rest_framework.routers import DefaultRouter

from problems.views import TasksView

router = DefaultRouter()
router.register(prefix='', basename='problems', viewset=TasksView)

urlpatterns = router.urls
