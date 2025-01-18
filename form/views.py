from rest_framework import viewsets
from .models import Submission
from .serializers import SubmissionSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .utils import send_thank_you_email
import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        # First, create the submission using the serializer
        response = super().create(request, *args, **kwargs)

        # Get the submission object from the response data
        submission_data = response.data
        to_email = submission_data.get("email")  # Assuming the 'email' field is in the serializer

        # Send the thank you email
        if to_email:
            send_thank_you_email(to_email)

        return response
    
    def get_queryset(self):
    # """
    # Return the submissions ordered by `date_submitted` in descending order.
    # """
        queryset = Submission.objects.all()

        # Order by 'date_submitted' in descending order (latest submissions first)
        return queryset.order_by('-date_submitted')
