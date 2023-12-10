from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from animal_detection.app.backend.detection.views import run_detection

urlpatterns = [
    path('run', run_detection, name='detection-run'),
    # path('<int:pk>', views.OrderDetail.as_view(), name='order-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)