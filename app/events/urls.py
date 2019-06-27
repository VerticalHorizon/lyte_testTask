from rest_framework.routers import SimpleRouter
from .viewsets import EventViewSet


router = SimpleRouter(trailing_slash=True)
router.register(r'', EventViewSet)

urlpatterns = router.urls
