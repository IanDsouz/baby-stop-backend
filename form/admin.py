from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("row_number", "name", "email", "product", "date_submitted")  # Show row numbers
    readonly_fields = ("date_submitted",)

    def row_number(self, obj):
        queryset = Submission.objects.all().order_by('id')  # Order by ID to maintain sequence
        index = list(queryset).index(obj) + 1  # Get the position and start from 1
        return index

    row_number.short_description = "ID"  # Column name in the admin panel