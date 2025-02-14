from rest_framework import viewsets, status
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

        submission_data = response.data
        to_email = submission_data.get("email")  # Assuming the 'email' field is in the serializer

        if to_email and DEVELOPMENT_MODE is False:
            send_thank_you_email(to_email)
        return response
    
    def get_queryset(self):
        # Order submissions by most recent first
        return Submission.objects.all().order_by('-date_submitted')
    

    @action(detail=True, methods=['POST'])
    def duplicate(self, request, pk=None):
        """
        Duplicate an existing submission and allow modifications before saving.
        """
        try:
            original_submission = self.get_object()
            duplicated_data = SubmissionSerializer(original_submission).data

            # Remove the existing ID so a new record is created
            duplicated_data.pop("id", None)

            # Merge request data (e.g., updated product, name, etc.)
            duplicated_data.update(request.data)  # Merge incoming fields

            # Save the new submission
            serializer = SubmissionSerializer(data=duplicated_data)
            if serializer.is_valid():
                new_submission = serializer.save()

                # Send thank-you email for duplicated submission
                if new_submission.email and not DEVELOPMENT_MODE:
                    send_thank_you_email(new_submission.email)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Submission.DoesNotExist:
            return Response({"error": "Submission not found"}, status=status.HTTP_404_NOT_FOUND)