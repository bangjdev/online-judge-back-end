from rest_framework.routers import DefaultRouter

from .views import TestsView

router = DefaultRouter()
router.register(prefix='', basename='tests', viewset=TestsView)

urlpatterns = router.urls
