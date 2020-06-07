from rest_framework.routers import DefaultRouter

from problems.views import ProblemsView

router = DefaultRouter()
router.register(prefix='', basename='problems', viewset=ProblemsView)

urlpatterns = router.urls
