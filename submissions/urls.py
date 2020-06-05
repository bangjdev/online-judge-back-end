from rest_framework.routers import DefaultRouter

from .views import SubmissionsView

router = DefaultRouter()
router.register(prefix='', basename='submissions', viewset=SubmissionsView)

urlpatterns = router.urls
