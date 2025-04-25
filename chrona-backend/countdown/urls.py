from countdown.views import TimerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'countdown', TimerViewSet, basename='timer')


urlpatterns = router.urls