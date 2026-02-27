from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, reverse
from .models import Submission
import csv

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("row_number", "name", "email", "product", "date_submitted")  # Show row numbers
    readonly_fields = ("date_submitted",)
    actions = ["export_as_csv"]

    def row_number(self, obj):
        queryset = Submission.objects.all().order_by('id')  # Order by ID to maintain sequence
        index = list(queryset).index(obj) + 1  # Get the position and start from 1
        return index

    row_number.short_description = "ID"  # Column name in the admin panel

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_csv_url'] = reverse('admin:export_all_submissions_csv')
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-csv/', self.export_all_csv, name='export_all_submissions_csv'),
        ]
        return custom_urls + urls

    def export_all_csv(self, request):
        """Export all submissions to CSV"""
        queryset = Submission.objects.all().order_by('-date_submitted')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="submissions.csv"'
        
        writer = csv.writer(response)
        # Write header row
        writer.writerow(['ID', 'Name', 'Email', 'Mobile', 'Product', 'Date Submitted'])
        
        # Write data rows
        for submission in queryset:
            writer.writerow([
                submission.id,
                submission.name,
                submission.email,
                submission.mobile or '',
                submission.product,
                submission.date_submitted.strftime('%Y-%m-%d %H:%M:%S') if submission.date_submitted else ''
            ])
        
        return response

    @admin.action(description="Download selected submissions as CSV")
    def export_as_csv(self, request, queryset):
        """
        Export selected submissions to CSV file.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="submissions.csv"'
        
        writer = csv.writer(response)
        # Write header row
        writer.writerow(['ID', 'Name', 'Email', 'Mobile', 'Product', 'Date Submitted'])
        
        # Write data rows
        for submission in queryset:
            writer.writerow([
                submission.id,
                submission.name,
                submission.email,
                submission.mobile or '',
                submission.product,
                submission.date_submitted.strftime('%Y-%m-%d %H:%M:%S') if submission.date_submitted else ''
            ])
        
        return response
    
    export_as_csv.short_description = "Download selected submissions as CSV"