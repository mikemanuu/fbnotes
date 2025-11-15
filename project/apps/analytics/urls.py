from django.urls import path
from .views import MetricsAPIView, Last7DaysAPIView

urlpatterns = [
    path("metrics/", MetricsAPIView.as_view(), name="api-metrics"),
    path("notes_last_7/", Last7DaysAPIView.as_view(), {"model_name":"notes"}, name="notes-last-7"),  
    path("bookmarks_last_7/", Last7DaysAPIView.as_view(), {"model_name":"bookmarks"}, name="bookmarks-last-7"),
    # better: explicit paths:
    path("analytics/<str:model_name>/", Last7DaysAPIView.as_view(), name="analytics-last-7"),
]
