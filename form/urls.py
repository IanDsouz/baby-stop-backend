from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.http import HttpResponse
from .views import SubmissionViewSet

router = SimpleRouter()
router.register(r'submissions', SubmissionViewSet)

def empty_view(request):
    """Return empty response for root path"""
    return HttpResponse(status=404)

urlpatterns = [
    path('', empty_view, name='form-root'),
] + router.urls
